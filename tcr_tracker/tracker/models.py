from django.db import models
from django.db.models import (
    CharField,
    DateField,
    FloatField,
    TextField,
    DateTimeField,
    ForeignKey,
    BooleanField,
    IntegerField)
from django.urls import reverse

from tcr_tracker.tracker.errors import TrackerNotAssigned, \
    TrackerAlreadyAssigned, TrackerNotPossessed

TRACKER_WORKING_STATUS = (
    ('working', 'Working'),
    ('broken', 'Broken'),
    ('to_be_tested', 'To Be Tested'),
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
    ('not_yet_started', 'Not Yet Started'),
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

RIDER_EVENT_CATEGORIES = (
    ('payment_in', 'Payment In'),
    ('payment_out', 'Payment Out'),
    ('start_race', 'Start Race'),
    ('finish_race', 'Finish Race'),
    ('scratch', 'Scratch'),
    ('arrive_checkpoint', 'Arrive Checkpoint'),
    ('add_tracker_assignment', 'Tracker Assigned'),
    ('remove_tracker_assignment', 'Tracker remove assignment'),
    ('add_tracker_possession', 'Tracker Possession Add'),
    ('remove_tracker_possession', 'Tracker Possession Remove')
)

TRACKER_OWNER = (
    ('lost_dot', 'Lost Dot'),
    ('rider_owned', 'Rider Owned'),
    ('third_party', 'Third Party')
)

TRACKER_EVENT_CATEGORIES = (
    ('tested_OK', 'Tested OK'),
    ('tested_broken', 'Tested Broken'),
    ('add_tracker_assignment', 'Tracker add assignment'),
    ('remove_tracker_assignment', 'Tracker remove assignment'),
    ('add_tracker_possession', 'Tracker add possession'),
    ('remove_tracker_possession', 'Tracker remove possession'),
)


class TimeStampedModel(models.Model):
    created = DateTimeField(auto_now_add=True)
    modified = DateTimeField(auto_now=True)


class Riders(models.Model):

    first_name = CharField(max_length=50, verbose_name='First Name')
    last_name = CharField(max_length=50)
    email = CharField(max_length=50)
    cap_number = CharField(max_length=50)
    race_status = "In progress"
    category = CharField(max_length=50, choices=RIDER_CATEGORIES, null=True)
    gender = CharField(max_length=10, choices=RIDER_GENDERS, null=True)
    # todo put balance in pence
    balance = IntegerField(null=True, default=0)
    tcr_id = CharField(max_length=10, null=True)
    country_code = CharField(max_length=5, null=True)
    hire_tracker = BooleanField(null=True)
    tracker_url = CharField(null=True, max_length=200, blank=True)

    @property
    def current_tracker(self):
        return self.trackers_possessed.all().last() or None

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def url(self):
        return self.get_absolute_url()

    @property
    def all_events(self):
        return self.events.all()

    @property
    def all_notes(self):
        return self.notes.all()

    @property
    def all_notes_and_events(self):
        all_items = list(self.all_events) + list(self.all_notes)
        all_items.sort(key=lambda x: x.created, reverse=True)
        return all_items


    # todo link riders who are in pairs? or does the capnumber do that???
    # todo add checkpoints stuff!

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

    # todo: add url_edit method for riders

    def _record_tracker_rider_notes(
        self,
        tracker,
        notes,
        rider_event,
        tracker_event
    ):
        RiderNotes(
            rider=self,
            notes=notes,
            event=rider_event
        ).save()
        TrackerNotes(
            tracker=tracker,
            notes=notes,
            event=tracker_event
        ).save()

    def _record_tracker_rider_events(
        self,
        tracker,
        event_type,
        balance_change
    ):
        rider_event = RiderEvents(
            event_type=event_type,
            balance_change=balance_change,
            rider=self
        )
        rider_event.save()
        tracker_event = TrackerEvents(
            event_type=event_type,
            tracker=tracker
        )
        tracker_event.save()
        return rider_event, tracker_event

    def tracker_add_assignment(self, tracker, notes, deposit):
        if tracker.rider_assigned is not None:
            raise TrackerAlreadyAssigned()
        self.trackers_assigned.add(tracker)
        self.save()
        rider_event, tracker_event = self._record_tracker_rider_events(
            tracker,
            'add_tracker_assignment',
            deposit * -1
        )
        if notes:
            self._record_tracker_rider_notes(
                tracker,
                notes,
                rider_event,
                tracker_event
            )
        self.balance -= deposit
        self.save()

    def tracker_remove_assignment(self, tracker, notes, deposit):
        if tracker not in self.trackers_assigned.all():
            raise TrackerNotAssigned()
        self.trackers_assigned.remove(tracker)
        self.save()
        rider_event, tracker_event = self._record_tracker_rider_events(
            tracker,
            'remove_tracker_assignment',
            deposit
        )
        if notes:
            self._record_tracker_rider_notes(
                tracker,
                notes,
                rider_event,
                tracker_event
            )
        self.balance += deposit
        self.save()

    def tracker_add_possession(self, tracker, notes):
        if tracker not in self.trackers_assigned.all():
            raise TrackerNotAssigned()
        self.trackers_possessed.add(tracker)
        rider_event, tracker_event = self._record_tracker_rider_events(
            tracker,
            'add_tracker_possession',
            0
        )
        if notes:
            self._record_tracker_rider_notes(
                tracker,
                notes,
                rider_event,
                tracker_event
            )
        self.save()

    def tracker_remove_possession(self, tracker, notes):
        if tracker not in self.trackers_possessed.all():
            raise TrackerNotPossessed()
        self.trackers_possessed.remove(tracker)
        rider_event, tracker_event = self._record_tracker_rider_events(
            tracker,
            'remove_tracker_possession',
            0
        )
        if notes:
            self._record_tracker_rider_notes(
                tracker,
                notes,
                rider_event,
                tracker_event
            )
        self.save()

    class Meta:
        verbose_name_plural = 'Riders'

    def __str__(self):
        return self.full_name


class RiderEvents(TimeStampedModel):
    # user_id = Column(Integer, ForeignKey('users.id'))
    event_type = CharField(max_length=50, choices=RIDER_EVENT_CATEGORIES)
    user = "Anna Haslock"
    balance_change = FloatField(null=True)
    rider = ForeignKey(Riders,
                       on_delete=models.CASCADE,
                       related_name='events')


class RiderNotes(TimeStampedModel):
    rider = ForeignKey(Riders,
                       on_delete=models.CASCADE,
                       related_name='notes')
    user = "Anna Haslock"
    notes = TextField(null=True)
    event = ForeignKey(
        RiderEvents,
        on_delete=models.CASCADE,
        related_name='notes',
        null=True
    )


class Trackers(models.Model):

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
                                on_delete=models.CASCADE,
                                related_name='trackers_assigned',
                                null=True,
                                blank=True)
    rider_possess = ForeignKey(Riders,
                               on_delete=models.CASCADE,
                               related_name='trackers_possessed',
                               null=True,
                               blank=True)
    tcr_id = CharField(max_length=20, null=True)
    # todo add relationship to user!
    test_by = CharField(max_length=20, null=True, blank=True)
    clip = BooleanField(null=True)

    @property
    def all_events(self):
        return self.events.all()

    @property
    def all_notes(self):
        return self.notes.all()

    @property
    def assignable(self):
        return self.rider_assigned is None

    @property
    def url(self):
        return self.get_absolute_url()

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

    def record_test(self, result):
        self.working_status = 'working' if result == 'working' else 'broken'
        self.save()

    class Meta:
        verbose_name_plural = 'Trackers'

    def __str__(self):
        return str(self.id)


class TrackerEvents(TimeStampedModel):
    event_type = CharField(max_length=50,
                           choices=TRACKER_EVENT_CATEGORIES)
    user = "Rory Kemper"
    tracker = ForeignKey(Trackers,
                         on_delete=models.CASCADE,
                         related_name='events')


class TrackerNotes(TimeStampedModel):
    tracker = ForeignKey(Trackers,
                         on_delete=models.CASCADE,
                         related_name='notes')
    notes = TextField(null=True)
    user = "Rory Kemper"
    event = ForeignKey(
        TrackerEvents,
        on_delete=models.CASCADE,
        related_name='notes',
        null=True,
        blank=True
    )


class Checkpoints(models.Model):
    name = CharField(max_length=50)
    abbreviation = CharField(max_length=50)
    latitude = CharField(max_length=50)
    longitude = CharField(max_length=50)


class RiderCheckpoints(TimeStampedModel):
    rider = ForeignKey(
        Riders,
        on_delete=models.CASCADE,
        related_name='checkpoints',
    )
    checkpoint = ForeignKey(
        Riders,
        on_delete=models.CASCADE,
        related_name='riders'
    )


