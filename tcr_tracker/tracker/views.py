from django.views.generic import ListView, DetailView, UpdateView

from tcr_tracker.forms import EditTracker
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
    template_name = 'tracker/tracker_edit.html'


class AllRiders(ListView):
    model = Riders


class OneRider(DetailView):
    model = Riders


