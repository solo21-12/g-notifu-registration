from uuid import uuid4
from django.db import models
from django.conf import settings
from core.utils.custome_primary_key_generate import CustomPrimaryKeyField

Key = CustomPrimaryKeyField()


class Vehicel(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    chassis_number = models.CharField(max_length=32, unique=True)
    plate_number = models.CharField(max_length=32, unique=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.id)

