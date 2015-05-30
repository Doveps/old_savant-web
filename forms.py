from wtforms import Form, SelectField, SelectMultipleField, validators

import savant.comparisons
import savant.sets

class DiffForm(Form):
    diffs = SelectMultipleField('Diffs', [validators.Required()], choices=[])
    action = SelectField('Action', [validators.Required()], choices=[('add', 'Adds'),('subtract', 'Subtracts')])
    system = SelectField('System', [validators.Required()], choices=[])
    name = SelectField('Named', [validators.Required()], choices=[])

class DynamicDiff(object):
    def __init__(self, db, diff_id, request=None):
        self.db = db
        self.diff_id = diff_id
        self.set_id = None
        self.set_choices = []

        if request is None:
            self.form = DiffForm()
        else:
            self.form = DiffForm(request.form)
            self.set_id = self.form.action.data +'|'+ self.form.system.data +'|'+ self.form.name.data
            for delta in self.form.diffs.data:
                if delta.startswith('I'):
                    continue
                self.set_choices.append(delta)

        self.comp = savant.comparisons.get(db, self.diff_id)
        self.diff_choices = []
        self.system_choices = []
        self.name_choices = []

        for system_name in sorted(self.comp.keys()):
            self.diff_choices.append(('Isystem', system_name))
            self.system_delta('add', system_name)
            self.system_delta('subtract', system_name)

            self.system_choices.append((system_name, system_name.capitalize()))

        self.form.diffs.choices = self.diff_choices
        self.form.system.choices = self.system_choices

        self.name_choices = list(set(self.name_choices))
        self.name_choices.sort()
        self.form.name.choices = self.name_choices

    def system_delta(self, delta_type, system_name):
        if len(self.comp[system_name][delta_type]) == 0:
            return
        self.diff_choices.append(('I'+delta_type, '- '+delta_type))
        for change_instance in sorted(self.comp[system_name][delta_type].keys()):
            change_key = system_name+'|'+delta_type+'|'+change_instance
            set_id_count = str(len(savant.sets.find(change_key, self.db)))
            self.diff_choices.append((change_key, '--- '+change_instance+' ('+set_id_count+')'))
            self.name_choices.append((change_instance, change_instance))
