from django.db import models
from django.conf import settings
from core.utils.custome_primary_key_generate import CustomPrimaryKeyField

Key = CustomPrimaryKeyField()


class Vehicel(models.Model):
    id = models.CharField(
        primary_key=True, default=Key.generate_key(), max_length=16)
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return str(self.id)
