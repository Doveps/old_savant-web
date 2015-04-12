#!/usr/bin/env python
import argparse

from flask import Flask, g, redirect, url_for, render_template, flash, request

from savant.inferences import db

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
    return render_template('diff.html', id=id)

@app.route('/add', methods=['POST'])
def add():
    flash('New set added using diff')
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

