from django.utils import timezone

from .models import Competition


def get_current_competition():
    """
    Pick the competition most relevant right now: the live one if any,
    otherwise the soonest upcoming one, otherwise the most recently ended one.
    """
    now = timezone.now()
    qs = Competition.objects.filter(is_published=True)

    live = qs.filter(start_time__lte=now, end_time__gte=now).order_by("start_time").first()
    if live:
        return live

    upcoming = qs.filter(start_time__gt=now).order_by("start_time").first()
    if upcoming:
        return upcoming

    return qs.order_by("-end_time").first()
