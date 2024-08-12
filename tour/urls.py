from django.urls import path, include
from rest_framework import routers
from .views import TourViewSet, HighlightViewSet, TransferViewSet, ReviewViewSet, HotelViewSet

router = routers.DefaultRouter()

router.register(r"tours", TourViewSet)
router.register(r"highlights", HighlightViewSet)
router.register(r"transfers", TransferViewSet)
router.register(r"reviews", ReviewViewSet)
router.register(r"hotels", HotelViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
