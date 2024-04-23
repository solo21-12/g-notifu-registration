from django.contrib import admin
from .models import Address, CompanyOwner, IndividualOwner, Owner
from django.contrib.admin import ModelAdmin

# Register your models here.


@admin.register(Address)
class Address(ModelAdmin):
    pass


@admin.register(CompanyOwner)
class CompanyOwners(ModelAdmin):
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['company_name']
    list_display = ['company_name', 'owner_type',
                    'contact']
    search_fields = ['company_name', 'contact']


@admin.register(IndividualOwner)
class IndividualOwners(ModelAdmin):
    list_per_page = 10
    list_select_related = ['user']
    list_display = ['first_name', 'middle_name', 'last_name',
                    'owner_type', 'contact']
    search_fields = ['user__first_name__istartswith',
                     'user__last_name__istartswith']
