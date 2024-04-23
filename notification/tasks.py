from celery import shared_task
from django.utils import timezone
from documents.models import Document
from .utils import SendEmail
from .notification_types import NotificationTypes
from core.models import User

current_date = timezone.now().date()
thirty_days_from_now = current_date + timezone.timedelta(days=30)
notification_types = NotificationTypes()


def send_email(recipient_list, days, document_name, car_id):
    email_sender = SendEmail()
    email_sender.send_expiration_message(
        recipient_list, days, document_name, car_id)


@shared_task
def check_expiry_date():
    documents_within_30_days = Document.objects.filter(
        expiry_date__lte=thirty_days_from_now)

    for document in documents_within_30_days:

        email = document.vehicle.owner
        car_id = document.vehicle.id
        document_id = document.id
        expiry_date = document.expiry_date
        document_name = document.document_type

        difference = expiry_date - current_date
        if timezone.timedelta(days=0) <= difference <= timezone.timedelta(days=7):
            notification_types.create_notification(
                document_id, 'Low', difference, 'Reminder')

            send_email([email], difference, document_name, car_id)
        elif timezone.timedelta(days=0) <= difference <= timezone.timedelta(days=15):
            notification_types.create_notification(
                document_id, 'Medium', difference, 'Update')
            send_email([email], difference, document_name, car_id)

        elif timezone.timedelta(days=0) <= difference <= timezone.timedelta(days=30):
            notification_types.create_with_update_notification(
                document_id, 'High', difference, 'Alert')

            send_email([email], difference, document_name, car_id)

        else:
            continue


@shared_task
def clean_unverfied_user():
    all_users = User.objects.all()

    for user in all_users:
        if user.verification_pin:
            if user.created_at.date() < current_date - timezone.timedelta(hours=3):
                user.delete()
