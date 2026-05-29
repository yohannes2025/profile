# backend/api/urls.py
from django.urls import path
from config.urls import api_root  # Import the central API endpoints overview map
from .views import (
    ProjectListView, SkillListView, TestimonialListView,
    ExperienceListView, EducationListView, ContactCreateView,
    DashboardStatsView
)

urlpatterns = [
    # Catches the bare /api/ root path passed down from the core URLs inclusion
    path('', api_root, name='api-index'),
    
    path('projects/', ProjectListView.as_view(), name='projects'),
    path('skills/', SkillListView.as_view(), name='skills'),
    path('testimonials/', TestimonialListView.as_view(), name='testimonials'),
    path('experiences/', ExperienceListView.as_view(), name='experiences'),
    path('education/', EducationListView.as_view(), name='education'),
    path('contact/', ContactCreateView.as_view(), name='contact'),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]