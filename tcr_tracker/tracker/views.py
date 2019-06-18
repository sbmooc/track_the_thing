from django.views.generic import ListView, DetailView, UpdateView

from tcr_tracker.forms import EditTracker, EditRider
from tcr_tracker.tracker.models import Trackers, Riders


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


class RiderEdit(UpdateView):
    model = Riders
    form_class = EditRider
    template_name = 'tracker/riders_edit.html'


class AllRiders(ListView):
    model = Riders


class OneRider(DetailView):
    model = Riders
