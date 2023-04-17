from __future__ import absolute_import, unicode_literals
from datetime import timedelta
import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core", include=["app.tasks"])

app.conf.beat_schedule = {
    'scrape_data': {
        'task': 'app.tasks.scrape_data',
        'schedule': crontab(minute="*/3"),
    },
}


app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
