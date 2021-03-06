from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from tcr_tracker.tracker.views import (
    AllTrackers,
    AllRiders,
    OneTracker,
    OneRider,
    TrackerEdit,
    RiderEdit,
    TrackerTest,
    AddNotes,
    RiderControlpointView,
    ScratchRider,
    GiveRetriveView,
    AddPayment,
    AddRefund,
    RecordIssue,
    TrackerLoginView,
    AssignmentPossessionView,
    AllEvents,
    Registration,
    CPOrder,
    RefundableRiders,
)

urlpatterns = [
    path(r'', RedirectView.as_view(url='/accounts/login', permanent=False), name='index'),
    path('admin/', admin.site.urls),
    path('riders/', AllRiders.as_view(), name='all_riders'),
    path('riders/<int:pk>/', OneRider.as_view(), name='one_rider'),
    path('riders/<int:pk>/edit/', RiderEdit.as_view(), name='rider_edit'),
    path('riders/<int:pk>/assignment_possession/', AssignmentPossessionView.as_view(),
         name='rider_ass_pos'),
    path('riders/<int:pk>/notes/', AddNotes.as_view(),
         name='rider_add_notes'),
    path('riders/<int:pk>/control_point/', RiderControlpointView.as_view(),
         name='rider_add_control_point'),
    path('riders/<int:pk>/scratch/', ScratchRider.as_view(),
         name='scratch_rider'),
    path('riders/<int:pk>/add_payment/', AddPayment.as_view(),
         name='add_payment'),
    path('riders/<int:pk>/add_refund/', AddRefund.as_view(),
         name='add_refund'),
    path('riders/<int:pk>/give_retrive/', GiveRetriveView.as_view(),
         name='rider_give_retrive'),
    path('riders/<int:pk>/registration/', Registration.as_view(),
         name='rider_registration'),
    path('riders/refundable', RefundableRiders.as_view(),
         name='refundable_riders'),
    path('trackers/', AllTrackers.as_view(), name='all_trackers'),
    path('trackers/<int:pk>/', OneTracker.as_view(), name='one_tracker'),
    path('trackers/<int:pk>/edit/', TrackerEdit.as_view(), name='tracker_edit'),
    path('trackers/<int:pk>/test/', TrackerTest.as_view(), name='tracker_test'),
    path('trackers/<int:pk>/assignment_possession/', AssignmentPossessionView.as_view(),
         name='tracker_ass_poss'),
    path('trackers/<int:pk>/notes/', AddNotes.as_view(),
         name='tracker_add_notes'),
    path('trackers/<int:pk>/give_retrive/', GiveRetriveView.as_view(),
         name='tracker_give_retrive'),
    path('issues/record/', RecordIssue.as_view(),
         name='record_issue'),
    path('events/', AllEvents.as_view(), name='all_events'),
    path('cp_order/', CPOrder.as_view(), name='cp_order'),
    path('accounts/login/', TrackerLoginView.as_view(redirect_authenticated_user=True)),
    path('accounts/', include('django.contrib.auth.urls')),
]
