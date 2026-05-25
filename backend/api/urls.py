# backend/api/urls.py
from django.urls import path
from .views import (
    ProjectListView, SkillListView, TestimonialListView,
    ExperienceListView, EducationListView, ContactCreateView,
    DashboardStatsView
)

urlpatterns = [
    path('projects/', ProjectListView.as_view(), name='projects'),
    path('skills/', SkillListView.as_view(), name='skills'),
    path('testimonials/', TestimonialListView.as_view(), name='testimonials'),
    path('experiences/', ExperienceListView.as_view(), name='experiences'),
    path('education/', EducationListView.as_view(), name='education'),
    path('contact/', ContactCreateView.as_view(), name='contact'),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
]