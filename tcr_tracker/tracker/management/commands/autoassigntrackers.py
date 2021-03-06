from django.core.management.base import BaseCommand
from tcr_tracker.tracker.models import Tracker, Rider


class Command(BaseCommand):
    help = 'Auto assign trackers to riders'

    def handle(self, *args, **options):
        count = 0
        all_riders_without_trackers = Rider.objects.filter(
            trackers_assigned=None,
            payment__isnull=False,
            race='TPR'
        )
        print(str(all_riders_without_trackers.count()) + ' without assigned trackers')
        assignable_trackers = Tracker.objects.filter(
            test_status='ping_test_OK',
            rider_assigned=None,
            active_tracker=True
        )
        print(len(assignable_trackers))

        for rider, tracker in list(zip(all_riders_without_trackers, assignable_trackers)):
            print(rider, tracker)
            # try:
            #     rider.tracker_add_assignment(
            #         tracker,
            #         'Bulk Assignment',
            #         None,
            #         'management_command'
            #     )
            #     count += 1
            # except Exception as e:
            #     print(e)
            #     print(f'unable to attach {rider} to {tracker} tracker_did_not_import')

        print(f'Assigned {count} riders to trackers')
        print(f"There are {Rider.objects.filter(trackers_assigned=None, race='TPR').count()} riders without a tracker")

