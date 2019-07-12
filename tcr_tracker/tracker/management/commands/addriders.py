import csv

from django.core.management.base import BaseCommand, CommandError
from tcr_tracker.tracker.models import Riders

class Command(BaseCommand):
    help = 'Add riders to application'

    def add_arguments(self, parser):
        parser.add_argument('rider_csv')

    def handle(self, *args, **options):

        rider_csv = options['rider_csv']

        if not rider_csv:
            print('No csv!')
            return
        count = 0
        with open(rider_csv, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                row['hire_tracker'] = True if row['hire_tracker'] == 'Hire TCR' else False
                # row['balance'] = int(row['balance'])
                row.pop('balance')
                rider = Riders(**row)
                try:
                    rider.save()
                    count += 1
                except:
                    print(
                        row['tcr_id'], row['first_name'], row['last_name'] + ' did not import')

        print(str(count) + ' riders successfully imported')

