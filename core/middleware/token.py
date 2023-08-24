from django.conf import settings
import jwt


class TokenExpiryCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        token = request.META.get("HTTP_AUTHORIZATION", None)
        if token:
            token = token.replace("Bearer ", "")
            try:
                jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            except (jwt.ExpiredSignatureError, jwt.DecodeError, jwt.InvalidTokenError):
                response.data = {
                    "detail": "Token expired or invalid, Please re-authenticate!"
                }
                response.status_code = 401

        return response
