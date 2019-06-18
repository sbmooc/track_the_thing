from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from tcr_tracker.tracker.models import Trackers, Riders


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


class TrackerAssignmentForm(forms.ModelForm):

    tracker = forms.ModelChoiceField(
        queryset=Trackers.objects.filter(
            rider_assigned=None
        )
    )
    deposit = forms.IntegerField()
    notes = forms.CharField()

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


class TrackerPossessionForm(forms.ModelForm):

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
        self.fields['notes'] = forms.CharField()
