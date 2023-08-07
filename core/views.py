from datetime import datetime
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Car, Booking, Review
from .serializers import (
    BookingSerializer,
    CarSerializer,
    ReviewSerializer,
)
import stripe


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def search(self, request, *args, **kwargs):
        pickup = request.data["pickup_datetime"]
        dropoff = request.data["dropoff_datetime"]
        pickup_datetime = datetime.strptime(pickup, "%Y-%m-%dT%H:%M")
        dropoff_datetime = datetime.strptime(dropoff, "%Y-%m-%dT%H:%M")
        cars = self.get_queryset()
        available_cars = [
            car
            for car in cars
            if car.check_availability(pickup_datetime, dropoff_datetime)
        ]
        serialized = CarSerializer(
            available_cars, many=True, context={"request": request}
        )

        return Response(serialized.data)


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def book(self, request):
        stripe.api_key = settings.STRIPE_KEY
        pickup = request.data["pickup_datetime"]
        dropoff = request.data["dropoff_datetime"]
        pickup_datetime = datetime.strptime(pickup, "%Y-%m-%dT%H:%M")
        dropoff_datetime = datetime.strptime(dropoff, "%Y-%m-%dT%H:%M")
        chargeType = request.data["chargeType"]
        selected_car_id = request.data["selectedCar"]
        booking_amount = request.data["booking_amount"]
        tota_cost: request.data["tota_cost"]
        email: request.data["email"]
        payment_method_id: request.data["payment_method_id"]

        customer = stripe.Customer.create(email=email, payment_method=payment_method_id)

        stripe.PaymentIntent.create(
            customer=customer,
            payment_method=payment_method_id,
            currency="usd",
            amount=tota_cost * 100,
            confirm=True,
        )
        return Response({})


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
