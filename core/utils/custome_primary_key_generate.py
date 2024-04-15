import random
import string

from django.db import models
import secrets


class CustomPrimaryKeyField(models.Field):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 16
        kwargs['primary_key'] = True
        super().__init__(*args, **kwargs)

    def get_prep_value(self, value):
        if not value:
            value = self.generate_key()
        return super().get_prep_value(value)

    def generate_key(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
