from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.models import UserManager
from django.utils import timezone


class CustomUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = models.CharField(
        blank=True,
        null=True,
        max_length=150,
    )
    email = models.EmailField(blank=False, null=False, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)
    objects = CustomUserManager()

    class Meta:
        swappable = "AUTH_USER_MODEL"
        verbose_name = "user"
        verbose_name_plural = "users"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def send_email(self, booking):
        if booking.booking_status in ["idle", "upcomming"]:
            subject = "Booking Confirmed"
            message = "created successfully."
            template = "email/BookingConfirm.html"
        else:
            subject = "Booking Canceled"
            message = "canceled."
            template = "email/BookingCancel.html"

        from_email = "AutoRent Rentals"
        recipient_list = [self.email]

        text_message = f"This email confirms that your booking with #{booking.booking_number} number was {message}"
        today = timezone.now()
        html_message = render_to_string(template, {"booking": booking, "today": today})

        # Create the EmailMultiAlternatives object
        email = EmailMultiAlternatives(
            subject, text_message, from_email, recipient_list
        )
        email.attach_alternative(html_message, "text/html")
        email.send()

    def __str__(self) -> str:
        return self.email
