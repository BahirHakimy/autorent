from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from .serializers import (
    UserSerializer,
)
from .token_factory import create_token


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ObtainJWTTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            token = create_token(user)
            return Response({"token": token}, status=HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=HTTP_400_BAD_REQUEST)
