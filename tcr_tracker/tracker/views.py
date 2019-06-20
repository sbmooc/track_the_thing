from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView, FormView

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

from tcr_tracker.tracker.models import Trackers, Riders, TrackerNotes, \
    RiderNotes


class RiderAddNotes(UpdateView):
    # todo: double check that UpdateView is right (previously FormView which wasn't working)
    form_class = AddRiderNotes
    model = Riders
    template_name = 'tracker/basic_form.html'

    def form_valid(self, form):
        RiderNotes(
            rider=self.object,
            notes=form.cleaned_data['notes']
        ).save()
        return super(RiderAddNotes, self).form_valid(form)


class TrackerAddNotes(UpdateView):
    form_class = AddTrackerNotes
    model = Trackers
    template_name = 'tracker/basic_form.html'

    def form_valid(self, form):
        TrackerNotes(
            tracker=self.object,
            notes=form.cleaned_data['notes']
        ).save()
        return super(TrackerAddNotes, self).form_valid(form)


class TrackerRiderPossession(UpdateView):
    model = Trackers
    form_class = TrackerRiderPossessionForm
    template_name = 'tracker/basic_form.html'

    def form_valid(self, form):
        rider = form.cleaned_data['rider']
        if form.cleaned_data['add_or_remove']:
            rider.tracker_add_possession(
                self.object,
                form.cleaned_data['notes'],
            )
        else:
            rider.tracker_remove_possession(
                self.object,
                form.cleaned_data['notes']
            )
        return HttpResponseRedirect(self.get_success_url())


class TrackerRiderAssignment(LoginRequiredMixin, UpdateView):
    model = Trackers
    form_class = TrackerRiderAssignmentForm
    template_name = 'tracker/basic_form.html'

    def form_valid(self, form):
        rider = form.cleaned_data['rider']
        if form.cleaned_data['add_or_remove']:
            rider.tracker_add_assignment(
                self.object,
                form.cleaned_data['notes'],
                form.cleaned_data['deposit']
            )
        else:
            rider.tracker_remove_assignment(
                self.object,
                form.cleaned_data['notes'],
                form.cleaned_data['deposit']
            )
        a='a'
        return HttpResponseRedirect(self.get_success_url())


class AllTrackers(ListView):
    model = Trackers


class OneTracker(DetailView):
    model = Trackers

    def get_context_data(self, **kwargs):
        context = super(OneTracker, self).get_context_data(**kwargs)
        context['tracker_dict'] = context['trackers'].__dict__
        return context


class TrackerEdit(UpdateView):
    model = Trackers
    form_class = EditTracker
    template_name = 'tracker/trackers_edit.html'


class TrackerTest(DetailView):
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


class RiderTrackerAssignment(UpdateView):
    model = Riders
    form_class = RiderTrackerAssignmentForm
    template_name = 'tracker/basic_form.html'
    # todo update success_url

    def form_valid(self, form):
        if form.cleaned_data['add_or_remove']:
            self.object.tracker_add_assignment(
                form.cleaned_data['tracker'],
                form.cleaned_data['notes'],
                form.cleaned_data['deposit']
            )
        else:
            self.object.tracker_remove_assignment(
                form.cleaned_data['tracker'],
                form.cleaned_data['notes'],
                form.cleaned_data['deposit']
            )
        return super(RiderTrackerAssignment, self).form_valid(form)


class RiderTrackerPossession(UpdateView):
    model = Riders
    form_class = RiderTrackerPossessionForm
    template_name = 'tracker/basic_form.html'

    def form_valid(self, form):
        if form.cleaned_data['add_or_remove']:
            self.object.tracker_add_possession(
                form.cleaned_data['tracker'],
                form.cleaned_data['notes'],
            )
        else:
            self.object.tracker_remove_possession(
                form.cleaned_data['tracker'],
                form.cleaned_data['notes']
            )
        return super(RiderTrackerPossession, self).form_valid(form)


class RiderEdit(UpdateView):
    model = Riders
    form_class = EditRider
    template_name = 'tracker/riders_edit.html'


class AllRiders(ListView):
    model = Riders


class OneRider(DetailView):
    model = Riders

    def get_context_data(self, **kwargs):
        context = super(OneRider, self).get_context_data(**kwargs)
        context['rider_dict'] = context['riders'].__dict__
        return context
