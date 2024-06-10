from .common import *

DEBUG = True
SECRET_KEY = 'django-insecure-n*$*z$cr4*7c$5lkbya##ztk@l2vr8!$i+-ha_9daq85(d)vh3'
ALLOWED_HOSTS = ['*']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        # 'ENGINE': 'django.db.backends.postgresql',
        # 'NAME': 'railway',
        # 'USER': 'postgres',
        # 'PASSWORD': 'GqccPbtnFNOEHxQEardYENRVFeEjUDEu',
        # 'HOST': 'monorail.proxy.rlwy.net',
        # 'PORT': '56393',
    }
}


EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'dawitabrham0021@gmail.com'
EMAIL_HOST_PASSWORD = 'xqapvbcwtyicjxpq'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
CELERY_BROKER_URL = 'redis://redis:6379/1'

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda request: True
}
