from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from .models import Competition
from .services import get_current_competition


def make_competition(**overrides):
    now = timezone.now()
    defaults = {
        "name": "Test Cup",
        "start_time": now - timedelta(hours=1),
        "end_time": now + timedelta(days=1),
        "is_published": True,
    }
    defaults.update(overrides)
    return Competition.objects.create(**defaults)


class CompetitionStatusTests(TestCase):
    def test_status_before_start_is_upcoming(self):
        now = timezone.now()
        competition = make_competition(start_time=now + timedelta(days=1), end_time=now + timedelta(days=2))
        self.assertEqual(competition.status(), "upcoming")
        self.assertFalse(competition.accepts_submissions())

    def test_status_within_window_is_live(self):
        competition = make_competition()
        self.assertEqual(competition.status(), "live")
        self.assertTrue(competition.accepts_submissions())

    def test_status_after_end_is_ended(self):
        now = timezone.now()
        competition = make_competition(start_time=now - timedelta(days=2), end_time=now - timedelta(hours=1))
        self.assertEqual(competition.status(), "ended")
        self.assertFalse(competition.accepts_submissions())

    def test_end_boundary_is_exclusive(self):
        """Submissions must stop the instant end_time is reached, not one second after."""
        now = timezone.now()
        competition = make_competition(start_time=now - timedelta(hours=1), end_time=now)
        self.assertEqual(competition.status(now), "ended")


class GetCurrentCompetitionTests(TestCase):
    def test_prefers_live_over_upcoming(self):
        now = timezone.now()
        make_competition(name="Upcoming", start_time=now + timedelta(days=5), end_time=now + timedelta(days=6))
        live = make_competition(name="Live")
        self.assertEqual(get_current_competition(), live)

    def test_falls_back_to_soonest_upcoming(self):
        now = timezone.now()
        soon = make_competition(name="Soon", start_time=now + timedelta(days=1), end_time=now + timedelta(days=2))
        make_competition(name="Later", start_time=now + timedelta(days=10), end_time=now + timedelta(days=11))
        self.assertEqual(get_current_competition(), soon)

    def test_unpublished_competitions_are_ignored(self):
        make_competition(name="Draft", is_published=False)
        self.assertIsNone(get_current_competition())
