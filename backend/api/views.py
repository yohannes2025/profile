# backend/api/views.py
from rest_framework import generics, throttling
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from .models import Project, Skill, Testimonial, Experience, Education, ContactMessage
from .serializers import (
    ProjectSerializer, SkillSerializer, TestimonialSerializer,
    ExperienceSerializer, EducationSerializer, ContactMessageSerializer
)


@shared_task
def send_contact_email_task(name, email, subject, message):
    """
    Send two emails:
    1. Notification to admin (you)
    2. Auto-reply confirmation to the visitor
    """
    # 1. Send email to admin (you)
    admin_subject = f"Portfolio Contact: {subject}"
    admin_message = f"""
    New message from your portfolio website:
    
    Name: {name}
    Email: {email}
    Subject: {subject}
    
    Message:
    {message}
    
    ---
    Reply to: {email}
    """
    
    send_mail(
        subject=admin_subject,
        message=admin_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.CONTACT_EMAIL],
        fail_silently=False,
    )
    
    # 2. Send auto-reply confirmation to the visitor
    auto_reply_subject = "Thank you for contacting Yohannes Tekle"
    auto_reply_message = f"""
Dear {name},

Thank you for reaching out to me. I have received your message and will get back to you within 24-48 hours.

Here's a copy of your message:
"{message}"

In the meantime, feel free to:
• Check out my portfolio projects
• Connect with me on LinkedIn
• Follow me on GitHub

Best regards,
Yohannes Tekle
Full-Stack Developer

---
This is an automated confirmation. Please do not reply directly to this email.
© {__import__('datetime').datetime.now().year} Yohannes Tekle. All rights reserved.
"""
    
    send_mail(
        subject=auto_reply_subject,
        message=auto_reply_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )
    
    return f"Emails sent to admin ({settings.CONTACT_EMAIL}) and visitor ({email})"


class ContactThrottle(throttling.SimpleRateThrottle):
    """Rate limit for contact form to prevent spam"""
    rate = '5/hour'


class ProjectListView(generics.ListAPIView):
    """List all featured projects"""
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        cache_key = 'projects_list'
        queryset = cache.get(cache_key)
        if not queryset:
            queryset = Project.objects.filter(featured=True)
            cache.set(cache_key, queryset, 60 * 15)  # Cache for 15 minutes
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
    1. Notification to admin
    2. Auto-reply confirmation to the visitor
    """
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ContactThrottle]
    
    def perform_create(self, serializer):
        # Save the contact message to database
        message = serializer.save()
        
        # Send emails (admin notification + auto-reply) via Celery task
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
        cache.set(cache_key, posts, 60 * 15)  # Cache for 15 minutes
    
    serializer = BlogPostListSerializer(posts, many=True)
    return Response(serializer.data)