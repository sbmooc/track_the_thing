from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView

from tcr_tracker.tracker.models import Trackers, Riders


class AllTrackers(ListView):
    model = Trackers


class AllRiders(ListView):
    model = Riders


# class OneTracker(TemplateView):
#     template_name = "tracker.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['tracker_id'] = Trackers.objects.all()
#         return context
