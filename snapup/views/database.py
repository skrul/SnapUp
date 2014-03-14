import flask
import flask_wtf

import wtforms
from wtforms import validators


from snapup import app
from snapup import db
from snapup import models


class DatabaseSourceForm(flask_wtf.Form):
    name = wtforms.TextField('Name', [validators.Length(max=255)])
    url = wtforms.TextField('URL', [validators.Length(max=1024)])


@app.route('/source/database/<int:source_id>', methods=('GET', 'POST'))
def database_source(source_id):
    if not source_id:
        source_id = 0
    form = DatabaseSourceForm()

    if form.validate_on_submit():
        if source_id:
            source = db.session.query(models.Source).get(source_id)
        else:
            source = models.Source()
            q = db.session.query(models.SourceType)
            q = q.filter(name='database')
            source_type = q.first()
            source.source_type = source_type
            db.session.add(source)

        source.name = form.name.data
        source.params = {'url': form.url.data}

        db.session.commit()

        flask.flash('Changes saved.')
        return flask.redirect(flask.url_for('database_source',
                                            source_id=source.id))
    else:
        if source_id:
            source = db.session.query(models.Source).get(source_id)
            params = source.params or {}
            data = {
                'name': source.name,
                'url': params.get('url')
            }
            form = DatabaseSourceForm(**data)
        else:
            form = DatabaseSourceForm()

        return flask.render_template('database_source.html',
                                     source_id=source_id,
                                     form=form)
