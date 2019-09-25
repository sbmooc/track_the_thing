import csv

from arrow import arrow
from django.core.management.base import BaseCommand
from django.db.models import Q

from tcr_tracker.tracker.models import Rider, Tracker


class Command(BaseCommand):
    help = 'Download all rider trackers'

    def handle(self, *args, **options):

        datetime = arrow.Arrow.now().format("DD-MM-YY")
        with open('tracker_download_'+datetime, 'w', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                'Tracker TCR ID',
                'Tracker ESN Number',
                'Test Status'
                ]
            )
            for tracker in Tracker.objects.all().exclude(
                    Q(tcr_id__startswith='AOS') | Q(tcr_id__startswith='RIDER_OWN')
            ):
                writer.writerow(
                    [
                        tracker.tcr_id,
                        tracker.esn_number,
                        tracker.test_status
                    ]
                )
