from .common import *
import os
import dj_database_url


DEBUG = False
ALLOWED_HOSTS = ['g-notify-user-auth-eb39843fac64.herokuapp.com']
SECRET_KEY = os.environ['SECRET_KEY']
DATABASES = {
    'default': dj_database_url.config()}


EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_USE_TLS = True
