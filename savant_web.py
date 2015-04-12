#!/usr/bin/env python
import argparse

from flask import Flask, g, redirect, url_for, render_template, flash, request

from savant.inferences import db

import forms

# configuration
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

@app.before_request
def before_request():
    g.db = db.DB(args.inference_db)

@app.route('/')
def home():
    return render_template('home.html', diffs=g.db.get_diffs())

@app.route('/diff/<id>')
def diff(id=None):
    form = forms.DiffForm()
    return render_template('diff.html', id=id, form=form)

@app.route('/add', methods=['POST'])
def add():
    form = forms.DiffForm(request.form)
    flash('New set added using diff, data %s'%form.testfield.data)
    return redirect(url_for('diff', id=request.form['id']))

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

