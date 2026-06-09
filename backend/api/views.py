# backend/api/views.py

from rest_framework import generics, throttling
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from django.core.cache import cache
from django.conf import settings

from celery import shared_task
import datetime
import os
import threading
import requests
import logging
import traceback

from .models import (
    Project, Skill, Testimonial,
    Experience, Education, ContactMessage
)

from .serializers import (
    ProjectSerializer, SkillSerializer, TestimonialSerializer,
    ExperienceSerializer, EducationSerializer, ContactMessageSerializer
)

from blog.models import BlogPost
from blog.serializers import BlogPostListSerializer

from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

from users.models import User


# =========================================================
# EMAIL SENDING (SENDGRID)
# =========================================================

@shared_task
def send_contact_email_task(name, email, subject, message, language='en'):
    """
    Sends emails via SendGrid HTTP API.
    Works in both Celery (local) and threading (production fallback).
    """

    current_year = datetime.datetime.now().year
    is_german = language == 'de'

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

    # ---------------- ADMIN EMAIL ----------------
    admin_html = f"""
    <h2>New Contact Message</h2>
    <p><b>Name:</b> {name}</p>
    <p><b>Email:</b> {email}</p>
    <p><b>Subject:</b> {subject}</p>
    <p><b>Message:</b><br>{message}</p>
    """

    admin_payload = {
        "personalizations": [{
            "to": [{"email": sender_identity}],
            "subject": f"Portfolio Contact: {subject}"
        }],
        "from": {"email": sender_identity, "name": "Portfolio Contact"},
        "reply_to": {"email": email, "name": name},
        "content": [{"type": "text/html", "value": admin_html}]
    }

    # ---------------- USER EMAIL ----------------
    visitor_subject = "Thank you for your message" if not is_german else "Danke für deine Nachricht"

    visitor_html = f"""
    <h2>Thank you {name}</h2>
    <p>Your message has been received.</p>
    <p><b>Your message:</b> {message}</p>
    """

    visitor_payload = {
        "personalizations": [{
            "to": [{"email": email}],
            "subject": visitor_subject
        }],
        "from": {"email": sender_identity, "name": "Yohannes Tekle"},
        "content": [{"type": "text/html", "value": visitor_html}]
    }

    try:
        admin_response = requests.post(url, json=admin_payload, headers=headers, timeout=10)
        visitor_response = requests.post(url, json=visitor_payload, headers=headers, timeout=10)

        print("Admin:", admin_response.status_code, admin_response.text)
        print("Visitor:", visitor_response.status_code, visitor_response.text)

        if admin_response.status_code in [200, 201, 202] and visitor_response.status_code in [200, 201, 202]:
            return "Success"

        return "SendGrid Error"

    except Exception as e:
        print("SendGrid Exception:", str(e))
        return str(e)


# =========================================================
# THROTTLE
# =========================================================

class ContactThrottle(throttling.SimpleRateThrottle):
    rate = '5/hour'

    def get_cache_key(self, request, view):
        return self.get_ident(request)


# =========================================================
# REST API VIEWS
# =========================================================

class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        cache_key = "projects_list"
        data = cache.get(cache_key)

        if not data:
            data = Project.objects.filter(featured=True)
            cache.set(cache_key, data, 60 * 15)

        return data


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


# =========================================================
# CONTACT FORM
# =========================================================

class ContactCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ContactThrottle]

    def create(self, request, *args, **kwargs):
        try:
            required = ['name', 'email', 'subject', 'message']

            for field in required:
                if not request.data.get(field):
                    return Response(
                        {"error": f"Missing field: {field}"},
                        status=400
                    )

            return super().create(request, *args, **kwargs)

        except Exception as e:
            return Response({"error": str(e)}, status=500)

    def perform_create(self, serializer):
        message = serializer.save()

        language = self.request.headers.get('Accept-Language', 'en')[:2]
        if language not in ['en', 'de']:
            language = 'en'

        is_production = os.environ.get('RENDER') == 'true' or not settings.DEBUG

        if is_production:
            threading.Thread(
                target=send_contact_email_task,
                args=(message.name, message.email, message.subject, message.message, language),
                daemon=True
            ).start()
        else:
            send_contact_email_task.delay(
                message.name,
                message.email,
                message.subject,
                message.message,
                language
            )


# =========================================================
# DASHBOARD
# =========================================================

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


# =========================================================
# BLOG - FIXED (THIS WAS YOUR ERROR)
# =========================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def recent_blog_posts(request):
    cache_key = "recent_blog_posts"
    posts = cache.get(cache_key)

    if not posts:
        posts = BlogPost.objects.filter(published=True)[:3]
        cache.set(cache_key, posts, 60 * 15)

    serializer = BlogPostListSerializer(posts, many=True)
    return Response(serializer.data)


# =========================================================
# HEALTH CHECK
# =========================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({
        "status": "healthy",
        "timestamp": datetime.datetime.now().isoformat()
    })


# =========================================================
# DEV / ADMIN UTILITIES
# =========================================================

@api_view(['POST'])
@permission_classes([AllowAny])
def test_post(request):
    return Response({"message": "POST works", "data": request.data})


@api_view(['GET'])
@permission_classes([AllowAny])
def list_users(request):
    users = User.objects.values("id", "username", "email")
    return Response(list(users))


@api_view(['POST'])
@permission_classes([AllowAny])
def create_superuser(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email", "")

    if not username or not password:
        return Response({"error": "Missing fields"}, status=400)

    if User.objects.filter(username=username).exists():
        return Response({"error": "User exists"}, status=400)

    User.objects.create_superuser(username=username, email=email, password=password)
    return Response({"message": "Superuser created"}, status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
def safe_migrate(request):
    secret = request.headers.get("X-Migrate-Secret")

    if secret != "your-secret-key-here":
        return Response({"error": "Unauthorized"}, status=401)

    from django.core.management import call_command
    import io

    out = io.StringIO()
    call_command("migrate", stdout=out)

    return Response({"output": out.getvalue()})