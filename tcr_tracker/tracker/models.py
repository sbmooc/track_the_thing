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
    IntegerField
)
from django.urls import reverse

from tcr_tracker.tracker.errors import (
    TrackerNotAssigned,
    TrackerAlreadyAssigned,
    TrackerNotPossessed
)

TRACKER_WORKING_STATUS = (
    ('working', 'Working'),
    ('broken', 'Broken'),
    ('to_be_tested', 'To Be Tested'),
    ('lost', 'Lost'),
    ('unknown', 'Unknown')
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
    ('male', 'M'),
    ('female', 'F')
)


RIDER_STATUS = (
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
    ('tested_OK', 'Tested OK'),
    ('tested_broken', 'Tested Broken'),
    ('add_tracker_assignment', 'Tracker add assignment'),
    ('remove_tracker_assignment', 'Tracker remove assignment'),
    ('add_tracker_possession', 'Tracker add possession'),
    ('remove_tracker_possession', 'Tracker remove possession'),
    ('add_note', 'Add_note')
)


class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    is_tcr_staff = BooleanField(null=True)
    is_collective_user = BooleanField(null=True)


class TimeStampedModel(models.Model):
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)
    # todo: uncomment before merge
    user = ForeignKey(
        Profile,
        on_delete=models.SET_NULL, null=True
    )


class AbstractModel(models.Model):

    @property
    def pre_race(self):
        last_race_status_object = RaceStatus.objects.last()
        return False if last_race_status_object is None else last_race_status_object.pre_race

    @property
    def url(self):
        return self.get_absolute_url()

    class Meta:
        abstract = True


class Riders(AbstractModel):

    first_name = CharField(max_length=50, verbose_name='First Name')
    last_name = CharField(max_length=50)
    email = CharField(max_length=50)
    cap_number = CharField(max_length=50)
    category = CharField(max_length=50, choices=RIDER_CATEGORIES, null=True)
    gender = CharField(max_length=10, choices=RIDER_GENDERS, null=True)
    # todo put balance in pence
    balance = IntegerField(null=True, default=0)
    tcr_id = CharField(max_length=10, null=True)
    country_code = CharField(max_length=5, null=True)
    hire_tracker = BooleanField(null=True)
    tracker_url = CharField(null=True, max_length=200, blank=True)
    status = CharField(max_length=50, choices=RIDER_STATUS, null=True)

    @property
    def race_status(self):
        return RaceStatus.objects.last().status

    @property
    def current_tracker(self):
        return self.trackers_possessed.all().last() or None

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'


    @property
    def all_events(self):
        return self.events.all()

    # todo link riders who are in pairs? or does the capnumber do that???

    def get_absolute_url(self):
        return reverse('one_rider', kwargs={'pk': self.id})

    @property
    def url_assign_tracker(self):
        return reverse('rider_tracker_assignment', kwargs={'pk': self.id})

    @property
    def url_possess_tracker(self):
        return reverse('rider_tracker_possession', kwargs={'pk': self.id})

    @property
    def url_add_notes(self):
        return reverse('rider_add_notes', kwargs={'pk': self.id})

    # todo: add url for refunds
    @property
    def url_refund(self):
        pass

    @property
    def pre_assign_button_display_state(self):
        # If pre-race, then show unless also given to rider. Combine assignment with possession during race.
        return True if self.pre_race and not self.current_tracker else False

    @property
    def de_assign_button_display_state(self):
        display_state = False

        # If during race, rider not active, all trackers returned and tested
        if not self.pre_race:
            if self.race_status != 'active' and self.current_tracker is None:
                display_state = True
                for tracker in self.trackers_assigned.all():
                    if tracker.working_status == 'to_be_tested':
                        display_state = False
                        break

        return display_state

    @property
    def give_button_display_state(self):
        # if pre-race, only when assigned
        if self.pre_race:
            if self.current_tracker is None and self.trackers_assigned.all() is None:
                return True
            else:
                return False

        if self.status == 'finished' or self.status == 'scratched':
            return False

        return True

    @property
    def retrieve_button_display_state(self):
        return True if self.current_tracker else False

    @property
    def race_event_button_display_state(self):
        return True if not self.pre_race and self.status == 'active' else False

    @property
    def refund_button_display_state(self):
        display_state = False

        # todo: add logic

        return display_state

    @property
    def get_buttons(self):
        return {
            'race_event': {
                'label': 'Add race event',
                # todo update url
                'url': reverse('rider_add_control_point', kwargs={'pk': self.id}),
                'display': self.race_event_button_display_state
            },
            'pre_assign': {
                'label': 'Pre-assign tracker',
                'url': reverse('rider_test', kwargs={'pk': self.id}),
                'display': self.pre_assign_button_display_state
            },
            'de_assign': {
                'label': 'De-assign tracker',
                'url': self.url_assign_tracker,
                'display': self.de_assign_button_display_state
            },
            'give': {
                'label': 'Give tracker',
                'url': self.url_possess_tracker,
                'display': self.give_button_display_state
            },
            'retrieve': {
                'label': 'Retrieve tracker',
                'url': self.url_possess_tracker,
                'display': self.retrieve_button_display_state
            },
            'refund': {
                'label': 'Refund',
                'url': self.url_refund,
                'display': self.refund_button_display_state
            },
            'notes': {
                'label': 'Add note',
                'url': self.url_add_notes,
                'display': True
            },
            'scratch': {
                'label': 'Scratch Rider',
                'url': reverse('scratch_rider', kwargs={'pk': self.id}),
                'display': False if self.status == 'finished' or self.status == 'scratched' else True
            }
        }

    # todo: add url_edit method for riders

    def tracker_add_assignment(self, tracker, notes, deposit, user):
        if tracker.rider_assigned is not None:
            raise TrackerAlreadyAssigned()
        self.trackers_assigned.add(tracker)
        self.save()
        Events.objects.create(
            rider=self,
            tracker=tracker,
            notes=notes,
            event_type='add_tracker_assignment',
            deposit_change=deposit * -1
        )
        self.balance -= deposit
        self.save()

    def tracker_remove_assignment(self, tracker, notes, deposit, user):
        if tracker not in self.trackers_assigned.all():
            raise TrackerNotAssigned()
        self.trackers_assigned.remove(tracker)
        self.save()
        Events.objects.create(
            rider=self,
            tracker=tracker,
            notes=notes,
            event_type='remove_tracker_assignment',
            deposit_change=deposit
        )
        self.balance += deposit
        self.save()

    def tracker_add_possession(self, tracker, notes, user):
        if tracker not in self.trackers_assigned.all():
            raise TrackerNotAssigned()
        self.trackers_possessed.add(tracker)
        Events.objects.create(
            rider=self,
            tracker=tracker,
            notes=notes,
            event_type='add_tracker_possession',
        )
        self.save()

    def tracker_remove_possession(self, tracker, notes, user):
        if tracker not in self.trackers_possessed.all():
            raise TrackerNotPossessed()
        self.trackers_possessed.remove(tracker)
        Events.objects.create(
            rider=self,
            tracker=tracker,
            notes=notes,
            event_type='remove_tracker_possession',
        )
        self.save()

    class Meta:
        verbose_name_plural = 'Riders'

    def __str__(self):
        return self.full_name


class Trackers(AbstractModel):

    esn_number = CharField(max_length=50)
    working_status = CharField(
        max_length=50,
        choices=TRACKER_WORKING_STATUS,
        verbose_name='Working Status')
    loan_status = CharField(max_length=50, choices=TRACKER_LOAN_STATUS, null=True)
    last_test_date = DateField(null=True)
    purchase_date = DateField(null=True)
    warranty_expiry = DateField(null=True)
    owner = CharField(max_length=50, choices=TRACKER_OWNER)
    rider_assigned = ForeignKey(Riders,
                                on_delete=models.SET_NULL, null=True,
                                related_name='trackers_assigned',
                                blank=True)
    rider_possesed = ForeignKey(Riders,
                               on_delete=models.SET_NULL, null=True,
                               related_name='trackers_possessed',
                               blank=True)
    tcr_id = CharField(max_length=20, null=True)
    # todo add relationship to user!
    test_by = CharField(max_length=20, null=True, blank=True)
    clip = BooleanField(null=True)

    @property
    def all_events(self):
        return self.events.all()

    @property
    def assignable(self):
        return self.rider_assigned is None and self.working_status == 'working' and self.rider_possesed is None

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
    def give_button_display_state(self):
        display_state = False

        # If pre-race, then only show when assigned but not yet possessed
        if self.pre_race:
            if self.rider_assigned and self.rider_possesed is None:
                display_state = True

        # During race, only show if assignable
        elif self.assignable:
            display_state = True

        return display_state

    @property
    def retrieve_button_display_state(self):
        display_state = False

        # At any time
        if self.rider_possesed:
            display_state = True

        return display_state

    @property
    def record_status_button_display_state(self):
        display_state = False

        # todo: add logic around admin users (across all cases)
        # If pre-race, then show unless given to rider
        if self.pre_race:
            if self.rider_possesed is None:
                display_state = True

        # If during/after race, display when back in staff possession. Use form to set status to "to_be_tested"
        elif self.working_status == 'to_be_tested':
            display_state = True

        return display_state

    # @property
    # def pre_assign_button_display_state(self):
    #     return True if self.pre_race and self.rider_assigned is not None else False

    @property
    def get_buttons(self):
        return {
            'record_status': {
                'label': 'Record status',
                #todo update url
                'url': self.record_test,
                'display': self.record_status_button_display_state
            },
            'give': {
                'label': 'Give to rider',
                'url': self.url_possess_tracker,
                'display': self.give_button_display_state
            },
            'retrieve': {
                'label': 'Retrieve',
                'url': self.url_possess_tracker,
                'display': self.retrieve_button_display_state
            },
            'notes': {
                'label': 'Add note',
                'url': self.url_add_notes,
                'display': True
            }
        }

    def record_test(self, result):
        self.working_status = 'working' if result == 'working' else 'broken'
        self.save()

    class Meta:
        verbose_name_plural = 'Trackers'

    def __str__(self):
        return str(self.tcr_id)


class Events(TimeStampedModel):
    event_type = CharField(
        max_length=50,
        choices=EVENT_CATEGORIES,
    )
    tracker = ForeignKey(
        Trackers,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events',
    )
    rider = ForeignKey(
        Riders,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events',
    )
    control_point = ForeignKey(
        'tracker.ControlPoints',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='events'
    )
    notes = TextField(null=True, blank=True)
    deposit_change = IntegerField(null=True, blank=True)
    input_by = CharField(
        max_length=50,
        null=True
    )


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


class ControlPoints(models.Model):
    name = CharField(max_length=50)
    abbreviation = CharField(max_length=50)
    latitude = CharField(max_length=50)
    longitude = CharField(max_length=50)

    def __str__(self):
        return self.abbreviation


class RiderControlPoints(TimeStampedModel):
    rider = ForeignKey(
        Riders,
        on_delete=models.SET_NULL, null=True,
        related_name='checkpoints',
    )
    control_point = ForeignKey(
        ControlPoints,
        on_delete=models.SET_NULL, null=True,
        related_name='riders'
    )
    race_time = DateField()
    input_by = CharField(
       max_length=50
    )
    race_time_string = CharField(
        max_length=100,
        null=True
    )


