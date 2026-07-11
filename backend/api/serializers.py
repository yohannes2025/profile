# backend/api/serializers.py

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Project, Skill, Testimonial, Experience, Education, ContactMessage
from blog.models import BlogPost, Category, Tag, Comment

class ProjectSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Project
        # 💡 Reverting to "__all__" avoids typos or missing model fields
        fields = "__all__"

    @extend_schema_field(serializers.URLField(allow_null=True))
    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        # 💡 Safely using "__all__" so 'level' configuration mismatch stops crashing
        fields = '__all__'

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = '__all__'

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']

class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = '__all__'
        depth = 1

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'name', 'email', 'comment', 'created_at']
        

class PortfolioDashboardStatsSerializer(serializers.Serializer):
    projects = serializers.IntegerField()
    skills = serializers.IntegerField()
    testimonials = serializers.IntegerField()
    experiences = serializers.IntegerField()
    education = serializers.IntegerField()
    messages = serializers.IntegerField()