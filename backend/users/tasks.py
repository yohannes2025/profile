# backend/users/tasks.py

from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mass_mail
from django.conf import settings
from datetime import timedelta
from .models import UserSession, PasswordReset, EmailVerification


@shared_task
def clear_expired_sessions():
    """Clear expired user sessions"""
    thirty_days_ago = timezone.now() - timedelta(days=30)
    deleted_count = UserSession.objects.filter(
        last_activity__lt=thirty_days_ago
    ).delete()[0]
    
    return f"Cleared {deleted_count} expired sessions"


@shared_task
def clear_expired_tokens():
    """Clear expired password reset and email verification tokens"""
    now = timezone.now()
    
    # Clear expired password resets
    password_resets_deleted = PasswordReset.objects.filter(
        expires_at__lt=now
    ).delete()[0]
    
    # Clear expired email verifications
    email_verifications_deleted = EmailVerification.objects.filter(
        expires_at__lt=now,
        verified_at__isnull=True
    ).delete()[0]
    
    return {
        'password_resets_cleared': password_resets_deleted,
        'email_verifications_cleared': email_verifications_deleted
    }


@shared_task
def send_welcome_email(user_id, email, name):
    """Send welcome email to new user"""
    from .models import User
    from django.core.mail import send_mail
    
    try:
        send_mail(
            subject="Welcome to Portfolio!",
            message=f"Hi {name},\n\nThank you for joining our community!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return f"Welcome email sent to {email}"
    except Exception as e:
        return f"Failed to send welcome email: {str(e)}"


@shared_task
def update_user_activity_stats():
    """Update user activity statistics (run daily)"""
    from .models import User, UserActivityLog
    from django.db.models import Count
    
    # Get active users in last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    active_users = UserActivityLog.objects.filter(
        created_at__gte=thirty_days_ago
    ).values('user').annotate(
        activity_count=Count('id')
    ).count()
    
    return {
        'active_users_last_30_days': active_users,
        'total_users': User.objects.count(),
    }