from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Files


@admin.register(Files)
class Files(ModelAdmin):
    list_display = ['id', 'file_name', 'file_address', 'file_type', 'content']
