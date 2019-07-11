from arrow import arrow
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView, FormView, CreateView
from tcr_tracker.tracker.views_mixins import RaceStatusMixin, EnvironmentMixin, GetObjectMixin, StaffOnlyMixin
from dateutil import tz
from .forms import (
    EditTracker,
    EditRider,
    RiderTrackerAssignmentForm,
    RiderTrackerPossessionForm,
    TrackerRiderAssignmentForm,
    TrackerRiderPossessionForm,
    AddNotesForm,
    RiderControlPointForm,
    ScratchRiderForm, TrackerRiderForm,
    AdjustBalanceForm)

from .models import Trackers, Riders, Events, RiderControlPoints, RaceStatus, Deposit


class AddPayment(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    StaffOnlyMixin,
    GetObjectMixin,
    FormView
):
    template_name = 'tracker/basic_form.html'
    form_class = AdjustBalanceForm
    model = Deposit
    event_type = 'payment_in'

    def form_valid(self, form):
        self.get_object()
        Events.objects.create(
            event_type=self.event_type,
            user=self.request.user.profile,
            rider=self.object
        )
        Deposit.objects.create(
            rider=self.object,
            amount_in_pence=form.cleaned_data['amount'] * 100
        )
        return HttpResponseRedirect(self.object.get_absolute_url())


class AddRefund(
    AddPayment
):
    def form_valid(self, form):
        form.cleaned_data['amount'] = form.cleaned_data['amount'] * -1
        self.event_type = 'payment_out'
        return super(AddRefund, self).form_valid(form)


class ScratchRider(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    UpdateView
):
    template_name = 'tracker/basic_form.html'
    form_class = ScratchRiderForm
    model = Riders

    def form_valid(self, form):
        Events.objects.create(
            event_type='scratch',
            notes=form.cleaned_data['notes'],
            user=self.request.user.profile,
            rider=self.object if type(self.object) is Riders else None
        )
        self.object.status = 'scratched'
        self.object.save()
        return HttpResponseRedirect(self.object.get_absolute_url())



class AddNotes(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    GetObjectMixin,
    FormView
):
    form_class = AddNotesForm
    template_name = 'tracker/basic_form.html'
    object = None


    def form_valid(self, form):
        self.get_object()
        Events.objects.create(
            event_type='add_note',
            notes=form.cleaned_data['notes'],
            user=self.request.user.profile,
            input_by=form.cleaned_data['input_by'],
            tracker=self.object if type(self.object) is Trackers else None,
            rider=self.object if type(self.object) is Riders else None
        )
        return HttpResponseRedirect(self.object.get_absolute_url())


class RiderControlpointView(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    UpdateView
):
    model = Riders
    template_name = 'tracker/basic_form.html'
    form_class = RiderControlPointForm

    def get_initial(self):
        initial = super(RiderControlpointView, self).get_initial()
        initial['race_time'] = arrow.Arrow.now(tzinfo=tz.gettz('Europe/Paris')).datetime
        return initial

    def form_valid(self, form):
        time_elapsed = RaceStatus.objects.last().elapsed_time_string
        RiderControlPoints.objects.create(
            rider=self.object,
            control_point=form.cleaned_data['control_point'],
            race_time=form.cleaned_data['race_time'],
            input_by=form.cleaned_data['input_by'],
            race_time_string=time_elapsed
        )
        Events.objects.create(
            event_type='arrive_checkpoint',
            rider=self.object,
            input_by=form.cleaned_data['input_by'],
            control_point=form.cleaned_data['control_point'],
            notes=time_elapsed
        )
        return HttpResponseRedirect(self.object.get_absolute_url())


class TrackerRiderPossession(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    UpdateView
):
    model = Trackers
    form_class = TrackerRiderPossessionForm
    template_name = 'tracker/basic_form.html'

    def form_valid(self, form):
        rider = form.cleaned_data['rider']
        if form.cleaned_data['add_or_remove']:
            rider.tracker_add_possession(
                self.object,
                form.cleaned_data['notes'],
                self.request.user.profile
            )
        else:
            rider.tracker_remove_possession(
                self.object,
                form.cleaned_data['notes'],
                self.request.user.profile
            )
        return HttpResponseRedirect(self.get_success_url())


class TrackerRiderAssignment(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    UpdateView
):
    model = Trackers
    form_class = TrackerRiderAssignmentForm
    template_name = 'tracker/basic_form.html'

    def form_valid(self, form):
        rider = form.cleaned_data['rider']
        if form.cleaned_data['add_or_remove']:
            rider.tracker_add_assignment(
                self.object,
                form.cleaned_data['notes'],
                form.cleaned_data['deposit'],
                self.request.user.profile
            )
        else:
            rider.tracker_remove_assignment(
                self.object,
                form.cleaned_data['notes'],
                form.cleaned_data['deposit'],
                self.request.user.profile
            )
        return HttpResponseRedirect(self.get_success_url())


class AllTrackers(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    ListView
):
    model = Trackers

    def get_context_data(self, **kwargs):
        context = super(AllTrackers, self).get_context_data(**kwargs)
        context['page_title'] = 'Trackers'
        context['active_tab'] = 'trackers'
        return context


class OneTracker(
    RaceStatusMixin,
    LoginRequiredMixin,
    DetailView,
    EnvironmentMixin
):
    model = Trackers

    def get_context_data(self, **kwargs):
        context = super(OneTracker, self).get_context_data(**kwargs)
        context['tracker_dict'] = context['trackers'].__dict__
        context['page_title'] = 'Tracker %s' % context['trackers'].tcr_id
        context['active_tab'] = 'trackers'
        return context


class TrackerEdit(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    UpdateView
):
    model = Trackers
    form_class = EditTracker
    template_name = 'tracker/trackers_edit.html'


class TrackerTest(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    DetailView
):
    model = Trackers
    template_name = 'tracker/trackers_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TrackerTest, self).get_context_data(**kwargs)
        context['alert'] = 'changed'
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.record_test(request.GET['result'])
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class RiderTrackerAssignment(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    UpdateView
):
    model = Riders
    form_class = RiderTrackerAssignmentForm
    template_name = 'tracker/basic_form.html'
    # todo update success_url

    def form_valid(self, form):
        if form.cleaned_data['add_or_remove']:
            self.object.tracker_add_assignment(
                form.cleaned_data['tracker'],
                form.cleaned_data['notes'],
                form.cleaned_data['deposit'],
                self.request.user.profile
            )
        else:
            self.object.tracker_remove_assignment(
                form.cleaned_data['tracker'],
                form.cleaned_data['notes'],
                form.cleaned_data['deposit'],
                self.request.user.profile
            )
        return super(RiderTrackerAssignment, self).form_valid(form)


class RiderTrackerPossession(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    UpdateView
):
    model = Riders
    form_class = RiderTrackerPossessionForm
    template_name = 'tracker/basic_form.html'

    def form_valid(self, form):
        if form.cleaned_data['add_or_remove']:
            self.object.tracker_add_possession(
                form.cleaned_data['tracker'],
                form.cleaned_data['notes'],
                self.request.user.profile
            )
        else:
            self.object.tracker_remove_possession(
                form.cleaned_data['tracker'],
                form.cleaned_data['notes'],
                self.request.user.profile
            )
        return super(RiderTrackerPossession, self).form_valid(form)


class RiderEdit(
    LoginRequiredMixin,
    UpdateView,
    RaceStatusMixin,
    EnvironmentMixin
):
    model = Riders
    form_class = EditRider
    template_name = 'tracker/riders_edit.html'


class AllRiders(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    ListView
):
    model = Riders

    def get_context_data(self, **kwargs):
        context = super(AllRiders, self).get_context_data(**kwargs)
        context['page_title'] = 'Riders'
        context['active_tab'] = 'riders'
        return context


class OneRider(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    DetailView
):
    model = Riders

    def get_context_data(self, **kwargs):
        context = super(OneRider, self).get_context_data(**kwargs)
        context['brevet_data'] = self.request.session.get('brevet_data')
        context['rider_dict'] = context['riders'].__dict__
        context['page_title'] = 'Rider: %s' % context['riders'].full_name
        context['active_tab'] = 'riders'
        return context


class TrackerRider(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    GetObjectMixin,
    FormView
):
    form_class = TrackerRiderForm
    template_name = 'tracker/basic_form.html'

    def get_form_kwargs(self):
        kwargs = super(TrackerRider, self).get_form_kwargs()
        self.get_object()
        kwargs.update(
            {
                'obj': self.object
            }
        )
        return kwargs

    def form_valid(self, form):
        pass
