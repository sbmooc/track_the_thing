from django.contrib import admin
from tcr_tracker.tracker.models import Rider, Tracker, Event, RaceStatus, Profile, ControlPoint, Deposit


@admin.register(Rider)
class RiderAdmin(admin.ModelAdmin):
    pass


@admin.register(Tracker)
class TrackerAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventsAdmin(admin.ModelAdmin):
    pass


@admin.register(RaceStatus)
class RaceStatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(ControlPoint)
class ControlPointAdmin(admin.ModelAdmin):
    pass


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    pass
