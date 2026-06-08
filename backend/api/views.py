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
import logging
import traceback

from .models import Project, Skill, Testimonial, Experience, Education, ContactMessage
from .serializers import (
    ProjectSerializer, SkillSerializer, TestimonialSerializer,
    ExperienceSerializer, EducationSerializer, ContactMessageSerializer
)

from blog.models import BlogPost
from blog.serializers import BlogPostListSerializer

from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

from users.models import User

logger = logging.getLogger(__name__)


# ==============================================================================
# EMAIL TASK (HYBRID: CELERY LOCAL / SENDGRID PROD)
# ==============================================================================

def send_contact_email_task(name, email, subject, message, language='en'):
    """
    Hybrid email system:
    - Local: Celery task (optional)
    - Production: SendGrid HTTP API (always used on Render)
    """

    current_year = datetime.datetime.now().year
    is_german = language == 'de'

    sendgrid_api_key = os.environ.get("SENDGRID_API_KEY")
    if not sendgrid_api_key:
        print("Missing SENDGRID_API_KEY")
        return "Missing API Key"

    url = "https://api.sendgrid.com/v3/mail/send"

    headers = {
        "Authorization": f"Bearer {sendgrid_api_key}",
        "Content-Type": "application/json"
    }

    sender_identity = settings.DEFAULT_FROM_EMAIL

    # =========================
    # ADMIN EMAIL HTML
    # =========================
    admin_html = f"""
    <html>
    <body>
        <h2>New Contact Message</h2>
        <p><b>Name:</b> {name}</p>
        <p><b>Email:</b> {email}</p>
        <p><b>Subject:</b> {subject}</p>
        <p><b>Message:</b><br>{message}</p>
    </body>
    </html>
    """

    # =========================
    # VISITOR AUTO REPLY
    # =========================
    visitor_subject = (
        "Vielen Dank für Ihre Nachricht" if is_german
        else "Thank you for contacting me"
    )

    visitor_html = f"""
    <html>
    <body>
        <p>Hello <b>{name}</b>,</p>
        <p>Thank you for your message. I will respond within 24–48 hours.</p>
        <p>Your message:</p>
        <blockquote>{message}</blockquote>
    </body>
    </html>
    """

    admin_payload = {
        "personalizations": [{
            "to": [{"email": settings.CONTACT_EMAIL}],
            "subject": f"Portfolio Contact: {subject}"
        }],
        "from": {
            "email": sender_identity,
            "name": "Portfolio Contact Form"
        },
        "reply_to": {
            "email": email,
            "name": name
        },
        "content": [{"type": "text/html", "value": admin_html}]
    }

    visitor_payload = {
        "personalizations": [{
            "to": [{"email": email}],
            "subject": visitor_subject
        }],
        "from": {
            "email": sender_identity,
            "name": "Yohannes Tekle"
        },
        "content": [{"type": "text/html", "value": visitor_html}]
    }

    try:
        print("Sending email via SendGrid...")

        admin_response = requests.post(url, json=admin_payload, headers=headers, timeout=10)
        visitor_response = requests.post(url, json=visitor_payload, headers=headers, timeout=10)

        print("Admin:", admin_response.status_code, admin_response.text)
        print("Visitor:", visitor_response.status_code, visitor_response.text)

        return "Success"

    except Exception as e:
        print(f"Email error: {str(e)}")
        return str(e)


# ==============================================================================
# CONTACT THROTTLE
# ==============================================================================
class ContactThrottle(throttling.SimpleRateThrottle):
    rate = '5/hour'

    def get_cache_key(self, request, view):
        return self.get_ident(request)


# ==============================================================================
# CONTACT VIEW (HYBRID EXECUTION)
# ==============================================================================
class ContactCreateView(generics.CreateAPIView):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ContactThrottle]

    def create(self, request, *args, **kwargs):
        try:
            required_fields = ['name', 'email', 'subject', 'message']

            for field in required_fields:
                if not request.data.get(field):
                    return Response(
                        {'error': f'Missing field: {field}'},
                        status=400
                    )

            return super().create(request, *args, **kwargs)

        except Exception as e:
            logger.error(traceback.format_exc())
            return Response({'error': str(e)}, status=500)

    def perform_create(self, serializer):
        message = serializer.save()

        language = self.request.headers.get('Accept-Language', 'en')[:2]
        if language not in ['en', 'de']:
            language = 'en'

        is_production = os.environ.get('RENDER') == 'true' or not settings.DEBUG

        # =========================
        # PRODUCTION (Render) → THREAD + SENDGRID
        # =========================
        if is_production:
            print("Production: using SendGrid via threading")

            threading.Thread(
                target=send_contact_email_task,
                args=(
                    message.name,
                    message.email,
                    message.subject,
                    message.message,
                    language
                )
            ).start()

        # =========================
        # LOCAL DEV → CELERY (optional)
        # =========================
        else:
            print("Local: using Celery")

            try:
                from .tasks import send_contact_email_task as celery_task
                celery_task.delay(
                    message.name,
                    message.email,
                    message.subject,
                    message.message,
                    language
                )
            except Exception:
                print("Celery not available, falling back to direct call")
                send_contact_email_task(
                    message.name,
                    message.email,
                    message.subject,
                    message.message,
                    language
                )


# ==============================================================================
# BLOG / PROJECT / OTHER VIEWS (UNCHANGED CORE LOGIC)
# ==============================================================================

class ProjectListView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        cache_key = 'projects_list'
        queryset = cache.get(cache_key)
        if not queryset:
            queryset = Project.objects.filter(featured=True)
            cache.set(cache_key, queryset, 60 * 15)
        return queryset


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


class DashboardStatsView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'projects': Project.objects.count(),
            'skills': Skill.objects.count(),
            'testimonials': Testimonial.objects.count(),
            'experiences': Experience.objects.count(),
            'education': Education.objects.count(),
            'messages': ContactMessage.objects.count(),
            'unread_messages': ContactMessage.objects.filter(replied=False).count(),
        })


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat()
    })