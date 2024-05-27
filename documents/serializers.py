from .models import Document
from rest_framework import serializers
from vehicle.serializers import VehicleSerializer


class DocumentSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer()

    class Meta:
        model = Document
        fields = ['id', 'document_type', 'renewal_status',
                  'renewal_date', 'expiry_date', 'vehicle']


class DocumentRenewalInitalizer(serializers.Serializer):
    chassis_number = serializers.CharField()
    transaction_code = serializers.CharField()
