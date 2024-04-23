from .models import Notification
from documents.serializers import DocumentSerializer
from rest_framework import serializers


class NotificationSerlizer(serializers.ModelSerializer):
    document = DocumentSerializer()

    class Meta:
        model = Notification
        fields = ['id', 'message_content', 'notification_type',
                  'priority_level', 'seen', 'document']
