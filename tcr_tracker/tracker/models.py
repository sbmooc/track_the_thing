from django.db import models
from django.db.models import (
    CharField,
    DateField,
    FloatField,
    TextField,
    DateTimeField,
    ForeignKey
)
from django.urls import reverse

from tcr_tracker.tracker.errors import TrackerNotAssigned, \
    TrackerAlreadyAssigned

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
    ('male', 'Male'),
    ('female', 'Female'),
    ('pair', 'Pair')
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
    category = CharField(max_length=50, choices=RIDER_CATEGORIES)
    balance = FloatField(null=True, default=0)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def url(self):
        return self.get_absolute_url()

    # todo link riders who are in pairs? or does the capnumber do that???
    # todo add checkpoints stuff!

    def get_absolute_url(self):
        return reverse('one_rider', kwargs={'pk': self.id})

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
        self.trackers_assigned.remove(tracker)
        rider_event, tracker_event = self._record_tracker_rider_events(
            tracker,
            'add',
            deposit * -1
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

    def tracker_possession_add(self, tracker, notes, datetime):
        if tracker not in self.assigned_trackers:
            raise TrackerNotAssigned()
        self.current_tracker.add(tracker)
        event = RiderEvents(
            datetime=datetime,
            event_type='tracker_add_possession',
            rider=self
        )
        event.save()
        if notes:
            RiderNotes(
                rider=self,
                datetime=datetime,
                notes=notes,
                events=event
            ).save()
        self.save()

    def tracker_possession_remove(self, tracker, notes, datetime):
        if tracker not in self.current_tracker:
            raise

    class Meta:
        verbose_name_plural = 'Riders'

    def __str__(self):
        return self.full_name


class RiderEvents(TimeStampedModel):
    # user_id = Column(Integer, ForeignKey('users.id'))
    event_type = CharField(max_length=50, choices=RIDER_EVENT_CATEGORIES)
    balance_change = FloatField(null=True)
    rider = ForeignKey(Riders,
                       on_delete=models.CASCADE,
                       related_name='events')


class RiderNotes(TimeStampedModel):
    rider = ForeignKey(Riders,
                       on_delete=models.CASCADE,
                       related_name='notes')
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
    loan_status = CharField(max_length=50, choices=TRACKER_LOAN_STATUS)
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
    def tracker_loan_status(self):
        return self.get_loan_status_display()

    def record_test(self, result):
        self.working_status = 'working' if result == 'working' else 'broken'
        self.save()

    def record_lost(self):
        pass

    def record_location(self):
        pass

    class Meta:
        verbose_name_plural = 'Trackers'


class TrackerEvents(TimeStampedModel):
    event_type = CharField(max_length=50,
                           choices=TRACKER_EVENT_CATEGORIES)
    tracker = ForeignKey(Trackers,
                         on_delete=models.CASCADE,
                         related_name='events')


class TrackerNotes(TimeStampedModel):
    tracker = ForeignKey(Trackers,
                         on_delete=models.CASCADE,
                         related_name='notes')
    notes = TextField()
    event = ForeignKey(TrackerEvents,
                       on_delete=models.CASCADE,
                       related_name='notes')


class Checkpoints(models.Model):
    name = CharField(max_length=50)
    abbriviation = CharField(max_length=50)
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


