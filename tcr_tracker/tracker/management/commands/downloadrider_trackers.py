import csv

from arrow import arrow
from django.core.management.base import BaseCommand, CommandError
from tcr_tracker.tracker.models import Rider, Deposit, Event


class Command(BaseCommand):
    help = 'Download all rider trackers'

    def handle(self, *args, **options):

        datetime = arrow.Arrow.now().format("DD-MM-YY HH:MM")
        with open('rider_tracker_download_'+datetime, 'w', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                'Rider TCR_ID',
                'Rider Cap Number',
                'Rider Full Name',
                'Trackers assigned to rider',
                'Trackers in possession by rider',


            )
            for rider in Rider.objects.filter(status='active').order_by('display_order'):
                number_of_trackers_assigned = len(rider.trackers_assigned.all())
                if number_of_trackers_assigned > 1:
                    print(f'Rider {rider.cap_number} {rider.full_name} has more than one'
                          f'tracker assigned')
                if number_of_trackers_assigned < 1:
                    print(f'Rider {rider.cap_number} {rider.full_name} has less than one'
                          f'tracker assigned')


                writer.writerow(
                    [
                        rider.tcr_id,
                        rider.cap_number,
                        rider.full_name,
                        [
                            f'{tracker.tcr_id}: '
                            f'{tracker.esn_number}'
                            f'' for tracker in rider.trackers_assigned.all()
                        ],
                        [
                            tracker.esn_number for tracker in rider.trackers_possessed.all()
                        ],
                        [
                            tracker.tcr_id for tracker in rider.trackers_possessed.all()
                        ],
                        rider.tracker_url,
                        len(rider.trackers_possessed.all())

                    ]
                )
