from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from notification.models import Notification
from documents.models import Document
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


class NotificationTypes:
    def create_notification(self, document_id, priority_level, days_left, notification_type, recurring=False):
        document = get_object_or_404(Document, pk=document_id)

        if not recurring:
            cur_notification = Notification.objects.filter(
                document=document,
                priority_level=priority_level
            ).first()

            if cur_notification:
                logger.info(
                    f'Notification already exists: {cur_notification.id}')
                return

        message_content = f'{days_left} days left for your deadline'

        new_notification = Notification.objects.create(
            message_content=message_content,
            notification_type=notification_type,
            priority_level=priority_level,
            document=document
        )
        new_notification.save()

        logger.info(f'Notification created: {new_notification.id}')

        self.send_email([document.vehicle.owner.email], days_left,
                        document.document_type, document.vehicle.chassis_number)

    def send_email(self, recipients, days_left, document_name, chassis_number):
        subject = f"Reminder: {document_name} expiry in {days_left} days"
        message = f"Your {document_name} for vehicle with chassis number {chassis_number} will expire in {days_left} days. Please take necessary action."
        # Ensure you have this set in your Django settings
        from_email = settings.EMAIL_HOST_USER

        try:
            send_mail(subject, message, from_email, recipients)
            logger.info(f'Email sent to {recipients} with subject "{subject}"')
        except Exception as e:
            logger.error(f'Failed to send email to {recipients}: {e}')
