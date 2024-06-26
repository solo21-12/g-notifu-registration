from uuid import uuid4
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from datetime import timedelta
from core.utils.custome_primary_key_generate import CustomPrimaryKeyField
from vehicle.models import Vehicel
from files.models import Files
from core.utils.document_type import DocumentType
Key = CustomPrimaryKeyField()
Doc = DocumentType()


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    vehicle = models.ForeignKey(Vehicel, on_delete=models.CASCADE)
    document_type = models.CharField(
        choices=Doc.document_type_choices, max_length=100)
    renewal_status = models.BooleanField(default=False)
    renewal_date = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    insurance_company_name = models.CharField(
        null=True, blank=True, max_length=32)
    files = models.ManyToManyField(Files, blank=True)
    renewed_tansaction_code = models.CharField(
        max_length=255, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.id)


@receiver(pre_save, sender=Document)
def update_renewal_date(sender, instance, **kwargs):
    if instance.renewal_date and not instance.expiry_date:
        instance.expiry_date = instance.renewal_date + timedelta(days=365)
