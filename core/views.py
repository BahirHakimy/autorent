from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import status
from .models import Car, Booking, Review, Payment
from django.shortcuts import render
from .serializers import (
    BookingSerializer,
    BookingCreateSerializer,
    CarSerializer,
    ReviewSerializer,
    PaymentSerializer,
)
import stripe

class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAdminUser]

    def list(self, request, *args, **kwargs):
        page_number = request.query_params.get("page", 1)
        paginated = Paginator(self.queryset, 20)
        paged_data = paginated.page(page_number)
        has_next = paged_data.has_next()

        serializer = CarSerializer(
            paged_data,
            many=True,
            context={"request": request},
        )
        return Response({"results": serializer.data, "has_next": has_next})

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def search(self, request, *args, **kwargs):
        pickup = request.data.get("pickup_datetime")
        dropoff = request.data.get("dropoff_datetime")
        filter_type = request.data.get("car_type")
        if pickup and dropoff:
            pickup_datetime = datetime.strptime(pickup, "%Y-%m-%dT%H:%M")
            dropoff_datetime = datetime.strptime(dropoff, "%Y-%m-%dT%H:%M")
            cars = self.get_queryset()
            if filter_type:
                cars = cars.filter(car_type=filter_type)
            available_cars = [
                car
                for car in cars
                if car.check_availability(pickup_datetime, dropoff_datetime)
            ]

            serializer = CarSerializer(
                available_cars,
                many=True,
                context={"request": request},
            )

            return Response(serializer.data)
        else:
            return Response(
                {"detail": "pickup_datetime and dropoff_datetime are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_permissions(self):
        if self.action in ["destroy", "get_report"]:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        for booking in self.queryset:
            booking.update_status()

        if request.user.is_staff:
            queryset = self.queryset.order_by("-created_at")
        else:
            queryset = self.queryset.filter(user=request.user)

        page_number = request.query_params.get("page", 1)
        paginated = Paginator(queryset, 20)
        paged_data = paginated.page(page_number)
        has_next = paged_data.has_next()

        serializer = self.get_serializer(paged_data, many=True)
        return Response({"results": serializer.data, "has_next": has_next})

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
        status = request.data.get("booking_status", None)
        instance = self.get_object()
        if not (request.user.is_staff or (instance.user == request.user)):
            return Response(
                {"message": "You are not allowed to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )
        send_email = False
        if status == "canceled" and instance.booking_status in ["active", "upcomming"]:
            send_email = True

        serializer = BookingCreateSerializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        booking = serializer.save()
        booking.user.send_email(booking)
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

    @action(detail=False, methods=["get"])
    def get_report(self, request):
        now = timezone.now()
        thisMonth = now - timedelta(days=now.day)
        payments = Payment.objects.filter(created_at__gte=thisMonth).aggregate(
            Sum("amount")
        )
        bookings_this_month = self.queryset.filter(created_at__gte=thisMonth).count()
        total_customers = get_user_model().objects.filter(is_staff=False).count()
        total_cars = Car.objects.count()
        bookings_per_month = {}
        bookings_per_car_type = {}
        bookings_states = {}
        bookings = self.queryset.order_by("created_at")
        reviews = Review.objects.all()
        ratings_per_car_type = {}
        for car_type, _ in Car.CAR_TYPES:
            ratings_per_car_type[car_type.capitalize()] = {
                "1": 0,
                "2": 0,
                "3": 0,
                "4": 0,
                "5": 0,
            }

        for review in reviews:
            rating = review.rating

            if ratings_per_car_type[review.car.car_type.capitalize()].get(
                rating.__str__(), None
            ):
                ratings_per_car_type[review.car.car_type.capitalize()][
                    rating.__str__()
                ] = (
                    ratings_per_car_type[review.car.car_type.capitalize()][
                        rating.__str__()
                    ]
                    + 1
                )
            else:
                ratings_per_car_type[review.car.car_type.capitalize()][
                    rating.__str__()
                ] = 1

        for booking in bookings:
            month = booking.created_at.strftime("%h")
            booking_status = booking.booking_status.capitalize()
            car_type = booking.car.car_type.capitalize()

            if bookings_per_car_type.get(car_type, None):
                bookings_per_car_type[car_type] = bookings_per_car_type[car_type] + 1
            else:
                bookings_per_car_type[car_type] = 1

            if bookings_states.get(booking_status, None):
                bookings_states[booking_status] = bookings_states[booking_status] + 1
            else:
                bookings_states[booking_status] = 1

            if bookings_per_month.get(month, None):
                bookings_per_month[month] = bookings_per_month[month] + 1
            else:
                bookings_per_month[month] = 1

        return Response(
            {
                "total_payments": payments["amount__sum"],
                "bookings_this_month": bookings_this_month,
                "total_customers": total_customers,
                "total_cars": total_cars,
                "bookings_per_month": bookings_per_month,
                "bookings_per_car_type": bookings_per_car_type,
                "bookings_states": bookings_states,
                "ratings_per_car_type": ratings_per_car_type,
            }
        )


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def list(self, request):
        page_number = request.query_params.get("page", 1)
        paginated = Paginator(self.queryset, 20)
        paged_data = paginated.page(page_number)
        has_next = paged_data.has_next()

        serializer = ReviewSerializer(
            paged_data,
            many=True,
        )

        return Response({"results": serializer.data, "has_next": has_next})

    def get_permissions(self):
        if self.action == "destroy":
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

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
            car_serializer = CarSerializer(booking.car, context={"request": request})
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


class PaymentViewSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action == "create":
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def list(self, request):
        page_number = request.query_params.get("page", 1)
        paginated = Paginator(self.queryset, 20)
        paged_data = paginated.page(page_number)
        has_next = paged_data.has_next()

        serializer = PaymentSerializer(
            paged_data,
            many=True,
        )

        return Response({"results": serializer.data, "has_next": has_next})
