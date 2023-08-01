from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    fullname = serializers.ReadOnlyField(source="get_full_name")

    class Meta:
        model = get_user_model()
        fields = ["fullname", "username", "email", "phone_number"]
