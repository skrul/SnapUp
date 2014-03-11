from snapup import app
from snapup import db
from snapup import models
from snapup import tasks


@app.route('/')
def hello_world():
    log = models.Log('hello from flask')
    db.session.add(log)
    db.session.commit()
    tasks.sql.delay()
    return 'Hello World!'
