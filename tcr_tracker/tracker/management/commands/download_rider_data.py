import csv

from arrow import arrow
from django.core.exceptions import MultipleObjectsReturned
from django.core.management.base import BaseCommand

from tcr_tracker.tracker.models import Rider


class Command(BaseCommand):
    help = 'Download all rider data'

    def _get_cp_attribute(self, rider, cp, attribute):
        try:
            cp = rider.controlpoints.get(control_point__abbreviation=cp)
            return getattr(cp, attribute)
        except MultipleObjectsReturned:
            return '***MultipleControlPointsForRider***'
        except:
            return 'N/A'

    def handle(self, *args, **options):
        datetime = arrow.Arrow.now().format("DD-MM-YY")
        with open('rider_results_' + datetime + '.csv', 'w', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([
                'Rider TCR ID',
                'Rider Cap Number',
                'Rider Full Name',
                'Rider Status',
                'CP1',
                'CP1_string',
                'CP1_position',
                'CP2',
                'CP2_string',
                'CP2_position',
                'CP3',
                'CP3_string',
                'CP3_position',
                # 'CP4',
                # 'CP4_string',
                # 'CP4_position',
                'Finish',
                'Finish_string',
                'Finish_position'
                ]
            )
            for rider in Rider.objects.filter(race='TPR'):
                    writer.writerow(
                        [
                            rider.tcr_id,
                            rider.cap_number,
                            rider.full_name,
                            rider.status,
                            str(self._get_cp_attribute(rider, 'CP1', 'race_time')),
                            str(self._get_cp_attribute(rider, 'CP1', 'race_time_string')),
                            str(self._get_cp_attribute(rider, 'CP1', 'position')),
                            str(self._get_cp_attribute(rider, 'CP2', 'race_time')),
                            str(self._get_cp_attribute(rider, 'CP2', 'race_time_string')),
                            str(self._get_cp_attribute(rider, 'CP2', 'position')),
                            str(self._get_cp_attribute(rider, 'CP3', 'race_time')),
                            str(self._get_cp_attribute(rider, 'CP3', 'race_time_string')),
                            str(self._get_cp_attribute(rider, 'CP3', 'position')),
                            # str(self._get_cp_attribute(rider, 'CP4', 'race_time')),
                            # str(self._get_cp_attribute(rider, 'CP4', 'race_time_string')),
                            # str(self._get_cp_attribute(rider, 'CP4', 'position')),
                            str(self._get_cp_attribute(rider, 'Finish', 'race_time')),
                            str(self._get_cp_attribute(rider, 'Finish', 'race_time_string')),
                            str(self._get_cp_attribute(rider, 'Finish', 'position'))
                        ]
                    )
