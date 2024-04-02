from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserValidator:
    def validate_user(self, value):
        User = get_user_model()

        try:
            user_instance = User.objects.get(pk=value)
            return user_instance
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")
