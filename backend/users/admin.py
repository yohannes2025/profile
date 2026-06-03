# backend/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

# 🌟 FIXED: Changed 'Verification' to 'EmailVerification' to match your models file
from .models import User, UserProfile, UserSession, UserActivityLog, EmailVerification, PasswordReset


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 🌟 FIXED: Removed the empty string element that breaks Django admin column parsing
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_email_verified', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_email_verified', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined', 'profile_views')
    
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Information', {
            'fields': ('avatar', 'bio', 'profession', 'company', 'location', 'website')
        }),
        ('Social Links', {
            'fields': ('github', 'linkedin', 'twitter', 'instagram', 'facebook', 'youtube')
        }),
        ('Professional Details', {
            'fields': ('years_of_experience', 'phone_number')
        }),
        ('Account Status', {
            'fields': ('is_email_verified', 'email_verification_token')
        }),
        ('Preferences', {
            'fields': ('email_notifications', 'dark_mode_default', 'language')
        }),
        ('Statistics', {
            'fields': ('profile_views',)
        }),
    )
    
    def get_avatar_preview(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.avatar)
        return "No Avatar"
    get_avatar_preview.short_description = 'Avatar'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'available_for_work', 'available_for_freelance', 'created_at')
    list_filter = ('available_for_work', 'available_for_freelance')
    search_fields = ('user__username', 'user__email', 'headline')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'device_type', 'login_time', 'last_activity', 'is_active')
    list_filter = ('is_active', 'login_time')
    search_fields = ('user__username', 'ip_address', 'user_agent')
    readonly_fields = ('session_key', 'login_time', 'last_activity')


@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity_type', 'created_at', 'ip_address')
    list_filter = ('activity_type', 'created_at')
    search_fields = ('user__username', 'description', 'ip_address')
    readonly_fields = ('created_at',)


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'created_at', 'expires_at', 'verified_at')
    list_filter = ('verified_at', 'created_at')
    search_fields = ('user__username', 'email')
    readonly_fields = ('token', 'created_at', 'expires_at')


@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'expires_at', 'used_at')
    list_filter = ('used_at', 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('token', 'created_at', 'expires_at')