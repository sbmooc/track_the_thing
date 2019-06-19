from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from tcr_tracker.tracker.models import Trackers, Riders, TrackerNotes


class TrackerAddNotesForm(forms.ModelForm):
    notes = forms.CharField()

    class Meta:
        model = TrackerNotes
        fields = (
            'notes',
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

class EditTracker(forms.ModelForm):

    class Meta:
        model = Trackers
        fields = (
            'esn_number',
            'owner',
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))


class EditRider(forms.ModelForm):

    class Meta:
        model = Riders
        exclude = ()

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))


class TrackerRiderPossessionForm(forms.ModelForm):

    class Meta:
        model = Trackers
        fields = ()

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
        self.tracker = kwargs.get('instance')
        self.fields['rider'] = forms.ModelChoiceField(
            queryset=Riders.objects.filter(
                trackers_assigned=self.tracker
            )
        )
        self.fields['notes'] = forms.CharField(required=False)
        self.fields['add_or_remove'] = forms.TypedChoiceField(
            choices=(
                (True, 'Add Tracker'),
                (False, 'Remove Tracker')
            ),
            coerce=bool
        )

class TrackerRiderAssignmentForm(forms.ModelForm):

    rider = forms.ModelChoiceField(
        queryset=Riders.objects.all()
    )
    deposit = forms.IntegerField()
    notes = forms.CharField(required=False)
    add_or_remove = forms.ChoiceField(
        choices=(
            (True, 'Add Tracker'),
            (False, 'Remove Tracker')
        )
    )

    class Meta:
        model = Trackers
        fields = (
            'rider',
            'deposit',
            'notes'
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))


class RiderTrackerAssignmentForm(forms.ModelForm):

    tracker = forms.ModelChoiceField(
        queryset=Trackers.objects.filter(
            rider_assigned=None
        )
    )
    deposit = forms.IntegerField()
    notes = forms.CharField(required=False)
    add_or_remove = forms.TypedChoiceField(
        choices=(
            (True, 'Add Tracker'),
            (False, 'Remove Tracker')
        ),
        coerce=bool
    )
    class Meta:
        model = Riders
        fields = (
            'tracker',
            'deposit',
            'notes'
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))


class RiderTrackerPossessionForm(forms.ModelForm):

    class Meta:
        model = Riders
        fields = ()

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
        self.rider = kwargs.get('instance')
        self.fields['tracker'] = forms.ModelChoiceField(
            queryset=self.rider.trackers_assigned.all()
        )
        self.fields['notes'] = forms.CharField(required=False)
        self.fields['add_or_remove'] = forms.ChoiceField(
            choices=[(True, 'Add Tracker'), (False, 'Remove Tracker')],
        )
