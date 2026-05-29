from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone
from cloudinary.models import CloudinaryField
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
import uuid


class User(AbstractUser):
    """
    Custom User model with additional fields for portfolio website
    """
    # Profile Information
    avatar = CloudinaryField('avatar', folder='users/avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)
    profession = models.CharField(max_length=200, blank=True, null=True)
    company = models.CharField(max_length=200, blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # Social Links
    github = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    
    # Professional Details
    years_of_experience = models.IntegerField(default=0)
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    
    # Account Status
    is_email_verified = models.BooleanField(default=False)
    email_verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    password_reset_token = models.UUIDField(blank=True, null=True)
    password_reset_created = models.DateTimeField(blank=True, null=True)
    
    # Preferences
    email_notifications = models.BooleanField(default=True)
    dark_mode_default = models.BooleanField(default=False)
    language = models.CharField(max_length=10, default='en')
    
    # Statistics
    profile_views = models.IntegerField(default=0)
    last_active = models.DateTimeField(auto_now=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.get_full_name() or self.username
    
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def get_short_name(self):
        return self.first_name or self.username
    
    def get_initials(self):
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        return self.username[:2].upper()
    
    def get_profile_completion_percentage(self):
        """Calculate profile completion percentage"""
        fields = [
            self.first_name, self.last_name, self.email,
            self.bio, self.profession, self.location,
            self.avatar, self.github, self.linkedin
        ]
        filled = sum(1 for field in fields if field)
        return int((filled / len(fields)) * 100)


class UserProfile(models.Model):
    """
    Extended user profile with additional portfolio-specific information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # Professional Summary
    headline = models.CharField(max_length=200, blank=True, null=True)
    summary = models.TextField(max_length=1000, blank=True, null=True)
    
    # Skills & Expertise
    skills = models.JSONField(default=list, help_text="List of skills with proficiency levels")
    certifications = models.JSONField(default=list, help_text="List of certifications")
    languages = models.JSONField(default=list, help_text="Languages spoken with proficiency")
    
    # Availability
    available_for_work = models.BooleanField(default=True)
    available_for_freelance = models.BooleanField(default=True)
    preferred_work_types = models.JSONField(default=list, help_text="['remote', 'onsite', 'hybrid']")
    expected_salary_range = models.CharField(max_length=100, blank=True, null=True)
    
    # Resume/CV
    resume_url = models.URLField(blank=True, null=True)
    resume_last_updated = models.DateTimeField(blank=True, null=True)
    
    # Portfolio Preferences
    show_email = models.BooleanField(default=True)
    show_phone = models.BooleanField(default=False)
    show_social_links = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"Profile of {self.user.get_full_name()}"


class UserSession(models.Model):
    """
    Track user sessions for analytics
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=40, unique=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    device_type = models.CharField(max_length=50, blank=True, null=True)
    browser = models.CharField(max_length=100, blank=True, null=True)
    os = models.CharField(max_length=100, blank=True, null=True)
    location = models.JSONField(default=dict, blank=True, null=True)
    login_time = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    logout_time = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'user_sessions'
        ordering = ['-login_time']
    
    def __str__(self):
        return f"Session for {self.user.username} at {self.login_time}"


class UserActivityLog(models.Model):
    """
    Log user activities for audit and analytics
    """
    ACTIVITY_TYPES = [
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('profile_update', 'Profile Update'),
        ('password_change', 'Password Change'),
        ('email_change', 'Email Change'),
        ('avatar_upload', 'Avatar Upload'),
        ('resume_upload', 'Resume Upload'),
        ('project_view', 'Project View'),
        ('blog_view', 'Blog View'),
        ('comment', 'Comment'),
        ('contact', 'Contact Form'),
        ('download', 'Download'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES)
    description = models.TextField(blank=True, null=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_activities'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['activity_type']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.activity_type} at {self.created_at}"


class EmailVerification(models.Model):
    """
    Email verification tokens
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_verifications')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    verified_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'email_verifications'
    
    def is_valid(self):
        return not self.verified_at and self.expires_at > timezone.now()
    
    def __str__(self):
        return f"Verification for {self.email}"


class PasswordReset(models.Model):
    """
    Password reset tokens
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_resets')
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'password_resets'
    
    def is_valid(self):
        return not self.used_at and self.expires_at > timezone.now()
    
    def __str__(self):
        return f"Password reset for {self.user.email}"