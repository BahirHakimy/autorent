from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import random


class CustomUser(AbstractUser):
    email = models.EmailField(blank=False, null=False, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)

    class Meta:
        swappable = "AUTH_USER_MODEL"

    def send_email(self):
        subject = "Hello from Django!"
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [self.email]

        # Plain Text Version
        text_message = "This is a test email sent using Django. (Plain Text)"

        # HTML Version
        html_message = render_to_string(
            "email/booking_confirmation.html", {"variable": "value"}
        )

        # Create the EmailMultiAlternatives object
        email = EmailMultiAlternatives(
            subject, text_message, from_email, recipient_list
        )
        email.attach_alternative(html_message, "text/html")

        email.send()


class Car(models.Model):
    CAR_TYPES = (
        ("sedan", "Sedan"),
        ("SUV", "SUV"),
        ("minivan", "MiniVan"),
        ("sport", "Sport"),
    )

    car_type = models.CharField(choices=CAR_TYPES, max_length=10)
    image = models.ImageField(upload_to="cars/", blank=True)
    model = models.CharField(max_length=100)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2)
    number_of_seats = models.IntegerField()

    def check_availability(self, from_date, to_date):
        is_available = True
        for booking in self.booking_set.filter(booking_status="active"):
            if from_date < booking.booked_from and to_date > booking.booked_from:
                is_available = False
            elif from_date < booking.booked_until:
                is_available = False
        return is_available

    def __str__(self):
        return f"{self.model} - {self.car_type}"


class Booking(models.Model):
    BOOKING_OPTIONS = (("days", "By Days"), ("distance", "By Distance"))
    BOOKING_STATUS = (
        ("active", "Active"),
        ("completed", "Completed"),
        ("canceled", "Canceled"),
    )
    booking_number = models.CharField(
        max_length=8, default=random.randint(10000000, 99999999)
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    pick_up_location = models.CharField(max_length=200)
    drop_off_location = models.CharField(max_length=200)
    booked_from = models.DateTimeField()
    booked_until = models.DateTimeField()
    booking_type = models.CharField(max_length=10, choices=BOOKING_OPTIONS)
    booking_amount = models.DecimalField(max_digits=10, decimal_places=5)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    booking_status = models.CharField(
        max_length=10, choices=BOOKING_STATUS, default="active"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.car.model} - {self.booked_from}"


class Review(models.Model):
    RATING_CHOICES = (
        (1, "1"),
        (2, "2"),
        (3, "3"),
        (4, "4"),
        (5, "5"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.car.model} - {self.rating}"


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.booking
