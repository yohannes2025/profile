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
    test_post
)


def api_root(request):
    return JsonResponse({
        "message": "Welcome to Portfolio API",
        "version": "1.0.0",
    })


urlpatterns = [
    path('', api_root),
    path('admin/', admin.site.urls),

    path('healthz', health_check),

    path('migrate/', run_migrations),
    path('safe-migrate/', safe_migrate),
    path('create-superuser/', create_superuser),
    path('list-users/', list_users),

    path('api/test-post/', test_post),

    path('api/schema/', SpectacularAPIView.as_view()),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema')),

    path('api/users/', include('users.urls')),
    path('api/', include('api.urls')),
    path('api/blog/', include('blog.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)