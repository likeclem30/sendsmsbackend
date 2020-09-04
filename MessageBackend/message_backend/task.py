from message_backend.models import MessageModel
from message_backend.db import db
from message_backend import celery
from message_backend import celeryconfig
from message_backend.message import send_message


def init_celery(celery, app):
    celery.config_from_object(celeryconfig)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask


@celery.task(name='message')
def messagetask():

    tasks = (MessageModel
             .query
             .filter(MessageModel.sent == 0)
             .filter(MessageModel.retry == 0)
             .filter(MessageModel.status == '0')
             .all())
    error = 0
    count = 0
    if not tasks:
        print('no work to be done')

    else:
        for i in tasks:

            message = i.message
            phoneNumber = i.phoneNumber

            sent = send_message(message, phoneNumber)

            if not sent['sent']:
                i.status = 'error'
                i.messageSid = 'n/a'
                error += 1

            else:
                response = sent['response']
                i.status = response.status
                i.messageSid = response.sid
                i.sent = 1
                count += 1

            db.session.add(i)

        db.session.commit()

        print(f'{count} task done, with {error} error(s)')


@celery.task(name='retry')
def retryTask():
    tasks = (MessageModel
             .query
             .filter(MessageModel.sent == 1)
             .filter(MessageModel.retry <= 5)
             .filter(MessageModel.status == '1')
             .all())
    error = 0
    count = 0

    if not tasks:
        print('no work to be done')

    else:
        for i in tasks:

            message = i.message
            phoneNumber = i.phoneNumber
            i.retry += 1

            sent = send_message(message, phoneNumber)

            if not sent['sent']:
                i.status = 'error'
                i.messageSid = 'n/a'
                error += 1

            else:
                response = sent['response']
                i.status = response.status
                i.messageSid = response.sid
                i.sent = 1
                count += 1

            db.session.add(i)

        db.session.commit()

        print(f'{count} task done, with {error} error(s)')
