#!/usr/bin/env python
from flask import Flask, g, redirect, url_for, render_template, flash, request

# configuration
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)

@app.before_request
def before_request():
    g.db = None

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        pass

@app.route('/')
def home():
    return render_template('home.html', diffs=[])

@app.route('/diff/<uuid>')
def diff(uuid=None):
    return render_template('diff.html', uuid=uuid)

@app.route('/add', methods=['POST'])
def add():
    flash('New diff was successfully added')
    return redirect(url_for('diff', uuid=request.form['uuid']))

if __name__ == '__main__':
    app.run()

