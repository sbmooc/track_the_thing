from datetime import datetime, tzinfo

import django
import pytz

django.setup()
from django.test import TestCase
from tcr_tracker.tracker.models import Riders, Trackers, RiderEvents, \
    TrackerEvents, TrackerNotes, RiderNotes


class TestRiders(TestCase):
    def setUp(self):
        Riders().save()
        Trackers().save()
        Trackers().save()
        self.rider_1 = Riders.objects.all().first()
        self.tracker_1 = Trackers.objects.all().first()
        self.tracker_2 = Trackers.objects.all()[1]
        self.test_datetime = datetime(2018, 1, 1)

    def tearDown(self) -> None:
        Riders.objects.all().delete()
        Trackers.objects.all().delete()
        RiderEvents.objects.all().delete()
        TrackerEvents.objects.all().delete()

    def test__record_tracker_rider_events(self):
        returned_rider_event, returned_tracker_event = self.rider_1._record_tracker_rider_events(
            self.tracker_1,
            'add_tracker_assignment',
            self.test_datetime,
            100
        )
        all_rider_events = RiderEvents.objects.all()
        all_tracker_events = TrackerEvents.objects.all()
        self.assertEqual(len(all_rider_events), 1)
        self.assertEqual(len(all_tracker_events), 1)
        self.assertEqual(all_rider_events[0].id, 1)
        self.assertEqual(all_rider_events[0].datetime, pytz.utc.localize(self.test_datetime))
        self.assertEqual(all_rider_events[0].event_type, 'add_tracker_assignment')
        self.assertEqual(all_rider_events[0].balance_change, 100)
        self.assertEqual(all_tracker_events[0].id, 1)
        self.assertEqual(all_tracker_events[0].datetime, pytz.utc.localize(self.test_datetime))
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
        self.assertEqual(rider_notes[0].id, 1)
        self.assertEqual(rider_notes[0].datetime, pytz.utc.localize(self.test_datetime))
        self.assertEqual(rider_notes[0].notes, 'TEST NOTES')
        self.assertEqual(rider_notes[0].event, returned_rider_event)
        self.assertEqual(tracker_notes[0].id, 1)
        self.assertEqual(tracker_notes[0].datetime, pytz.utc.localize(self.test_datetime))
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
        self.rider_1.tracker_add_assignment(self.tracker_1)
        self.rider_1.tracker_add_assignment(self.tracker_2)
        rider_from_db = Riders.objects.get(id=1)
        trackers = rider_from_db.assigned_trackers.all()
        self.assertEqual(
            len(trackers), 2
        )
        self.assertEqual(
            trackers[0], self.tracker_1
        )
        self.assertEqual(
            trackers[1], self.tracker_2
        )

    def test_remove_tracker_assignment(self):
        self.rider_1.tracker_add_assignment(self.tracker_1)
        self.rider_1.save()
        rider_from_db = Riders.objects.get(id=1)
        trackers = rider_from_db.assigned_trackers.all()
        self.assertEqual(
            trackers[0], self.tracker_1
        )
        self.rider_1.assign_tracker_remove(self.tracker_1)
        self.rider_1.save()
        rider_from_db = Riders.objects.get(id=1)
        trackers = rider_from_db.assigned_trackers.all()
        self.assertEqual(
            len(trackers), 0
        )


