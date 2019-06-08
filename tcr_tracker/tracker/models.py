import django
from django.db import models
from django.db.models import CharField, DateField, FloatField, TextField, \
    DateTimeField, ForeignKey

from tcr_tracker.tracker.errors import TrackerStillInPossession, \
    TrackerNotAssigned

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


class Riders(models.Model):

    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    email = CharField(max_length=50)
    cap_number = CharField(max_length=50)
    category = CharField(max_length=50, choices=RIDER_CATEGORIES)
    balance = FloatField(null=True, default=0)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    # todo link riders who are in pairs? or does the capnumber do that???
    # todo add checkpoints stuff!

    def _record_tracker_rider_notes(
        self,
        tracker,
        datetime,
        notes,
        rider_event,
        tracker_event
    ):

        RiderNotes(
            rider=self,
            datetime=datetime,
            notes=notes,
            event=rider_event
        ).save()
        TrackerNotes(
            tracker=tracker,
            datetime=datetime,
            notes=notes,
            event=tracker_event
        ).save()

    def _record_tracker_rider_events(
        self,
        tracker,
        event_type,
        datetime,
        balance_change
    ):
        rider_event = RiderEvents(
            datetime=datetime,
            event_type=event_type,
            balance_change=balance_change,
            rider=self
        )
        rider_event.save()
        tracker_event = TrackerEvents(
            datetime=datetime,
            event_type=event_type,
            tracker=tracker
        )
        tracker_event.save()
        return rider_event, tracker_event

    def tracker_add_assignment(self, tracker, notes, datetime, deposit):
        # todo add in logging here
        self.assigned_trackers.add(tracker)
        rider_event, tracker_event = self._record_tracker_rider_events(
            tracker,
            'add_tracker_assignment',
            datetime,
            deposit * -1
        )
        if notes:
            self._record_tracker_rider_notes(
                datetime,
                tracker,
                notes,
                rider_event,
                tracker_event
            )
        self.balance -= deposit
        self.save()

    def tracker_remove_assignment(self, tracker, notes, datetime, deposit):
        self.assigned_trackers.remove(tracker)
        rider_event, tracker_event = self._record_tracker_rider_events(
            tracker,
            'add',
            datetime,
            deposit * -1
        )
        if notes:
            self._record_tracker_rider_notes(
                datetime,
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
        return f'{self.id}: {self.full_name} (Cap: {self.cap_number})'

    def get_absolute_url(self):
        # todo!!!
        pass

class RiderEvents(models.Model):
    # user_id = Column(Integer, ForeignKey('users.id'))
    datetime = DateTimeField()
    event_type = CharField(max_length=50, choices=RIDER_EVENT_CATEGORIES)
    balance_change = FloatField(null=True)
    rider = ForeignKey(Riders,
                       on_delete=models.CASCADE,
                       related_name='events')


class RiderNotes(models.Model):
    rider = ForeignKey(Riders,
                       on_delete=models.CASCADE,
                       related_name='notes')
    datetime = DateTimeField(null=True)
    notes = TextField(null=True)
    event = ForeignKey(
        RiderEvents,
        on_delete=models.CASCADE,
        related_name='notes',
        null=True
    )


class Trackers(models.Model):

    esn_number = CharField(max_length=50)
    working_status = CharField(max_length=50, choices=TRACKER_WORKING_STATUS)
    loan_status = CharField(max_length=50, choices=TRACKER_LOAN_STATUS)
    last_test_date = DateField(null=True)
    purchase_date = DateField(null=True)
    warranty_expiry = DateField(null=True)
    owner = CharField(max_length=50, choices=TRACKER_OWNER)
    rider_assigned = ForeignKey(Riders,
                                on_delete=models.CASCADE,
                                related_name='assigned_trackers',
                                null=True)
    rider_possess = ForeignKey(Riders,
                               on_delete=models.CASCADE,
                               related_name='current_tracker',
                               null=True)
    #location = relationship('tracker_locations')

    def record_test(self):
        pass

    def record_lost(self):
        pass

    def record_location(self):
        pass

    class Meta:
        verbose_name_plural = 'Trackers'

class TrackerEvents(models.Model):
    # user_id = Column(Integer, ForeignKey('users.id'))
    datetime = DateTimeField()
    event_type = CharField(max_length=50,
                           choices=TRACKER_EVENT_CATEGORIES)
    tracker = ForeignKey(Trackers,
                         on_delete=models.CASCADE,
                         related_name='events')


class TrackerNotes(models.Model):
    tracker = ForeignKey(Trackers,
                         on_delete=models.CASCADE,
                         related_name='notes')
    datetime = DateTimeField()
    notes = TextField()
    # user = Column(Integer, ForeignKey('users.id'))
    event = ForeignKey(TrackerEvents,
                       on_delete=models.CASCADE,
                       related_name='notes')







# class RiderAssignment(Base):
#     rider = Column('rider', ForeignKey('riders.id'))
#     tracker = relationship('Trackers', uselist=False)
#
#
# class RiderPossession(Base):
#     rider = Column('rider', ForeignKey('riders.id'))
#     tracker = relationship('Trackers', uselist=False)
#
#
# class TrackerAssignment(Base):
#     tracker = Column('tracker', ForeignKey('trackers.id'))
#     rider = relationship('Riders', uselist=False)
#
#
# class TrackerPossession(Base):
#     tracker = Column('tracker', ForeignKey('trackers.id'))
#     rider = relationship('Riders', uselist=False)


# class TrackerLocations(models.Model):
#
#     __tablename__ = 'tracker_locations'
#     id = Column('id', Integer, primary_key=True)
#     tracker = Column('tracker_id', ForeignKey('trackers.id'), nullable=False)
#     rider = Column('rider', ForeignKey('riders.id'))
#     # location = Column('location', ForeignKey('locations.id'))


# class Locations(models.Model):
#     __tablename__ = 'locations'
#     id = Column('id', Integer, primary_key=True)
#     location = Column(String, unique=True)
#     # trackers = relationship('Trackers')


