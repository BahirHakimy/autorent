from django.conf import settings
from django.contrib.auth import get_user_model
import jwt
from datetime import datetime, timedelta


def create_token(user):
    payload = {
        "user_id": user.pk,
        "is_admin": user.is_staff,
        "email": user.email,
        "exp": datetime.utcnow()
        + timedelta(seconds=settings.JWT_EXPIRATION_TIME_SECONDS),
    }

    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def decode_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user_id = payload["user_id"]
        return get_user_model().objects.get(pk=user_id)
    except (
        jwt.ExpiredSignatureError,
        jwt.DecodeError,
        jwt.InvalidTokenError,
        get_user_model().DoesNotExist,
    ):
        return None
