from django.contrib import admin
from .models import Vehicel
from django.contrib.admin import ModelAdmin

@admin.register(Vehicel)
class Vehicle(ModelAdmin):
    list_select_related = ['owner']
    search_fields = ['id','owner']
    
    
    
