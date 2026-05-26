# backend/api/views.py
from rest_framework import generics, throttling
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
import datetime
from .models import Project, Skill, Testimonial, Experience, Education, ContactMessage
from .serializers import (
    ProjectSerializer, SkillSerializer, TestimonialSerializer,
    ExperienceSerializer, EducationSerializer, ContactMessageSerializer
)


@shared_task
def send_contact_email_task(name, email, subject, message):
    """
    Send two emails with HTML formatting:
    1. Notification to admin (you)
    2. Auto-reply confirmation to the visitor
    """
    current_year = datetime.datetime.now().year
    
    # 1. HTML Email to admin (you)
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
                    <div class="message-box">{message}</div>
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
    
    Name: {name}
    Email: {email}
    Subject: {subject}
    
    Message:
    {message}
    
    {'-' * 40}
    Reply to: {email}
    """
    
    # Send HTML email to admin
    send_mail(
        subject=f"Portfolio Contact: {subject}",
        message=admin_plain,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.CONTACT_EMAIL],
        fail_silently=False,
        html_message=admin_html,
    )
    
    # 2. HTML Auto-reply to visitor
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
            .social-links {{ margin: 15px 0; }}
            .social-links a {{ color: #0891b2; text-decoration: none; margin: 0 10px; }}
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
                    <p style="font-style: italic; margin: 10px 0 0 0;">"{message}"</p>
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
    • Check out my portfolio projects
    • Connect with me on LinkedIn
    • Follow me on GitHub
    
    Best regards,
    Yohannes Tekle
    Full-Stack Developer
    
    {'-' * 40}
    This is an automated confirmation. Please do not reply directly to this email.
    © {current_year} Yohannes Tekle. All rights reserved.
    """
    
    # Send HTML email to visitor
    send_mail(
        subject="Thank you for contacting Yohannes Tekle",
        message=visitor_plain,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
        html_message=visitor_html,
    )
    
    return f"Emails sent to admin ({settings.CONTACT_EMAIL}) and visitor ({email})"


class ContactThrottle(throttling.SimpleRateThrottle):
    """Rate limit for contact form to prevent spam"""
    rate = '5/hour'
    
    def get_cache_key(self, request, view):
        # Use IP address as the cache key for rate limiting
        return self.get_ident(request)


class ProjectListView(generics.ListAPIView):
    """List all featured projects"""
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
    """List all skills"""
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [AllowAny]


class TestimonialListView(generics.ListAPIView):
    """List all featured testimonials"""
    queryset = Testimonial.objects.filter(featured=True)
    serializer_class = TestimonialSerializer
    permission_classes = [AllowAny]


class ExperienceListView(generics.ListAPIView):
    """List all work experiences"""
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer
    permission_classes = [AllowAny]


class EducationListView(generics.ListAPIView):
    """List all education"""
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    permission_classes = [AllowAny]


class ContactCreateView(generics.CreateAPIView):
    """
    Create a new contact message.
    Sends two emails:
    1. Notification to admin (HTML formatted)
    2. Auto-reply confirmation to the visitor (HTML formatted)
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ContactThrottle]
    
    def perform_create(self, serializer):
        # Save the contact message to database
        message = serializer.save()
        
        # Send emails via Celery
        send_contact_email_task.delay(
            message.name, 
            message.email, 
            message.subject, 
            message.message
        )


class DashboardStatsView(generics.GenericAPIView):
    """Get dashboard statistics for admin"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        stats = {
            'projects': Project.objects.count(),
            'skills': Skill.objects.count(),
            'testimonials': Testimonial.objects.count(),
            'experiences': Experience.objects.count(),
            'education': Education.objects.count(),
            'messages': ContactMessage.objects.count(),
            'unread_messages': ContactMessage.objects.filter(replied=False).count(),
        }
        return Response(stats)


@api_view(['GET'])
@permission_classes([AllowAny])
def recent_blog_posts(request):
    """Get recent blog posts for the homepage"""
    from blog.models import BlogPost
    from blog.serializers import BlogPostListSerializer
    
    cache_key = 'recent_blog_posts'
    posts = cache.get(cache_key)
    
    if not posts:
        posts = BlogPost.objects.filter(published=True)[:3]
        cache.set(cache_key, posts, 60 * 15)
    
    serializer = BlogPostListSerializer(posts, many=True)
    return Response(serializer.data)