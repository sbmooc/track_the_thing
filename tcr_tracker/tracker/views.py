from django.views.generic import ListView, TemplateView, DetailView
from tcr_tracker.tracker.models import Trackers, Riders


class AllTrackers(ListView):
    model = Trackers


class OneTracker(DetailView):
    model = Trackers


class AllRiders(ListView):
    model = Riders



