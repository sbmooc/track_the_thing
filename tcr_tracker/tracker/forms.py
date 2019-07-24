from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from .models import Tracker, Rider, RiderControlPoint


class CrispyFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))


class RecordIssueForm(
    CrispyFormMixin,
    forms.Form,
):
    your_name = forms.CharField()
    brief_description_of_issue = forms.CharField(widget=forms.TextInput())
    details = forms.CharField(widget=forms.Textarea())
    url = forms.CharField(required=False, label='URL (not required)')


class AdjustBalanceForm(
    CrispyFormMixin,
    forms.Form
):
    amount = forms.FloatField()
    notes = forms.CharField(required=False)


class ScratchRiderForm(
    forms.ModelForm,
):

    notes = forms.CharField(required=False)

    class Meta:
        fields = ()
        model = Rider

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Are you sure you want to scratch this rider?'))


class AddNotesForm(
    CrispyFormMixin,
    forms.Form,
):
    notes = forms.CharField()
    input_by = forms.CharField()


class RiderControlPointForm(
    CrispyFormMixin,
    forms.ModelForm
):

    race_time = forms.SplitDateTimeField(
        widget=forms.widgets.SplitDateTimeWidget(date_attrs={'type': 'date'},
                                                 time_attrs={'type': 'time'}),
    )
    input_by = forms.CharField(
        label='Volunteer Name'
    )

    class Meta:
        model = RiderControlPoint
        fields = (
            'control_point',
            'input_by'
        )


class EditTracker(
    CrispyFormMixin,
    forms.ModelForm
):

    class Meta:
        model = Tracker
        exclude = (
            'rider_assigned',
            'rider_possesed'
        )


class EditRider(
    CrispyFormMixin,
    forms.ModelForm
):

    class Meta:
        model = Rider
        exclude = (
            'trackers_assigned',
            'trackers_possessed'
        )


class MultiActionForm(
    CrispyFormMixin,
    forms.Form
):
    def __init__(self, is_tcr_staff=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notes'] = forms.CharField(required=False)
        if not is_tcr_staff:
            self.fields['volunteer_name'] = forms.CharField()


class AssignmentPossessionForm(MultiActionForm):
    def __init__(self, obj=None, action=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = obj
        if action == 'assignment':
            self.define_assignment_fields()
        elif action == 'possession':
            self.define_possession_fields()

    def define_assignment_fields(self):
        if type(self.object) is Rider:
            self.assignment_rider_fields()

    def define_possession_fields(self):
        if type(self.object) is Tracker:
            self.possession_tracker_fields()
        if type(self.object) is Rider:
            self.possession_rider_fields()

    def assignment_rider_fields(self):
        # todo put assignable trackers into custom manager
        self.fields['assign_tracker'] = forms.ModelChoiceField(
            queryset=Tracker.objects.filter(
                rider_assigned=None,
                working_status='Functioning'
            ),
            required=False
        )
        if self.object.trackers_assigned.all():
            self.fields['remove_assignment'] = forms.ModelChoiceField(
                queryset=self.object.trackers_assigned,
                required=False,
                label='De-assign Tracker'
            )

    def possession_rider_fields(self):
        self.fields['add_possession'] = forms.ModelChoiceField(
            queryset=self.object.trackers_assigned_not_possessed,
            required=False
        )
        if self.object.trackers_possessed.all():
            self.fields['remove_possession'] = forms.ModelChoiceField(
                queryset=self.object.trackers_possessed,
                required=False
            )

    def possession_tracker_fields(self):
        if self.object.rider_possesed:
            self.fields['remove_possession'] = forms.ModelChoiceField(
                widget=forms.CheckboxInput, queryset=self.object.rider_possesed
            )
        else:
            self.fields['add_possession'] = forms.ModelChoiceField(
                widget=forms.CheckboxInput, queryset=self.object.rider_assigned
            )


class GiveRetriveForm(MultiActionForm):

    def __init__(self, obj=None, action=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['notes'] = forms.CharField(required=True)
        if action == 'give':
            self.define_give_fields(obj)
        elif action == 'retrive':
            self.define_retrive_fields(obj)

    def define_give_fields(self, obj):

        if type(obj) is Tracker:
            self.add_tracker_give_fields()
        else:
            self.add_rider_give_fields()

    def define_retrive_fields(self, obj):

        if type(obj) is Tracker:
            self.add_tracker_retrive_fields(obj)
        else:
            self.add_rider_retrive_fields(obj)

    def add_tracker_give_fields(self):
        self.fields['rider'] = forms.ModelChoiceField(queryset=Rider.objects.all())

    def add_rider_give_fields(self):
        self.fields['tracker'] = forms.ModelChoiceField(
            queryset=Tracker.objects.filter(
                rider_assigned=None,
                working_status='Functioning'
            )
        )

    def add_tracker_retrive_fields(self, obj):
        self.fields['rider'] = forms.ModelChoiceField(queryset=Rider.objects.filter(trackers_possessed=obj))

    def add_rider_retrive_fields(self, obj):
        self.fields['tracker'] = forms.ModelChoiceField(
            queryset=Tracker.objects.filter(
                rider_possesed=obj
            )
        )

