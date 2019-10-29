import arrow
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, FormView

from tcr_tracker.api_clients import GitHubClient
from tcr_tracker.tracker.views_mixins import(
    RaceStatusMixin,
    EnvironmentMixin,
    GetObjectMixin,
    StaffOnlyMixin,
    KeyStatsMixin
)
from .forms import (
    EditTracker,
    EditRider,
    AddNotesForm,
    RiderControlPointForm,
    ScratchRiderForm,
    GiveRetriveForm,
    AdjustBalanceForm,
    RecordIssueForm,
    AssignmentPossessionForm,
    TestTrackerForm
)

from .models import Tracker, Rider, Event, RiderControlPoint, RaceStatus, Deposit, ControlPoint


class TrackerLoginView(
    EnvironmentMixin,
    LoginView
):
    pass


class CPOrder(
    EnvironmentMixin,
    LoginRequiredMixin,
    KeyStatsMixin,
    ListView
):
    template_name = 'tracker/control_point_order.html'
    model = RiderControlPoint

    def get_context_data(self, **kwargs):
        context = super(CPOrder, self).get_context_data(**kwargs)
        context['active_tab'] = 'cp_order'
        context['control_points'] = {
            'cp_1':
                {
                    'name': 'Control Point 1',
                    'control_point': ControlPoint.objects.get(abbreviation='CP1', race='TPR'),
                    'rider_cps': context['ridercontrolpoint_list'].filter(
                        control_point=ControlPoint.objects.get(abbreviation='CP1', race='TPR')
                    ).order_by(
                        'race_time'
                    )
                },
            'cp_2':
                {
                    'name': 'Control Point 2',
                    'control_point': ControlPoint.objects.get(abbreviation='CP2', race='TPR'),
                    'rider_cps': context['ridercontrolpoint_list'].filter(
                        control_point=ControlPoint.objects.get(abbreviation='CP2', race='TPR')
                    ).order_by(
                        'race_time'
                    )
                },
            'cp_3':
                {
                    'name': 'Control Point 3',
                    'control_point': ControlPoint.objects.get(abbreviation='CP3', race='TPR'),
                    'rider_cps': context['ridercontrolpoint_list'].filter(
                        control_point=ControlPoint.objects.get(abbreviation='CP3', race='TPR')
                    ).order_by(
                        'race_time'
                    )
                },
            'finish':
                {
                    'name': 'Finished Riders',
                    'control_point': ControlPoint.objects.get(abbreviation='Finish', race='TPR'),
                    'rider_cps': context['ridercontrolpoint_list'].filter(
                        control_point=ControlPoint.objects.get(abbreviation='Finish', race='TPR')
                    ).order_by(
                        'race_time'
                    )
                }
        }
        return context


class RecordIssue(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    StaffOnlyMixin,
    GetObjectMixin,
    FormView
):
    template_name = 'tracker/basic_form.html'
    form_class = RecordIssueForm

    def form_valid(self, form):
        GitHubClient().create_issue(
            title=form.cleaned_data.get('brief_description_of_issue'),
            body=f'''URL: {form.cleaned_data.get('url')},
            REPORTED_BY: {form.cleaned_data.get('your_name')},
            DESCRIPTION: {form.cleaned_data.get('details')}
            '''
        )
        return HttpResponseRedirect(reverse('all_riders'))


class AddPayment(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    StaffOnlyMixin,
    GetObjectMixin,
    FormView
):
    template_name = 'tracker/basic_form.html'
    form_class = AdjustBalanceForm
    model = Deposit
    event_type = 'payment_in'

    def form_valid(self, form):
        self.get_object()
        deposit = Deposit.objects.create(
            rider=self.object,
            amount_in_pence=form.cleaned_data['amount'] * 100
        )
        Event.objects.create(
            event_type=self.event_type,
            user=self.request.user.profile,
            notes=form.cleaned_data['notes'],
            rider=self.object,
            deposit_change=deposit,
            race='TPR'
        )
        return HttpResponseRedirect(self.object.get_absolute_url())


class AddRefund(
    AddPayment
):
    def form_valid(self, form):
        form.cleaned_data['amount'] = form.cleaned_data['amount'] * -1
        self.event_type = 'payment_out'
        return super(AddRefund, self).form_valid(form)


class ScratchRider(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    UpdateView
):
    template_name = 'tracker/basic_form.html'
    form_class = ScratchRiderForm
    model = Rider

    def form_valid(self, form):
        Event.objects.create(
            event_type='scratch',
            notes=form.cleaned_data['notes'],
            user=self.request.user.profile,
            rider=self.object if type(self.object) is Rider else None,
            race='TPR'
        )
        self.object.status = 'scratched'
        self.object.save()
        return HttpResponseRedirect(self.object.get_absolute_url())


class AddNotes(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    GetObjectMixin,
    FormView
):
    form_class = AddNotesForm
    template_name = 'tracker/basic_form.html'
    object = None

    def form_valid(self, form):
        self.get_object()
        Event.objects.create(
            event_type='add_note',
            notes=form.cleaned_data['notes'],
            user=self.request.user.profile,
            input_by=form.cleaned_data['input_by'],
            tracker=self.object if type(self.object) is Tracker else None,
            rider=self.object if type(self.object) is Rider else None,
            race='TPR'
        )
        return HttpResponseRedirect(self.object.get_absolute_url())


class RiderControlpointView(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    UpdateView
):
    model = Rider
    template_name = 'tracker/basic_form.html'
    form_class = RiderControlPointForm

    def get_initial(self):
        initial = super(RiderControlpointView, self).get_initial()
        initial['race_time'] = arrow.Arrow.now().datetime
        return initial

    @staticmethod
    def days_hours_minutes(td):
        return td.days, td.seconds // 3600, (td.seconds // 60) % 60

    @classmethod
    def elapsed_time_string(cls, race_time, start_time):
        days, hours, minutes = cls.days_hours_minutes(
            race_time - start_time
        )
        return f'{days} Days {hours} Hours {minutes} Minutes'

    def form_valid(self, form):
        race_time = arrow.get(form.cleaned_data['race_time']).shift(hours=-2).datetime
        time_elapsed = self.elapsed_time_string(
            race_time,
            RaceStatus.objects.last().created
        )
        RiderControlPoint.objects.create(
            rider=self.object,
            control_point=form.cleaned_data['control_point'],
            race_time=race_time,
            input_by=form.cleaned_data['input_by'],
            race_time_string=time_elapsed
        )
        Event.objects.create(
            event_type='arrive_checkpoint',
            rider=self.object,
            input_by=form.cleaned_data['input_by'],
            control_point=form.cleaned_data['control_point'],
            notes=time_elapsed,
            race='TPR'
        )
        if form.cleaned_data['control_point'] == ControlPoint.objects.get(
                abbreviation='Finish',
                race='TPR'
        ):
            self.object.status = 'finished'
            self.object.save()

        return HttpResponseRedirect(self.object.get_absolute_url())


class AllTrackers(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    ListView
):
    model = Tracker
    queryset = Tracker.objects.order_by('test_status')

    def get_context_data(self, **kwargs):
        context = super(AllTrackers, self).get_context_data(**kwargs)
        context['page_title'] = 'Trackers'
        context['active_tab'] = 'trackers'
        return context


class OneTracker(
    RaceStatusMixin,
    LoginRequiredMixin,
    DetailView,
    EnvironmentMixin
):
    model = Tracker

    def get_context_data(self, **kwargs):
        context = super(OneTracker, self).get_context_data(**kwargs)
        context['tracker_dict'] = context['tracker'].__dict__
        context['page_title'] = 'Tracker %s' % context['tracker'].tcr_id
        context['active_tab'] = 'trackers'
        return context


class TrackerEdit(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    UpdateView
):
    model = Tracker
    form_class = EditTracker
    template_name = 'tracker/tracker_edit.html'


class RiderEdit(
    LoginRequiredMixin,
    UpdateView,
    RaceStatusMixin,
    EnvironmentMixin
):
    model = Rider
    form_class = EditRider
    template_name = 'tracker/rider_edit.html'


class Registration(
    LoginRequiredMixin,
    RaceStatusMixin,
    EnvironmentMixin,
    View
):
    def get(self, request, *args, **kwargs):
        rider = Rider.objects.get(**kwargs)
        rider.attended_registration_desk = True
        Event.objects.create(
            rider=rider,
            event_type='attend_registration',
            user=request.user.profile,
            race='TPR'
        )
        rider.save()
        return HttpResponseRedirect(rider.url)


class RefundableRiders(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    KeyStatsMixin,
    ListView
):
    model = Rider
    template_name = 'tracker/refund_riders.html'

    def get_queryset(self):
        all_riders = Rider.objects.all()
        return [rider for rider in all_riders if rider.balance > 0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Refund'
        context['active_tab'] = 'refundable_riders'
        return context


class AllRiders(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    KeyStatsMixin,
    ListView
):
    model = Rider
    queryset = Rider.objects.order_by('display_order').filter(race='TPR')

    def get_context_data(self, **kwargs):
        context = super(AllRiders, self).get_context_data(**kwargs)
        context['page_title'] = 'Riders'
        context['active_tab'] = 'riders'
        return context


class OneRider(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    DetailView
):
    model = Rider

    def get_context_data(self, **kwargs):
        context = super(OneRider, self).get_context_data(**kwargs)
        context['brevet_data'] = self.request.session.get('brevet_data')
        context['rider_dict'] = context['rider'].__dict__
        context['page_title'] = f"#{context['rider'].cap_number} {context['rider'].full_name}"
        context['active_tab'] = 'riders'
        return context


class AllEvents(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    ListView
):
    model = Event

    def get_context_data(self, **kwargs):
        context = super(AllEvents, self).get_context_data(**kwargs)
        context['page_title'] = 'Events'
        context['active_tab'] = 'events'
        return context


class TrackerTest(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    UpdateView
):
    model = Tracker
    form_class = TestTrackerForm
    template_name = 'tracker/basic_form.html'

    def form_valid(self, form):
        ok_test_status = (
            'visual_check_OK',
            'ping_test_OK'
        )
        Event.objects.create(
            event_type=form.cleaned_data['test_status'],
            user=self.request.user.profile,
            tracker=form.instance,
            race='TPR'
        )
        if form.cleaned_data['test_status'] in ok_test_status and form.instance.rider_assigned:
            form.instance.rider_assigned.tracker_remove_assignment(
                form.instance,
                'Tracker Assignment Removed - TEST OK',
                self.request.user,
                self.request.user.first_name
            )
        return super().form_valid(form)



class MultiActionFormView(
    RaceStatusMixin,
    EnvironmentMixin,
    LoginRequiredMixin,
    GetObjectMixin,
    FormView
):
    template_name = 'tracker/basic_form.html'

    def get(self, request, *args, **kwargs):
        self.get_object()
        return super(MultiActionFormView, self).get(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(MultiActionFormView, self).get_form_kwargs()
        self.get_object()
        kwargs.update(
            {
                'obj': self.object,
                'action': self.request.GET['action'],
                'is_tcr_staff': self.request.user.profile.is_tcr_staff
            }
        )
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(MultiActionFormView, self).get_context_data(**kwargs)
        context['tracker_form'] = True
        return context


class AssignmentPossessionView(
    MultiActionFormView
):
    form_class = AssignmentPossessionForm

    def get(self, request, *args, **kwargs):
        self.get_object()
        if request.GET.get('action') == 'assignment':
            if type(self.object) == Tracker:
                return HttpResponseRedirect(self.object.url)
            else:
                return super(AssignmentPossessionView, self).get(request, *args, **kwargs)
        elif request.GET.get('action') == 'possession':
            if type(self.object) == Tracker and not self.object.rider_assigned:
                return HttpResponseRedirect(self.object.url)
            elif type(self.object) == Rider and not self.object.trackers_assigned.all():
                return HttpResponseRedirect(self.object.url)
            else:
                return super(AssignmentPossessionView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(self.object.url)

    def form_valid(self, form):
        if type(self.object) == Rider:
            if self.request.GET.get('action') == 'assignment':
                if form.cleaned_data.get('assign_tracker'):
                    self.object.tracker_add_assignment(
                        tracker=form.cleaned_data['assign_tracker'],
                        notes=form.cleaned_data['notes'],
                        user=self.request.user,
                        input_by=form.cleaned_data.get('volunteer_name')
                    )
                if form.cleaned_data.get('remove_assignment'):
                    self.object.tracker_remove_assignment(
                        tracker=form.cleaned_data.get('remove_assignment'),
                        notes=form.cleaned_data['notes'],
                        user=self.request.user,
                        input_by=form.cleaned_data.get('volunteer_name')
                    )
            if self.request.GET.get('action') == 'possession':
                if form.cleaned_data['add_possession']:
                    self.object.tracker_add_possession(
                        tracker=form.cleaned_data.get('add_possession'),
                        notes=form.cleaned_data['notes'],
                        user=self.request.user,
                        input_by=form.cleaned_data.get('volunteer_name')
                    )
                if form.cleaned_data.get('remove_possession'):
                    self.object.tracker_remove_possession(
                        tracker=form.cleaned_data.get('remove_possession'),
                        notes=form.cleaned_data['notes'],
                        user=self.request.user,
                        input_by=form.cleaned_data.get('volunteer_name')
                    )
        elif type(self.object) == Tracker:
            if self.request.GET.get('action') == 'possession':
                rider = (
                        form.cleaned_data.get('remove_possession') or
                        form.cleaned_data.get('add_possession')
                )
                if form.cleaned_data.get('add_possession'):
                    rider.tracker_add_possession(
                        tracker=self.object,
                        notes=form.cleaned_data['notes'],
                        user=self.request.user,
                        input_by=form.cleaned_data.get('volunteer_name')
                    )
                else:
                    rider.tracker_remove_possession(
                        tracker=self.object,
                        notes=form.cleaned_data['notes'],
                        user=self.request.user,
                        input_by=form.cleaned_data.get('volunteer_name')
                    )
        return HttpResponseRedirect(self.object.url)


class GiveRetriveView(
    MultiActionFormView
):
    form_class = GiveRetriveForm

    def form_valid(self, form):
        if type(self.object) == Rider:
            if self.request.GET['action'] == 'give':
                self.object.tracker_add_assignment(
                    form.cleaned_data['tracker'],
                    form.cleaned_data['notes'],
                    self.request.user,
                    input_by=form.cleaned_data.get('input_by')
                )
                self.object.tracker_add_possession(
                    form.cleaned_data['tracker'],
                    form.cleaned_data['notes'],
                    self.request.user,
                    input_by=form.cleaned_data.get('input_by')
                )
            elif self.request.GET['action'] == 'retrive':
                self.object.tracker_remove_possession(
                    form.cleaned_data['tracker'],
                    form.cleaned_data['notes'],
                    self.request.user,
                    input_by=form.cleaned_data.get('input_by')
                )
        elif type(self.object) == Tracker:
            if self.request.GET['action'] == 'give':
                form.cleaned_data['rider'].tracker_add_assignment(
                    self.object,
                    form.cleaned_data['notes'],
                    self.request.user,
                    input_by=form.cleaned_data.get('input_by')
                )
                form.cleaned_data['rider'].tracker_add_possession(
                    self.object,
                    form.cleaned_data['notes'],
                    self.request.user,
                    input_by=form.cleaned_data.get('input_by')
                )
            elif self.request.GET['action'] == 'retrive':
                form.cleaned_data['rider'].tracker_remove_possession(
                    self.object,
                    form.cleaned_data['notes'],
                    self.request.user,
                    input_by=form.cleaned_data.get('input_by')
                )
        return HttpResponseRedirect(self.object.url)
