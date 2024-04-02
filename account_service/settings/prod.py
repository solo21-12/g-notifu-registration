from .common import *
import os
from dj_database_url import config


DEBUG = False
ALLOWED_HOSTS = ['g-notify-user-auth-eb39843fac64.herokuapp.com']
SECRET_KEY = os.environ['SECRET_KEY']
DATABASES = {
    'default': config()
    # DATABASE_URL

}


EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_USE_TLS = True
