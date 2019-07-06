from django.contrib import admin
from tcr_tracker.tracker.models import Riders, Trackers, Events, RaceStatus


@admin.register(Riders)
class RiderAdmin(admin.ModelAdmin):
    pass


@admin.register(Trackers)
class TrackerAdmin(admin.ModelAdmin):
    pass


@admin.register(Events)
class TrackerNotesAdmin(admin.ModelAdmin):
    pass

@admin.register(RaceStatus)
class TrackerNotesAdmin(admin.ModelAdmin):
    pass
