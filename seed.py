import random
import pytz
from datetime import datetime, timedelta
from faker import Faker
from django.conf import settings
from django.contrib.auth.hashers import make_password
from authentication.models import CustomUser
from core.models import Car, Booking, Review, Payment


fake = Faker()


# Create users
def create_users(num_users=10):
    for _ in range(num_users):
        email = fake.email()
        password = make_password("123123")
        phone_number = fake.phone_number()
        CustomUser.objects.create_user(
            email=email, password=password, phone_number=phone_number
        )


# Create cars
def create_cars(num_cars=10):
    car_types = ["sedan", "suv", "minivan", "sport"]
    for _ in range(num_cars):
        car_type = random.choice(car_types)
        image = "cars/car_image.jpg"  # Replace with the actual image path
        model = fake.word()
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
def create_bookings(num_bookings=20):
    users = CustomUser.objects.all()
    cars = Car.objects.all()
    booking_statuses = ["idle", "upcomming", "active", "completed", "canceled"]
    booking_options = ["days", "distance"]

    for _ in range(num_bookings):
        user = random.choice(users)
        car = random.choice(cars)
        pick_up_location = fake.address()
        drop_off_location = fake.address()
        booked_from = fake.date_time_between(start_date="-30d", end_date="+30d")
        booked_until = booked_from + timedelta(hours=random.randint(1, 72))
        booking_type = random.choice(booking_options)
        booking_amount = random.uniform(50, 500)
        total_cost = random.uniform(booking_amount, 1000)
        booking_status = random.choice(booking_statuses)
        Booking.objects.create(
            user=user,
            car=car,
            pick_up_location=pick_up_location,
            drop_off_location=drop_off_location,
            booked_from=booked_from,
            booked_until=booked_until,
            booking_type=booking_type,
            booking_amount=booking_amount,
            total_cost=total_cost,
            booking_status=booking_status,
        )


# Create reviews
def create_reviews(num_reviews=30):
    users = CustomUser.objects.all()
    cars = Car.objects.all()

    for _ in range(num_reviews):
        user = random.choice(users)
        car = random.choice(cars)
        rating = random.randint(1, 5)
        comment = fake.paragraph()
        Review.objects.create(user=user, car=car, rating=rating, comment=comment)


# Create payments
def create_payments(num_payments=40):
    bookings = Booking.objects.filter(booking_status="completed")

    for _ in range(num_payments):
        booking = random.choice(bookings)
        payment_id = fake.uuid4()
        amount = booking.total_cost
        Payment.objects.create(booking=booking, payment_id=payment_id, amount=amount)


# Seed the database
def seed_database():
    create_users()
    create_cars()
    create_bookings()
    create_reviews()
    create_payments()


if __name__ == "__main__":
    seed_database()
    print("Database seeding completed.")
