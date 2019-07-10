from django.contrib import admin
from django.urls import path, include, reverse
from django.views.generic import RedirectView

from tcr_tracker.tracker.views import (
    AllTrackers,
    AllRiders,
    OneTracker,
    OneRider,
    TrackerEdit,
    RiderEdit,
    TrackerTest,
    RiderTrackerAssignment,
    RiderTrackerPossession,
    TrackerRiderPossession,
    TrackerRiderAssignment,
    AddNotes, RiderControlpointView, ScratchRider)



urlpatterns = [
    path(r'', RedirectView.as_view(url='/accounts/login', permanent=False), name='index'),
    path('admin/', admin.site.urls),
    path('riders/', AllRiders.as_view(), name='all_riders'),
    path('riders/<int:pk>', OneRider.as_view(), name='one_rider'),
    path('riders/<int:pk>/edit', RiderEdit.as_view(), name='rider_edit'),
    path('riders/<int:pk>/assignment', RiderTrackerAssignment.as_view(),
         name='rider_tracker_assignment'),
    path('riders/<int:pk>/possession', RiderTrackerPossession.as_view(),
         name='rider_tracker_possession'),
    path('riders/<int:pk>/notes', AddNotes.as_view(),
         name='rider_add_notes'),
    path('riders/<int:pk>/control_point', RiderControlpointView.as_view(),
         name='rider_add_control_point'),
    path('riders/<int:pk>/scratch', ScratchRider.as_view(),
         name='scratch_rider'),
    path('trackers/', AllTrackers.as_view(), name='all_trackers'),
    path('trackers/<int:pk>', OneTracker.as_view(), name='one_tracker'),
    path('trackers/<int:pk>/edit', TrackerEdit.as_view(), name='tracker_edit'),
    path('trackers/<int:pk>/test/', TrackerTest.as_view(), name='tracker_test'),
    path('trackers/<int:pk>/possession', TrackerRiderPossession.as_view(),
         name='tracker_rider_possession'),
    path('trackers/<int:pk>/assignment', TrackerRiderAssignment.as_view(),
         name='tracker_rider_assignment'),
    path('trackers/<int:pk>/notes', AddNotes.as_view(),
         name='tracker_add_notes'),
    path('accounts/', include('django.contrib.auth.urls')),
]
