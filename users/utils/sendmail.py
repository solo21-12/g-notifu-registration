from typing import List
from django.core.mail import BadHeaderError
from templated_mail.mail import BaseEmailMessage


class SendEmail:
    def send_welcome_email(self, recipient_list: List[str], verification_code: str):
        try:
            message = BaseEmailMessage(
                template_name='email/welcome.html',
                context={"verification_code": verification_code}
            )
            message.send(recipient_list)
        except BadHeaderError:
            print("Error occured")

    def send_password_reset_email(self, recipient_list: List[str], passcode: str):
        try:
            message = BaseEmailMessage(
                template_name='email/reset_password.html',
                context={'passcode': passcode}
            )
            message.send(recipient_list)
        except BadHeaderError:
            print("Error Occured")
