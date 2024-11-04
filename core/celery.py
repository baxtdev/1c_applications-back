from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'change-clients-rate-every-month': {
#         'task': 'change_clients_rate',
#         'schedule': crontab(0, 0, day_of_month=1),
#     },
# }