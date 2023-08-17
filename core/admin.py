from django.contrib import admin
from core.models import Car, Booking, Review, Payment
from django.contrib.auth.models import Group


class BookingAdmin(admin.ModelAdmin):
    list_display = ("created_at", "booking_number")


admin.site.register([Car, Review, Payment])
admin.site.register(Booking, BookingAdmin)
admin.site.unregister(Group)
