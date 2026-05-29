# backend/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


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
        },
        'documentation': 'Visit /api/docs/ for interactive API documentation'
    })


urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/users/', include('users.urls')),
    path('api/', include('api.urls')),  # This includes projects, skills, testimonials, etc.
    path('api/blog/', include('blog.urls')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)