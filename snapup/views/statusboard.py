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
        'title': 'My Title',
        'datapoints': [
            {'label': 'text',
             'value': row.int_value}
        ]
    }
    return flask.jsonify(d)
