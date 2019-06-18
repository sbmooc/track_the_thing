from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, UpdateView, TemplateView, \
    FormView

from tcr_tracker.forms import EditTracker, EditRider, TrackerAssignmentForm, TrackerPossessionForm
from tcr_tracker.tracker.models import Trackers, Riders


class AllTrackers(ListView):
    model = Trackers


class OneTracker(DetailView):
    model = Trackers

    def get_context_data(self, **kwargs):
        context = super(OneTracker, self).get_context_data(**kwargs)
        context['tracker_dict'] = context['trackers'].__dict__
        context['tracker_dict'].pop('_state')
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


class TrackerAssignment(UpdateView):
    model = Riders
    form_class = TrackerAssignmentForm
    template_name = 'tracker/riders_tracker_assignment.html'
    # todo update success_url
    success_url = 'http://www.bbc.co.uk'

    def form_valid(self, form):
        self.object.tracker_add_assignment(
            form.cleaned_data['tracker'],
            form.cleaned_data['notes'],
            form.cleaned_data['deposit']
        )
        return super(TrackerAssignment, self).form_valid(form)


class TrackerPossession(UpdateView):
    model = Riders
    form_class = TrackerPossessionForm
    template_name = 'tracker/riders_tracker_assignment.html'
    success_url = 'http://www.bbc.co.uk'

    def form_valid(self, form):
        self.object.tracker_possession_add(
            form.cleaned_data['tracker'],
            form.cleaned_data['notes'],
        )
        return super(TrackerPossession, self).form_valid(form)


class RiderEdit(UpdateView):
    model = Riders
    form_class = EditRider
    template_name = 'tracker/riders_edit.html'


class AllRiders(ListView):
    model = Riders


class OneRider(DetailView):
    model = Riders
