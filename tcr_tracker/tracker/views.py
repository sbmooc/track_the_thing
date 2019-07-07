from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView
from tcr_tracker.tracker.views_mixins import RaceStatusMixin, EnvironmentMixin

from tcr_tracker.forms import (
    EditTracker,
    EditRider,
    RiderTrackerAssignmentForm,
    RiderTrackerPossessionForm,
    TrackerRiderAssignmentForm,
    TrackerRiderPossessionForm,
    AddRiderNotes,
    AddTrackerNotes
)

from tcr_tracker.tracker.models import Trackers, Riders, Events


class RiderAddNotes(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    UpdateView
):
    form_class = AddRiderNotes
    model = Riders
    template_name = 'tracker/basic_form.html'

    def form_valid(self, form):
        Events.objects.create(
            rider=self.object,
            notes=form.cleaned_data['notes'],
            user=self.request.user.profile
        )
        return super(RiderAddNotes, self).form_valid(form)


class TrackerAddNotes(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    UpdateView
):
    form_class = AddTrackerNotes
    model = Trackers
    template_name = 'tracker/basic_form.html'

    def form_valid(self, form):
        Events.objects.create(
            tracker=self.object,
            notes=form.cleaned_data['notes'],
            user=self.request.user.profile
        )
        return super(TrackerAddNotes, self).form_valid(form)


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


class OneTracker(RaceStatusMixin, LoginRequiredMixin, DetailView):
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


class RiderEdit(LoginRequiredMixin, UpdateView):
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
        context['rider_dict'] = context['riders'].__dict__
        context['page_title'] = 'Rider: %s' % context['riders'].full_name
        context['active_tab'] = 'riders'
        return context

