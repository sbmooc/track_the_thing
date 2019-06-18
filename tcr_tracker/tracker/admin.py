from django.contrib import admin
from tcr_tracker.tracker.models import Riders, Trackers, TrackerNotes, \
    RiderNotes, TrackerEvents, RiderEvents


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


@admin.register(TrackerEvents)
class TrackerEventsAdmin(admin.ModelAdmin):
    pass


@admin.register(RiderEvents)
class RiderEventsAdmin(admin.ModelAdmin):
    pass

