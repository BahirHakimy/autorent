from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


class CustomUser(AbstractUser):
    email = models.EmailField(blank=False, null=False, unique=True)
    phone_number = models.CharField(max_length=12, blank=True)

    class Meta:
        swappable = "AUTH_USER_MODEL"

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def send_email(self, booking):
        subject = "Booking Confirmed"
        from_email = "AutoRent Rentals"
        recipient_list = [self.email]

        text_message = f"This email confirms that your booking with #{booking.booking_number} number was created successfully."
        time = datetime.now().strftime("%b, %e %Y - %I:%M:%S")
        html_message = render_to_string(
            "email/Booking_Confirm.html", {"booking": booking, "time": time}
        )

        # Create the EmailMultiAlternatives object
        email = EmailMultiAlternatives(
            subject, text_message, from_email, recipient_list
        )
        email.attach_alternative(html_message, "text/html")

        email.send()

    def __str__(self) -> str:
        return self.username
