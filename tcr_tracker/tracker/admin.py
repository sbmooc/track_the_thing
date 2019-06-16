from django.contrib import admin
from tcr_tracker.tracker.models import Riders, Trackers, TrackerNotes, \
    RiderNotes


@admin.register(Riders)
class RiderAdmin(admin.ModelAdmin):
    pass


@admin.register(Trackers)
class TrackerAdmin(admin.ModelAdmin):
    pass


@admin.register(TrackerNotes)
class TrackerNotesAdmin(admin.ModelAdmin):
    pass


@admin.register(RiderNotes)
class RiderNotesAdmin(admin.ModelAdmin):
    pass


