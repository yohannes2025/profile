# users/serializers.py
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserProfile, UserSession, UserActivityLog, EmailVerification, PasswordReset
import uuid

# Import extend_schema_field to resolve documentation types
from drf_spectacular.utils import extend_schema_field

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Check if email already exists
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "Email already exists."})
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        # Check if login is with email
        if '@' in username:
            try:
                user_obj = User.objects.get(email=username)
                username = user_obj.username
            except User.DoesNotExist:
                pass
        
        user = authenticate(username=username, password=password)
        
        if not user:
            raise serializers.ValidationError("Invalid username or password.")
        
        if not user.is_active:
            raise serializers.ValidationError("This account is inactive.")
        
        # Log user activity
        UserActivityLog.objects.create(
            user=user,
            activity_type='login',
            ip_address=self.context.get('request').META.get('HTTP_X_FORWARDED_FOR', 
                     self.context.get('request').META.get('REMOTE_ADDR')),
            user_agent=self.context.get('request').META.get('HTTP_USER_AGENT'),
        )
        
        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    initials = serializers.SerializerMethodField()
    profile_completion = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'full_name',
            'initials', 'avatar', 'bio', 'profession', 'company', 'location',
            'website', 'github', 'linkedin', 'twitter', 'instagram', 'facebook',
            'youtube', 'years_of_experience', 'phone_number', 'is_email_verified',
            'email_notifications', 'dark_mode_default', 'language', 'profile_views',
            'profile_completion', 'date_joined', 'last_login', 'created_at'
        ]
        read_only_fields = ['id', 'is_email_verified', 'profile_views', 'date_joined', 'last_login', 'created_at']
        # Explicit unique schema definition target name
        ref_name = 'AppUserSerializer'
    
    @extend_schema_field(str)
    def get_full_name(self, obj):
        return obj.get_full_name()
    
    @extend_schema_field(str)
    def get_initials(self, obj):
        return obj.get_initials()
    
    @extend_schema_field(int)
    def get_profile_completion(self, obj):
        return obj.get_profile_completion_percentage()


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'bio', 'profession', 'company',
            'location', 'website', 'github', 'linkedin', 'twitter',
            'instagram', 'facebook', 'youtube', 'phone_number',
            'email_notifications', 'dark_mode_default', 'language'
        ]
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Log activity
        UserActivityLog.objects.create(
            user=instance,
            activity_type='profile_update',
            description="Updated profile information"
        )
        
        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords don't match."})
        return attrs
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value


class ResetPasswordSerializer(serializers.Serializer):
    token = serializers.UUIDField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)
    
    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "Passwords don't match."})
        return attrs
    
    def validate_token(self, value):
        try:
            reset_obj = PasswordReset.objects.get(token=value)
            if not reset_obj.is_valid():
                raise serializers.ValidationError("Password reset token has expired.")
            return reset_obj
        except PasswordReset.DoesNotExist:
            raise serializers.ValidationError("Invalid password reset token.")


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.UUIDField(required=True)
    
    def validate_token(self, value):
        try:
            verification = EmailVerification.objects.get(token=value)
            if not verification.is_valid():
                raise serializers.ValidationError("Verification token has expired.")
            return verification
        except EmailVerification.DoesNotExist:
            raise serializers.ValidationError("Invalid verification token.")


class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = '__all__'
        read_only_fields = ['id', 'session_key', 'login_time', 'last_activity']


class UserActivityLogSerializer(serializers.ModelSerializer):
    formatted_time = serializers.SerializerMethodField()
    
    class Meta:
        model = UserActivityLog
        fields = ['id', 'activity_type', 'description', 'created_at', 'formatted_time']
        read_only_fields = ['id', 'created_at']
    
    @extend_schema_field(str)
    def get_formatted_time(self, obj):
        return obj.created_at.strftime("%B %d, %Y at %I:%M %p")


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()


class AvatarUploadSerializer(serializers.Serializer):
    avatar = serializers.ImageField(required=True)


class ResumeUploadSerializer(serializers.Serializer):
    resume = serializers.FileField(required=True)
    
    def validate_resume(self, value):
        allowed_types = ['application/pdf', 'application/msword', 
                        'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
        if value.content_type not in allowed_types:
            raise serializers.ValidationError("Only PDF and DOC files are allowed.")
        
        if value.size > 5 * 1024 * 1024:  # 5MB
            raise serializers.ValidationError("File size must be less than 5MB.")
        
        return value


class DashboardStatsSerializer(serializers.Serializer):
    total_projects = serializers.IntegerField()
    total_blog_posts = serializers.IntegerField()
    total_views = serializers.IntegerField()
    total_comments = serializers.IntegerField()
    profile_views = serializers.IntegerField()
    recent_activities = UserActivityLogSerializer(many=True)