from .models import Vehicel
from rest_framework import serializers
from django.contrib.auth import get_user_model
User = get_user_model()


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email',
                  'first_name', 'middle_name', 'last_name']


class VehicleSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer()

    class Meta:
        model = Vehicel
        fields = ['id', 'chassis_number', 'plate_number', 'owner', 'unique_id']


class AddVehicleSerlizer(serializers.Serializer):
    chassis_number = serializers.CharField(max_length=32)
    plate_number = serializers.CharField(max_length=32)
    insurance_company_name = serializers.CharField(max_length=32)
