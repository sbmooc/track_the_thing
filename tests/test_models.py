from datetime import datetime

import django

from tcr_tracker.tracker.errors import TrackerAlreadyAssigned

django.setup()
from django.test import TestCase
from tcr_tracker.tracker.models import (
    Riders,
    Trackers,
    RiderEvents,
    TrackerEvents,
    TrackerNotes,
    RiderNotes
)


class TestRiders(TestCase):
    def setUp(self):
        Riders().save()
        Riders().save()
        Trackers().save()
        Trackers().save()
        self.rider_1 = Riders.objects.all()[0]
        self.rider_2 = Riders.objects.all()[1]
        self.tracker_1 = Trackers.objects.all().first()
        self.tracker_2 = Trackers.objects.all()[1]
        self.test_datetime = datetime(2018, 1, 1)

    def tearDown(self) -> None:
        Riders.objects.all().delete()
        Trackers.objects.all().delete()
        RiderEvents.objects.all().delete()
        TrackerEvents.objects.all().delete()

    def test__record_tracker_rider_events(self):
        returned_rider_event, returned_tracker_event = (
            self.rider_1._record_tracker_rider_events(
                    self.tracker_1,
                    'add_tracker_assignment',
                    self.test_datetime,
                    100
                )
            )
        all_rider_events = RiderEvents.objects.all()
        all_tracker_events = TrackerEvents.objects.all()
        self.assertEqual(len(all_rider_events), 1)
        self.assertEqual(len(all_tracker_events), 1)
        self.assertEqual(all_rider_events[0].event_type, 'add_tracker_assignment')
        self.assertEqual(all_rider_events[0].balance_change, 100)
        self.assertEqual(all_tracker_events[0].event_type, 'add_tracker_assignment')
        self.assertEqual(
            returned_rider_event, all_rider_events[0]
        )
        self.assertEqual(
            returned_tracker_event, all_tracker_events[0]
        )

    def test__add_rider_and_tracker_notes(self):
        returned_rider_event, returned_tracker_event = \
            self.rider_1._record_tracker_rider_events(
                self.tracker_1,
                'add_tracker_assignment',
                self.test_datetime,
                100
        )
        self.rider_1._record_tracker_rider_notes(
            self.tracker_1,
            self.test_datetime,
            'TEST NOTES',
            returned_rider_event,
            returned_tracker_event
        )
        rider_notes = RiderNotes.objects.all()
        tracker_notes = TrackerNotes.objects.all()
        self.assertEqual(len(rider_notes), 1)
        self.assertEqual(len(tracker_notes), 1)
        self.assertEqual(rider_notes[0].notes, 'TEST NOTES')
        self.assertEqual(rider_notes[0].event, returned_rider_event)
        self.assertEqual(tracker_notes[0].notes, 'TEST NOTES')
        self.assertEqual(tracker_notes[0].event, returned_tracker_event)

    def test_add_tracker_assignment(self):
        self.rider_1.tracker_add_assignment(
            self.tracker_1,
            None,
            self.test_datetime,
            100
        )
        rider_from_db = Riders.objects.all()[0]
        assigned_trackers = rider_from_db.assigned_trackers.all()
        self.assertEqual(
            len(assigned_trackers), 1
        )
        self.assertEqual(
            assigned_trackers[0], self.tracker_1
        )
        self.assertEqual(
            rider_from_db.balance, -100
        )

    def test_add_multiple_tracker_assignment(self):
        self.rider_1.tracker_add_assignment(
            self.tracker_1,
            None,
            self.test_datetime,
            100
        )
        self.rider_1.tracker_add_assignment(
            self.tracker_2,
            None,
            self.test_datetime,
            100
        )
        rider_from_db = Riders.objects.get(id=1)
        trackers = rider_from_db.assigned_trackers.all()
        self.assertEqual(
            len(trackers), 2
        )
        self.assertEqual(
            rider_from_db.balance, -200
        )
        self.assertEqual(
            trackers[0], self.tracker_1
        )
        self.assertEqual(
            trackers[1], self.tracker_2
        )

    def test_remove_tracker_assignment(self):
        self.rider_1.tracker_add_assignment(
            self.tracker_1,
            None,
            self.test_datetime,
            100
        )
        rider_from_db = Riders.objects.get(id=1)
        trackers = rider_from_db.assigned_trackers.all()
        self.assertEqual(
            trackers[0], self.tracker_1
        )
        self.rider_1.tracker_remove_assignment(
            self.tracker_1,
            None,
            self.test_datetime,
            100
        )
        rider_from_db.refresh_from_db()
        trackers = rider_from_db.assigned_trackers.all()
        self.assertEqual(
            len(trackers), 0
        )
        self.assertEqual(
            rider_from_db.balance, 0
        )

    def test_same_tracker_cant_be_assigned_to_more_than_one_rider(self):
        self.rider_1.tracker_add_assignment(
            self.tracker_1,
            None,
            100
        )

        with self.assertRaises(TrackerAlreadyAssigned):
            self.rider_2.tracker_add_assignment(
                self.tracker_1,
                None,
                100
            )


class TestTrackers(TestCase):

    def setUp(self):
        Trackers().save()
        Riders().save()
        self.tracker = Trackers.objects.all()[0]
        self.rider = Riders.objects.all()[0]

    def tearDown(self):
        Trackers.objects.all().delete()
        Riders.objects.all().delete()

    def test_is_assignable_not_assignable(self):
        self.assertTrue(self.tracker.assignable)

    def test_is_assignable_assignable(self):
        self.tracker.rider_assigned = self.rider
        self.assertFalse(self.tracker.assignable)

