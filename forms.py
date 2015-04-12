from wtforms import Form, TextField

class DiffForm(Form):
    testfield = TextField('Test field')
