from celery.schedules import crontab
from datetime import timedelta

CELERY_TIMEZONE = 'UTC'

CELERY_TASK_SERILAIZER = 'json'

CELERY_RESULT_SERILAIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'send-message-1-minute': {
        'task': 'message',
        'schedule': crontab()
        },
    'try-resend-failed message': {
        'task': 'retry',
        'schedule': timedelta(minutes=30)
        },
    }
