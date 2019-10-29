import arrow as arrow
from django.contrib.auth.models import User
from django.db import models
from django.db.models import (
    CharField,
    DateField,
    TextField,
    DateTimeField,
    ForeignKey,
    BooleanField,
    IntegerField,
    NullBooleanField
)
from django.urls import reverse

from django.conf import settings

from tcr_tracker.tracker.errors import (
    TrackerNotAssigned,
    TrackerAlreadyAssigned,
    TrackerNotPossessed,
    TrackerNotAssignable)

TRACKER_WORKING_STATUS = (
    ('functioning', 'Functioning'),
    ('broken', 'Broken'),
    ('to_be_tested', 'To Be Tested'),
    ('lost', 'Lost'),
    ('unknown', 'Unknown'),
)

TRACKER_TESTING_STATUS = (
    ('to_be_tested', 'To Be Tested'),
    ('visual_check_OK', 'Visual Check OK'),
    ('visual_check_FAIL', 'Visual Check Fail'),
    ('ping_test_OK', 'Ping Test OK'),
    ('ping_test_FAIL', 'Ping Test Fail'),
    ('missing', 'Missing'),
    ('no_spot_plan', 'No Spot Plan')
)

TRACKER_LOAN_STATUS = (
    ('with_rider', 'With Rider'),
    ('not_loaned', 'Not Loaned'),
    ('other', 'Other'),
)

RIDER_CATEGORIES = (
    ('pairs', 'Pairs'),
    ('solo', 'Solo')
)

RIDER_GENDERS = (
    ('M', 'M'),
    ('F', 'F')
)


RIDER_STATUS = (
    ('dns', 'DNS'),
    ('active', 'Active'),
    ('finished', 'Finished'),
    ('scratched', 'Scratched')
)

DEPOSIT_STATUS = (
    ('not_yet_paid', 'Not Yet Paid'),
    ('paid', 'Paid'),
    ('to_be_refunded', 'To be refunded'),
    ('deposit_kept', 'Deposit Kept'),
    ('refunded', 'Refunded')
)

TRACKER_OWNER = (
    ('lost_dot', 'Lost Dot'),
    ('rider_owned', 'Rider Owned'),
    ('third_party', 'Third Party')
)

EVENT_CATEGORIES = (
    ('payment_in', 'Payment In'),
    ('payment_out', 'Payment Out'),
    ('start_race', 'Start Race'),
    ('finish_race', 'Finish Race'),
    ('scratch', 'Scratch'),
    ('arrive_checkpoint', 'Arrive Checkpoint'),
    ('add_tracker_assignment', 'Tracker Assigned'),
    ('remove_tracker_assignment', 'Tracker remove assignment'),
    ('add_tracker_possession', 'Tracker Possession Add'),
    ('remove_tracker_possession', 'Tracker Possession Remove'),
    ('add_tracker_assignment', 'Tracker add assignment'),
    ('remove_tracker_assignment', 'Tracker remove assignment'),
    ('add_tracker_possession', 'Tracker add possession'),
    ('remove_tracker_possession', 'Tracker remove possession'),
    ('add_note', 'Add_note'),
    ('attend_registation', 'Attend Registration')
)
EVENT_CATEGORIES += TRACKER_TESTING_STATUS


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    is_tcr_staff = BooleanField(null=True)
    is_collective_user = BooleanField(null=True)

    def __str__(self):
        return str(self.user)


class TimeStampedModel(models.Model):
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)
    # todo: uncomment before merge
    user = ForeignKey(
        Profile,
        on_delete=models.SET_NULL, null=True, blank=True
    )


class AbstractModel(models.Model):

    @property
    def pre_race(self):
        last_race_status_object = RaceStatus.objects.last()
        return False if last_race_status_object is None else last_race_status_object.pre_race

    @property
    def url(self):
        return self.get_absolute_url()

    @property
    def race_status(self):
        return RaceStatus.objects.last().status

    class Meta:
        abstract = True


class Rider(AbstractModel):

    first_name = CharField(max_length=50, verbose_name='First Name')
    last_name = CharField(max_length=50)
    email = CharField(max_length=50)
    cap_number = CharField(max_length=50)
    category = CharField(max_length=50, choices=RIDER_CATEGORIES, null=True)
    gender = CharField(max_length=10, choices=RIDER_GENDERS, null=True)
    tcr_id = CharField(max_length=10, null=True)
    country_code = CharField(max_length=5, null=True)
    hire_tracker = BooleanField(null=True)
    tracker_url = CharField(null=True, max_length=200, blank=True)
    status = CharField(
        max_length=50,
        choices=RIDER_STATUS,
        null=True,
        blank=True,
        default='active'
    )
    display_order = IntegerField()
    attended_registration_desk = NullBooleanField()
    visible = BooleanField(
        default=False
    )
    race = CharField(max_length=3, default='TCR')
    offset = IntegerField(null=True, default=0)

    @property
    def last_control(self):
        last_control = self.controlpoints.last()
        if last_control:
            return last_control.control_point.abbreviation
        else:
            return 'N/A'

    @property
    def balance(self):
        all_deposits = Deposit.objects.filter(
            rider=self
        )
        return sum(paym.amount_in_pence for paym in all_deposits) / 100

    @property
    def balance_string(self):
        sign = "-" if self.balance < 0 else ""
        return sign + "£" + '%.2f' % abs(self.balance)

    @property
    def current_tracker(self):
        return self.trackers_possessed.all().last() or None

    @property
    def trackers_assigned_not_possessed(self):
        # todo sort out this unecessary hit on the db
        return Tracker.objects.filter(rider_assigned=self, rider_possesed=None)

    @property
    def url_edit(self):
        return reverse('rider_edit', kwargs={'pk': self.id})

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def all_events(self):
        return self.events.all().order_by('created')

    def get_absolute_url(self):
        return reverse('one_rider', kwargs={'pk': self.id})

    @property
    def scratch_button_display_state(self):
        return True if self.status == 'active' else False

    @property
    def get_buttons(self):

        return {
            'race_event': {
                'label': 'Add race event',
                'url': reverse('rider_add_control_point', kwargs={'pk': self.id}),
                'staff_only': False,
                'display': True
            },
            'give': {
                'label': 'Give tracker',
                'url': reverse('rider_give_retrive', kwargs={'pk': self.id}) + '?action=give',
                'staff_only': False,
                'display': True
            },
            'retrieve': {
                'label': 'Retrieve tracker',
                'url': reverse('rider_give_retrive', kwargs={'pk': self.id}) + '?action=retrive',
                'staff_only': False,
                'display': True
            },
            'assign': {
                'label': 'Tracker Assignment',
                'url': reverse('rider_ass_pos', kwargs={'pk': self.id}) + '?action=assignment',
                'staff_only': True,
                'display': True
            },
            'possession': {
                'label': 'Tracker Possession',
                'url': reverse('rider_ass_pos', kwargs={'pk': self.id}) + '?action=possession',
                'staff_only': True,
                'display': True if self.trackers_assigned.all() else False
            },
            'scratch': {
                'label': 'Scratch Rider',
                'url': reverse('scratch_rider', kwargs={'pk': self.id}),
                'staff_only': True,
                'display': self.scratch_button_display_state
            },
            'refund': {
                'label': 'Refund',
                'url': reverse('add_refund', kwargs={'pk': self.id}),
                'staff_only': True,
                'display': True
            },
            'add_payment': {
                'label': 'Add payment',
                'url': reverse('add_payment', kwargs={'pk': self.id}),
                'staff_only': True,
                'display': True
            },
            'attend_registration': {
                'label': 'Attend Registration',
                'url': reverse('rider_registration', kwargs={'pk': self.id}),
                'staff_only': True,
                'display': True if self.pre_race else False
            },
            'notes': {
                'label': 'Add note',
                'url': reverse('rider_add_notes', kwargs={'pk': self.id}),
                'staff_only': False,
                'display': True
            }
        }

    def tracker_add_assignment(self, tracker, notes, user, input_by, deposit=10000):
        if tracker.rider_assigned is not None:
            raise TrackerAlreadyAssigned()
        if not tracker.assignable:
            raise TrackerNotAssignable()
        self.trackers_assigned.add(tracker)
        deposit = Deposit.objects.create(
            rider=self,
            amount_in_pence=deposit * -1,
            user=user.profile if user else None
        )
        Event.objects.create(
            rider=self,
            tracker=tracker,
            notes=notes,
            event_type='add_tracker_assignment',
            deposit_change=deposit,
            user=user.profile if user else None,
            input_by=input_by,
            race='TPR'
        )
        self.save()

    def tracker_remove_assignment(self, tracker, notes, user, input_by, deposit=10000):
        if tracker not in self.trackers_assigned.all():
            raise TrackerNotAssigned()
        tracker.rider_assigned = None
        deposit = Deposit.objects.create(
            rider=self,
            amount_in_pence=deposit,
            user=user.profile if user else None
        )
        Event.objects.create(
            rider=self,
            tracker=tracker,
            notes=notes,
            event_type='remove_tracker_assignment',
            deposit_change=deposit,
            user=user.profile if user else None,
            input_by=input_by,
            race='TPR'
        )
        tracker.working_status = 'to_be_tested'
        tracker.save()
        self.save()

    def tracker_add_possession(self, tracker, notes, user, input_by):
        if tracker not in self.trackers_assigned.all():
            raise TrackerNotAssigned()
        self.trackers_possessed.add(tracker)
        Event.objects.create(
            rider=self,
            tracker=tracker,
            notes=notes,
            event_type='add_tracker_possession',
            user=user.profile if user else None,
            input_by=input_by,
            race='TPR'
        )
        self.save()

    def tracker_remove_possession(self, tracker, notes, user, input_by):
        if tracker not in self.trackers_possessed.all():
            raise TrackerNotPossessed()
        tracker.rider_possesed = None
        Event.objects.create(
            rider=self,
            tracker=tracker,
            notes=notes,
            event_type='remove_tracker_possession',
            user=user.profile if user else None,
            input_by=input_by,
            race='TPR'
        )
        tracker.save()
        self.save()

    class Meta:
        verbose_name_plural = 'Riders'

    def __str__(self):
        return '#' + self.race + self.cap_number


class Deposit(TimeStampedModel):

    rider = ForeignKey(
        Rider,
        on_delete=models.SET_NULL,
        null=True,
        related_name='payment',
    )
    amount_in_pence = IntegerField()


class Tracker(AbstractModel):

    esn_number = CharField(max_length=50)
    working_status = CharField(
        max_length=50,
        choices=TRACKER_WORKING_STATUS,
        verbose_name='Working Status',
        null=True)
    loan_status = CharField(max_length=50, choices=TRACKER_LOAN_STATUS, null=True)
    last_test_date = DateField(null=True)
    purchase_date = DateField(null=True)
    warranty_expiry = DateField(null=True)
    owner = CharField(max_length=50, choices=TRACKER_OWNER)
    rider_assigned = ForeignKey(Rider,
                                on_delete=models.SET_NULL, null=True,
                                related_name='trackers_assigned',
                                blank=True)
    rider_possesed = ForeignKey(Rider,
                                on_delete=models.SET_NULL, null=True,
                                related_name='trackers_possessed',
                                blank=True)
    tcr_id = CharField(max_length=20, null=True)
    test_by = CharField(max_length=20, null=True)
    clip = BooleanField(null=True)
    test_status = CharField(
        max_length=50,
        choices=TRACKER_TESTING_STATUS,
        null=True,
        default='to_be_tested'
    )
    active_tracker = BooleanField(default=True)

    @property
    def all_events(self):
        return self.events.all().order_by('created')

    @property
    def assignable(self):
        return (
                self.rider_assigned is None
                and self.test_status == 'ping_test_OK'
                and self.rider_possesed is None
        )

    @property
    def rider_url(self):
        return self.rider_assigned.url if self.rider_assigned else None

    def get_absolute_url(self):
        return reverse('one_tracker', kwargs={'pk': self.id})

    @property
    def url_assign_tracker(self):
        return reverse('tracker_rider_assignment', kwargs={'pk': self.id})

    @property
    def url_possess_tracker(self):
        return reverse('tracker_rider_possession', kwargs={'pk': self.id})

    @property
    def url_add_notes(self):
        return reverse('tracker_add_notes', kwargs={'pk': self.id})

    @property
    def url_edit(self):
        return reverse('tracker_edit', kwargs={'pk': self.id})

    @property
    def tracker_loan_status(self):
        return self.get_loan_status_display()

    @property
    def get_buttons(self):
        return {
            'record_status': {
                'label': 'Test',
                'url': reverse('tracker_test', kwargs={'pk': self.id}),
                'staff_only': True,
                'display': True
            },
            'give': {
                'label': 'Give to rider',
                'url': reverse('tracker_give_retrive', kwargs={'pk': self.id}) + '?action=give',
                'staff_only': False,
                'display': False if Tracker.rider_assigned else True
            },
            'retrieve': {
                'label': 'Retrieve from rider',
                'url': reverse('tracker_give_retrive', kwargs={'pk': self.id}) + '?action=retrive',
                'staff_only': False,
                'display': True if Tracker.rider_possesed else False
            },
            'notes': {
                'label': 'Add note',
                'url': self.url_add_notes,
                'staff_only': False,
                'display': True
            }
        }

    class Meta:
        verbose_name_plural = 'Trackers'

    def __str__(self):
        return str(self.tcr_id)


class Event(TimeStampedModel):
    event_type = CharField(
        max_length=50,
        choices=EVENT_CATEGORIES,
        null=True,
    )
    tracker = ForeignKey(
        Tracker,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events',
    )
    rider = ForeignKey(
        Rider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events',
    )
    control_point = ForeignKey(
        'tracker.ControlPoint',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )
    notes = TextField(null=True, blank=True)
    deposit_change = ForeignKey(
        Deposit,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )
    input_by = CharField(
        max_length=50,
        null=True
    )
    race = CharField(
        choices=(('TCR', 'TCR'), ('TPR', 'TPR')),
        max_length=50,
        null=True,
        default='TPR',
    )

    @property
    def deposit_change_string(self):
        sign = "-" if self.deposit_change.amount_in_pence < 0 else "+"
        return sign + "£" + '%.2f' % abs(self.deposit_change.amount_in_pence / 100)


class RaceStatus(TimeStampedModel):
    status = CharField(
        max_length=20,
        choices=(
            ('pre_race', 'Pre_Race'),
            ('started', 'Started'),
            ('finished', 'Finished')
        ),
        unique=True
    )
    race = CharField(
        max_length=3,
        default='TCR'
    )

    @property
    def pre_race(self):
        return self.status == 'pre_race'

    @property
    def race_seconds(self):
        if self.pre_race:
            return 0
        elif self.status == 'started':
            return arrow.now().timestamp - self.created.timestamp()
        else:
            return 0

    @staticmethod
    def days_hours_minutes(td):
        return td.days, td.seconds // 3600, (td.seconds // 60) % 60

    @property
    def elapsed_time_string(self):
        if self.pre_race:
            return 'Race Not Started'
        elif self.status == 'started':
            days, hours, minutes = self.days_hours_minutes(
                arrow.now().datetime - self.created
            )
            return f'{days} Days {hours} Hours {minutes} Minutes'

    def __str__(self):
        return self.status


class ControlPoint(models.Model):
    name = CharField(max_length=50)
    abbreviation = CharField(max_length=50)
    race = CharField(max_length=3, default='TCR')

    def __str__(self):
        return self.abbreviation


class RiderControlPoint(TimeStampedModel):
    rider = ForeignKey(
        Rider,
        on_delete=models.SET_NULL, null=True,
        related_name='controlpoints',
    )
    control_point = ForeignKey(
        ControlPoint,
        on_delete=models.SET_NULL, null=True,
        related_name='riders'
    )
    race_time = DateTimeField()
    input_by = CharField(
       max_length=50
    )
    race_time_string = CharField(
        max_length=100,
        null=True
    )
    position = IntegerField(null=True)

    def __str__(self):
        return self.rider.cap_number + "--" + self.rider.full_name + "--" + self.race_time_string


