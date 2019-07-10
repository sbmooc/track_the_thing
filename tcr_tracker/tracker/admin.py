from django.contrib import admin
from tcr_tracker.tracker.models import Riders, Trackers, Events, RaceStatus, Profile, ControlPoints


@admin.register(Riders)
class RiderAdmin(admin.ModelAdmin):
    pass


@admin.register(Trackers)
class TrackerAdmin(admin.ModelAdmin):
    pass


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    pass


@admin.register(RaceStatus)
class RaceStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(ControlPoints)
class ControlPointAdmin(admin.ModelAdmin):
    pass
