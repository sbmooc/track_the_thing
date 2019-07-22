import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from tcr_tracker.tracker.models import Tracker, Rider


class Command(BaseCommand):
    help = 'Add trackers to application'

    def add_arguments(self, parser):
        parser.add_argument('tracker_csv')

    def handle(self, *args, **options):

        tracker_csv = options['tracker_csv']

        count = 0
        with open(tracker_csv, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                try:
                    rider = Rider.objects.get(
                        tcr_id=row['rider_id']
                    )
                    rider_own_id = 'RIDER_OWN_' + str(count)
                    tracker = Tracker.objects.create(
                        esn_number=row['tracker_esn'],
                        owner='rider_owned',
                        working_status='Functioning',
                        tcr_id=rider_own_id
                    )
                    rider.tracker_add_assignment(
                        tracker,
                        'Assignment on import',
                        None,
                        'management_command',
                        deposit=0
                    )
                    rider.tracker_add_possession(
                        tracker,
                        'Assignment on import',
                        None,
                        'management_command',
                    )
                    rider.tracker_url = row['tracker_url']
                    rider.save()
                    count += 1
                except:
                    print(row['rider_id'] + ' tracker_did_not_import')
            print(str(count) + ' riders own trackers successfully imported')

