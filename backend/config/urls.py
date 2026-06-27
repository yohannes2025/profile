# backend/config/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  # Keep this one
from django.http import JsonResponse

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# ✅ ONLY import functions that actually exist in api/views.py
from api.views import health_check, recent_blog_posts, test_post


def api_root(request):
    return JsonResponse({
        "message": "Welcome to Portfolio API",
        "version": "1.0.0",
        "endpoints": {
            "admin": "/admin/",
            "api_docs": "/api/docs/",
            "api_schema": "/api/schema/",
            "users": "/api/users/",
            "projects": "/api/projects/",
            "skills": "/api/skills/",
            "testimonials": "/api/testimonials/",
            "experiences": "/api/experiences/",
            "education": "/api/education/",
            "blog": "/api/blog/",
            "recent_posts": "/api/recent-posts/",
            "health": "/healthz",
            "test_post": "/api/test-post/",
        },
        "documentation": "Visit /api/docs/ for interactive API documentation"
    })


urlpatterns = [
    path("", api_root, name="api-root"),

    path("admin/", admin.site.urls),
    
    # ✅ Mounted rich text image/file upload internal routing endpoints
    path("ckeditor5/", include('django_ckeditor_5.urls')),

    path("healthz", health_check, name="health-check"),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    path("api/users/", include("users.urls")),
    path("api/", include("api.urls")),
    path("api/blog/", include("blog.urls")),

    path("api/recent-posts/", recent_blog_posts, name="recent-posts"),
    path("api/test-post/", test_post, name="test-post"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)