import logging

from wtforms import Form, SelectField, SelectMultipleField, validators

import savant.comparisons
import savant.sets
import savant.diffs

class DiffForm(Form):
    diffs = SelectMultipleField('Diffs', [validators.Required()], choices=[])

class DiffNamingForm(DiffForm):
    action = SelectField('Action', [validators.Required()], choices=[('add', 'Adds'),('subtract', 'Subtracts')])
    system = SelectField('System', [validators.Required()], choices=[])
    name = SelectField('Named', [validators.Required()], choices=[])

class DDiffBase(object):
    '''Shared methods for DDiff Forms.'''
    def get_diff_choices(self, diff_ids, exclude_set_ids=[]):
        diff_choices = []

        prev_system = ''
        prev_action = ''
        self.logger.debug('excluding set ids: %s',exclude_set_ids)

        # take a list of savant set objects
        # turn them into a python set, for disjoint comparisons
        exclude_set_ids = set(exclude_set_ids)
        # yes this is confusing

        for id in sorted(diff_ids):
            diff = savant.diffs.Diff(id)

            set_ids_with_diff = savant.sets.find_with_diff(diff, self.db)
            # the sets this diff is in are part of the excluded ids?
            if not exclude_set_ids.isdisjoint(set_ids_with_diff):
                continue

            set_id_count = str(len(set_ids_with_diff))

            if diff.system != prev_system:
                diff_choices.append(('Isystem', diff.system))
                prev_system = diff.system
                prev_action = ''

            if diff.action != prev_action:
                diff_choices.append(('I'+diff.action, '- '+diff.action))
                prev_action = diff.action

            diff_choices.append(
                    (diff.id, '--- '+diff.name+' ('+set_id_count+')'))

        return(diff_choices)

    def get_valid_choices(self, given_choices):
        choices = []
        for diff in given_choices:
            if diff.startswith('I'):
                continue
            choices.append(diff)
        return choices

class DDiffForm(DDiffBase):
    '''This is the dynamic version of the DiffForm.'''
    def __init__(self, db, set_id, request=None):
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.db = db
        self.set_id = set_id

        self.set_obj = savant.sets.Set(self.db, self.set_id)
        self.delete_diffs = []

        if request is None:
            self.form = DiffForm()
        else:
            self.form = DiffForm(request.form)
            self.delete_diffs = self.get_valid_choices(self.form.diffs.data)

        self.form.diffs.choices = self.get_diff_choices(self.set_obj.get_diff_ids())

class DDiffNamingForm(DDiffBase):
    '''This is the dynamic version of the DiffNamingForm.'''
    def __init__(self, db, comparison_id, request=None, exclude_set_ids=[]):
        self.logger = logging.getLogger(__name__ + '.' + type(self).__name__)
        self.db = db
        self.comparison_id = comparison_id
        self.set_id = None
        self.set_choices = []

        if request is None:
            self.form = DiffNamingForm()
        else:
            self.form = DiffNamingForm(request.form)
            self.set_id = self.form.action.data +'|'+ self.form.system.data +'|'+ self.form.name.data
            self.set_choices = self.get_valid_choices(self.form.diffs.data)

        comparison = savant.comparisons.Comparison(db, id=comparison_id)
        self.form.diffs.choices = self.get_diff_choices(comparison.get_diff_ids(), exclude_set_ids)
        self.form.name.choices = self.get_name_choices()

        self.system_choices = []
        for system_name in sorted(comparison.get_systems()):
            self.system_choices.append((system_name, system_name.capitalize()))
        self.form.system.choices = self.system_choices

    def get_name_choices(self):
        '''Get name options based on the diff choice names set in this form.'''
        name_choices = []

        for choice in self.form.diffs.choices:
            if choice[0].startswith('I'):
                continue
            diff = savant.diffs.Diff(choice[0])
            name_choices.append((diff.name, diff.name))

        return sorted(list(set(name_choices)))
