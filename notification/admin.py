from django.contrib import admin

from .models import Notification

# Register your models here.


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['message_content', 'notification_type',
                    'priority_level', 'seen', 'created_at']
    list_filter = ['created_at']
    list_per_page = 10
    ordering = ['created_at']
