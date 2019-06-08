from django.contrib import admin
from tcr_tracker.tracker.models import Riders, Trackers


@admin.register(Riders)
class RiderAdmin(admin.ModelAdmin):
    pass


@admin.register(Trackers)
class TrackerAdmin(admin.ModelAdmin):
    pass
