from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    BasePermission,
)
from rest_framework import viewsets
from .serializers import UserSerializer, UserCreateSerializer
from .token_factory import create_token


class IsOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        instance = view.get_object()
        return bool(request.user.is_staff or instance == request.user)


class UserViewSet(viewsets.ModelViewSet):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ["retrieve", "update"]:
            permission_classes = [IsOwnerOrAdmin]
        elif self.action == "list":
            permission_classes = [IsAdminUser]
        elif self.action == "create":
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        queryset = self.queryset.exclude(id=request.user.id)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        instance.set_password(serializer.data["password"])
        instance.save()
        token = create_token(instance)
        return Response({"token": token}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = request.method == "PATCH"
        password = request.data.get("password", None)
        instance = self.get_object()
        serializer = UserSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        if not request.user.is_staff and password:
            old_password = request.data.get("old_password", None)
            if not old_password:
                return Response(
                    {"old_password": "old_password is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not instance.check_password(old_password):
                return Response(
                    {"old_password": "Invalid password."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        user = serializer.save()
        if password:
            user.set_password(password)
            user.save()

        return Response(serializer.data)

    @action(detail=False)
    def check_admin(self, request):
        return Response({"isAdmin": request.user.is_staff})


class ObtainJWTTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)
        if user is not None:
            token = create_token(user)
            return Response(
                {"token": token, "is_admin": user.is_staff}, status=status.HTTP_200_OK
            )
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )
