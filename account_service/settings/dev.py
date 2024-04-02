from .common import *

DEBUG = True
SECRET_KEY = 'django-insecure-n*$*z$cr4*7c$5lkbya##ztk@l2vr8!$i+-ha_9daq85(d)vh3'


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