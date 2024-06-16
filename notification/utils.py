from typing import List
from django.core.mail import BadHeaderError
from templated_mail.mail import BaseEmailMessage

import logging

logger = logging.getLogger(__name__)


class SendEmail:
    def send_expiration_message(self, recipient_list: List[str], days: int, document_name: str, car_id: str):

        try:
            message = BaseEmailMessage(
                template_name='emails/expiration_date.html',
                context={
                    'document_name': document_name,
                    'car_id': car_id,
                    'days': days
                }
            )
            message.send(recipient_list)

            logger.info('Email sent successfully')
        except BadHeaderError:
            logging.error("Error sending email")
