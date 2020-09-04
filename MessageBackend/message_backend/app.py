import os
from flask import Flask
from flask_restplus import Api
from message_backend.task import init_celery
from flask_cors import CORS

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split("/")[-1]


def create_app(app_name=PKG_NAME, **kwargs):

    from message_backend.api_namespace import api_namespace
    from message_backend.admin_namespace import admin_namespace
    application = Flask(app_name)
    CORS(application)
    api = Api(application, version='0.1', title='Message Backend API',
              description='A Simple CRUD API')

    if kwargs.get("celery"):
        init_celery(kwargs.get("celery"), application)

    from message_backend.db import db, db_config
    application.config['RESTPLUS_MASK_SWAGGER'] = False
    application.config.update(db_config)

    db.init_app(application)
    application.db = db

    api.add_namespace(api_namespace)
    api.add_namespace(admin_namespace)

    return application
