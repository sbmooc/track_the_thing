from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from tcr_tracker.tracker import views
from tcr_tracker.tracker.views import AllTrackers, AllRiders, OneTracker


urlpatterns = [
    path('admin/', admin.site.urls),
    path('trackers/', AllTrackers.as_view()),
    path('riders/', AllRiders.as_view()),
    path('tracker/', OneTracker.as_view()),
    # path('riders/<int:rider_id>', views.rider)
]
