import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tradeapp_django.settings')

app = Celery('tradeapp_django')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
