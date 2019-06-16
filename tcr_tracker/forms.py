from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from tcr_tracker.tracker.models import Trackers


class EditTracker(forms.ModelForm):

    class Meta:
        model = Trackers
        fields = ('working_status', )

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save'))
