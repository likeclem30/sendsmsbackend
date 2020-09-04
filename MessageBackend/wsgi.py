from message_backend.app import create_app
import message_backend as app

application = create_app(celery=app.celery)
application.app_context().push()
