import datetime

from snapup import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)
    value = db.Column(db.String(255))

    def __init__(self, value):
        self.created = datetime.datetime.now()
        self.value = value

    def __repr__(self):
        return '<Log %r>' % self.value
