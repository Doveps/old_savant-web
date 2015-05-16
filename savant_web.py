#!/usr/bin/env python
import argparse

from flask import Flask, g, redirect, url_for, render_template, flash, request, Markup

import savant.db
import savant.comparisons

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

@app.route('/add', methods=['POST'])
def add():
    id=request.form['id']
    dform = forms.DynamicDiff(g.db, id, request)
    message = Markup('New set; action: <strong>%s</strong>; system: <strong>%s</strong>; name: <strong>%s</strong>; diffs: <strong>%s</strong>' %
        (
        dform.form.action.data,
        dform.form.system.data,
        dform.form.name.data,
        dform.form.diffs.data
        ))
    flash(message)
    return redirect(url_for('diff', id=id))

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

