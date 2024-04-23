release: python manage.py migrate
web:  gunicorn account_service.wsgi
worker: celery -A account_service worker