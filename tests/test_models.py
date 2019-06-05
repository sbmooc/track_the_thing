import django
django.setup()
from django.test import TestCase
from tcr_tracker.tracker.models import Riders, Trackers


class TestRiders(TestCase):
    def setUp(self):
        # todo add in logging here
        Riders(balance=1).save()
        Trackers().save()
        Trackers().save()
        self.rider_1 = Riders.objects.get(id=1)
        self.tracker_1 = Trackers.objects.get(id=1)
        self.tracker_2 = Trackers.objects.get(id=2)

    def test_add_tracker_assignment(self):
        self.rider_1.tracker_add_assignment(self.tracker_1)
        self.rider_1.save()
        rider_from_db = Riders.objects.get(id=1)
        trackers = rider_from_db.assigned_trackers.all()
        self.assertEqual(
            len(trackers), 1
        )
        self.assertEqual(
            trackers[0], self.tracker_1
        )

    def test_add_multiple_tracker_assignment(self):
        self.rider_1.tracker_add_assignment(self.tracker_1)
        self.rider_1.tracker_add_assignment(self.tracker_2)
        self.rider_1.save()
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


