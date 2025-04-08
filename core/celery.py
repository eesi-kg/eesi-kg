import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_connection_retry_on_startup = True
app.conf.broker_connection_max_retries = 30
app.conf.broker_connection_retry_delay = 5
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'deactivate-expired-ads-daily': {
        'task': 'real_estate.tasks.check_expiring_ads',
        'schedule': 86400,  # 24 часа в секундах
        'options': {'queue': 'maintenance'},
    },
}