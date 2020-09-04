from celery import Celery


def make_celery(app_name=__name__):
    return Celery(
        app_name,
        backend='rpc://',
        broker='amqp://rabbitmq'
        )


celery = make_celery()
