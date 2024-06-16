from uuid import uuid4
from django.db import models
from django.conf import settings
from core.utils.custome_primary_key_generate import CustomPrimaryKeyField
from core.utils.gen_unique_id import unique_string_from_two_strings
Key = CustomPrimaryKeyField()


class Vehicel(models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True)
    chassis_number = models.CharField(max_length=32, unique=True)
    plate_number = models.CharField(max_length=32, unique=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    unique_id = models.CharField(
        max_length=8, unique=True, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.id)

    def save(self, *args, **kwargs):

        if not self.unique_id:
            self.unique_id = unique_string_from_two_strings(
                self.chassis_number, self.plate_number)

        super().save(*args, **kwargs)
