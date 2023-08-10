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
        car = Car.objects.get(id=car_id)
        pickup = request.data["pickup_datetime"]
        dropoff = request.data["dropoff_datetime"]
        user = User.objects.get(email=user_email)
        pickup_datetime = datetime.strptime(pickup, "%Y-%m-%dT%H:%M")
        dropoff_datetime = datetime.strptime(dropoff, "%Y-%m-%dT%H:%M")

        if car.check_availability(pickup_datetime, dropoff_datetime):
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
            instance = serializer.save()
            booking = BookingSerializer(instance, context={"request": request})
            return Response(booking.data, status=status.HTTP_201_CREATED)
        return Response(
            {
                "message": "Selected car is not availble for given date and times",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    def update(self, request, *args, **kwargs):
        partial = request.method == "PATCH"
        instance = self.get_object()
        serializer = BookingCreateSerializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        serialized = BookingSerializer(booking, context={"request": request})

        return Response(serialized.data)

    @action(detail=False, methods=["post"])
    def payment(self, request):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        booking_id = request.data["booking_id"]
        booking = Booking.objects.get(id=booking_id)
        if booking.booking_status == "idle":
            try:
                intent = stripe.PaymentIntent.create(
                    amount=int(booking.total_cost * 100),
                    currency="usd",
                )
                return Response({"client_secret": intent.client_secret})
            except Exception as e:
                return Response({"error": str(e)})
        elif booking.booking_status == "completed":
            return Response({"error": "You have already paid for the booking"})
        elif booking.booking_status == "canceled":
            return Response({"error": "This booking is canceled"})
        else:
            return Response({"error": "This booking is not active"})

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
        return Response({"message": "Payment was successfully"})


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    @action(detail=False, methods=["post"])
    def get_reviews(self, request):
        user = request.user
        booking_id = request.data["bookingId"]
        try:
            booking = Booking.objects.get(id=booking_id)
            self_review = self.queryset.filter(user=user, car=booking.car).first()
            others_review = self.queryset.filter(car=booking.car).exclude(user=user)

            self_serialized = (
                self.serializer_class(self_review) if self_review else None
            )

            others_serialized = self.serializer_class(others_review, many=True)
            car_serializer = CarSerializer(booking.car)
            return Response(
                {
                    "self_review": self_serialized.data if self_serialized else None,
                    "data": others_serialized.data,
                    "car": car_serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Booking.DoesNotExist:
            return Response(
                {
                    "message": "Invalid Booking ID",
                },
                status=status.HTTP_404_NOT_FOUND,  # 01b3cb
            )

    def create(self, request):
        user = request.user
        booking_id = request.data["booking_id"]
        booking = Booking.objects.get(id=booking_id)
        car = booking.car

        if booking.user != user:
            return Response(
                {
                    "message": "You can't rate other's booking",
                },
                status=status.HTTP_400_BAD_REQUEST,  # 01b3cb
            )
        already_reviewed = Review.objects.filter(car=car, user=user)
        if already_reviewed.exists():
            return Response(
                {
                    "message": "You have already rated this car",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        review = Review.objects.create(
            user=user,
            car=booking.car,
            rating=request.data["rating"],
            comment=request.data["comment"],
        )
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
