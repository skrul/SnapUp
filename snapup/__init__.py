from __future__ import absolute_import

from celery import Celery
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import flask_bootstrap
from flask_wtf.csrf import CsrfProtect


app = Flask(__name__)
app.config.from_pyfile('config.py')
app.secret_key = 'snapguide forever'

flask_bootstrap.Bootstrap(app)
CsrfProtect(app)

db = SQLAlchemy(app)


def make_celery(app):
    celery = Celery(app.import_name,
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)

import snapup.models
import snapup.views.main
import snapup.views.statusboard
