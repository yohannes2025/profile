# backend/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from api.views import recent_blog_posts, health_check, create_superuser, run_migrations


def api_root(request):
    """Root endpoint showing available API endpoints"""
    return JsonResponse({
        'message': 'Welcome to Portfolio API',
        'version': '1.0.0',
        'endpoints': {
            'admin': '/admin/',
            'api_docs': '/api/docs/',
            'api_schema': '/api/schema/',
            'users': '/api/users/',
            'projects': '/api/projects/',
            'skills': '/api/skills/',
            'testimonials': '/api/testimonials/',
            'experiences': '/api/experiences/',
            'education': '/api/education/',
            'blog': '/api/blog/',
            'recent_posts': '/api/recent-posts/',
            'health': '/healthz',
            'migrate': '/migrate/',
            'create_superuser': '/create-superuser/',
        },
        'documentation': 'Visit /api/docs/ for interactive API documentation'
    })


urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('healthz', health_check, name='health-check'), 
    path('migrate/', run_migrations, name='migrate'),
    path('create-superuser/', create_superuser, name='create-superuser'), 
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/users/', include('users.urls')),
    
    # --- Strict Catchers for the Base API Route ---
    path('api', api_root, name='api-root-noslash'),  # Catches exactly /api
    path('api/', api_root, name='api-root-slash'),   # Catches exactly /api/
    # ----------------------------------------------

    path('api/', include('api.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/recent-posts/', recent_blog_posts, name='recent-posts'),
    path('create-admin/', create_default_admin, name='create-default-admin'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)