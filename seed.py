import random
from datetime import timedelta
from django.utils import timezone
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autorent.settings")
import django

django.setup()
from faker import Faker
from faker_vehicle import VehicleProvider
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from core.models import Car, Booking, Review, Payment


fake = Faker()

fake.add_provider(VehicleProvider)

images = [
    "cars/Audi-x43.png",
    "cars/bmw-gran-coup.png",
    "cars/bmw-i7.png",
    "cars/bmw-x4.png",
    "cars/bmw-x6.png",
    "cars/bmw-xli-sport.png",
    "cars/bmw-z4.png",
    "cars/Huandai-minivan.png",
    "cars/Huandai.png",
    "cars/kia_yFhoJv5.png",
    "cars/nissan-gtr_V2chwd7.png",
    "cars/nissan-rogue-sport .png",
    "cars/nissan-rogue-sport_.png",
    "cars/saleva-sedan.png",
    "cars/vehicle.png",
]


# Create users
def create_users(num_users=10):
    for _ in range(num_users):
        email = fake.email()
        password = make_password("123123")
        phone_number = fake.phone_number()
        get_user_model().objects.create_user(
            email=email, password=password, phone_number=phone_number
        )


# Create cars
def create_cars(num_cars=10):
    car_types = ["sedan", "suv", "minivan", "sport"]
    for _ in range(num_cars):
        car_type = random.choice(car_types)
        image = random.choice(images)  # Replace with the actual image path
        model = fake.vehicle_year_make_model()
        price_per_hour = random.uniform(20, 100)
        price_per_km = random.uniform(0.1, 1)
        number_of_seats = random.randint(2, 7)
        Car.objects.create(
            car_type=car_type,
            image=image,
            model=model,
            price_per_hour=price_per_hour,
            price_per_km=price_per_km,
            number_of_seats=number_of_seats,
        )


# Create bookings and related objects
def create_bookings(start_date, num_bookings=20):
    users = get_user_model().objects.filter(is_staff=False)
    cars = Car.objects.all()
    booking_statuses = ["idle", "upcomming", "active", "completed", "canceled"]
    booking_options = "days"
    start_from = start_date

    for _ in range(num_bookings):
        user = random.choice(users)
        car = random.choice(cars)
        pick_up_location = fake.address()
        drop_off_location = fake.address()
        booked_from = fake.date_time_between(
            start_date="-30d", end_date="+30d", tzinfo=timezone.utc
        )
        booked_until = booked_from + timedelta(days=random.randint(1, 7))
        booking_type = random.choice(booking_options)
        booking_amount = (booked_until - booked_from).days
        total_cost = booking_amount * (car.price_per_hour * 24)
        booking_status = random.choice(booking_statuses)
        Booking.objects.create(
            user=user,
            car=car,
            pick_up_location=pick_up_location,
            drop_off_location=drop_off_location,
            booked_from=booked_from,
            booked_until=booked_until,
            booking_type=booking_type,
            booking_amount=(booked_until - booked_from).days,
            total_cost=total_cost,
            booking_status=booking_status,
            created_at=start_from,
        )
        start_from = start_from + timedelta(days=4)


# Create reviews
def create_reviews(num_reviews=30):
    bookings = Booking.objects.filter(booking_status="completed")

    for booking in bookings:
        user = booking.user
        car = booking.car
        rating = random.randint(1, 5)
        comment = fake.paragraph()
        Review.objects.create(user=user, car=car, rating=rating, comment=comment)


# Create payments
def create_payments(num_payments=40):
    bookings = Booking.objects.filter(booking_status="completed")

    for booking in bookings:
        payment_id = fake.uuid4()
        amount = booking.total_cost
        Payment.objects.create(booking=booking, payment_id=payment_id, amount=amount)


# Seed the database
def seed_database():
    create_users()
    create_bookings()
    create_payments()
    create_reviews()


if __name__ == "__main__":
    seed_database()
    print("Database seeding completed.")
