from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Trackers, Riders, RiderControlPoints, ControlPoints, Deposit


class AdjustBalanceForm(
    forms.Form
):
    amount = forms.FloatField()

    class Meta:
        model = Deposit

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
    deposit = forms.IntegerField()
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
            'deposit',
            'notes'
        )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))


class TrackerRiderForm(forms.Form):

    def __init__(self, obj=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
        self.define_fields(obj)

    def define_fields(self, obj):
        if type(obj) is Trackers:
            self.add_tracker_fields()
        else:
            self.add_rider_fields()
        self.fields['notes'] = forms.CharField(required=False)
        self.fields['deposit'] = forms.IntegerField()

    def add_tracker_fields(self):
        self.fields['rider'] = forms.ModelChoiceField(queryset=Riders.objects.all())

    def add_rider_fields(self):
        self.fields['tracker'] = forms.ModelChoiceField(
            queryset=Trackers.objects.filter(
                rider_assigned=None
            ),
            initial=Trackers.objects.filter(
                rider_assigned=None
            ).first()
        )


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
        coerce=lambda x: x and (x.lower() != 'false')
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
        self.fields['add_or_remove'] = forms.TypedChoiceField(
            choices=[(True, 'Add Tracker'), (False, 'Remove Tracker')],
            coerce=lambda x: x and (x.lower() != 'false')
        )
