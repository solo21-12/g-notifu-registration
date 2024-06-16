from rest_framework import serializers
from documents.models import Document

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['document_type', 'renewal_status', 'expiry_date']
