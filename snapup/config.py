# Database
SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:@localhost/snapup'

# Celery
CELERY_BROKER_URL = 'sqla+mysql://root:@localhost/snapup'
#CELERY_RESULT_BACKEND = CELERY_BROKER_URL
