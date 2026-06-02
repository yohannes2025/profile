# backend/api/views.py
from rest_framework import generics, throttling
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
import datetime
import os
import threading  # Added for decoupled, non-blocking production execution

# Internal app models and serializers
from .models import Project, Skill, Testimonial, Experience, Education, ContactMessage
from .serializers import (
    ProjectSerializer, SkillSerializer, TestimonialSerializer,
    ExperienceSerializer, EducationSerializer, ContactMessageSerializer
)

# Cross-app imports from blog app
from blog.models import BlogPost, Category, Tag, Comment
from blog.serializers import BlogPostListSerializer

# OpenAPI documentation tools
from drf_spectacular.utils import extend_schema
from drf_spectacular.types import OpenApiTypes

# Use the custom User model from users app
from users.models import User


@shared_task
def send_contact_email_task(name, email, subject, message, language='en'):
    """
    Send two emails with HTML formatting:
    1. Notification to admin (you)
    2. Auto-reply confirmation to the visitor (in their language)
    """
    current_year = datetime.datetime.now().year
    
    # Determine language for auto-reply
    is_german = language == 'de'
    
    # Check for empty configurations to prevent hard crashes before processing
    if not settings.DEFAULT_FROM_EMAIL or not settings.CONTACT_EMAIL:
        error_msg = "SMTP settings are incomplete (DEFAULT_FROM_EMAIL or CONTACT_EMAIL missing)."
        print(error_msg)
        return error_msg
    
    # 1. HTML Email to admin (you) - Shows which language was used
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
    
    Language: {'German' if is_german else 'English'}
    
    Name: {name}
    Email: {email}
    Subject: {subject}
    
    Message:
    {message}
    
    {'-' * 40}
    Reply to: {email}
    """
    
    # 2. Auto-reply to visitor - IN THEIR LANGUAGE
    if is_german:
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
                        <p style="font-style: italic; margin: 10px 0 0 0;">"{message}"</p>
                    </div>
                    
                    <p>In der Zwischenzeit können Sie gerne:</p>
                    <ul>
                        <li>📱 Mit mir auf <a href="https://linkedin.com/in/yohannes" style="color: #0891b2;">LinkedIn</a> verbinden</li>
                        <li>💻 Meine <a href="https://github.com/yohannes" style="color: #0891b2;">GitHub</a> Projekte ansehen</li>
                    </ul>
                    
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
    
    Mit freundlichen Grüßen,
    Yohannes Tekle
    Full-Stack Entwickler
    
    {'-' * 40}
    Dies ist eine automatische Bestätigung. Bitte antworten Sie nicht direkt auf diese E-Mail.
    © {current_year} Yohannes Tekle. Alle Rechte vorbehalten.
    """
        email_subject = "Vielen Dank für Ihre Nachricht"
    
    else:
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
                    </ul>
                    
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
    
    Best regards,
    Yohannes Tekle
    Full-Stack Developer
    
    {'-' * 40}
    This is an automated confirmation. Please do not reply directly to this email.
    © {current_year} Yohannes Tekle. All rights reserved.
    """
        email_subject = "Thank you for contacting Yohannes Tekle"
    
    # Safe SMTP Transmission engine wrap
    try:
        print(f"Initiating SMTP handshake with {settings.EMAIL_HOST}...")
        # Send HTML email to admin
        send_mail(
            subject=f"Portfolio Contact: {subject}",
            message=admin_plain,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            fail_silently=False,
            html_message=admin_html,
        )
        
        # Send HTML email to visitor
        send_mail(
            subject=email_subject,
            message=visitor_plain,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
            html_message=visitor_html,
        )
        success_msg = "Emails successfully sent to admin and visitor."
        print(success_msg)
        return success_msg
    except Exception as e:
        error_log = f"SMTP Transmission Exception: {str(e)}"
        print(error_log)
        return error_log


class ContactThrottle(throttling.SimpleRateThrottle):
    """Rate limit for contact form to prevent spam"""
    rate = '5/hour'
    
    def get_cache_key(self, request, view):
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
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]
    throttle_classes = [ContactThrottle]
    
    def create(self, request, *args, **kwargs):
        import logging
        import traceback
        logger = logging.getLogger(__name__)
        
        try:
            logger.info(f"Contact POST request received: {request.data}")
            print(f"Contact data: {request.data}")
            
            # Validate required fields
            required_fields = ['name', 'email', 'subject', 'message']
            for field in required_fields:
                if not request.data.get(field):
                    return Response(
                        {'error': f'Missing required field: {field}'}, 
                        status=400
                    )
            
            return super().create(request, *args, **kwargs)
            
        except Exception as e:
            error_msg = f"Contact error: {str(e)}\n{traceback.format_exc()}"
            logger.error(error_msg)
            print(error_msg)
            return Response(
                {'error': str(e), 'traceback': traceback.format_exc()}, 
                status=500
            )
    
    def perform_create(self, serializer):
        try:
            print("Saving contact message...")
            message = serializer.save()
            print(f"Message saved with id: {message.id}")
            
            language = self.request.headers.get('Accept-Language', 'en')[:2]
            if language not in ['en', 'de']:
                language = 'en'
            print(f"Language: {language}")
            
            # Check environment to determine whether to hand off to Celery or Threading
            # This allows local testing via Docker Compose Celery worker and handles Render gracefully.
            is_production = os.environ.get('RENDER') == 'true' or not settings.DEBUG
            
            if is_production:
                print("Production detected: Dispatched email via native background threading...")
                # Run the task function inside an isolated native Python background thread.
                # Keeps the Render API non-blocking without needing a separate worker service.
                email_thread = threading.Thread(
                    target=send_contact_email_task,
                    args=(message.name, message.email, message.subject, message.message, language)
                )
                email_thread.daemon = True
                email_thread.start()
            else:
                print("Local environment: Handing task execution off to Celery queue...")
                # Run standard celery task distribution when debugging locally via Docker setup
                send_contact_email_task.delay(
                    message.name, 
                    message.email, 
                    message.subject, 
                    message.message,
                    language
                )
            
        except Exception as e:
            import traceback
            print(f"Error in perform_create: {traceback.format_exc()}")
            raise e


class DashboardStatsView(generics.GenericAPIView):
    """Get dashboard statistics for admin"""
    permission_classes = [IsAuthenticated]
    serializer_class = SkillSerializer
    
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


@extend_schema(
    responses={200: BlogPostListSerializer(many=True)},
    description="Fetches recent posts layout array data structures targeting public index pages."
)
@api_view(['GET'])
@permission_classes([AllowAny])
def recent_blog_posts(request):
    """Get recent blog posts for the homepage"""
    cache_key = 'recent_blog_posts'
    posts = cache.get(cache_key)
    
    if not posts:
        posts = BlogPost.objects.filter(published=True)[:3]
        cache.set(cache_key, posts, 60 * 15)
    
    serializer = BlogPostListSerializer(posts, many=True)
    return Response(serializer.data)


@extend_schema(
    responses={200: OpenApiTypes.OBJECT},
    description="Simple health checking verification pipeline target."
)
@api_view(['GET'])
@permission_classes([AllowAny])
@throttle_classes([])  
def health_check(request):
    """Health check endpoint for Render"""
    return Response({'status': 'healthy', 'timestamp': datetime.datetime.now().isoformat()})


@api_view(['GET'])
@permission_classes([AllowAny])
def run_migrations(request):
    """Temporary endpoint to run migrations"""
    from django.core.management import call_command
    import io
    import sys
    
    if settings.DEBUG == True:
        return Response({'error': 'Not allowed in production'}, status=403)
    
    out = io.StringIO()
    sys.stdout = out
    
    try:
        call_command('migrate', stdout=out)
        output = out.getvalue()
        return Response({'status': 'success', 'output': output})
    except Exception as e:
        return Response({'status': 'error', 'error': str(e)}, status=500)
    finally:
        sys.stdout = sys.__stdout__
        

@api_view(['POST'])
@permission_classes([AllowAny])
def create_superuser(request):
    """Temporary endpoint to create superuser"""
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')
        
        if not username:
            return Response({'error': 'Username is required'}, status=400)
        
        if not password:
            return Response({'error': 'Password is required'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': f'User "{username}" already exists'}, 
                status=400
            )
        
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        
        return Response(
            {'message': f'Superuser "{username}" created successfully'}, 
            status=201
        )
        
    except Exception as e:
        return Response(
            {'error': str(e)}, 
            status=500
        )
        

@api_view(['GET'])
@permission_classes([AllowAny])
def list_users(request):
    """List all users (for debugging only - remove in production)"""
    users = User.objects.values('id', 'username', 'email', 'is_superuser', 'is_staff')
    return Response(list(users))

@api_view(['POST'])
@permission_classes([AllowAny])
def safe_migrate(request):
    """Safe migration endpoint with secret key"""
    secret = request.headers.get('X-Migrate-Secret')
    if secret != 'your-secret-key-here':
        return Response({'error': 'Unauthorized'}, status=401)
    
    from django.core.management import call_command
    import io
    
    out = io.StringIO()
    call_command('migrate', stdout=out)
    
    return Response({'status': 'ok', 'output': out.getvalue()})

@api_view(['POST'])
@permission_classes([AllowAny])
def test_post(request):
    """Simple test endpoint to verify POST works"""
    return Response({'message': 'POST works!', 'data': request.data}, status=200)