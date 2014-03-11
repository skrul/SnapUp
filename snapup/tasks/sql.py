from snapup import celery
from snapup import db
from snapup import models


@celery.task
def sql():
    print 'hello from sql task'
    log = models.Log('hello from celery')
    db.session.add(log)
    db.session.commit()
