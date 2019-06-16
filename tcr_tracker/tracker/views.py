from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView
from tcr_tracker.tracker.models import Trackers, Riders




class AllTrackers(ListView):
    model = Trackers


class AllRiders(ListView):
    model = Riders


class OneTracker(TemplateView):
    template_name = "tracker.html"

    def get_context_data(self, **kwargs):
        context = super(OneTracker, self).get_context_data(**kwargs)
        context['dummy_field_list'] = ["esn_number", "working_status", "loan_status", "last_test_date", "purchase_date", "warranty_expiry",
                  "owner"]
        return context
