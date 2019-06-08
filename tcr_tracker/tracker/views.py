from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView

from tcr_tracker.tracker.models import Trackers, Riders


class AllTrackers(ListView):
    model = Trackers


class AllRiders(ListView):
    model = Riders

