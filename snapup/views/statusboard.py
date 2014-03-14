import datetime
import flask

from snapup import app
from snapup import db
from snapup import models


@app.route('/statusboard/metric/<int:metric_id>')
def statusboard_metric(metric_id):
    q = db.session.query(models.MetricData)
    q = q.filter_by(metric_id=metric_id)
    q = q.order_by(models.MetricData.created.desc())
    row = q.first()

    d = {
        'graph': {
            'type': 'bar',
            'datasequences': [{
                'title': 'Visitors on the Web',
                'datapoints': [{
                    'title': 'People',
                    'label': 'text',
                    'value': row.int_value
                }],
            }]
        }
    }
    return flask.jsonify(d)


@app.route('/statusboard/metric/<int:metric_id>/last-hour')
def statusboard_metric_last_hour(metric_id):
    now = datetime.datetime.now()
    hour_ago = now - datetime.timedelta(hours=1)

    metric = db.session.query(models.Metric).get(metric_id)

    q = db.session.query(models.MetricData)
    q = q.filter_by(metric=metric)
    q = q.filter(models.MetricData.created > hour_ago)
    q = q.order_by(models.MetricData.created.asc())

    datapoints = []
    for row in q.all():
        datapoints.append({
            'title': str(row.created.minute),
            'value': '{:02}'.format(row.int_value)
        })

    d = {
        'graph': {
            'title': metric.name,
            'refreshEveryNSeconds': 60,
            'type': 'bar',
            'datasequences': [{
                'title': 'Users',
                'datapoints': datapoints
            }]
        }
    }
    return flask.jsonify(d)


@app.route('/statusboard/metric/<int:metric_id>/daily')
def statusboard_metric_daily(metric_id):
    now = datetime.datetime.now()
    two_weeks_ago = now - datetime.timedelta(days=14)

    metric = db.session.query(models.Metric).get(metric_id)

    q = db.session.query(models.MetricData)
    q = q.filter_by(metric=metric)
    q = q.filter(models.MetricData.created > two_weeks_ago)
    q = q.order_by(models.MetricData.created.asc())

    datapoints = []
    for row in q.all():
        datapoints.append({
            'title': row.created.strftime('%Y-%m-%d'),
            'value': '{:02}'.format(row.int_value)
        })

    d = {
        'graph': {
            'title': metric.name,
            'refreshEveryNSeconds': 60,
            'type': 'bar',
            'datasequences': [{
                'title': 'Guides',
                'datapoints': datapoints
            }]
        }
    }
    return flask.jsonify(d)
