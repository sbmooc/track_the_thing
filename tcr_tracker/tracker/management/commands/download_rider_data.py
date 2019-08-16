import csv

from arrow import arrow
from django.core.management.base import BaseCommand
from tcr_tracker.tracker.models import Rider, Tracker, ControlPoint


class Command(BaseCommand):
    help = 'Download all rider data'

    def _get_cp_race_time(self, rider, cp):
        try:
            return rider.controlpoints.get(control_point__abbreviation=cp).race_time
        except ControlPoint.DoesNotExist:
            return 'N/A'
        except ControlPoint.MultipleObjectsReturned:
            return '***MultipleControlPointsForRider***'

    def _get_cp_time_string(self, rider, cp):
        try:
            return rider.controlpoints.get(control_point__abbreviation=cp).race_time_string
        except:
            return 'N/A'

    def handle(self, *args, **options):

        datetime = arrow.Arrow.now().format("DD-MM-YY")
        with open('rider_data_download_'+datetime, 'w', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                'Rider TCR ID',
                'Rider Cap Number',
                'Rider Full Name',
                'Rider Status',
                'CP1_CEST',
                'CP1',
                'CP2_CEST',
                'CP2',
                'CP3_CEST',
                'CP3',
                'CP4_CEST',
                'CP4',
                'Finish_CEST'
                'Finish'
                ]
            )
            # warn if riders have multiple trackers or no trackers
            for rider in Rider.objects.all():

                    writer.writerow(
                        [
                            rider.tcr_id,
                            rider.cap_number,
                            rider.full_name,
                            rider.status,
                            str(self._get_cp_race_time(rider, 'CP1')),
                            str(self._get_cp_time_string(rider, 'CP1')),
                            str(self._get_cp_race_time(rider, 'CP2')),
                            str(self._get_cp_time_string(rider, 'CP2')),
                            str(self._get_cp_race_time(rider, 'CP3')),
                            str(self._get_cp_time_string(rider, 'CP3')),
                            str(self._get_cp_race_time(rider, 'CP4')),
                            str(self._get_cp_time_string(rider, 'CP4')),
                            str(self._get_cp_race_time(rider, 'Finish')),
                            str(self._get_cp_time_string(rider, 'Finish'))
                        ]
                    )
