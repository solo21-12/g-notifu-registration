from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import timedelta
from core.utils.custome_primary_key_generate import CustomPrimaryKeyField
from vehicle.models import Vehicel
from files.models import Files

Key = CustomPrimaryKeyField()
THIRD_PARTY_INSURANCE = 'Third party insurance'
ROAD_FUND = 'Road fund'
ROAD_AUTHORITY = 'Road Authority'
BOLO = 'Bolo'

document_type_choices = [
    (THIRD_PARTY_INSURANCE, 'Third party insurance'),
    (ROAD_FUND, 'Road Fund'),
    (ROAD_AUTHORITY, 'Road Authority'),
    (BOLO, 'Bolo')
]


class Document(models.Model):
    vehicle = models.ForeignKey(Vehicel, on_delete=models.CASCADE)
    document_type = models.CharField(
        choices=document_type_choices, max_length=100)
    renewal_status = models.BooleanField(default=False)
    renewal_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    files = models.ManyToManyField(Files, blank=True)

    def __str__(self) -> str:
        return str(self.id)


@receiver(pre_save, sender=Document)
def update_renewal_date(sender, instance, **kwargs):
    if instance.renewal_date and not instance.expiry_date:
        instance.expiry_date = instance.renewal_date + timedelta(days=365)
