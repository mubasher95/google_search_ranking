import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'google_search_ranking.settings')

celery_app = Celery('google_search_ranking')

celery_app.config_from_object('django.conf:settings', namespace='CELERY')

celery_app.autodiscover_tasks()