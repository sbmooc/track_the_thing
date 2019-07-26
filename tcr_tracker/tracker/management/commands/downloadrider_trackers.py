import csv

from arrow import arrow
from django.core.management.base import BaseCommand
from tcr_tracker.tracker.models import Rider, Tracker


class Command(BaseCommand):
    help = 'Download all rider trackers'

    def handle(self, *args, **options):

        datetime = arrow.Arrow.now().format("DD-MM-YY")
        with open('rider_tracker_download_'+datetime, 'w', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                'Tracker TCR ID',
                'Tracker ESN Number',
                'Rider Cap Number',
                'Rider TCR_ID',
                'Rider Full Name',
                'Tracker URL (if rider\'s own tracker',
                ]
            )
            # warn if riders have multiple trackers or no trackers
            for rider in Rider.objects.filter(status='active'):
                if len(rider.trackers_assigned.all()) != 1:
                    print(f'Rider {rider.cap_number} {rider.full_name} has '
                          f'{len(rider.trackers_assigned.all())} trackers assigned!')
            for tracker in Tracker.objects.filter(
                    rider_assigned__isnull=False,
                    rider_assigned__status='active'
            ):

               if tracker.rider_possesed:
                    writer.writerow(
                        [
                            tracker.rider_possesed.tcr_id,
                            tracker.esn_number,
                        ]
                    )
