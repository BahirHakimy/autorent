from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import random


class Car(models.Model):
    CAR_TYPES = (
        ("sedan", "Sedan"),
        ("suv", "SUV"),
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


class Booking(models.Model):
    BOOKING_OPTIONS = (("days", "By Days"), ("distance", "By Distance"))
    BOOKING_STATUS = (
        ("idle", "Idle"),
        ("upcomming", "Upcomming"),
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
    booking_amount = models.DecimalField(max_digits=10, decimal_places=2)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    booking_status = models.CharField(
        max_length=10, choices=BOOKING_STATUS, default="idle"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.car.model} - {self.booked_from}"

    def update_status(self):
        now = timezone.now()
        if self.booking_status in ["active", "upcomming"]:
            if now >= self.booked_from:
                if now >= self.booked_until:
                    self.booking_status = "completed"
                    self.save()
                elif self.booking_status != "active":
                    self.booking_status = "active"
                    self.save()
        elif self.booking_status == "idle":
            if now >= self.booked_until:
                self.booking_status = "canceled"
                self.save()


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
        return f"{self.id} - {self.car.model} - {self.rating}"


class Payment(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.booking.id} {self.amount}"


@receiver(post_save, sender=Payment)
def send_confirmation_email(sender, instance, created, **kwargs):
    if created:
        user = instance.booking.user
        user.send_email(instance.booking)
