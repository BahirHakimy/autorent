from rest_framework import serializers
from .models import Car, Booking, Payment, Review

from authentication.serializers import UserSerializer


class CarSerializer(serializers.ModelSerializer):
    rating = serializers.ReadOnlyField(source="get_average_rating")
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Car

        fields = [
            "id",
            "car_type",
            "image",
            "model",
            "price_per_hour",
            "price_per_km",
            "number_of_seats",
            "rating",
        ]


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    car = CarSerializer()
    booking_type = serializers.ReadOnlyField(source="get_booking_type_display")
    booking_status = serializers.ReadOnlyField(source="get_booking_status_display")

    class Meta:
        model = Booking
        fields = [
            "id",
            "booking_number",
            "user",
            "car",
            "pick_up_location",
            "drop_off_location",
            "booked_from",
            "booked_until",
            "booking_type",
            "booking_amount",
            "total_cost",
            "booking_status",
            "created_at",
        ]


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "booking_number",
            "user",
            "car",
            "pick_up_location",
            "drop_off_location",
            "booked_from",
            "booked_until",
            "booking_type",
            "booking_amount",
            "total_cost",
            "booking_status",
            "created_at",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    car = CarSerializer(read_only=True)
    rating = serializers.ReadOnlyField(source="get_rating_display")

    class Meta:
        model = Review
        fields = [
            "id",
            "user",
            "car",
            "rating",
            "comment",
            "created_at",
        ]
