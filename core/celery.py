from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update-db-every-day': {
        'task': 'rechner.tasks.update_price_db',
        'schedule': crontab(hour='5', minute='0', day_of_week='*'),
        'args': (),
    },
}
