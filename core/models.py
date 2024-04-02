from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    username = models.EmailField(unique=True, primary_key=True)
    verfication_pin = models.IntegerField(null=True, blank=True)
    password_reset_pin = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.email
