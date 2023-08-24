import random
from datetime import timedelta
from django.utils import timezone
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autorent.settings_prod")
import django

django.setup()
from faker import Faker
from faker_vehicle import VehicleProvider
from django.contrib.auth import get_user_model
from core.models import Car, Booking, Review, Payment


fake = Faker()

fake.add_provider(VehicleProvider)

images = [
    "https://raw.githubusercontent.com/BahirHakimy/file_storage_for_autorent/main//Audi-x43.png",
    "https://raw.githubusercontent.com/BahirHakimy/file_storage_for_autorent/main//bmw-gran-coup.png",
    "https://raw.githubusercontent.com/BahirHakimy/file_storage_for_autorent/main//bmw-i7.png",
    "https://raw.githubusercontent.com/BahirHakimy/file_storage_for_autorent/main//bmw-x4.png",
    "https://raw.githubusercontent.com/BahirHakimy/file_storage_for_autorent/main//bmw-x6.png",
    "https://raw.githubusercontent.com/BahirHakimy/file_storage_for_autorent/main//bmw-xli-sport.png",
    "https://raw.githubusercontent.com/BahirHakimy/file_storage_for_autorent/main//bmw-z4.png",
    "https://raw.githubusercontent.com/BahirHakimy/file_storage_for_autorent/main//Huandai-minivan.png",
    "https://raw.githubusercontent.com/BahirHakimy/file_storage_for_autorent/main//Huandai.png",
    "https://raw.githubusercontent.com/BahirHakimy/file_storage_for_autorent/main//nissan-rogue-sport .png",
    "https://raw.githubusercontent.com/BahirHakimy/file_storage_for_autorent/main//nissan-rogue-sport_.png",
    "https://raw.githubusercontent.com/BahirHakimy/file_storage_for_autorent/main//saleva-sedan.png",
    "https://raw.githubusercontent.com/BahirHakimy/file_storage_for_autorent/main//vehicle.png",
]


# Create users
def create_users(num_users=10):
    print("***** Creating Users *****")
    for _ in range(num_users):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone_number = f"+937{random.randint(10000000,99999999)}"
        password = "123123"
        print(f"    User [{email}]")
        get_user_model().objects.create_user(
            email=email,
            password=password,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
        )
    print("***** Users Seeding Complete *****")


# Create cars
def create_cars(num_cars=10):
    print("***** Creating Users *****")
    car_types = ["sedan", "suv", "minivan", "sport"]
    for _ in range(num_cars):
        car_type = random.choice(car_types)
        image = random.choice(images)
        model = fake.vehicle_year_make_model()
        price_per_hour = random.uniform(20, 100)
        price_per_km = random.uniform(0.1, 1)
        number_of_seats = random.randint(2, 7)
        print(f"    Car [{model}]")
        Car.objects.create(
            car_type=car_type,
            image=image,
            model=model,
            price_per_hour=price_per_hour,
            price_per_km=price_per_km,
            number_of_seats=number_of_seats,
        )
    print("***** Cars Seeding Complete *****")


# Create bookings and related objects
def create_bookings(start_date, num_bookings=20):
    print("***** Creating Bookings *****")
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
            start_date="-180d", end_date="+30d", tzinfo=timezone.utc
        )
        booked_until = booked_from + timedelta(days=random.randint(1, 7))
        booking_type = booking_options
        booking_amount = (booked_until - booked_from).days
        total_cost = booking_amount * (car.price_per_hour * 24)
        booking_status = random.choice(booking_statuses)
        booking = Booking.objects.create(
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
        )
        booking.created_at = start_from
        booking.save()
        print(f"    Booking [{booking.booking_number}]")
        start_from = start_from + timedelta(days=4)
    print("***** Bookings Seeding Complete *****")


# Create reviews
def create_reviews():
    print("***** Creating Reviews *****")

    bookings = Booking.objects.filter(booking_status="completed")

    for booking in bookings:
        user = booking.user
        car = booking.car
        rating = random.randint(1, 5)
        comment = fake.paragraph()
        print(f"    Review [{comment}]")
        Review.objects.create(user=user, car=car, rating=rating, comment=comment)
    print("***** Reviews Seeding Complete *****")


# Create payments
def create_payments():
    print("***** Creating Payments *****")

    bookings = Booking.objects.filter(booking_status="completed")

    for booking in bookings:
        payment_id = fake.uuid4()
        amount = booking.total_cost
        print(f"    Review [{amount}]")
        payment = Payment.objects.create(
            booking=booking, payment_id=payment_id, amount=amount
        )
        payment.created_at = booking.created_at
        payment.save()
    print("***** Payments Seeding Complete *****")


# Seed the database
def seed_database():
    start_time = timezone.now() - timedelta(days=200)
    create_users(5)
    # create_cars(25)
    # create_bookings(start_date=start_time, num_bookings=50)
    # create_payments()
    # create_reviews()


if __name__ == "__main__":
    print("=================== Database seeding started ===================")
    seed_database()
    print("=================== Database seeding completed ===================")
