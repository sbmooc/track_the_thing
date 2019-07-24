import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from tcr_tracker.tracker.models import Tracker

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
                if row['last_test_date']:
                    row['last_test_date'] = datetime.strptime(row['last_test_date'].strip(), '%d/%m/%y')
                else:
                    row['last_test_date'] = None
                row.update(
                    {
                        'warranty_expiry': None,
                        'purchase_date': None
                     }
                )
                tracker = Tracker(**row)
                try:
                    tracker.save()
                    count += 1
                except:
                    print('tracker_did_not_import')

        print(str(count) + ' trackers successfully imported')

