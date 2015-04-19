from wtforms import Form, SelectField, SelectMultipleField

class DiffForm(Form):
    diffs = SelectMultipleField('Diffs', choices=[])
    action = SelectField('Action', choices=[('', '-----'),('add', 'Adds'),('subtract', 'Subtracts')])
    system = SelectField('System', choices=[])
    name = SelectField('Named', choices=[])

class DynamicDiff(object):
    def __init__(self, db, diff_id, request=None):
        self.db = db
        self.diff_id = diff_id

        if request is None:
            self.form = DiffForm()
        else:
            self.form = DiffForm(request.form)

        self.diff = db.dbroot['diffs'][self.diff_id]
        self.diff_choices = []
        self.system_choices = [('', '-----')]
        self.name_choices = []

        for system_name in sorted(self.diff.keys()):
            self.diff_choices.append(('Isystem', system_name))
            self.system_delta('add', system_name)
            self.system_delta('subtract', system_name)

            self.system_choices.append((system_name, system_name.capitalize()))

        self.form.diffs.choices = self.diff_choices
        self.form.system.choices = self.system_choices

        self.name_choices = list(set(self.name_choices))
        self.name_choices.sort()
        self.name_choices.insert(0, ('', '-----'))
        self.form.name.choices = self.name_choices

    def system_delta(self, delta_type, system_name):
        if len(self.diff[system_name][delta_type]) == 0:
            return
        self.diff_choices.append(('I'+delta_type, '- '+delta_type))
        for change_instance in sorted(self.diff[system_name][delta_type].keys()):
            self.diff_choices.append((system_name+'|'+delta_type+'|'+change_instance, '--- '+change_instance+' (0)'))
            self.name_choices.append((change_instance, change_instance))
