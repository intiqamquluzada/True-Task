from __future__ import absolute_import, unicode_literals
from datetime import timedelta
import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("core")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'run-every-3-minutes': {
        'task': 'app.tasks.scrape_data',
        'schedule': timedelta(minutes=3),

    },
}

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
