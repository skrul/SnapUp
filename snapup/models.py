import datetime
import json

import sqlalchemy as sa
from sqlalchemy import sql
from sqlalchemy.ext import compiler

from snapup import db


@compiler.compiles(sql.expression.Insert)
def append_string(insert, compiler, **kwargs):
    """Append an arbitrary string (e.g. ON DUPLICATE KEY UPDATE) to an insert.

    Taken from http://stackoverflow.com/a/10561643
    """
    s = compiler.visit_insert(insert, **kwargs)
    if 'append_string' in insert.kwargs:
        return s + ' ' + insert.kwargs['append_string']
    return s


class JsonType(sa.types.TypeDecorator):
    impl = sa.Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    value = db.Column(db.String(255))

    def __init__(self, value):
        self.created = datetime.datetime.now()
        self.value = value

    def __repr__(self):
        return '<Log %r>' % self.value


class SourceType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)


class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    source_type_id = db.Column(db.Integer, db.ForeignKey('source_type.id'))
    source_type = db.relationship(
        'SourceType',
        backref=db.backref('sources', lazy='dynamic'))
    params = db.Column(JsonType)


class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'))
    source = db.relationship(
        'Source',
        backref=db.backref('metrics', lazy='dynamic'))
    #schedule
    #transform

    def batch_update(self, rows):
        if not rows:
            return

        row_list = []
        for row in rows:
            row_list.append({
                'created': row[0],
                'metric_id': self.id,
                'int_value': int(row[1])
            })

        # TODO: Using append_string here raises a SA warming because
        # it isn't part of the dialect.
        db.session.execute(
            MetricData.__table__.insert(
                append_string='ON DUPLICATE KEY UPDATE int_value=int_value',
            ),
            row_list,
        )
        db.session.expire_all()


class MetricData(db.Model):
    __table_args__ = (sa.UniqueConstraint('metric_id', 'created'),)
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False)
    metric_id = db.Column(db.Integer, db.ForeignKey('metric.id'))
    metric = db.relationship(
        'Metric',
        backref=db.backref('metric_data', lazy='dynamic'))
    int_value = db.Column(db.Integer)
