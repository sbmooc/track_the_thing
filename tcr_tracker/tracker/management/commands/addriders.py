import csv

from django.core.management.base import BaseCommand, CommandError
from tcr_tracker.tracker.models import Rider, Deposit, Event


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
                row['hire_tracker'] = True if row['hire_tracker'] == 'HIRE TRACKER' else False
                balance = int(row['balance'])
                row.pop('balance')
                rider = Rider(
                    **row,
                    visible=True,
                    race='TPR'
                )
                try:
                    rider.display_order = int(rider.cap_number)
                except ValueError:
                    rider.display_order = int(rider.cap_number[:-1])
                try:
                    rider.save()
                    if balance > 0:
                        deposit = Deposit.objects.create(
                            rider=rider,
                            amount_in_pence=balance*100
                        )
                        Event.objects.create(
                            deposit_change=deposit,
                            rider=rider,
                            event_type='payment_in',
                            notes='Automatic Import'
                        )
                    count += 1
                except Exception as e:
                    print(e)
                    print(
                        row['tcr_id'], row['first_name'], row['last_name'] + ' did not import')

        print(str(count) + ' riders successfully imported')

