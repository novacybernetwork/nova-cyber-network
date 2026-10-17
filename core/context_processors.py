from django.conf import settings
from django.utils import timezone

from competitions.services import get_current_competition


def site_context(request):
    competition = get_current_competition()
    return {
        "SITE_NAME": settings.SITE_NAME,
        "CONTACT_EMAIL": settings.CONTACT_EMAIL,
        "current_competition": competition,
        "competition_status": competition.status() if competition else None,
        "now": timezone.now(),
    }
