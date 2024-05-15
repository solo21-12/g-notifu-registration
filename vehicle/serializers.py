from .models import Vehicel
from rest_framework import serializers
from documents.models import Document


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicel
        fields = ['id', 'chassis_number', 'plate_number', 'owner']


class AddVehicleSerlizer(serializers.Serializer):
    chassis_number = serializers.CharField(max_length=32)
    plate_number = serializers.CharField(max_length=32)
    insurance_company_name = serializers.CharField(max_length=32)
