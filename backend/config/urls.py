# backend/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# SAFE IMPORT (IMPORTANT FIX)
from api import views as api_views


def api_root(request):
    return JsonResponse({
        'message': 'Welcome to Portfolio API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'api_docs': '/api/docs/',
            'api_schema': '/api/schema/',
            'projects': '/api/projects/',
            'skills': '/api/skills/',
            'contact': '/api/contact/',
            'recent_posts': '/api/recent-posts/',
            'health': '/healthz',
        }
    })


urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),

    # system endpoints
    path('healthz', api_views.health_check, name='health-check'),
    path('migrate/', api_views.run_migrations, name='migrate'),
    path('safe-migrate/', api_views.safe_migrate, name='safe-migrate'),
    path('create-superuser/', api_views.create_superuser, name='create-superuser'),
    path('list-users/', api_views.list_users, name='list-users'),
    path('api/test-post/', api_views.test_post, name='test-post'),

    # API docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # app routes
    path('api/', include('api.urls')),
    path('api/blog/', include('blog.urls')),

    # IMPORTANT: recent posts moved here safely
    path('api/recent-posts/', api_views.recent_blog_posts, name='recent-posts'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)