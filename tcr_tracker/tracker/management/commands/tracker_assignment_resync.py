from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from tcr_tracker.tracker.models import Tracker


class Command(BaseCommand):
    help = 'Backdate Tracker Assignment for previously tested trackers'

    def handle(self, *args, **options):
        ok_test_status = (
            'visual_check_OK',
            'ping_test_OK'
        )
        all_trackers = Tracker.objects.all()
        anna = User.objects.get(first_name='Anna')
        for tracker in all_trackers:
            if tracker.test_status in ok_test_status:
                tracker.rider_assigned.tracker_remove_assignment(
                    tracker,
                    'Tracker Assignment Removed - TEST OK',
                    anna,
                    anna.first_name
                )
