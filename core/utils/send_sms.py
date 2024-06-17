from twilio.rest import Client
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv(
    'TWILIO_PHONE_NUMBER')  # Rename to avoid confusion

client = Client(account_sid, auth_token)


class SMSManger:
    @staticmethod
    def send_sms(recipient_phone_number, message):

        validation_request = client.validation_requests \
            .create(
                friendly_name=f'Verify {recipient_phone_number}',
                phone_number=recipient_phone_number
            )

        try:
            message = client.messages.create(
                from_=twilio_phone_number,
                to=recipient_phone_number,
                body=message
            )
            return message.sid
        except Exception as e:
            print(e)
            return None
