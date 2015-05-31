#!/usr/bin/env python
import argparse
import urllib

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

@app.before_request
def before_request():
    g.db = savant.db.DB(args.inference_db)

@app.route('/')
def home():
    return render_template('home.html', diffs=savant.comparisons.all(g.db))

@app.route('/diff/<id>')
def diff(id=None):
    dform = forms.DynamicDiff(g.db, id)
    return render_template('diff.html', id=id, form=dform.form)

@app.route('/diff/add', methods=['POST'])
def diff_add():
    id=request.form['id']
    dform = forms.DynamicDiff(g.db, id, request)
    new_set = savant.sets.Set(g.db, dform.set_id)
    new_set.add_data(dform.set_choices)
    message = Markup('New set; action: <strong>%s</strong>; system: <strong>%s</strong>; name: <strong>%s</strong>; diffs: <strong>%s</strong>' %
        (
        dform.form.action.data,
        dform.form.system.data,
        dform.form.name.data,
        str(len(dform.set_choices)),
        ))
    flash(message)
    return redirect(url_for('diff', id=id))

@app.route('/sets')
def sets():
    set_ids = savant.sets.all(g.db)
    sets = []
    for set_id in set_ids:
        set_results = savant.sets.get(set_id, g.db)
        data = {
                'id': set_id,
                'esc': urllib.quote(set_id, ''),
                'action': set_results.action,
                'system': set_results.system,
                'name': set_results.name,
                'len': len(set_results),
                }
        sets.append(data)
    return render_template('sets.html', sets=sets)

@app.route('/set/<escaped_id>')
def set(escaped_id=None):
    set_id = urllib.unquote(escaped_id)
    set_results = savant.sets.get(set_id, g.db)
    return render_template('set.html', esc = escaped_id, res = set_results)

@app.route('/set/update', methods=['POST'])
def set_update():
    escaped_id=request.form['escaped_id']
    set_id = urllib.unquote(escaped_id)
    set_results = savant.sets.get(set_id, g.db)
    message = Markup('Set updated: <strong>%s %s: %s</strong>' %
            (
                set_results.action,
                set_results.system,
                set_results.name
                ))
    flash(message)
    return redirect(url_for('sets'))

@app.route('/set/delete', methods=['POST'])
def set_delete():
    escaped_id=request.form['escaped_id']
    set_id = urllib.unquote(escaped_id)
    set_results = savant.sets.get(set_id, g.db)
    savant.sets.delete(set_id, g.db)
    message = Markup('Set deleted: <strong>%s %s: %s</strong>' %
            (
                set_results.action,
                set_results.system,
                set_results.name
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

