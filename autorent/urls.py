from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from authentication.views import ObtainJWTTokenView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/login", ObtainJWTTokenView.as_view()),
    path("api/", include("core.urls")),
]

from django.conf import settings

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
