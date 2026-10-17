from django.db import IntegrityError, transaction
from django.db.models import Count, IntegerField, Max, Q, Sum, Value
from django.db.models.functions import Coalesce

from .models import Team, TeamInvite, TeamMembership


class TeamActionError(Exception):
    """Raised for any user-facing team operation failure."""


def create_team(*, user, competition, name, description=""):
    if not competition.registration_open:
        raise TeamActionError("Registration is closed for this competition.")
    if TeamMembership.objects.filter(user=user, competition=competition).exists():
        raise TeamActionError("You are already on a team for this competition.")

    try:
        with transaction.atomic():
            team = Team.objects.create(competition=competition, name=name, description=description, captain=user)
            TeamMembership.objects.create(team=team, user=user, competition=competition, role=TeamMembership.ROLE_CAPTAIN)
            TeamInvite.objects.create(team=team, code=team.invite_code, created_by=user)
    except IntegrityError:
        raise TeamActionError("A team with that name already exists.")
    return team


def join_team_by_code(*, user, competition, invite_code):
    if not competition.registration_open:
        raise TeamActionError("Registration is closed for this competition.")
    if TeamMembership.objects.filter(user=user, competition=competition).exists():
        raise TeamActionError("You are already on a team for this competition.")

    invite_code = (invite_code or "").strip().upper()
    try:
        with transaction.atomic():
            team = Team.objects.select_for_update().get(
                competition=competition, invite_code=invite_code, is_disqualified=False
            )
            if team.is_full():
                raise TeamActionError(f"{team.name} is full ({competition.max_team_size} members max).")
            TeamMembership.objects.create(team=team, user=user, competition=competition, role=TeamMembership.ROLE_MEMBER)
    except Team.DoesNotExist:
        raise TeamActionError("Invalid invite code.")
    except IntegrityError:
        raise TeamActionError("You are already on a team for this competition.")
    return team


def leave_team(*, user, competition):
    if competition.team_changes_locked():
        raise TeamActionError("Team changes are locked once the competition starts. Contact an administrator.")

    membership = TeamMembership.objects.filter(user=user, competition=competition).select_related("team").first()
    if not membership:
        raise TeamActionError("You are not on a team for this competition.")

    team = membership.team
    with transaction.atomic():
        membership.delete()
        if team.captain_id == user.id:
            next_member = team.memberships.order_by("joined_at").first()
            if next_member:
                team.captain = next_member.user
                next_member.role = TeamMembership.ROLE_CAPTAIN
                next_member.save(update_fields=["role"])
                team.save(update_fields=["captain"])
            else:
                team.delete()


def leaderboard_queryset(competition):
    """
    Server-side ranking computed from Solve rows (the source of truth), honoring
    a scoreboard freeze. Tie-break: equal points ranks by whoever reached that
    score first (earlier last-solve time ranks higher), matching standard CTF
    scoreboard conventions.
    """
    cutoff = competition.leaderboard_cutoff()
    solved_filter = Q(solves__solved_at__lte=cutoff)
    return (
        Team.objects.filter(competition=competition, is_disqualified=False)
        .annotate(
            score=Coalesce(Sum("solves__points_awarded", filter=solved_filter), Value(0), output_field=IntegerField()),
            solve_count=Count("solves", filter=solved_filter),
            last_solve=Max("solves__solved_at", filter=solved_filter),
        )
        .order_by("-score", "last_solve", "name")
    )
