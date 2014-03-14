from datetime import timedelta


# Database
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:@localhost/snapup'

# Celery
CELERY_BROKER_URL = 'sqla+mysql://root:@localhost/snapup'
#CELERY_RESULT_BACKEND = CELERY_BROKER_URL

CELERYBEAT_SCHEDULE = {
    'every-30-seconds': {
        'task': 'snapup.tasks.tick.tick',
        'schedule': timedelta(seconds=30)
    }
}
