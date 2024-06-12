from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rpg_dashboard_service.settings')

app = Celery('rpg_dashboard_service')

app.conf.broker_url = 'redis://:{}@{}:{}/{}'.format(
    settings.REDIS_PASSWORD,
    settings.REDIS_ADDRESS,
    settings.REDIS_PORT,
    settings.REDIS_INDEX
)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
