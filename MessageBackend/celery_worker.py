from message_backend import celery
from message_backend.app import create_app
from message_backend.task import init_celery

app = create_app()

init_celery(celery, app)
