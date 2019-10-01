import csv

from django.core.management.base import BaseCommand
from tcr_tracker.tracker.models import Tracker, Rider


class Command(BaseCommand):
    help = 'Add trackers to application'

    def add_arguments(self, parser):
        parser.add_argument('riders_trackers_csv')

    def handle(self, *args, **options):

        csv_ = options['riders_trackers_csv']

        count = 0
        with open(csv_, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                tracker_id = row['tcr_id']
                cap_number = row['cap_number']
                try:
                    if cap_number == '':
                        continue
                    tracker = Tracker.objects.get(tcr_id=tracker_id)
                    rider = Rider.objects.get(cap_number=cap_number, race='TPR')
                    rider.tracker_add_assignment(
                        tracker,
                        'Auto_Assignment',
                        None,
                        'management_command'
                    )
                    count += 1
                except BaseException as e:
                    print(e)
                    print(f'tracker {tracker_id} not allocated due to issue')

        print(str(count) + ' trackers successfully allocated')

