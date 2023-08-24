from .settings_base import *

# Security
SECRET_KEY = config("SECRET_KEY")
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY")
JWT_EXPIRATION_TIME_SECONDS = int(config("JWT_EXPIRATION_TIME_SECONDS"))
ALLOWED_HOSTS = [config("ALLOWED_HOST"), "autorent-rentals.onrender.com"]
CORS_ALLOWED_ORIGINS = [config("FRONTEND_URL")]

DEBUG = True

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}
