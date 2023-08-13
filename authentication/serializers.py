from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.ReadOnlyField(source="get_full_name")

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "is_staff",
            "date_joined",
            "fullname",
            "email",
            "phone_number",
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "password", "first_name", "last_name", "phone_number"]
