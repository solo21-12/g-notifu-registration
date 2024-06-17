# from twilio.rest import Client
# import os
# from pathlib import Path
# from dotenv import load_dotenv

# # Load .env file
# env_path = Path('.') / '.env'
# load_dotenv(dotenv_path=env_path)

# account_sid = os.getenv('TWILIO_ACCOUNT_SID')
# auth_token = os.getenv('TWILIO_AUTH_TOKEN')
# twilio_phone_number = os.getenv(
#     'TWILIO_PHONE_NUMBER')  # Rename to avoid confusion

# client = Client(account_sid, auth_token)
# recipient_phone_number = '+251920225619'

# validation_request = client.validation_requests \
#     .create(
#         friendly_name=f'Verify {recipient_phone_number}',
#         phone_number=recipient_phone_number
#     )


#  cur_user = GetUser.get_owner(document.vehicle.owner)
#         phone_number = '0920225619'

#         if phone_number[0] != '+':
#             phone_number = f'+251{phone_number}'


#         # result = SMSManger.send_sms(phone_number, message_content)

#         # if result:
#         #     logger.info(f'SMS sent to {cur_user.contact.phone_number}')
#         # else:
#         #     logger.error(
#         #         f'Failed to send SMS to {cur_user.contact.phone_number}')
