# backend/api/views.py
from rest_framework import generics, throttling
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from django.core.cache import cache
from django.conf import settings

import datetime
import os
import threading
import requests

from celery import shared_task

# Models
from .models import (
    Project, Skill, Testimonial,
    Experience, Education, ContactMessage
)

from .serializers import (
    ProjectSerializer, SkillSerializer, TestimonialSerializer,
    ExperienceSerializer, EducationSerializer, ContactMessageSerializer
)

# Blog imports
from blog.models import BlogPost
from blog.serializers import BlogPostListSerializer

from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

from users.models import User


# =============================================================================
# SENDGRID EMAIL TASK (PRODUCTION + CELERY HYBRID READY)
# =============================================================================
@shared_task
def send_contact_email_task(name, email, subject, message, language='en'):
    """
    Sends emails via SendGrid API (HTTP REST).
    Works for both Celery (local) and threading (production fallback).
    """

    sendgrid_api_key = os.environ.get('SENDGRID_API_KEY')
    if not sendgrid_api_key:
        print("Missing SENDGRID_API_KEY")
        return "Missing API Key"

    url = "https://api.sendgrid.com/v3/mail/send"
    headers = {
        "Authorization": f"Bearer {sendgrid_api_key}",
        "Content-Type": "application/json"
    }

    sender_identity = settings.DEFAULT_FROM_EMAIL

    admin_payload = {
        "personalizations": [{
            "to": [{"email": sender_identity}],
            "subject": f"Portfolio Contact: {subject}"
        }],
        "from": {"email": sender_identity, "name": "Portfolio"},
        "reply_to": {"email": email, "name": name},
        "content": [{"type": "text/html", "value": message}]
    }

    visitor_payload = {
        "personalizations": [{
            "to": [{"email": email}],
            "subject": "Thanks for contacting me"
        }],
        "from": {"email": sender_identity, "name": "Portfolio"},
        "content": [{"type": "text/html", "value": message}]
    }

    try:
        requests.post(url, json=admin_payload, headers=headers)
        requests.post(url, json=visitor_payload, headers=headers)
        return "Success"
    except Exception as e:
        print(f"SendGrid error: {e}")
        return str(e)


# =============================================================================
# BLOG POSTS (FIXED IMPORT ISSUE)
# =============================================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def recent_blog_posts(request):
    """Return latest 3 blog posts"""
    cache_key = "recent_blog_posts"
    posts = cache.get(cache_key)

    if not posts:
        posts = BlogPost.objects.filter(published=True).order_by("-id")[:3]
        cache.set(cache_key, posts, 60 * 15)

    serializer = BlogPostListSerializer(posts, many=True)
    return Response(serializer.data)


# =============================================================================
# CONTACT EMAIL THROTTLE
# =============================================================================
class ContactThrottle(throttling.SimpleRateThrottle):
    rate = '5/hour'

    def get_cache_key(self, request, view):
        return self.get_ident(request)


# =============================================================================
# BASIC LIST VIEWS
# =============================================================================
class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Project.objects.filter(featured=True)


class SkillListView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]


class TestimonialListView(generics.ListAPIView):
    queryset = Testimonial.objects.filter(featured=True)
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]


class ExperienceListView(generics.ListAPIView):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [AllowAny]


class EducationListView(generics.ListAPIView):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [AllowAny]


# =============================================================================
# CONTACT FORM
# =============================================================================
class ContactCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ContactThrottle]

    def perform_create(self, serializer):
        message = serializer.save()

        is_production = os.environ.get('RENDER') == 'true' or not settings.DEBUG

        if is_production:
            threading.Thread(
                target=send_contact_email_task,
                args=(message.name, message.email, message.subject, message.message)
            ).start()
        else:
            send_contact_email_task.delay(
                message.name,
                message.email,
                message.subject,
                message.message
            )


# =============================================================================
# DASHBOARD
# =============================================================================
class DashboardStatsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            "projects": Project.objects.count(),
            "skills": Skill.objects.count(),
            "testimonials": Testimonial.objects.count(),
            "experiences": Experience.objects.count(),
            "education": Education.objects.count(),
            "messages": ContactMessage.objects.count(),
        })


# =============================================================================
# HEALTH CHECK
# =============================================================================
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat()
    })


# =============================================================================
# TEST ENDPOINT
# =============================================================================
@api_view(['POST'])
@permission_classes([AllowAny])
def test_post(request):
    return Response({"message": "POST works", "data": request.data})