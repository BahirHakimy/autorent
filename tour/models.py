from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import random


class TourImage(models.Model):
    tour_id = models.ForeignKey("Tour",related_name="image_ids", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="tour_images")


class Highlights(models.Model):
    title = models.CharField(max_length=55)


class Tour(models.Model):

    AVAILABILITY_CHOICES = (
        ("all_year", "All Year"),
        ("half_year", "Half Year"),
    )

    CATEGORY_CHOICES = (
        ("airport_transfer", "Airport Transfer"),
        ("private_transfer", "Private Transfer"),
        ("normal_trip", "Normal Trip"),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    highlights = models.ManyToManyField("Highlights")
    availability = models.CharField(choices=AVAILABILITY_CHOICES, max_length=55)
    category = models.CharField(choices=AVAILABILITY_CHOICES, max_length=55)
    sub_category = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to="tour_covers")
    duration = models.DecimalField(max_digits=10, decimal_places=2)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    price_from = models.DecimalField(max_digits=10, decimal_places=2)
    pickup = models.BooleanField()
    featured = models.BooleanField()
    pickup_information = models.TextField()
    additional_notes = models.TextField()

    def check_availability(self, from_date, to_date):
        from_date = timezone.make_aware(from_date, timezone.get_default_timezone())
        to_date = timezone.make_aware(to_date, timezone.get_default_timezone())
        bookings = self.booking_set.filter(
            booking_status__in=["idle", "upcomming", "active"]
        )

        if not bookings.exists():
            return True

        for booking in bookings:
            if (
                (from_date >= booking.booked_from and from_date < booking.booked_until)
                or (to_date > booking.booked_from and to_date <= booking.booked_until)
                or (
                    from_date <= booking.booked_from and to_date >= booking.booked_until
                )
            ):
                return False
        return True

    def get_average_rating(self):
        reviews = self.review_set.all()
        total = 0
        for review in reviews:
            total += review.rating

        if reviews.count() > 0:
            return {"average": f"{total / reviews.count():.1f}", "count": len(reviews)}
        else:
            return None

    def __str__(self):
        return f"{self.model} - {self.car_type}"
