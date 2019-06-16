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
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('riders/', AllRiders.as_view(), name='all_riders'),
    path('riders/<int:pk>', OneRider.as_view(), name='one_rider'),
    path('riders/<int:pk>/edit', RiderEdit.as_view(), name='rider_edit'),
    path('trackers/', AllTrackers.as_view(), name='all_trackers'),
    path('trackers/<int:pk>', OneTracker.as_view(), name='one_tracker'),
    path('trackers/<int:pk>/edit', TrackerEdit.as_view(), name='tracker_edit'),
    path('trackers/<int:pk>/test/', TrackerTest.as_view(), name='tracker_test')
]
