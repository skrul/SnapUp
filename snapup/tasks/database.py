import datetime

import sqlalchemy

from snapup import celery
from snapup import db
from snapup import models


@celery.task
def database(metric_id, start_date, end_date):
    metric = db.session.query(models.Metric).get(metric_id)
    source = metric.source

    engine = sqlalchemy.create_engine(source.params['url'])
    conn = engine.connect()

    today_start = datetime.datetime(day=start_date.day,
                                    month=start_date.month,
                                    year=start_date.year)
    today_end = (today_start + datetime.timedelta(days=1) -
                 datetime.timedelta(seconds=1))

    yesterday_start = today_start - datetime.timedelta(days=1)
    yesterday_end = (yesterday_start + datetime.timedelta(days=1) -
                     datetime.timedelta(seconds=1))

    sql = sqlalchemy.text(
        'select count(1) from guide where first_published between :start and :end')
    result = conn.execute(sql, start=today_start, end=today_end)
    today_count = result.first()[0]

    result = conn.execute(sql, start=yesterday_start, end=yesterday_end)
    yesterday_count = result.first()[0]
    conn.close()

    metric_rows = [(today_start, today_count),
                   (yesterday_start, yesterday_count)]
    metric.batch_update(metric_rows)
    db.session.commit()
