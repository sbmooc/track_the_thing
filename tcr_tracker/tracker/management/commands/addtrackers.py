import csv
from datetime import datetime

from django.core.management.base import BaseCommand, CommandError
from tcr_tracker.tracker.models import Riders, Trackers

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
                row['last_test_date'] = datetime.strptime(row['last_test_date'].strip(), '%d/%m/%y')
                row['purchase_date'] = datetime.strptime(row['purchase_date'].strip(), '%d/%m/%Y')
                row['warranty_expiry'] = datetime.strptime(row['warranty_expiry'].strip(), '%d/%m/%Y')
                row['clip'] = row['clip'] == 'Y'
                tracker = Trackers(**row)
                try:
                    tracker.save()
                    count += 1
                except:
                    print('tracker_did_not_import')

        print(str(count) + ' trackers successfully imported')

