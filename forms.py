from wtforms import Form, SelectMultipleField

class DiffForm(Form):
    diffs = SelectMultipleField('Diffs', choices=[])

class DynamicDiff(object):
    def __init__(self, db, diff_id, request=None):
        self.db = db
        self.diff_id = diff_id

        if request is None:
            self.form = DiffForm()
        else:
            self.form = DiffForm(request.form)

        self.diff = db.dbroot['diffs'][self.diff_id]
        self.choices = []
        for system_name in self.diff.keys():
            self.choices.append((system_name, system_name))
            self.delta('add', system_name)
            self.delta('subtract', system_name)

        self.form.diffs.choices = self.choices

    def delta(self, delta_type, system_name):
        if len(self.diff[system_name][delta_type]) == 0:
            return
        self.choices.append((delta_type, '- '+delta_type))
        for change_instance in self.diff[system_name][delta_type].keys():
            self.choices.append((change_instance, '--- '+change_instance+' (0)'))
