from django.contrib import admin
from .models import Project, Skill, Testimonial, Experience, Education, ContactMessage

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'featured', 'order', 'created_at')
    list_filter = ('featured', 'technologies')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('featured', 'order')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency', 'order')
    list_filter = ('category',)
    list_editable = ('proficiency', 'order')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'rating', 'featured', 'created_at')
    list_filter = ('featured', 'rating')
    search_fields = ('name', 'company', 'feedback')

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'start_date', 'end_date', 'current')
    list_filter = ('current', 'company')
    search_fields = ('title', 'company', 'description')

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('degree', 'institution', 'start_year', 'end_year')
    search_fields = ('degree', 'institution')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'replied', 'created_at')
    list_filter = ('replied', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)