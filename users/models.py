from uuid import uuid4
from django.db import models
from django.core.validators import RegexValidator
from django.conf import settings
from django.contrib import admin
class Address(models.Model):
    phone_number = models.CharField(
        max_length=255,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+251999999'. Up to 13 digits allowed."
            ),])
    city = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.phone_number

class Owner(models.Model):
    INDIVIDUAL = 'Individual'
    COMPANY = 'Company'
    OWNER_TYPE_CHOICES = [
        (INDIVIDUAL, 'Individual'),
        (COMPANY, 'Company'),
    ]
    id = models.UUIDField(default=uuid4, primary_key=True)
    owner_type = models.CharField(max_length=10, choices= OWNER_TYPE_CHOICES)
    contact = models.OneToOneField(Address, on_delete=models.CASCADE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete= models.CASCADE)
    
    class Meta:
        abstract = True
        
    def __str__(self) -> str:
        if self.owner_type == self.INDIVIDUAL:
            return f'{self.user.first_name} {self.user.last_name}'
        elif self.owner_type == self.COMPANY:
            return self.company_name
        
    def save(self,  *args, **kwargs):
        if not self.owner_type:
            raise ValueError("Owner type must be set")
        super().save(*args, **kwargs)

class IndividualOwner(Owner):    
    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    @admin.display(ordering='user__middle_name')
    def middle_name(self):
        return self.user.middle_name
    
    def save(self,  *args, **kwargs):
        if not self.user.first_name :
            raise ValueError("First name must be set")
        
        if not self.user.last_name :
            raise ValueError("Last name must be set")
        super().save(*args, **kwargs)

class CompanyOwner(Owner):
    company_name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.company_name
