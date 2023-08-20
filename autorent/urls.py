from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from authentication.views import ObtainJWTTokenView
from django.views.generic import TemplateView, RedirectView

urlpatterns = [
    path("admin-panel/", admin.site.urls),
    path("api/login", ObtainJWTTokenView.as_view()),
    path("api/", include("core.urls")),
    path("", TemplateView.as_view(template_name="index.html")),
    re_path(r"^(?P<path>.*)/$", TemplateView.as_view(template_name="index.html")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
