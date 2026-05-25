from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BlogPost, Category, Tag, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'post_count']
    
    def get_post_count(self, obj):
        return obj.blogpost_set.filter(published=True).count()


class TagSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'post_count']
    
    def get_post_count(self, obj):
        return obj.blogpost_set.filter(published=True).count()


class CommentSerializer(serializers.ModelSerializer):
    formatted_date = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'name', 'email', 'comment', 'created_at', 'approved', 'formatted_date']
        read_only_fields = ['approved', 'created_at']
    
    def get_formatted_date(self, obj):
        return obj.created_at.strftime("%B %d, %Y")
    
    def validate_comment(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Comment must be at least 3 characters long.")
        return value


class BlogPostListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    author_name = serializers.CharField(source='author.get_full_name', read_only=True)
    author_username = serializers.CharField(source='author.username', read_only=True)
    tag_names = serializers.SerializerMethodField()
    formatted_date = serializers.SerializerMethodField()
    reading_time = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'featured_image',
            'created_at', 'updated_at', 'views', 'published',
            'category_name', 'category_slug', 'author_name', 
            'author_username', 'tag_names', 'formatted_date',
            'reading_time'
        ]
    
    def get_tag_names(self, obj):
        return [tag.name for tag in obj.tags.all()]
    
    def get_formatted_date(self, obj):
        return obj.created_at.strftime("%B %d, %Y")
    
    def get_reading_time(self, obj):
        word_count = len(obj.content.split())
        minutes = max(1, round(word_count / 200))
        return f"{minutes} min read"


# Add this alias for backward compatibility
BlogPostSerializer = BlogPostListSerializer


class BlogPostDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)
    comments = serializers.SerializerMethodField()
    related_posts = serializers.SerializerMethodField()
    formatted_date = serializers.SerializerMethodField()
    formatted_updated_date = serializers.SerializerMethodField()
    reading_time = serializers.SerializerMethodField()
    
    class Meta:
        model = BlogPost
        fields = [
            'id', 'title', 'slug', 'excerpt', 'content', 'featured_image',
            'category', 'tags', 'author', 'views', 'published',
            'created_at', 'updated_at', 'comments', 'related_posts',
            'formatted_date', 'formatted_updated_date', 'reading_time'
        ]
    
    def get_comments(self, obj):
        comments = obj.comments.filter(approved=True)
        return CommentSerializer(comments, many=True).data
    
    def get_related_posts(self, obj):
        related = BlogPost.objects.filter(
            published=True
        ).exclude(
            id=obj.id
        ).filter(
            category=obj.category
        )[:3]
        
        if related.count() < 3:
            additional = BlogPost.objects.filter(
                published=True
            ).exclude(
                id=obj.id
            ).exclude(
                id__in=related.values_list('id', flat=True)
            )[:3 - related.count()]
            related = list(related) + list(additional)
        
        return BlogPostListSerializer(related, many=True).data
    
    def get_formatted_date(self, obj):
        return obj.created_at.strftime("%B %d, %Y")
    
    def get_formatted_updated_date(self, obj):
        return obj.updated_at.strftime("%B %d, %Y")
    
    def get_reading_time(self, obj):
        word_count = len(obj.content.split())
        minutes = max(1, round(word_count / 200))
        return f"{minutes} min read"


class BlogPostCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(),
        write_only=True,
        required=False
    )
    
    class Meta:
        model = BlogPost
        fields = [
            'title', 'slug', 'excerpt', 'content', 'featured_image',
            'category', 'tags', 'published'
        ]
    
    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        blog_post = BlogPost.objects.create(**validated_data)
        
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(
                name=tag_name.lower(),
                defaults={'slug': tag_name.lower().replace(' ', '-')}
            )
            blog_post.tags.add(tag)
        
        return blog_post
    
    def update(self, instance, validated_data):
        tags_data = validated_data.pop('tags', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if tags_data is not None:
            instance.tags.clear()
            for tag_name in tags_data:
                tag, created = Tag.objects.get_or_create(
                    name=tag_name.lower(),
                    defaults={'slug': tag_name.lower().replace(' ', '-')}
                )
                instance.tags.add(tag)
        
        return instance


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'comment']
    
    def validate(self, data):
        spam_keywords = ['viagra', 'casino', 'porn', 'gambling']
        comment_lower = data['comment'].lower()
        
        for keyword in spam_keywords:
            if keyword in comment_lower:
                raise serializers.ValidationError("Your comment contains inappropriate content.")
        
        return data


class BlogArchiveSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    month_name = serializers.CharField()
    count = serializers.IntegerField()


class BlogSearchSerializer(serializers.Serializer):
    query = serializers.CharField(required=True, min_length=2)
    page = serializers.IntegerField(required=False, default=1)