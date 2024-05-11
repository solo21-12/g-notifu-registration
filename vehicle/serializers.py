from .models import Vehicel
from rest_framework import serializers


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicel
        fields = '__all__'


class AddVehicleSerlizer(serializers.Serializer):
    chassis_number = serializers.CharField(max_length=32)
