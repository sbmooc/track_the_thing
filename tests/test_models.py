from datetime import datetime

import django
# django.setup()
from django.contrib.auth.models import User

from tcr_tracker.tracker.errors import TrackerAlreadyAssigned
from django.test import TransactionTestCase
from tcr_tracker.tracker.models import (
    Riders,
    Trackers,
    Profile)


class TestRiders(TransactionTestCase):
    # def setUp(self):
    #     Riders().save()
    #     Riders().save()
    #     Trackers().save()
    #     Trackers().save()
    #     self.rider_1 = Riders.objects.all()[0]
    #     self.rider_2 = Riders.objects.all()[1]
    #     self.tracker_1 = Trackers.objects.all().first()
    #     self.tracker_2 = Trackers.objects.all()[1]
    #     self.test_datetime = datetime(2018, 1, 1)
    #     self.user = User.objects.create()
    #
    # def tearDown(self) -> None:
    #     Riders.objects.all().delete()
    #     Trackers.objects.all().delete()

    def test_add_tracker_assignment(self):
        a='a'
        self.rider_1.tracker_add_assignment(
            self.tracker_1,
            None,
            100,
            self.user.profile
        )
        rider_from_db = Riders.objects.all()[0]
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


class TestTrackers(TransactionTestCase):

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

