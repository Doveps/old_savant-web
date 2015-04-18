from wtforms import Form, SelectMultipleField

class DiffForm(Form):
    diffs = SelectMultipleField('Diffs', choices=[])
