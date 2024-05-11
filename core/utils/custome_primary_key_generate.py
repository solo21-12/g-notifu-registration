import random
import string
import uuid

from django.db import models
import secrets


class CustomPrimaryKeyField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('primary_key', True)
        kwargs.setdefault('editable', False)
        kwargs.setdefault('unique', True)
        kwargs.setdefault('default', self.generate_key)
        super().__init__(*args, **kwargs)

    @staticmethod
    def generate_key():
        return str(uuid.uuid4().hex)[:16]
