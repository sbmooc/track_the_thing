from django.contrib import admin
from django.urls import path
from tcr_tracker.tracker.views import (
    AllTrackers,
    AllRiders,
    OneTracker,
    OneRider,
    TrackerEdit
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trackers/', AllTrackers.as_view()),
    path('riders/', AllRiders.as_view()),
    path('trackers/<int:pk>', OneTracker.as_view()),
    path('trackers/<int:pk>/edit', TrackerEdit.as_view()),
    path('riders/<int:pk>', OneRider.as_view()),
]
