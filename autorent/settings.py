import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Security
SECRET_KEY = "django-insecure-#0z@kvg1o4epk)4ae#$lano^3nw-emw#%zd4(m#40pbn+f6-6+"
STRIPE_SECRET_KEY = "sk_test_51NcOaFB1Lcz9jTJ0hBKio5dJVN20M6UscSJEMiYcLtZkGcD3ssH7NlvSohwiMJ5jA1vQENpN8QwTzcO74K1BkFp500uPa71wCB"
JWT_EXPIRATION_TIME_SECONDS = 86400
ALLOWED_HOSTS = []
CORS_ALLOWED_ORIGINS = ["http://127.0.0.1:5173", "http://localhost:5173"]

DEBUG = True

# Email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "bahirhakimy2015@gmail.com"
EMAIL_HOST_PASSWORD = "gdsunesznrfhagpm"

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kabul"
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
FRONTEND_ROOT = os.path.join(BASE_DIR, "public")

ROOT_URLCONF = "autorent.urls"
WSGI_APPLICATION = "autorent.wsgi.application"
AUTH_USER_MODEL = "authentication.CustomUser"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "core.apps.CoreConfig",
    "authentication.apps.AuthenticationConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "core.middleware.token.TokenExpiryCheckMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("authentication.backends.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
}

# Database
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates/"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
