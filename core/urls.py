from django.urls import path, include
from django.conf import settings
from rest_framework import routers
from .views import CarViewSet, BookingViewSet, ReviewViewSet
from authentication.views import UserViewSet

router = routers.DefaultRouter()

router.register(r"users", UserViewSet)
router.register(r"cars", CarViewSet)
router.register(r"bookings", BookingViewSet)
router.register(r"reviews", ReviewViewSet)

urlpatterns = [path("", include(router.urls))]
