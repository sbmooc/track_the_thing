from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Trackers, Riders, RiderControlPoints

class RecordIssueForm(
    forms.Form
):
    url = forms.CharField()
    brief_description_of_issue = forms.CharField(widget=forms.TextInput())
    details = forms.CharField(widget=forms.Textarea())
    your_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))


class AdjustBalanceForm(
    forms.Form
):
    amount = forms.FloatField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))

class ScratchRiderForm(
    forms.ModelForm
):

    notes = forms.CharField(required=False)

    class Meta:
        fields = ()
        model = Riders

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Are you sure you want to scratch this rider?'))


class AddNotesForm(forms.Form):
    notes = forms.CharField()
    input_by = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))


class RiderControlPointForm(forms.ModelForm):

    race_time = forms.SplitDateTimeField(
        widget=forms.widgets.SplitDateTimeWidget(date_attrs={'type': 'date'},
                                                 time_attrs={'type': 'time'})
    )

    class Meta:
        model = RiderControlPoints
        fields = (
            'control_point',
            'input_by'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))


class EditTracker(forms.ModelForm):

    class Meta:
        model = Trackers
        exclude = (
            'rider_assigned',
            'rider_possesed'
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))


class EditRider(forms.ModelForm):

    class Meta:
        model = Riders
        exclude = (
            'trackers_assigned',
            'trackers_possessed'
        )

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
            coerce=lambda x: x and (x.lower() != 'false')
        )


class TrackerRiderAssignmentForm(forms.ModelForm):

    rider = forms.ModelChoiceField(
        queryset=Riders.objects.all()
    )
    notes = forms.CharField(required=False)
    add_or_remove = forms.TypedChoiceField(
        choices=(
            (True, 'Add Tracker'),
            (False, 'Remove Tracker')
        ),
        coerce=lambda x: x and (x.lower() != 'false')
    )

    class Meta:
        model = Trackers
        fields = (
            'rider',
            'notes'
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))


class TrackerRiderForm(forms.Form):

    def __init__(self, obj=None, action=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
        if action == 'give':
            self.define_give_fields(obj)
        elif action == 'retrive':
            self.define_retrive_fields(obj)
        self.fields['notes'] = forms.CharField(required=False)

    def define_give_fields(self, obj):

        if type(obj) is Trackers:
            self.add_tracker_give_fields()
        else:
            self.add_rider_give_fields()

    def define_retrive_fields(self, obj):

        if type(obj) is Trackers:
            self.add_tracker_retrive_fields(obj)
        else:
            self.add_rider_retrive_fields(obj)

    def add_tracker_give_fields(self):
        self.fields['rider'] = forms.ModelChoiceField(queryset=Riders.objects.all())

    def add_rider_give_fields(self):
        self.fields['tracker'] = forms.ModelChoiceField(
            queryset=Trackers.objects.filter(
                rider_assigned=None,
                working_status='Functioning'
            )
        )

    def add_tracker_retrive_fields(self, obj):
        self.fields['rider'] = forms.ModelChoiceField(queryset=Riders.objects.filter(trackers_possessed=obj))

    def add_rider_retrive_fields(self, obj):
        self.fields['tracker'] = forms.ModelChoiceField(
            queryset=Trackers.objects.filter(
                rider_possesed=obj
            )
        )


class RiderTrackerAssignmentForm(forms.ModelForm):

    tracker = forms.ModelChoiceField(
        queryset=Trackers.objects.filter(
            rider_assigned=None
        )
    )
    notes = forms.CharField(required=False)
    add_or_remove = forms.TypedChoiceField(
        choices=(
            (True, 'Add Tracker'),
            (False, 'Remove Tracker')
        ),
        coerce=lambda x: x and (x.lower() != 'false')
    )
    class Meta:
        model = Riders
        fields = (
            'tracker',
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
        self.fields['add_or_remove'] = forms.TypedChoiceField(
            choices=[(True, 'Add Tracker'), (False, 'Remove Tracker')],
            coerce=lambda x: x and (x.lower() != 'false')
        )
