import os
from celery import Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'account_service.settings.dev')


celery = Celery('g-notify')
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.autodiscover_tasks()
