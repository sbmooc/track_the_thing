from django.contrib import admin
from django.urls import path
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
    TrackerRiderPossession, TrackerRiderAssignment, TrackerAddNotes)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('riders/', AllRiders.as_view(), name='all_riders'),
    path('riders/<int:pk>', OneRider.as_view(), name='one_rider'),
    path('riders/<int:pk>/edit', RiderEdit.as_view(), name='rider_edit'),
    path('riders/<int:pk>/assignment', RiderTrackerAssignment.as_view(),
         name='rider_tracker_assignment'),
    path('riders/<int:pk>/possession', RiderTrackerPossession.as_view(),
         name='rider_tracker_possession'),
    path('trackers/', AllTrackers.as_view(), name='all_trackers'),
    path('trackers/<int:pk>', OneTracker.as_view(), name='one_tracker'),
    path('trackers/<int:pk>/edit', TrackerEdit.as_view(), name='tracker_edit'),
    path('trackers/<int:pk>/test/', TrackerTest.as_view(), name='tracker_test'),
    path('trackers/<int:pk>/possession', TrackerRiderPossession.as_view(),
         name='tracker_rider_possession'),
    path('trackers/<int:pk>/assignment', TrackerRiderAssignment.as_view(),
         name='tracker_rider_possession'),
    path('trackers/<int:pk>/notes', TrackerAddNotes.as_view(),
         name='tracker_add_notes'),
]
