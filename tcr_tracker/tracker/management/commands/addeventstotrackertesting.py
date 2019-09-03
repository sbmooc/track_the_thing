from django.core.management.base import BaseCommand
from tcr_tracker.tracker.models import Tracker, Profile, Event
from datetime import datetime


class Command(BaseCommand):
    help = 'Backdate Events for previously tested trackers'

    def handle(self, *args, **options):
        all_trackers = Tracker.objects.all()
        anna = Profile.objects.get(user__first_name='Anna')
        sat_31_aug = datetime(2019, 8, 31, 9)
        for tracker in all_trackers:
            if tracker.test_status != 'to_be_tested':
                Event.objects.create(
                    event_type=tracker.test_status,
                    tracker=tracker,
                    user=anna,
                    created=sat_31_aug
                )
