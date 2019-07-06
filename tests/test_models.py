from django.contrib.auth.models import User

from tcr_tracker.tracker.errors import TrackerAlreadyAssigned
from django.test import TestCase
from tcr_tracker.tracker.models import (
    Riders,
    Trackers,
)


class TestRiders(TestCase):
    def setUp(self):
        self.rider_1 = Riders.objects.create()
        self.rider_2 = Riders.objects.create()
        self.tracker_1 = Trackers.objects.create()
        self.tracker_2 = Trackers.objects.create()
        self.user = User.objects.create()

    def test_add_tracker_assignment(self):
        self.rider_1.tracker_add_assignment(
            self.tracker_1,
            None,
            100,
            self.user.profile
        )
        rider_from_db = Riders.objects.get(id=self.rider_1.id)
        assigned_trackers = rider_from_db.trackers_assigned.all()
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
            100,
            self.user.profile
        )
        self.rider_1.tracker_add_assignment(
            self.tracker_2,
            None,
            100,
            self.user.profile
        )
        rider_from_db = Riders.objects.get(id=self.rider_1.id)
        trackers = rider_from_db.trackers_assigned.all()
        self.assertEqual(
            len(trackers), 2
        )
        self.assertEqual(
            rider_from_db.balance, -200
        )
        self.assertCountEqual(
            trackers, [self.tracker_1, self.tracker_2]
        )

    def test_remove_tracker_assignment(self):
        self.rider_1.tracker_add_assignment(
            self.tracker_1,
            None,
            100,
            self.user.profile
        )
        rider_from_db = Riders.objects.get(id=self.rider_1.id)
        trackers = rider_from_db.trackers_assigned.all()
        self.assertEqual(
            trackers[0], self.tracker_1
        )
        self.rider_1.tracker_remove_assignment(
            self.tracker_1,
            None,
            100,
            self.user.profile
        )
        rider_from_db.refresh_from_db()
        trackers = rider_from_db.trackers_assigned.all()
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
            100,
            self.user.profile
        )

        with self.assertRaises(TrackerAlreadyAssigned):
            self.rider_2.tracker_add_assignment(
                self.tracker_1,
                None,
                100,
                self.user.profile
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

