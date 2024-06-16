from celery import shared_task
from django.utils import timezone
from documents.models import Document
from .utils import SendEmail
from .notification_types import NotificationTypes
from core.models import User
import logging

current_date = timezone.now().date()
thirty_days_from_now = current_date + timezone.timedelta(days=30)
notification_types = NotificationTypes()
logger = logging.getLogger(__name__)


@shared_task
def check_expiry_date():
    current_date = timezone.now().date()
    thirty_days_from_now = current_date + timezone.timedelta(days=30)
    documents_within_30_days = Document.objects.filter(
        expiry_date__lte=thirty_days_from_now)

    logging.info(documents_within_30_days)

    notification_types = NotificationTypes()

    for document in documents_within_30_days:
        document_id = document.id
        expiry_date = document.expiry_date
        difference = expiry_date - current_date

        if timezone.timedelta(days=0) <= difference <= timezone.timedelta(days=7):
            notification_types.create_notification(
                document_id, 'High', difference.days, 'Alert', recurring=True)
        elif timezone.timedelta(days=0) <= difference <= timezone.timedelta(days=15):
            notification_types.create_notification(
                document_id, 'Medium', difference.days, 'Update')
        elif timezone.timedelta(days=0) <= difference <= timezone.timedelta(days=30):
            notification_types.create_notification(
                document_id, 'Low', difference.days, 'Reminder')


@shared_task
def clean_unverfied_user():
    all_users = User.objects.all()
    for user in all_users:
        if user.verification_pin:
            if user.created_at.date() < current_date - timezone.timedelta(hours=3):
                user.delete()
