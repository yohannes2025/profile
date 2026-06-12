# backend/users/views.py
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import Count, Sum, Q
from django.core.cache import cache
from datetime import timedelta
import uuid
import cloudinary.uploader

# Import drf-spectacular utilities to register metadata cleanly
from drf_spectacular.utils import extend_schema, extend_schema_field
from drf_spectacular.types import OpenApiTypes

from .models import User, UserProfile, UserSession, UserActivityLog, EmailVerification, PasswordReset
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserSerializer,
    UserUpdateSerializer, ChangePasswordSerializer, ForgotPasswordSerializer,
    ResetPasswordSerializer, EmailVerificationSerializer, UserSessionSerializer,
    UserActivityLogSerializer, TokenSerializer, AvatarUploadSerializer,
    ResumeUploadSerializer, DashboardStatsSerializer, UserProfileSerializer
)
from api.models import Project, ContactMessage
from blog.models import BlogPost, Comment


class RegisterView(generics.CreateAPIView):
    """
    User registration endpoint
    """
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create email verification token
        verification = EmailVerification.objects.create(
            user=user,
            email=user.email,
            expires_at=timezone.now() + timedelta(days=1)
        )
        
        # Send verification email
        verification_link = f"{settings.FRONTEND_URL}/verify-email/{verification.token}"
        send_mail(
            subject="Verify Your Email Address",
            message=f"Click the link to verify your email: {verification_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'User registered successfully. Please verify your email.',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """
    User login endpoint with JWT tokens
    """
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer
    
    @extend_schema(
        request=UserLoginSerializer,
        responses={200: TokenSerializer},
        description="Authenticates a user via credentials and issues JSON Web Tokens."
    )
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Update last login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        # Track session
        session_key = request.META.get('HTTP_USER_AGENT', '') + str(uuid.uuid4())
        UserSession.objects.create(
            user=user,
            session_key=session_key,
            ip_address=request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')),
            user_agent=request.META.get('HTTP_USER_AGENT'),
        )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'Login successful',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })


class LogoutView(APIView):
    """
    User logout endpoint
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request=None,
        responses={200: OpenApiTypes.OBJECT},
        description="Blacklists the provided refresh token and invalidates the session context."
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            
            # Update session
            session_key = request.META.get('HTTP_USER_AGENT', '')
            UserSession.objects.filter(
                user=request.user,
                session_key=session_key,
                is_active=True
            ).update(
                logout_time=timezone.now(),
                is_active=False
            )
            
            # Log activity
            UserActivityLog.objects.create(
                user=request.user,
                activity_type='logout',
                description="User logged out"
            )
            
            return Response({'message': 'Logout successful'})
        except Exception as e:
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    """
    Refresh JWT token
    """
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=None,
        responses={200: OpenApiTypes.OBJECT},
        description="Generates a replacement short-lived access token using a valid long-lived refresh token token string."
    )
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                'access': str(refresh.access_token),
            })
        except Exception as e:
            return Response({'error': 'Invalid refresh token'}, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Get and update user profile
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    # Force unique operation IDs to clear path collisions against PublicProfileView
    @extend_schema(operation_id="retrieve_personal_profile")
    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @extend_schema(operation_id="update_personal_profile")
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @extend_schema(operation_id="partial_update_personal_profile")
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)


class ChangePasswordView(APIView):
    """
    Change user password
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    
    @extend_schema(
        request=ChangePasswordSerializer,
        responses={200: OpenApiTypes.OBJECT},
        description="Updates an authenticated user password matching their old identity check requirements."
    )
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        # Log activity
        UserActivityLog.objects.create(
            user=user,
            activity_type='password_change',
            description="Password changed"
        )
        
        return Response({'message': 'Password changed successfully'})


class ForgotPasswordView(APIView):
    """
    Request password reset
    """
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer
    
    @extend_schema(
        request=ForgotPasswordSerializer,
        responses={200: OpenApiTypes.OBJECT},
        description="Dispatches a recovery token link to an identified matching account email context."
    )
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        user = User.objects.get(email=email)
        
        # Create reset token
        reset = PasswordReset.objects.create(
            user=user,
            expires_at=timezone.now() + timedelta(hours=24)
        )
        
        # Send reset email
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{reset.token}"
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )
        
        return Response({'message': 'Password reset link sent to your email'})


class ResetPasswordView(APIView):
    """
    Reset password with token
    """
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer
    
    @extend_schema(
        request=ResetPasswordSerializer,
        responses={200: OpenApiTypes.OBJECT},
        description="Applies replacement credentials evaluating verification hash parameters."
    )
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        reset_obj = serializer.validated_data['token']
        user = reset_obj.user
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        reset_obj.used_at = timezone.now()
        reset_obj.save()
        
        # Log activity
        UserActivityLog.objects.create(
            user=user,
            activity_type='password_change',
            description="Password reset"
        )
        
        return Response({'message': 'Password reset successfully'})


class VerifyEmailView(APIView):
    """
    Verify email with token
    """
    permission_classes = [AllowAny]
    serializer_class = EmailVerificationSerializer
    
    @extend_schema(
        request=EmailVerificationSerializer,
        responses={200: OpenApiTypes.OBJECT},
        description="Marks a registered user profile status parameter as confirmed when providing signature token."
    )
    def post(self, request):
        serializer = EmailVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        verification = serializer.validated_data['token']
        user = verification.user
        
        user.is_email_verified = True
        user.save()
        
        verification.verified_at = timezone.now()
        verification.save()
        
        return Response({'message': 'Email verified successfully'})


class ResendVerificationEmailView(APIView):
    """
    Resend verification email
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request=None,
        responses={200: OpenApiTypes.OBJECT},
        description="Generates an email verification token if user profile state is not verified."
    )
    def post(self, request):
        user = request.user
        
        if user.is_email_verified:
            return Response({'error': 'Email already verified'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create new verification token
        verification = EmailVerification.objects.create(
            user=user,
            email=user.email,
            expires_at=timezone.now() + timedelta(days=1)
        )
        
        # Send verification email
        verification_link = f"{settings.FRONTEND_URL}/verify-email/{verification.token}"
        send_mail(
            subject="Verify Your Email Address",
            message=f"Click the link to verify your email: {verification_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
        
        return Response({'message': 'Verification email sent'})


class UploadAvatarView(APIView):
    """
    Upload user avatar
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AvatarUploadSerializer
    
    @extend_schema(
        request=AvatarUploadSerializer,
        responses={200: OpenApiTypes.OBJECT},
        description="Uploads profile image configurations targeting attached remote Cloudinary bucket pipelines."
    )
    def post(self, request):
        serializer = AvatarUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        avatar = serializer.validated_data['avatar']
        
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            avatar,
            folder='users/avatars/',
            transformation={'width': 400, 'height': 400, 'crop': 'fill'}
        )
        
        request.user.avatar = upload_result['secure_url']
        request.user.save()
        
        # Log activity
        UserActivityLog.objects.create(
            user=request.user,
            activity_type='avatar_upload',
            description="Avatar uploaded"
        )
        
        return Response({'avatar_url': upload_result['secure_url']})


class DeleteAvatarView(APIView):
    """
    Delete user avatar
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        responses={200: OpenApiTypes.OBJECT},
        description="Removes the user's avatar image URL reference."
    )
    def delete(self, request):
        if request.user.avatar:
            request.user.avatar = None
            request.user.save()
            
            # Log activity
            UserActivityLog.objects.create(
                user=request.user,
                activity_type='avatar_upload',
                description="Avatar deleted"
            )
        
        return Response({'message': 'Avatar deleted'})


class UploadResumeView(APIView):
    """
    Upload user resume/CV
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ResumeUploadSerializer
    
    @extend_schema(
        request=ResumeUploadSerializer,
        responses={200: OpenApiTypes.OBJECT},
        description="Saves a portfolio resume file link payload context into remote asset stores."
    )
    def post(self, request):
        serializer = ResumeUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        resume = serializer.validated_data['resume']
        
        # Upload to Cloudinary
        upload_result = cloudinary.uploader.upload(
            resume,
            folder='users/resumes/',
            resource_type='raw'
        )
        
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.resume_url = upload_result['secure_url']
        profile.resume_last_updated = timezone.now()
        profile.save()
        
        # Log activity
        UserActivityLog.objects.create(
            user=request.user,
            activity_type='resume_upload',
            description="Resume uploaded"
        )
        
        return Response({'resume_url': upload_result['secure_url']})


class UserSessionsView(generics.ListAPIView):
    """
    List user active sessions
    """
    serializer_class = UserSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserSession.objects.filter(
            user=self.request.user,
            is_active=True
        )


class TerminateSessionView(APIView):
    """
    Terminate a specific session
    """
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        responses={200: OpenApiTypes.OBJECT},
        description="Updates tracking configurations for a specific session identifier, toggling activity parameters false."
    )
    def delete(self, request, session_id):
        session = get_object_or_404(UserSession, id=session_id, user=request.user)
        session.is_active = False
        session.logout_time = timezone.now()
        session.save()
        
        return Response({'message': 'Session terminated'})


class UserActivitiesView(generics.ListAPIView):
    """
    List user activities
    """
    serializer_class = UserActivityLogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserActivityLog.objects.filter(user=self.request.user)[:50]


class DashboardStatsView(APIView):
    """
    Get dashboard statistics for authenticated user
    """
    permission_classes = [IsAuthenticated]
    serializer_class = DashboardStatsSerializer
    
    @extend_schema(
        responses={200: DashboardStatsSerializer},
        description="Gathers analytical aggregation parameters across system assets linked with metrics data profiles."
    )
    def get(self, request):
        cache_key = f"dashboard_stats_{request.user.id}"
        stats = cache.get(cache_key)
        
        if not stats:
            user = request.user
            
            # Calculate stats
            stats = {
                'total_projects': Project.objects.filter(featured=True).count(),
                'total_blog_posts': BlogPost.objects.filter(published=True).count(),
                'total_views': BlogPost.objects.aggregate(total=Sum('views'))['total'] or 0,
                'total_comments': Comment.objects.filter(approved=True).count(),
                'profile_views': user.profile_views,
                'recent_activities': UserActivityLog.objects.filter(user=user)[:10]
            }
            
            cache.set(cache_key, stats, 60 * 5)  # 5 minutes cache
        
        serializer = DashboardStatsSerializer(stats)
        return Response(serializer.data)


class PublicProfileView(generics.RetrieveAPIView):
    """
    View public user profile by username
    """
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'username'
    
    def get_queryset(self):
        return User.objects.filter(is_active=True)
    
    @extend_schema(operation_id="retrieve_public_profile")
    def get(self, request, *args, **kwargs):
        user = self.get_object()
        
        # Increment profile views (once per session)
        viewer_key = f"profile_view_{user.id}_{request.META.get('REMOTE_ADDR')}"
        if not cache.get(viewer_key):
            user.profile_views += 1
            user.save(update_fields=['profile_views'])
            cache.set(viewer_key, True, 3600)  # 1 hour cooldown
        
        serializer = self.get_serializer(user)
        return Response(serializer.data)


# CRITICAL FIX: @extend_schema placed ABOVE @api_view decorator block
@extend_schema(
    responses={200: OpenApiTypes.OBJECT},
    description="Soft deletes the user account state flag context configuration."
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    """
    Delete user account (soft delete)
    """
    user = request.user
    user.is_active = False
    user.save()
    
    # Log activity
    UserActivityLog.objects.create(
        user=user,
        activity_type='logout',
        description="Account deleted"
    )
    
    return Response({'message': 'Account deleted successfully'})


# CRITICAL FIX: @extend_schema placed ABOVE @api_view decorator block
@extend_schema(
    responses={200: OpenApiTypes.OBJECT},
    description="Compiles comprehensive internal logs and identity mapping parameters to export records for GDPR validation workflows."
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_user_data(request):
    """
    Export all user data for GDPR compliance
    """
    user = request.user
    profile = UserProfile.objects.get(user=user)
    
    export_data = {
        'user_info': UserSerializer(user).data,
        'profile_info': UserProfileSerializer(profile).data,
        'activities': UserActivityLogSerializer(user.activities.all(), many=True).data,
        'sessions': UserSessionSerializer(user.sessions.all(), many=True).data,
        'export_date': timezone.now().isoformat()
    }
    
    return Response(export_data)