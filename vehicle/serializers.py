from .models import Vehicel
from rest_framework import serializers
from documents.models import Document


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicel
        fields = ['id', 'chassis_number', 'owner']

        # def get_document(self, obj):
        #     return Document.objects.get(id=obj.id)


class AddVehicleSerlizer(serializers.Serializer):
    chassis_number = serializers.CharField(max_length=32)
    insurance_company_name = serializers.CharField(max_length=32)
