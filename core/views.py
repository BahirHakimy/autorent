from django.shortcuts import render
from rest_framework import viewsets
from .models import Car, Booking, Review
from .serializers import (
    BookingSerializer,
    CarSerializer,
    ReviewSerializer,
)


def hello_world(request):
    return render(request, "index.html")


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
