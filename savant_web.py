#!/usr/bin/env python
import argparse
import urllib
import logging
import logging.config

from flask import Flask, g, redirect, url_for, render_template, flash, request, Markup

import savant.db
import savant.comparisons
import savant.sets

import forms

# configuration
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

logging.config.fileConfig('log.conf')

@app.before_request
def before_request():
    g.db = savant.db.DB(args.inference_db)

@app.route('/')
def home():
    return render_template('home.html', comparisons=savant.comparisons.all(g.db))

@app.route('/comparison/<id>')
def comparison(id=None):
    dform = forms.DDiffNamingForm(g.db, id)
    return render_template('comparison.html', id=id, form=dform.form)

@app.route('/sets')
def sets():
    set_ids = savant.sets.all(g.db)
    sets = []
    for set_id in set_ids:
        set_obj = savant.sets.get(set_id, g.db)
        data = {
                'id': set_id,
                'esc': urllib.quote(set_id, ''),
                'action': set_obj.info.action,
                'system': set_obj.info.system,
                'name': set_obj.info.name,
                'len': len(set_obj),
                }
        sets.append(data)
    return render_template('sets.html', sets=sets)

@app.route('/set/<escaped_id>')
def set(escaped_id=None):
    set_id = urllib.unquote(escaped_id)
    dform = forms.DDiffForm(g.db, set_id)
    return render_template('set.html', esc = escaped_id, res = dform.set_obj.info, form = dform.form)

@app.route('/set/add', methods=['POST'])
def set_add():
    id=request.form['id']
    dform = forms.DDiffNamingForm(g.db, id, request)
    new_set = savant.sets.Set(g.db, dform.set_id)
    new_set.update_diffs(dform.set_choices)
    message = Markup('New set; action: <strong>%s</strong>; system: <strong>%s</strong>; name: <strong>%s</strong>; diffs: <strong>%s</strong>' %
        (
        dform.form.action.data,
        dform.form.system.data,
        dform.form.name.data,
        str(len(dform.set_choices)),
        ))
    flash(message)
    return redirect(url_for('comparison', id=id))

@app.route('/set/update_diffs', methods=['POST'])
def set_update_diffs():
    escaped_id=request.form['escaped_id']
    set_id = urllib.unquote(escaped_id)
    dform = forms.DDiffForm(g.db, set_id, request)
    valid_choices = [tup[0] for tup in dform.form.diffs.choices]
    for diff in dform.form.diffs.data:
        assert diff in valid_choices
        logging.warn('deleting diff %s',diff)
        dform.set_obj.delete_diff(diff)
    message = Markup('Set updated: <strong>%s %s: %s</strong>' %
            (
                dform.set_obj.info.action,
                dform.set_obj.info.system,
                dform.set_obj.info.name
                ))
    flash(message)
    return redirect(url_for('set', escaped_id=escaped_id))

@app.route('/set/delete', methods=['POST'])
def set_delete():
    escaped_id=request.form['escaped_id']
    set_id = urllib.unquote(escaped_id)
    set_obj = savant.sets.get(set_id, g.db)
    savant.sets.delete(set_id, g.db)
    message = Markup('Set deleted: <strong>%s %s: %s</strong>' %
            (
                set_obj.info.action,
                set_obj.info.system,
                set_obj.info.name
                ))
    flash(message)
    return redirect(url_for('sets'))

if __name__ == '__main__':
    arg_parser = argparse.ArgumentParser(
            description='App to assign diffs to sets')
    arg_parser.add_argument(
            '-i', '--inference-db',
            required=True,
            help='The path to the directory containing the inference ZODB \
                    files')
    args = arg_parser.parse_args()

    app.run()

