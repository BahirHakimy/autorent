from .settings_base import *

# Security
SECRET_KEY = "django-insecure-#0z@kvg1o4epk)4ae#$lano^3nw-emw#%zd4(m#40pbn+f6-6+"
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default="")
JWT_EXPIRATION_TIME_SECONDS = 172800
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_ALL_ORIGINS = True

DEBUG = True

# Database
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
}
