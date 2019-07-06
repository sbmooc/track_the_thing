from tcr_tracker.tracker.models import RaceStatus


class RaceStatusMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pre_race'] = RaceStatus.objects.last().pre_race
        context['race_seconds'] = None
        context['elapsed_time_string'] = None
        return context
