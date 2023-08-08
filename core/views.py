from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.generics import GenericAPIView
from .models import Car, Booking, Review, Payment
from .serializers import (
    BookingSerializer,
    BookingCreateSerializer,
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

    def create(self, request):
        User = get_user_model()
        user_email = request.data["email"]
        car_id = request.data["car_id"]
        pickup = request.data["pickup_datetime"]
        dropoff = request.data["dropoff_datetime"]
        user = User.objects.get(email=user_email)
        pickup_datetime = datetime.strptime(pickup, "%Y-%m-%dT%H:%M")
        dropoff_datetime = datetime.strptime(dropoff, "%Y-%m-%dT%H:%M")
        serializer = BookingCreateSerializer(
            data={
                **request.data,
                "booked_from": pickup_datetime,
                "booked_until": dropoff_datetime,
                "user": user.id,
                "car": car_id,
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"])
    def payment(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        booking_id = request.data["booking_id"]
        booking = Booking.objects.get(id=booking_id)
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(booking.total_cost * 100),
                currency="usd",
            )
            return Response({"client_secret": intent.client_secret})
        except Exception as e:
            return Response({"error": str(e)})

    @action(detail=False, methods=["post"])
    def create_payment(self, request):
        booking_id = request.data["booking_id"]
        booking = Booking.objects.get(id=booking_id)
        payment_data = request.data["paymentIntent"]
        payment = Payment.objects.create(
            booking=booking,
            payment_id=payment_data["id"],
            amount=(payment_data["amount"] / 100),
        )
        payment.save()
        booking.booking_status = "active"
        booking.save()
        return Response({"message": "Payment created successfully"})


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
