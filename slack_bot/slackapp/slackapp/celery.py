import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'slackapp.settings')

app = Celery('slackapp')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'find_new_posts': {
        'task': 'actions.tasks.find_new_posts',
        'schedule': crontab(minute='*/1'),
    },
}
