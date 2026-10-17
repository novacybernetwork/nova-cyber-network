from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from competitions.models import Competition

from .models import Team, TeamMembership
from .services import TeamActionError, create_team, join_team_by_code, leaderboard_queryset, leave_team


def make_competition(**overrides):
    now = timezone.now()
    defaults = {
        "name": "Test Cup",
        "start_time": now - timedelta(hours=1),
        "end_time": now + timedelta(days=1),
        "is_published": True,
        "registration_open": True,
        "max_team_size": 3,
    }
    defaults.update(overrides)
    return Competition.objects.create(**defaults)


def make_approved_user(username):
    user = User.objects.create_user(username=username, password="StrongPass123!")
    user.profile.is_approved = True
    user.profile.save()
    return user


class TeamCreationAndJoiningTests(TestCase):
    def setUp(self):
        self.competition = make_competition()
        self.captain = make_approved_user("captain")
        self.member = make_approved_user("teammate")

    def test_create_team_via_view(self):
        self.client.login(username="captain", password="StrongPass123!")
        response = self.client.post(reverse("teams:team_create"), {"name": "Byte Busters", "description": "go team"})
        self.assertEqual(response.status_code, 302)
        team = Team.objects.get(name="Byte Busters")
        self.assertEqual(team.captain, self.captain)
        membership = TeamMembership.objects.get(user=self.captain, competition=self.competition)
        self.assertEqual(membership.role, TeamMembership.ROLE_CAPTAIN)

    def test_user_cannot_create_two_teams_in_same_competition(self):
        create_team(user=self.captain, competition=self.competition, name="First")
        with self.assertRaises(TeamActionError):
            create_team(user=self.captain, competition=self.competition, name="Second")

    def test_join_team_with_valid_code(self):
        team = create_team(user=self.captain, competition=self.competition, name="Byte Busters")
        joined = join_team_by_code(user=self.member, competition=self.competition, invite_code=team.invite_code)
        self.assertEqual(joined.pk, team.pk)
        self.assertEqual(team.member_count, 2)

    def test_join_with_invalid_code_raises(self):
        with self.assertRaises(TeamActionError):
            join_team_by_code(user=self.member, competition=self.competition, invite_code="NOTREAL1")

    def test_leave_team_promotes_next_member_to_captain(self):
        self.competition.start_time = timezone.now() + timedelta(days=1)
        self.competition.save()
        team = create_team(user=self.captain, competition=self.competition, name="Byte Busters")
        join_team_by_code(user=self.member, competition=self.competition, invite_code=team.invite_code)
        leave_team(user=self.captain, competition=self.competition)
        team.refresh_from_db()
        self.assertEqual(team.captain, self.member)

    def test_leave_team_deletes_team_when_last_member_leaves(self):
        self.competition.start_time = timezone.now() + timedelta(days=1)
        self.competition.save()
        team = create_team(user=self.captain, competition=self.competition, name="Solo Squad")
        leave_team(user=self.captain, competition=self.competition)
        self.assertFalse(Team.objects.filter(pk=team.pk).exists())


class TeamSizeRestrictionTests(TestCase):
    def setUp(self):
        self.competition = make_competition(max_team_size=2)
        self.captain = make_approved_user("cap")
        self.m1 = make_approved_user("m1")
        self.m2 = make_approved_user("m2")

    def test_join_blocked_once_team_is_full(self):
        team = create_team(user=self.captain, competition=self.competition, name="Tiny Team")
        join_team_by_code(user=self.m1, competition=self.competition, invite_code=team.invite_code)
        self.assertEqual(team.member_count, 2)
        with self.assertRaises(TeamActionError):
            join_team_by_code(user=self.m2, competition=self.competition, invite_code=team.invite_code)
        self.assertEqual(team.member_count, 2)


class TeamLockAfterStartTests(TestCase):
    def setUp(self):
        self.competition = make_competition()
        self.captain = make_approved_user("captain")

    def test_leave_blocked_once_competition_is_live(self):
        create_team(user=self.captain, competition=self.competition, name="Locked In")
        self.assertTrue(self.competition.is_live())
        with self.assertRaises(TeamActionError):
            leave_team(user=self.captain, competition=self.competition)

    def test_leave_allowed_before_competition_starts(self):
        self.competition.start_time = timezone.now() + timedelta(days=1)
        self.competition.save()
        team = create_team(user=self.captain, competition=self.competition, name="Early Birds")
        leave_team(user=self.captain, competition=self.competition)
        self.assertFalse(Team.objects.filter(pk=team.pk).exists())


class LeaderboardOrderingTests(TestCase):
    def setUp(self):
        self.competition = make_competition()

    def test_higher_score_ranks_first(self):
        low = Team.objects.create(competition=self.competition, name="Low", total_points=100)
        high = Team.objects.create(competition=self.competition, name="High", total_points=300)
        ranked = list(leaderboard_queryset(self.competition))
        self.assertEqual([t.pk for t in ranked], [high.pk, low.pk])

    def test_tiebreak_favors_earlier_solve_time(self):
        from challenges.models import Challenge, ChallengeCategory, Solve

        category = ChallengeCategory.objects.create(name="Misc")
        c1 = Challenge.objects.create(
            competition=self.competition, category=category, title="C1", description="d", points=100
        )
        c1.set_flag("x")
        c1.save()
        c2 = Challenge.objects.create(
            competition=self.competition, category=category, title="C2", description="d", points=100
        )
        c2.set_flag("y")
        c2.save()

        early_team = Team.objects.create(competition=self.competition, name="Early")
        late_team = Team.objects.create(competition=self.competition, name="Late")

        now = timezone.now()
        Solve.objects.create(team=early_team, challenge=c1, points_awarded=100)
        Solve.objects.filter(team=early_team, challenge=c1).update(solved_at=now - timedelta(minutes=10))
        Solve.objects.create(team=late_team, challenge=c2, points_awarded=100)
        Solve.objects.filter(team=late_team, challenge=c2).update(solved_at=now)

        early_team.total_points = 100
        early_team.last_solve_at = now - timedelta(minutes=10)
        early_team.save()
        late_team.total_points = 100
        late_team.last_solve_at = now
        late_team.save()

        ranked = list(leaderboard_queryset(self.competition))
        self.assertEqual([t.pk for t in ranked], [early_team.pk, late_team.pk])

    def test_disqualified_teams_excluded(self):
        Team.objects.create(competition=self.competition, name="Clean", total_points=50)
        Team.objects.create(competition=self.competition, name="DQd", total_points=999, is_disqualified=True)
        ranked = list(leaderboard_queryset(self.competition))
        self.assertEqual(len(ranked), 1)
        self.assertEqual(ranked[0].name, "Clean")
