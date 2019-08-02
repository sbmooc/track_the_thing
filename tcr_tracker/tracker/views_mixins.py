from django.conf import settings

from tcr_tracker.tracker.models import RaceStatus, Tracker, Rider, RiderControlPoint, ControlPoint


class KeyStatsMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key_stats'] = {
            'active_riders':
                Rider.objects.filter(status='active').count(),
            'scratched_riders':
                Rider.objects.filter(status='scratched').count(),
            'starters':
                Rider.objects.all().count() - Rider.objects.filter(status='dns').count(),
            'cp1':
                RiderControlPoint.objects.filter(
                    control_point=ControlPoint.objects.get(
                        abbreviation='CP1'
                    )
                ).count(),
            'cp2':
                RiderControlPoint.objects.filter(
                    control_point=ControlPoint.objects.get(
                        abbreviation='CP2'
                    )
                ).count(),
            'cp3':
                RiderControlPoint.objects.filter(
                    control_point=ControlPoint.objects.get(
                        abbreviation='CP3'
                    )
                ).count(),
            'cp4':
                RiderControlPoint.objects.filter(
                    control_point=ControlPoint.objects.get(
                        abbreviation='CP4'
                    )
                ).count(),
        }

        return context


class GetObjectMixin:

    def get_object(self):
        path_string = self.request.path
        model_names = {
            'trackers': Tracker,
            'riders': Rider
        }
        model, pk, _, _= path_string[1:].split('/')
        self.object = model_names[model].objects.get(id=pk)


class RaceStatusMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_race_status_object = RaceStatus.objects.last()
        context['pre_race'] = (
            False if last_race_status_object is None else
            last_race_status_object.pre_race
        )
        context['race_seconds'] = (
            None if last_race_status_object is None else last_race_status_object.race_seconds
        )
        context['elapsed_time_string'] = (
            None if last_race_status_object is None else last_race_status_object.elapsed_time_string
        )
        return context


class EnvironmentMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['environment'] = settings.ENVIRONMENT
        return context


class StaffOnlyMixin:
    pass
