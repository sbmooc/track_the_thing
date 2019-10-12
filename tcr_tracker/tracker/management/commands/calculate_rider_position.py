from django.core.management.base import BaseCommand

from tcr_tracker.tracker.models import RiderControlPoint, ControlPoint


class Command(BaseCommand):
    help = 'Add positions to each rider control point'

    def add_arguments(self, parser):
        parser.add_argument('race')

    def handle(self, *args, **options):
        race = options['race']
        for cp in ControlPoint.objects.filter(race=race):
            rider_control_points = RiderControlPoint.objects.filter(
                control_point=cp
            ).order_by(
                'race_time'
            )
            for idx, rcp in enumerate(rider_control_points):
                rcp.position = idx + 1
                rcp.save()


