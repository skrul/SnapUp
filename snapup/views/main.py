import base64

import flask
from flask_wtf.file import FileField
import flask_wtf

import wtforms
from wtforms import validators


from snapup import app
from snapup import db
from snapup import models
from snapup import tasks


class GASourceForm(flask_wtf.Form):
    name = wtforms.TextField('Name', [validators.Length(max=255)])
    service_account_name = wtforms.TextField(
        'Service account name', [validators.Length(max=255)])
    account_id = wtforms.TextField(
        'Account ID', [validators.Length(max=255)])
    web_property_id = wtforms.TextField(
        'Web Property ID', [validators.Length(max=255)])
    profile_id = wtforms.TextField(
        'Profile ID', [validators.Length(max=255)])
    private_key = FileField('Private Key')


@app.route('/')
def index():
    return flask.render_template('index.html')


@app.route('/update-schedule')
def update_schedule():
    tasks.update_schedule.delay()
    return flask.redirect(flask.url_for('index'))


@app.route('/sources')
def sources():
    sources = db.session.query(models.Source).all()
    return flask.render_template('sources.html', sources=sources)


@app.route('/source/ga/<int:source_id>', methods=('GET', 'POST'))
def ga_source(source_id):
    if not source_id:
        source_id = 0
    form = GASourceForm()

    if form.validate_on_submit():
        if source_id:
            source = db.session.query(models.Source).get(source_id)
        else:
            source = models.Source()
            q = db.session.query(models.SourceType)
            q = q.filter(name='google analytics')
            source_type = q.first()
            source.source_type = source_type
            db.session.add(source)

        params = {
            'service_account_name': form.service_account_name.data,
            'account_id': form.account_id.data,
            'web_property_id': form.web_property_id.data,
            'profile_id': form.profile_id.data,
        }

        if form.private_key.has_file():
            private_key_bytes = form.private_key.data.read()
            params['private_key'] = base64.b64encode(private_key_bytes)
        else:
            params['private_key'] = source.params['private_key']

        source.name = form.name.data
        source.params = params

        db.session.commit()

        flask.flash('Changes saved.')
        return flask.redirect(flask.url_for('ga_source',
                                            source_id=source.id))
    else:
        if source_id:
            source = db.session.query(models.Source).get(source_id)
            params = source.params or {}
            data = {
                'name': source.name,
                'service_account_name': params.get('service_account_name'),
                'account_id': params.get('account_id'),
                'web_property_id': params.get('web_property_id'),
                'profile_id': params.get('profile_id')
            }
            form = GASourceForm(**data)
        else:
            form = GASourceForm()

        return flask.render_template('ga_source.html', source_id=source_id,
                                     form=form)
