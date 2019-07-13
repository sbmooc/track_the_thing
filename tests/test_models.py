from unittest import mock

import arrow
from django.contrib.auth.models import User

from tcr_tracker.tracker.errors import TrackerAlreadyAssigned
from django.test import TestCase
from tcr_tracker.tracker.models import (
    Rider,
    Tracker,
    RaceStatus, Deposit)
from django.db.utils import IntegrityError


class TrackerRiderTests(TestCase):

    def setUp(self):
        self.rider_1 = Rider.objects.create()
        self.rider_2 = Rider.objects.create()
        self.tracker_1 = Tracker.objects.create()
        self.tracker_2 = Tracker.objects.create()
        self.user = User.objects.create()



class TestRiders(TrackerRiderTests):

    def test_add_tracker_assignment(self):
        self.rider_1.tracker_add_assignment(
            self.tracker_1,
            None,
            100,
            self.user.profile
        )
        rider_from_db = Rider.objects.get(id=self.rider_1.id)
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
        rider_from_db = Rider.objects.get(id=self.rider_1.id)
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
        rider_from_db = Rider.objects.get(id=self.rider_1.id)
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

    def test_balance_calculation(self):
        Deposit.objects.create(
            rider=self.rider_1,
            amount_in_pence=10000
        )
        Deposit.objects.create(
            rider=self.rider_1,
            amount_in_pence=10000
        )
        Deposit.objects.create(
            rider=self.rider_1,
            amount_in_pence=-10000
        )
        self.assertEqual(self.rider_1.balance, 10000)


class TestTrackers(TrackerRiderTests):

    def test_is_assignable_not_assignable(self):
        self.tracker_1.working_status = 'Functioning'
        self.assertTrue(self.tracker_1.assignable)

    def test_is_assignable_assignable(self):
        self.tracker_1.rider_assigned = self.rider_1
        self.assertFalse(self.tracker_1.assignable)

    def test_buttons_pre_race_tracker_not_assigned(self):
        RaceStatus.objects.create(status='pre_race')

    def test_buttons_pre_race_tracker_assigned(self):
        RaceStatus.objects.create(status='pre_race')

    def test_buttons_during_race_tracker_assigned(self):
        RaceStatus.objects.create(status='pre_race')
        RaceStatus.objects.create(status='started')


class TestRaceStatus(TestCase):

    def setUp(self):
        self.mock_time = arrow.Arrow(2019, 1, 1).datetime
        self.pr = RaceStatus.objects.create(
            status='pre_race',
        )

    def test_status_is_pre_race(self):
        self.assertTrue(self.pr.pre_race)

    def test_uniqueness(self):

        with self.assertRaises(IntegrityError):
            RaceStatus.objects.create(status='pre_race')

    def test_race_seconds(self):
        started = RaceStatus.objects.create(
            status='started',
        )
        started.created = self.mock_time
        # number of seconds in ten hours, ten minutes, ten seconds = 36000 + 600 + 10 = 36610
        with mock.patch('tcr_tracker.tracker.models.arrow.now', return_value=arrow.Arrow(
                2019, 1, 1, 10, 10, 10)):
            self.assertEquals(started.race_seconds, 36610)

    def test_elapsed_string_0_days(self):
        started = RaceStatus.objects.create(
            status='started',
        )
        started.created = self.mock_time
        # number of seconds in ten hours, ten minutes, ten seconds = 36000 + 600 + 10 = 36610
        with mock.patch('tcr_tracker.tracker.models.arrow.now', return_value=arrow.Arrow(
                2019, 1, 1, 10, 10, 10)):
            self.assertEquals(started.elapsed_time_string, '0 Days 10 Hours 10 Minutes')

    def test_elapsed_string_multiple_days(self):
        started = RaceStatus.objects.create(
            status='started',
        )
        started.created = self.mock_time
        # number of seconds in ten hours, ten minutes, ten seconds = 36000 + 600 + 10 = 36610
        with mock.patch('tcr_tracker.tracker.models.arrow.now', return_value=arrow.Arrow(
                2019, 1, 4, 10, 10, 10)):
            self.assertEquals(started.elapsed_time_string, '3 Days 10 Hours 10 Minutes')

    def test_elapsed_string_over_month_boundary(self):
        started = RaceStatus.objects.create(
            status='started',
        )
        started.created = arrow.Arrow(2019, 7, 28)
        # number of seconds in ten hours, ten minutes, ten seconds = 36000 + 600 + 10 = 36610
        with mock.patch('tcr_tracker.tracker.models.arrow.now', return_value=arrow.Arrow(
                2019, 8, 1, 10, 10, 10)):
            self.assertEquals(started.elapsed_time_string, '4 Days 10 Hours 10 Minutes')
