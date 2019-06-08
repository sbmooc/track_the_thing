from django.contrib import admin
from django.urls import path
from tcr_tracker.tracker import views
from tcr_tracker.tracker.views import AllTrackers, AllRiders

urlpatterns = [
    path('admin/', admin.site.urls),
    path('trackers/', AllTrackers.as_view()),
    path('riders/', AllRiders.as_view()),
    # path('trackers/<int:tracker_id>', views.tracker),
    # path('riders/<int:rider_id>', views.rider)
]
