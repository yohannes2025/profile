from django.urls import path
from .views import (
    BlogListView, BlogDetailView, BlogPostCreateView,
    BlogPostUpdateView, BlogPostDeleteView, CategoryListView,
    CategoryDetailView, TagListView, TagDetailView,
    CommentListView, CommentCreateView, CommentApproveView,
    blog_archive, blog_search, featured_posts, popular_posts,
    clear_blog_cache
)

urlpatterns = [
    # Blog posts
    path('', BlogListView.as_view(), name='blog-list'),
    path('create/', BlogPostCreateView.as_view(), name='blog-create'),
    path('<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),
    path('<slug:slug>/update/', BlogPostUpdateView.as_view(), name='blog-update'),
    path('<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='blog-delete'),
    
    # Categories
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),
    
    # Tags
    path('tags/', TagListView.as_view(), name='tag-list'),
    path('tags/<slug:slug>/', TagDetailView.as_view(), name='tag-detail'),
    
    # Comments
    path('<slug:post_slug>/comments/', CommentListView.as_view(), name='comment-list'),
    path('<slug:post_slug>/comments/create/', CommentCreateView.as_view(), name='comment-create'),
    path('comments/<int:pk>/approve/', CommentApproveView.as_view(), name='comment-approve'),
    
    # Utilities
    path('archive/', blog_archive, name='blog-archive'),
    path('search/', blog_search, name='blog-search'),
    path('featured/', featured_posts, name='featured-posts'),
    path('popular/', popular_posts, name='popular-posts'),
    path('clear-cache/', clear_blog_cache, name='clear-cache'),
]