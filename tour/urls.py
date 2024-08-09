from django.urls import path, include
from rest_framework import routers
from .views import TourViewSet, HighlightViewSet

router = routers.DefaultRouter()

router.register(r"tours", TourViewSet)
router.register(r"highlights", HighlightViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
