from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Document


@admin.register(Document)
class Document(ModelAdmin):
    list_display = ['id', 'vehicle', 'document_type',
                    'renewal_status', 'renewal_date', 'expiry_date']
