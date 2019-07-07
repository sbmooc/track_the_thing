from django.conf import settings

from tcr_tracker.tracker.models import RaceStatus


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
