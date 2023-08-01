from rest_framework.authentication import BaseAuthentication
from django.contrib.auth import get_user_model
from .token_factory import decode_token


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.META.get("HTTP_AUTHORIZATION", None)
        if not token:
            return None

        token = token.replace("Bearer ", "")

        user = decode_token(token)
        if user:
            return user, None
        return None
