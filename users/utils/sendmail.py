from typing import List
from django.core.mail import BadHeaderError
from templated_mail.mail import BaseEmailMessage
import logging
from django.core.mail import send_mail

loger = logging.getLogger(__name__)


class SendEmail:
    def send_welcome_email(self, recipient_list: List[str], verification_code: str):
        try:
            message = BaseEmailMessage(
                template_name='email/welcome.html',
                context={"verification_code": verification_code}
            )
            message.send(recipient_list)
        except BadHeaderError:
            logging.ERROR("Error sending a welcome email")

    def send_password_reset_email(self, recipient_list: List[str], passcode: str):
        try:
            send_mail(
                'Password Reset', f'Your password reset code is {passcode}', 'dawitabrham0021@gmail.com', recipient_list)
        except BadHeaderError:
            logging.ERROR("Error sending a welcome email")
