from django.db import models
from core.utils.custome_primary_key_generate import CustomPrimaryKeyField
from documents.models import Document

key = CustomPrimaryKeyField()


class Notification(models.Model):
    ALERT = 'alert'
    UPDATE = 'update'
    REMINDER = 'reminder'
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    SEEN = 'SEEN'
    DELIVERED = ' delivered'
    PENDING = 'pending'

    Notification_type_choices = [
        (ALERT, 'Alert'),
        (UPDATE, 'Update'),
        (REMINDER, 'Reminder')
    ]

    PRIORITY_LEVEL_CHOICE = [
        (LOW, 'Low'),
        (MEDIUM, 'Medium'),
        (HIGH, 'High')
    ]

    message_content = models.TextField(blank=True)
    notification_type = models.CharField(
        max_length=20, choices=Notification_type_choices, null=True)
    priority_level = models.CharField(
        max_length=10, choices=PRIORITY_LEVEL_CHOICE, default=LOW)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
