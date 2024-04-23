from django.core.exceptions import ObjectDoesNotExist
from notification.models import Notification
from documents.models import Document
import logging

logger = logging.getLogger(__name__)


class NotificationTypes:
    def create_notification(self, document_id, priority_level, days_left, notification_type):

        try:
            cur_notification = Notification.objects.filter(
                document=document_id, priority_level=priority_level)

            if not cur_notification.exists():
                docs = Document.objects.filter(pk=document_id)

                for doc in docs:
                    new_notification = Notification.objects.create(
                        message_content=f'{days_left} days have left for your deadline',
                        notification_type=notification_type,
                        priority_level=priority_level,
                        document=doc
                    )

                    new_notification.save()  # Save the notification

                # Log the notification id
                logger.info('Notification created', new_notification.id)
            else:
                logger.info('Notification already exists')

        except ObjectDoesNotExist:
            logger.error('Document not found')

    def create_with_update_notification(self, document_id, priority_level, days_left, notification_type):

        try:
            cur_notification = Notification.objects.filter(
                document=document_id, priority_level=priority_level)

            if not cur_notification.exists():
                docs = Document.objects.filter(pk=document_id)

                for doc in docs:
                    new_notification = Notification.objects.create(
                        message_content=f'{days_left} days have left for your deadline',
                        notification_type=notification_type,
                        priority_level=priority_level,
                        document=doc
                    )

                    new_notification.save()  # Save the notification

                # Log the notification id
                    logger.info(
                        f'Notification updated : {cur_notification.id}')

            else:
                cur_notification.update(
                    message_content=f'{days_left} days have left for your deadline',
                    notification_type=notification_type,
                    priority_level=priority_level
                )

                logger.info(f'Notification updated : {cur_notification.id}')

        except ObjectDoesNotExist:
            logger.error('Document not found')
