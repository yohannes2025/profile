from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, RefreshTokenView,
    UserProfileView, ChangePasswordView, ForgotPasswordView,
    ResetPasswordView, VerifyEmailView, ResendVerificationEmailView,
    UploadAvatarView, DeleteAvatarView, UploadResumeView,
    UserSessionsView, TerminateSessionView, UserActivitiesView,
    DashboardStatsView, PublicProfileView, delete_account, export_user_data
)

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token-refresh'),
    
    # Profile Management
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/<str:username>/', PublicProfileView.as_view(), name='public-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    
    # Password Reset
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    
    # Email Verification
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification/', ResendVerificationEmailView.as_view(), name='resend-verification'),
    
    # File Uploads
    path('upload-avatar/', UploadAvatarView.as_view(), name='upload-avatar'),
    path('delete-avatar/', DeleteAvatarView.as_view(), name='delete-avatar'),
    path('upload-resume/', UploadResumeView.as_view(), name='upload-resume'),
    
    # Sessions & Activities
    path('sessions/', UserSessionsView.as_view(), name='sessions'),
    path('sessions/<int:session_id>/terminate/', TerminateSessionView.as_view(), name='terminate-session'),
    path('activities/', UserActivitiesView.as_view(), name='activities'),
    
    # Dashboard & Utilities
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('delete-account/', delete_account, name='delete-account'),
    path('export-data/', export_user_data, name='export-data'),
]