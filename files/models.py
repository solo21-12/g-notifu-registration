from django.db import models
from core.utils import custome_primary_key_generate

Key = custome_primary_key_generate.CustomPrimaryKeyField()


class Files(models.Model):
    id = models.CharField(
        primary_key=True, default=Key.generate_key(), max_length=16)
    file_name = models.CharField(max_length=255)
    file_address = models.CharField(max_length=255)
    file_type = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self) -> str:
        return self.file_name
