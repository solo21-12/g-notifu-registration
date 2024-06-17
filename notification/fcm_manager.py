import os
import firebase_admin
from firebase_admin import credentials, messaging
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
ACCOUNT_KEY_PATH = os.getenv('ACCOUNT_KEY_PATH')
device_token = os.getenv('DEVICE_TOKEN')

cred = credentials.Certificate(ACCOUNT_KEY_PATH)
firebase_admin.initialize_app(cred)


def send_push_notification(device_token, title, body):
    message = messaging.Message(
        notification=messaging.Notification(title=title, body=body),
        token=device_token
    )

    try:
        response = messaging.send(message)
        return response
    except Exception as e:
        print(e)
        return None
