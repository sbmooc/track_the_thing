from django.conf import settings

from tcr_tracker.tracker.models import RaceStatus, Tracker, Rider, RiderControlPoint, ControlPoint


class KeyStatsMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key_stats'] = {
            'active_riders':
                Rider.objects.filter(status='active', race='TPR').count(),
            'scratched_riders':
                Rider.objects.filter(status='scratched', race='TPR').count(),
            'starters':
                Rider.objects.filter(race='TPR').count(
                ) - Rider.objects.filter(status='dns', race='TPR').count(),
            'cp1':
                RiderControlPoint.objects.filter(
                    control_point=ControlPoint.objects.get(
                        abbreviation='CP1',
                        race='TPR'
                    )
                ).count(),
            'cp2':
                RiderControlPoint.objects.filter(
                    control_point=ControlPoint.objects.get(
                        abbreviation='CP2',
                        race='TPR'
                    )
                ).count(),
            'cp3':
                RiderControlPoint.objects.filter(
                    control_point=ControlPoint.objects.get(
                        abbreviation='CP3',
                        race='TPR'
                    )
                ).count(),
            'finish':
                RiderControlPoint.objects.filter(
                    control_point=ControlPoint.objects.get(
                        abbreviation='Finish',
                        race='TPR'
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
