from django.urls import path, include
from rest_framework import routers
from .views import CarViewSet, BookingViewSet, ReviewViewSet, PaymentViewSet
from authentication.views import UserViewSet

router = routers.DefaultRouter()

router.register(r"users", UserViewSet)
router.register(r"cars", CarViewSet)
router.register(r"bookings", BookingViewSet)
router.register(r"reviews", ReviewViewSet)
router.register(r"payments", PaymentViewSet)

urlpatterns = [path("", include(router.urls))]
