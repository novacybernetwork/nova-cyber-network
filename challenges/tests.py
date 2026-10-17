import threading
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import close_old_connections
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.utils import timezone

from competitions.models import Competition
from teams.models import Team, TeamMembership

from .models import Challenge, ChallengeCategory, Solve, Submission
from .services import submit_flag


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


def make_challenge(competition, flag="NOVA{test_flag}", points=100, **overrides):
    category, _ = ChallengeCategory.objects.get_or_create(name=overrides.pop("category_name", "Web Security"))
    challenge = Challenge.objects.create(
        competition=competition,
        category=category,
        title=overrides.pop("title", "Sample"),
        description="desc",
        points=points,
        is_published=True,
        **overrides,
    )
    challenge.set_flag(flag)
    challenge.save()
    return challenge


def make_team_with_user(competition, username, team_name):
    user = User.objects.create_user(username=username, password="StrongPass123!")
    user.profile.is_approved = True
    user.profile.save()
    team = Team.objects.create(competition=competition, name=team_name, captain=user)
    TeamMembership.objects.create(team=team, user=user, competition=competition, role=TeamMembership.ROLE_CAPTAIN)
    return user, team


class FlagSubmissionTests(TestCase):
    def setUp(self):
        self.competition = make_competition()
        self.challenge = make_challenge(self.competition, flag="NOVA{correct_flag}", points=150)
        self.user, self.team = make_team_with_user(self.competition, "solver", "Solvers")

    def test_correct_flag_awards_points(self):
        result = submit_flag(team=self.team, user=self.user, challenge=self.challenge, submitted_text="NOVA{correct_flag}")
        self.assertTrue(result.correct)
        self.assertFalse(result.already_solved)
        self.team.refresh_from_db()
        self.assertEqual(self.team.total_points, 150)
        self.assertEqual(Solve.objects.filter(team=self.team, challenge=self.challenge).count(), 1)

    def test_incorrect_flag_rejected(self):
        result = submit_flag(team=self.team, user=self.user, challenge=self.challenge, submitted_text="NOVA{nope}")
        self.assertFalse(result.correct)
        self.team.refresh_from_db()
        self.assertEqual(self.team.total_points, 0)
        self.assertFalse(Solve.objects.filter(team=self.team, challenge=self.challenge).exists())

    def test_duplicate_correct_submission_does_not_award_twice(self):
        submit_flag(team=self.team, user=self.user, challenge=self.challenge, submitted_text="NOVA{correct_flag}")
        result = submit_flag(team=self.team, user=self.user, challenge=self.challenge, submitted_text="NOVA{correct_flag}")
        self.assertTrue(result.already_solved)
        self.team.refresh_from_db()
        self.assertEqual(self.team.total_points, 150)
        self.assertEqual(Solve.objects.filter(team=self.team, challenge=self.challenge).count(), 1)

    def test_teammate_cannot_score_again_after_teammate_solved(self):
        teammate = User.objects.create_user(username="teammate", password="StrongPass123!")
        TeamMembership.objects.create(team=self.team, user=teammate, competition=self.competition)
        submit_flag(team=self.team, user=self.user, challenge=self.challenge, submitted_text="NOVA{correct_flag}")
        result = submit_flag(team=self.team, user=teammate, challenge=self.challenge, submitted_text="NOVA{correct_flag}")
        self.assertTrue(result.already_solved)
        self.team.refresh_from_db()
        self.assertEqual(self.team.total_points, 150)

    def test_flag_is_case_sensitive_by_default(self):
        result = submit_flag(team=self.team, user=self.user, challenge=self.challenge, submitted_text="nova{correct_flag}")
        self.assertFalse(result.correct)

    def test_submission_is_logged_for_both_correct_and_incorrect(self):
        submit_flag(team=self.team, user=self.user, challenge=self.challenge, submitted_text="NOVA{nope}")
        submit_flag(team=self.team, user=self.user, challenge=self.challenge, submitted_text="NOVA{correct_flag}")
        self.assertEqual(Submission.objects.filter(team=self.team, challenge=self.challenge).count(), 2)

    def test_plaintext_flag_never_stored_on_model(self):
        self.assertNotIn("correct_flag", self.challenge.flag_hash)


class ConcurrentSubmissionTests(TransactionTestCase):
    """Two teammates racing to submit the same correct flag must only score once."""

    def setUp(self):
        self.competition = make_competition()
        self.challenge = make_challenge(self.competition, flag="NOVA{race_me}", points=200)
        self.user_a, self.team = make_team_with_user(self.competition, "racer_a", "Racers")
        self.user_b = User.objects.create_user(username="racer_b", password="StrongPass123!")
        TeamMembership.objects.create(team=self.team, user=self.user_b, competition=self.competition)

    def test_concurrent_correct_submissions_award_points_once(self):
        # SQLite only allows one writer at a time, so a losing thread here may surface as a raw
        # "database is locked" OperationalError rather than the graceful already_solved path our
        # IntegrityError handling produces on a real MVCC database like the Postgres used in
        # production. Either outcome is an acceptable way to "lose the race" for this test: what
        # must hold regardless is the invariant that matters — exactly one Solve, points awarded
        # exactly once.
        from django.db.utils import OperationalError

        results = []
        errors = []

        def attempt(user):
            close_old_connections()
            try:
                res = submit_flag(team=self.team, user=user, challenge=self.challenge, submitted_text="NOVA{race_me}")
                results.append(res)
            except OperationalError as exc:
                errors.append(exc)

        t1 = threading.Thread(target=attempt, args=(self.user_a,))
        t2 = threading.Thread(target=attempt, args=(self.user_b,))
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        self.assertEqual(len(results) + len(errors), 2)
        self.assertEqual(Solve.objects.filter(team=self.team, challenge=self.challenge).count(), 1)
        self.team.refresh_from_db()
        self.assertEqual(self.team.total_points, 200)
        self.assertEqual(sum(1 for r in results if r.correct and not r.already_solved), 1)


class ContestTimingRestrictionTests(TestCase):
    def setUp(self):
        self.now = timezone.now()

    def test_challenges_hidden_before_competition_starts(self):
        competition = make_competition(
            start_time=self.now + timedelta(days=1), end_time=self.now + timedelta(days=2)
        )
        challenge = make_challenge(competition)
        self.assertFalse(challenge.is_visible(competition))

        user, _team = make_team_with_user(competition, "early", "Early Team")
        self.client.login(username="early", password="StrongPass123!")
        response = self.client.get(reverse("challenges:challenge_list"))
        self.assertContains(response, "locked")

    def test_submissions_rejected_after_competition_ends(self):
        competition = make_competition(
            start_time=self.now - timedelta(days=2), end_time=self.now - timedelta(hours=1)
        )
        self.assertFalse(competition.accepts_submissions())

    def test_submissions_accepted_while_live(self):
        competition = make_competition()
        self.assertTrue(competition.accepts_submissions())

    def test_submissions_paused_overrides_live_window(self):
        competition = make_competition(submissions_paused=True)
        self.assertFalse(competition.accepts_submissions())

    def test_challenge_detail_blocks_submission_when_not_live(self):
        competition = make_competition(
            start_time=self.now + timedelta(days=1), end_time=self.now + timedelta(days=2)
        )
        challenge = make_challenge(competition)
        user, team = make_team_with_user(competition, "waiter", "Waiting Room")
        self.client.login(username="waiter", password="StrongPass123!")
        response = self.client.get(reverse("challenges:challenge_list"))
        self.assertEqual(response.status_code, 200)
        detail_response = self.client.get(reverse("challenges:challenge_detail", args=[challenge.slug]))
        self.assertEqual(detail_response.status_code, 302)
