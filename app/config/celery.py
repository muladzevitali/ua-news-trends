import os

from celery import Celery

__all__ = ('app',)

os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('ua-news')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(packages=('apps.news',), related_name='tasks', force=True)
