from django.db.models import Q, Count
from django.core.cache import cache
from django.utils import timezone
from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django.utils.decorators import method_decorator
from datetime import timedelta
from .models import BlogPost, Category, Tag, Comment
from .serializers import (
    BlogPostListSerializer, BlogPostDetailSerializer, 
    BlogPostCreateUpdateSerializer, CategorySerializer, 
    TagSerializer, CommentSerializer, CommentCreateSerializer,
    BlogArchiveSerializer, BlogSearchSerializer
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = 'page_size'
    max_page_size = 50


@method_decorator(cache_page(60 * 15), name='dispatch')
@method_decorator(vary_on_headers('Authorization'), name='dispatch')
class BlogListView(generics.ListAPIView):
    serializer_class = BlogPostListSerializer
    permission_classes = [AllowAny]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'excerpt', 'content', 'tags__name', 'category__name']
    ordering_fields = ['created_at', 'views', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        cache_key = f"blog_list_{self.request.GET.urlencode()}"
        queryset = cache.get(cache_key)
        
        if not queryset:
            queryset = BlogPost.objects.filter(published=True)
            
            category_slug = self.request.query_params.get('category')
            if category_slug:
                queryset = queryset.filter(category__slug=category_slug)
            
            tag_slug = self.request.query_params.get('tag')
            if tag_slug:
                queryset = queryset.filter(tags__slug=tag_slug)
            
            author_username = self.request.query_params.get('author')
            if author_username:
                queryset = queryset.filter(author__username=author_username)
            
            start_date = self.request.query_params.get('start_date')
            end_date = self.request.query_params.get('end_date')
            if start_date:
                queryset = queryset.filter(created_at__gte=start_date)
            if end_date:
                queryset = queryset.filter(created_at__lte=end_date)
            
            year = self.request.query_params.get('year')
            month = self.request.query_params.get('month')
            if year and month:
                queryset = queryset.filter(
                    created_at__year=year,
                    created_at__month=month
                )
            elif year:
                queryset = queryset.filter(created_at__year=year)
            
            queryset = queryset.select_related('category', 'author').prefetch_related('tags')
            cache.set(cache_key, queryset, 60 * 15)
        
        return queryset


@method_decorator(cache_page(60 * 15), name='dispatch')
class BlogDetailView(generics.RetrieveAPIView):
    queryset = BlogPost.objects.filter(published=True)
    serializer_class = BlogPostDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        
        viewer_key = f"viewed_post_{instance.id}_{request.META.get('REMOTE_ADDR')}"
        if not cache.get(viewer_key):
            instance.views += 1
            instance.save(update_fields=['views'])
            cache.set(viewer_key, True, 3600)
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BlogPostCreateView(generics.CreateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostCreateUpdateSerializer
    permission_classes = [IsAdminUser]
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BlogPostUpdateView(generics.UpdateAPIView):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostCreateUpdateSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'
    
    def perform_update(self, serializer):
        serializer.save()
        cache_key = f"blog_detail_{self.kwargs.get('slug')}"
        cache.delete(cache_key)
        cache.delete_pattern("blog_list_*")


class BlogPostDeleteView(generics.DestroyAPIView):
    queryset = BlogPost.objects.all()
    permission_classes = [IsAdminUser]
    lookup_field = 'slug'


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.annotate(
        post_count=Count('blogpost', filter=Q(blogpost__published=True))
    )
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        cache_key = 'categories_list'
        queryset = cache.get(cache_key)
        if not queryset:
            queryset = super().get_queryset()
            cache.set(cache_key, queryset, 60 * 60)
        return queryset


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class TagListView(generics.ListAPIView):
    queryset = Tag.objects.annotate(
        post_count=Count('blogpost', filter=Q(blogpost__published=True))
    )
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        cache_key = 'tags_list'
        queryset = cache.get(cache_key)
        if not queryset:
            queryset = super().get_queryset()
            cache.set(cache_key, queryset, 60 * 60)
        return queryset


class TagDetailView(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        post_slug = self.kwargs.get('post_slug')
        post = BlogPost.objects.get(slug=post_slug)
        return Comment.objects.filter(post=post, approved=True)


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        post_slug = self.kwargs.get('post_slug')
        post = BlogPost.objects.get(slug=post_slug)
        serializer.save(post=post, approved=False)


class CommentApproveView(generics.UpdateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAdminUser]
    serializer_class = CommentSerializer
    
    def perform_update(self, serializer):
        serializer.save(approved=True)


@api_view(['GET'])
@permission_classes([AllowAny])
def blog_archive(request):
    cache_key = 'blog_archive'
    archives = cache.get(cache_key)
    
    if not archives:
        archives = BlogPost.objects.filter(published=True) \
            .dates('created_at', 'month', order='DESC')
        
        result = []
        for date in archives:
            count = BlogPost.objects.filter(
                published=True,
                created_at__year=date.year,
                created_at__month=date.month
            ).count()
            result.append({
                'year': date.year,
                'month': date.month,
                'month_name': date.strftime('%B'),
                'count': count
            })
        
        archives = result
        cache.set(cache_key, archives, 60 * 60 * 24)
    
    serializer = BlogArchiveSerializer(archives, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def blog_search(request):
    serializer = BlogSearchSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    
    query = serializer.validated_data['query']
    page = serializer.validated_data.get('page', 1)
    page_size = 10
    
    results = BlogPost.objects.filter(
        Q(published=True)
    ).filter(
        Q(title__icontains=query) |
        Q(content__icontains=query) |
        Q(excerpt__icontains=query) |
        Q(tags__name__icontains=query) |
        Q(category__name__icontains=query)
    ).distinct().select_related('category', 'author').prefetch_related('tags')
    
    scored_results = []
    for post in results:
        score = 0
        title_lower = post.title.lower()
        content_lower = post.content.lower()
        query_lower = query.lower()
        
        if query_lower in title_lower:
            score += 10
            if title_lower.startswith(query_lower):
                score += 5
        
        score += content_lower.count(query_lower) * 2
        
        if query_lower in [tag.name.lower() for tag in post.tags.all()]:
            score += 8
        
        if post.category and query_lower in post.category.name.lower():
            score += 6
        
        scored_results.append((post, score))
    
    scored_results.sort(key=lambda x: x[1], reverse=True)
    
    start = (page - 1) * page_size
    end = start + page_size
    paginated_results = [post for post, _ in scored_results[start:end]]
    
    result_serializer = BlogPostListSerializer(paginated_results, many=True)
    
    return Response({
        'count': len(scored_results),
        'results': result_serializer.data,
        'query': query,
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def featured_posts(request):
    cache_key = 'featured_posts'
    featured = cache.get(cache_key)
    
    if not featured:
        thirty_days_ago = timezone.now() - timedelta(days=30)
        featured = BlogPost.objects.filter(
            published=True,
            created_at__gte=thirty_days_ago
        ).order_by('-views')[:5]
        cache.set(cache_key, featured, 60 * 60 * 6)
    
    serializer = BlogPostListSerializer(featured, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def popular_posts(request):
    cache_key = 'popular_posts'
    popular = cache.get(cache_key)
    
    if not popular:
        popular = BlogPost.objects.filter(published=True).order_by('-views')[:5]
        cache.set(cache_key, popular, 60 * 60 * 12)
    
    serializer = BlogPostListSerializer(popular, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def clear_blog_cache(request):
    cache.delete_pattern("blog_*")
    cache.delete_pattern("categories_*")
    cache.delete_pattern("tags_*")
    return Response({'message': 'Blog cache cleared successfully'})