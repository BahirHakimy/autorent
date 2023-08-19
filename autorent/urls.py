from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from authentication.views import ObtainJWTTokenView
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/login", ObtainJWTTokenView.as_view()),
    path("api/", include("core.urls")),
    path(
        "react/", serve, {"document_root": settings.FRONTEND_ROOT, "path": "index.html"}
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
