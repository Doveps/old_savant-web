#!/usr/bin/env python
import argparse
import urllib
import logging
import logging.config

from flask import Flask, g, redirect, url_for, render_template, flash, request, Markup
import flask_debugtoolbar
from flask_debugtoolbar_lineprofilerpanel.profile import line_profile

import savant.db
import savant.comparisons
import savant.diffs
import savant.sets

import forms

# configuration
DEBUG = True
SECRET_KEY = 'development key'

app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True

app.config['DEBUG_TB_PANELS'] = [
    'flask_debugtoolbar.panels.versions.VersionDebugPanel',
    'flask_debugtoolbar.panels.timer.TimerDebugPanel',
    'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
    'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
    'flask_debugtoolbar.panels.template.TemplateDebugPanel',
    #'flask_debugtoolbar.panels.sqlalchemy.SQLAlchemyDebugPanel',
    #'flask_debugtoolbar.panels.logger.LoggingPanel',
    'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel',
    'flask_debugtoolbar_lineprofilerpanel.panels.LineProfilerPanel'
]
app.config['DEBUG_TB_PROFILER_ENABLED'] = True
toolbar = flask_debugtoolbar.DebugToolbarExtension(app)

try:
    logging.config.fileConfig('log.conf', disable_existing_loggers=False)
except ConfigParser.NoSectionError:
    # probably no log.conf file
    logging.basicConfig(
            format='%(message)s',
            )

logger = logging.getLogger(__name__)

try:
    from log_override import LOG_OVERRIDES
    logging.config.dictConfig(LOG_OVERRIDES)
except:
    logger.debug('unable to load log_override; ignoring')

@app.before_request
def before_request():
    g.db = savant.db.DB(args.inference_db)

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def home():
    return render_template(
            'home.html',
            )

@app.route('/comparisons')
def comparisons():
    all_comps = savant.comparisons.all(g.db)
    complete = []
    incomplete = []

    for comp_id in all_comps:
        comp_obj = savant.comparisons.Comparison(g.db, id=comp_id)
        if comp_obj.all_assigned():
            complete.append(comp_obj.id)
        else:
            incomplete.append(comp_obj.id)

    return render_template(
            'comparisons.html',
            comparisons = all_comps,
            complete = complete,
            incomplete = incomplete,
            )

@app.route('/comparison/<id>')
def comparison(id=None):
    comp_obj = savant.comparisons.Comparison(g.db, id=id)

    sets = []
    for diff_id in comp_obj.get_diff_ids():
        diff = savant.diffs.Diff(diff_id)
        sets.extend(savant.sets.find_with_diff(diff, g.db))
    sets = sorted(list(set(sets)))
    sets = [savant.sets.Set(g.db, s) for s in sets]
    exclude_set_ids = [s.id for s in sets]

    include_id = request.args.get('include')
    if include_id is not None:
        include_id = urllib.unquote(include_id)
        exclude_set_ids.remove(include_id)
    dform = forms.DDiffNamingForm(g.db, id, exclude_set_ids=exclude_set_ids)

    return render_template(
            'comparison.html',
            id = id,
            sets = sets,
            form = dform.form,
            )

@app.route('/sets')
def sets():
    set_ids = savant.sets.all(g.db)
    sets = []
    for set_id in set_ids:
        set_obj = savant.sets.Set(g.db, set_id)

        comparisons = []
        other_sets = []

        for diff_id in set_obj.get_diff_ids():
            diff = savant.diffs.Diff(diff_id)
            comparisons.extend(savant.comparisons.find_with_diff(diff, g.db))
            other_sets.extend(savant.sets.find_with_diff(diff, g.db))

        comparisons = sorted(list(set(comparisons)))

        other_sets = sorted(list(set(other_sets)))
        other_sets.remove(set_id)
        other_sets = [savant.sets.Set(g.db, s) for s in other_sets]

        data = {
                'set': set_obj,
                'comparisons': comparisons,
                'other_sets': other_sets,
                }
        sets.append(data)
    return render_template('sets.html', sets=sets)

@app.route('/set/edit/<escaped_id>')
def set_edit(escaped_id=None):
    set_id = urllib.unquote(escaped_id)
    dform = forms.DDiffForm(g.db, set_id)
    set_obj = dform.set_obj

    comparisons = []
    for diff_id in set_obj.get_diff_ids():
        diff = savant.diffs.Diff(diff_id)
        comparisons.extend(savant.comparisons.find_with_diff(diff, g.db))
    comparisons = sorted(list(set(comparisons)))
    comparisons = [savant.comparisons.Comparison(g.db, c) for c in comparisons]

    return render_template(
            'set.html',
            set = set_obj,
            comparisons = comparisons,
            form = dform.form)

@app.route('/set/add', methods=['POST'])
def set_add():
    id=request.form['id']
    dform = forms.DDiffNamingForm(g.db, id, request)
    if len(dform.set_choices) == 0:
        flash(Markup('Did you forget to choose diffs?'))
        return redirect(url_for('comparison', id=id))

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
    for diff in dform.delete_diffs:
        diff_obj = savant.diffs.Diff(diff)
        dform.set_obj.delete_diff(diff_obj)
    message = Markup('Set updated: <strong>%s %s: %s</strong>' %
            (
                dform.set_obj.info.action,
                dform.set_obj.info.system,
                dform.set_obj.info.name
                ))
    flash(message)
    return redirect(url_for('set_edit', escaped_id=escaped_id))

@app.route('/set/delete', methods=['POST'])
def set_delete():
    escaped_id=request.form['escaped_id']
    set_id = urllib.unquote(escaped_id)
    set_obj = savant.sets.Set(g.db, set_id)
    set_obj.delete()
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

