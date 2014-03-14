import datetime

from celery import schedules

from snapup import celery
from snapup import db
from snapup import models

import database
import ga


@celery.task
def tick():
    metrics = db.session.query(models.Metric).all()
    for metric in metrics:
        cron = schedules.crontab(
            minute=metric.cron_minute or '*',
            hour=metric.cron_hour or '*',
            day_of_week=metric.cron_dow or '*',
            day_of_month=metric.cron_dom or '*',
            month_of_year=metric.cron_moy or '*')

        last_run = metric.last_run
        if not last_run:
            last_run = datetime.datetime.fromtimestamp(0)

        is_due, next_time_to_run = cron.is_due(last_run)
        if is_due:
            fn = None
            if metric.source.source_type.name == 'google analytics':
                fn = ga.ga
            elif metric.source.source_type.name == 'database':
                fn = database.database
            else:
                raise Exception('bad source type')

            fn.delay(metric.id, datetime.datetime.now(), None)
            metric.last_run = datetime.datetime.now()
    db.session.commit()
