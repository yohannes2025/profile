# backend/config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from api.views import (
    health_check,
    create_superuser,
    run_migrations,
    list_users,
    safe_migrate,
    test_post,
    recent_blog_posts,
)


def api_root(request):
    return JsonResponse({
        "message": "Portfolio API",
        "version": "1.0",
        "endpoints": {
            "projects": "/api/projects/",
            "skills": "/api/skills/",
            "blog": "/api/blog/",
            "recent_posts": "/api/recent-posts/",
            "health": "/healthz",
        }
    })


urlpatterns = [
    path("", api_root),

    path("admin/", admin.site.urls),

    # Health
    path("healthz", health_check),

    # API core
    path("api/", include("api.urls")),
    path("api/users/", include("users.urls")),
    path("api/blog/", include("blog.urls")),

    # Blog shortcut endpoint
    path("api/recent-posts/", recent_blog_posts),

    # Docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),

    # Utilities
    path("migrate/", run_migrations),
    path("safe-migrate/", safe_migrate),
    path("create-superuser/", create_superuser),
    path("list-users/", list_users),
    path("api/test-post/", test_post),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)