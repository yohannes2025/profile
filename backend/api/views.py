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
# SENDGRID EMAIL TASK (PRODUCTION + CELERY HYBRID READY WITH STYLISH TEMPLATES)
# =============================================================================
@shared_task
def send_contact_email_task(name, email, subject, message, language='en'):
    """
    Sends beautiful HTML/Plain text emails via SendGrid API (HTTP REST).
    1. Notification to admin
    2. Auto-reply confirmation to the visitor (Bilingual: DE/EN)
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
    current_year = datetime.datetime.now().year
    is_german = language == 'de'

    # -------------------------------------------------------------------------
    # 1. ADMIN EMAIL TEMPLATES (HTML & Plain)
    # -------------------------------------------------------------------------
    admin_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; background: #f9fafb; border-radius: 10px; overflow: hidden; }}
            .header {{ background: linear-gradient(135deg, #0891b2, #3b82f6); color: white; padding: 25px; text-align: center; }}
            .content {{ padding: 25px; background: white; }}
            .field {{ margin-bottom: 20px; }}
            .label {{ font-weight: bold; color: #374151; margin-bottom: 5px; font-size: 14px; }}
            .value {{ background: #f3f4f6; padding: 10px; border-radius: 8px; margin-top: 5px; }}
            .message-box {{ background: #fef3c7; padding: 15px; border-radius: 8px; border-left: 4px solid #f59e0b; margin-top: 10px; }}
            .language-badge {{ display: inline-block; background: #e0e7ff; color: #3730a3; padding: 4px 12px; border-radius: 20px; font-size: 12px; margin-bottom: 15px; }}
            .footer {{ text-align: center; font-size: 12px; color: #6b7280; margin-top: 20px; padding-top: 20px; border-top: 1px solid #e5e7eb; }}
            hr {{ margin: 20px 0; border: none; border-top: 1px solid #e5e7eb; }}
            .reply-btn {{ display: inline-block; background: #0891b2; color: white; padding: 10px 20px; border-radius: 8px; text-decoration: none; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h2 style="margin: 0;">📧 New Portfolio Contact Message</h2>
            </div>
            <div class="content">
                <div class="language-badge">
                    🌐 Language: {'German' if is_german else 'English'}
                </div>
                
                <div class="field">
                    <div class="label">👤 Name:</div>
                    <div class="value">{name}</div>
                </div>
                
                <div class="field">
                    <div class="label">📧 Email:</div>
                    <div class="value">{email}</div>
                </div>
                
                <div class="field">
                    <div class="label">📝 Subject:</div>
                    <div class="value">{subject}</div>
                </div>
                
                <div class="field">
                    <div class="label">💬 Message:</div>
                    <div class="value message-box" style="white-space: pre-wrap;">{message}</div>
                </div>
                
                <hr>
                
                <div class="footer">
                    <strong>💡 Quick Reply:</strong><br>
                    <a href="mailto:{email}?subject=Re: {subject}" class="reply-btn">Reply to {name}</a>
                </div>
            </div>
        </div>
    </body>
    </html>
    """

    admin_plain = f"""
    NEW PORTFOLIO CONTACT MESSAGE
    {'=' * 40}
    
    Language: {'German' if is_german else 'English'}
    
    Name: {name}
    Email: {email}
    Subject: {subject}
    
    Message:
    {message}
    
    {'-' * 40}
    Reply to: {email}
    """

    # -------------------------------------------------------------------------
    # 2. VISITOR EMAIL TEMPLATES (HTML & Plain based on language)
    # -------------------------------------------------------------------------
    if is_german:
        visitor_subject = "Vielen Dank für Ihre Nachricht"
        visitor_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; background: #f9fafb; border-radius: 10px; overflow: hidden; }}
                .header {{ background: linear-gradient(135deg, #0891b2, #3b82f6); color: white; padding: 25px; text-align: center; }}
                .content {{ padding: 25px; background: white; }}
                .message-box {{ background: #f0fdf4; padding: 15px; border-radius: 8px; border-left: 4px solid #22c55e; margin: 15px 0; }}
                .signature {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; }}
                .btn {{ display: inline-block; background: #0891b2; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; margin: 5px; }}
                hr {{ margin: 20px 0; border: none; border-top: 1px solid #e5e7eb; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2 style="margin: 0;">Vielen Dank für Ihre Nachricht! 🙏</h2>
                </div>
                <div class="content">
                    <p>Sehr geehrte(r) <strong>{name}</strong>,</p>
                    
                    <p>Vielen Dank, dass Sie mich kontaktiert haben. Ich habe Ihre Nachricht erhalten und werde mich so schnell wie möglich bei Ihnen melden (in der Regel innerhalb von 24-48 Stunden).</p>
                    
                    <div class="message-box">
                        <p><strong>📝 Hier ist eine Kopie Ihrer Nachricht:</strong></p>
                        <p style="font-style: italic; margin: 10px 0 0 0; white-space: pre-wrap;">"{message}"</p>
                    </div>
                    
                    <p>In der Zwischenzeit können Sie gerne:</p>
                    <ul>
                        <li>📱 Mit mir auf <a href="https://linkedin.com/in/yohannes" style="color: #0891b2;">LinkedIn</a> verbinden</li>
                        <li>💻 Meine <a href="https://github.com/yohannes" style="color: #0891b2;">GitHub</a> Projekte ansehen</li>
                        <li>📂 Meine <a href="http://localhost:5173/#projects" style="color: #0891b2;">Portfolio-Projekte</a> durchstöbern</li>
                    </ul>
                    
                    <div style="background: #f3f4f6; padding: 15px; border-radius: 8px; text-align: center; margin: 20px 0;">
                        <p style="margin: 0;">💡 Schauen Sie sich in der Zwischenzeit meine neuesten Arbeiten an!</p>
                        <a href="http://localhost:5173/#projects" class="btn">Zum Portfolio</a>
                    </div>
                    
                    <hr>
                    
                    <p>Mit freundlichen Grüßen,<br>
                    <strong>Yohannes Tekle</strong><br>
                    Full-Stack Entwickler</p>
                    
                    <div class="signature">
                        <p style="font-size: 12px; color: #6b7280;">Dies ist eine automatische Bestätigung. Bitte antworten Sie nicht direkt auf diese E-Mail.</p>
                        <p style="font-size: 12px; color: #6b7280;">© {current_year} Yohannes Tekle. Alle Rechte vorbehalten.</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        visitor_plain = f"""
    Vielen Dank für Ihre Nachricht!
    {'=' * 40}
    
    Sehr geehrte(r) {name},
    
    Vielen Dank, dass Sie mich kontaktiert haben. Ich habe Ihre Nachricht erhalten und werde mich so schnell wie möglich bei Ihnen melden (in der Regel innerhalb von 24-48 Stunden).
    
    Hier ist eine Kopie Ihrer Nachricht:
    "{message}"
    
    In der Zwischenzeit können Sie gerne:
    • Mit mir auf LinkedIn verbinden
    • Meine GitHub Projekte ansehen
    • Meine Portfolio-Projekte durchstöbern
    
    Mit freundlichen Grüßen,
    Yohannes Tekle
    Full-Stack Entwickler
    
    {'-' * 40}
    Dies ist eine automatische Bestätigung. Bitte antworten Sie nicht direkt auf diese E-Mail.
    © {current_year} Yohannes Tekle. Alle Rechte vorbehalten.
    """
    else:
        # English fallback
        visitor_subject = "Thank you for contacting Yohannes Tekle"
        visitor_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; background: #f9fafb; border-radius: 10px; overflow: hidden; }}
                .header {{ background: linear-gradient(135deg, #0891b2, #3b82f6); color: white; padding: 25px; text-align: center; }}
                .content {{ padding: 25px; background: white; }}
                .message-box {{ background: #f0fdf4; padding: 15px; border-radius: 8px; border-left: 4px solid #22c55e; margin: 15px 0; }}
                .signature {{ margin-top: 20px; padding-top: 20px; border-top: 1px solid #e5e7eb; text-align: center; }}
                .btn {{ display: inline-block; background: #0891b2; color: white; padding: 8px 16px; border-radius: 6px; text-decoration: none; margin: 5px; }}
                hr {{ margin: 20px 0; border: none; border-top: 1px solid #e5e7eb; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2 style="margin: 0;">Thank You for Reaching Out! 🙏</h2>
                </div>
                <div class="content">
                    <p>Dear <strong>{name}</strong>,</p>
                    
                    <p>Thank you for contacting me. I have received your message and will get back to you as soon as possible (usually within 24-48 hours).</p>
                    
                    <div class="message-box">
                        <p><strong>📝 Here's a copy of your message:</strong></p>
                        <p style="font-style: italic; margin: 10px 0 0 0; white-space: pre-wrap;">"{message}"</p>
                    </div>
                    
                    <p>In the meantime, feel free to:</p>
                    <ul>
                        <li>📱 Connect with me on <a href="https://linkedin.com/in/yohannes" style="color: #0891b2;">LinkedIn</a></li>
                        <li>💻 Check out my <a href="https://github.com/yohannes" style="color: #0891b2;">GitHub</a> projects</li>
                        <li>📂 Browse my <a href="http://localhost:5173/#projects" style="color: #0891b2;">portfolio projects</a></li>
                    </ul>
                    
                    <div style="background: #f3f4f6; padding: 15px; border-radius: 8px; text-align: center; margin: 20px 0;">
                        <p style="margin: 0;">💡 While you wait, check out my latest work!</p>
                        <a href="http://localhost:5173/#projects" class="btn">View Portfolio</a>
                    </div>
                    
                    <hr>
                    
                    <p>Best regards,<br>
                    <strong>Yohannes Tekle</strong><br>
                    Full-Stack Developer</p>
                    
                    <div class="signature">
                        <p style="font-size: 12px; color: #6b7280;">This is an automated confirmation. Please do not reply directly to this email.</p>
                        <p style="font-size: 12px; color: #6b7280;">© {current_year} Yohannes Tekle. All rights reserved.</p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        visitor_plain = f"""
    Thank You for Reaching Out!
    {'=' * 40}
    
    Dear {name},
    
    Thank you for contacting me. I have received your message and will get back to you as soon as possible (usually within 24-48 hours).
    
    Here's a copy of your message:
    "{message}"
    
    In the meantime, feel free to:
    • Connect with me on LinkedIn
    • Check out my GitHub projects
    • Browse my portfolio projects
    
    Best regards,
    Yohannes Tekle
    Full-Stack Developer
    
    {'-' * 40}
    This is an automated confirmation. Please do not reply directly to this email.
    © {current_year} Yohannes Tekle. All rights reserved.
    """

    # -------------------------------------------------------------------------
    # 3. CONSTRUCT SENDGRID PAYLOADS
    # -------------------------------------------------------------------------
    admin_payload = {
        "personalizations": [{
            "to": [{"email": settings.CONTACT_EMAIL}],
            "subject": f"Portfolio Contact: {subject}"
        }],
        "from": {"email": sender_identity, "name": "Portfolio Admin Notification"},
        "reply_to": {"email": email, "name": name},
        "content": [
            {"type": "text/plain", "value": admin_plain},
            {"type": "text/html", "value": admin_html}
        ]
    }

    visitor_payload = {
        "personalizations": [{
            "to": [{"email": email}],
            "subject": visitor_subject
        }],
        "from": {"email": sender_identity, "name": "Yohannes Tekle"},
        "content": [
            {"type": "text/plain", "value": visitor_plain},
            {"type": "text/html", "value": visitor_html}
        ]
    }

    try:
        res_admin = requests.post(url, json=admin_payload, headers=headers)
        res_visitor = requests.post(url, json=visitor_payload, headers=headers)
        return f"Success (Admin status: {res_admin.status_code}, Visitor status: {res_visitor.status_code})"
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

        # Extract browser language sent from frontend
        language = self.request.headers.get('Accept-Language', 'en')[:2]
        if language not in ['en', 'de']:
            language = 'en'

        is_production = os.environ.get('RENDER') == 'true' or not settings.DEBUG

        if is_production:
            threading.Thread(
                target=send_contact_email_task,
                args=(message.name, message.email, message.subject, message.message, language)
            ).start()
        else:
            send_contact_email_task.delay(
                message.name,
                message.email,
                message.subject,
                message.message,
                language
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