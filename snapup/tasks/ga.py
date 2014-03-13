from datetime import datetime
import base64

from snapup import celery
from snapup import db
from snapup import models
from snapup.lib import google_analytics


# data request is either a point in time sample or

@celery.task
def ga(metric_id, start_date, end_date):
    metric = db.session.query(models.Metric).get(metric_id)
    source = metric.source

    ga = google_analytics.GoogleAnalytics(
        source.params['service_account_name'],
        base64.b64decode(source.params['private_key']),
        source.params['profile_id'])

    if not end_date:
        end_date = start_date

    # rows = ga.date_query(
    #     dimensions='ga:date',
    #     start_date=start_date,
    #     end_date=end_date,
    #     metrics='ga:pageviews')

    rows = ga.realtime_query(
        metrics='rt:activeVisitors')

    metric_rows = [(datetime.now(), rows[0][0])]
    print metric_rows
    metric.batch_update(metric_rows)
    db.session.commit()
