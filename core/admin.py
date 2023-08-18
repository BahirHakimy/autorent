from django.contrib import admin
from core.models import Car, Booking, Review, Payment
from django.contrib.auth.models import Group

admin.site.site_header = "Administration"
admin.site.site_title = "AutoRent"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "created_at",
        "user",
        "car",
        "booking_status",
    )
    list_filter = ("booking_status", "booking_type")
    search_fields = ("booking_number", "user__email", "car__model")


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        "model",
        "car_type",
        "number_of_seats",
        "price_per_hour",
        "price_per_km",
    )
    list_filter = ("car_type",)
    search_fields = ("model",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "car",
        "rating",
        "created_at",
    )

    list_filter = ("rating",)
    search_fields = ("car_model", "user__email")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "booking",
        "amount",
        "created_at",
    )
    search_fields = ("payment_id", "booking__booking_number")


admin.site.unregister(Group)
