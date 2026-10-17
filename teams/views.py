from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from competitions.services import get_current_competition
from core.models import log_action

from .forms import TeamCreateForm, TeamJoinForm, TeamManageForm
from .models import Team, TeamMembership
from .services import TeamActionError, create_team, join_team_by_code, leaderboard_queryset, leave_team


def _require_approved(request):
    profile = getattr(request.user, "profile", None)
    if not profile or not profile.is_approved:
        messages.error(request, "Your account is not yet approved to participate. Claim your invite or contact an admin.")
        return False
    return True


@login_required
def team_list(request):
    competition = get_current_competition()
    teams = Team.objects.filter(competition=competition).select_related("captain") if competition else []
    return render(request, "teams/team_list.html", {"competition": competition, "teams": teams})


@login_required
def team_detail(request, slug):
    competition = get_current_competition()
    team = get_object_or_404(Team, competition=competition, slug=slug)
    members = team.memberships.select_related("user", "user__profile").all()
    return render(request, "teams/team_detail.html", {"team": team, "members": members, "competition": competition})


@login_required
def team_create(request):
    competition = get_current_competition()
    if not _require_approved(request):
        return redirect("core:dashboard")
    if not competition:
        messages.error(request, "There is no active competition to register for.")
        return redirect("core:dashboard")

    if request.method == "POST":
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            try:
                team = create_team(
                    user=request.user,
                    competition=competition,
                    name=form.cleaned_data["name"],
                    description=form.cleaned_data["description"],
                )
            except TeamActionError as exc:
                form.add_error(None, str(exc))
            else:
                log_action(request.user, "team.create", target=team)
                messages.success(request, f"Team '{team.name}' created! Share invite code {team.invite_code} with teammates.")
                return redirect("teams:team_detail", slug=team.slug)
    else:
        form = TeamCreateForm()
    return render(request, "teams/team_create.html", {"form": form, "competition": competition})


@login_required
def team_join(request):
    competition = get_current_competition()
    if not _require_approved(request):
        return redirect("core:dashboard")
    if not competition:
        messages.error(request, "There is no active competition to register for.")
        return redirect("core:dashboard")

    if request.method == "POST":
        form = TeamJoinForm(request.POST)
        if form.is_valid():
            try:
                team = join_team_by_code(
                    user=request.user, competition=competition, invite_code=form.cleaned_data["invite_code"]
                )
            except TeamActionError as exc:
                form.add_error(None, str(exc))
            else:
                log_action(request.user, "team.join", target=team)
                messages.success(request, f"You joined {team.name}!")
                return redirect("teams:team_detail", slug=team.slug)
    else:
        form = TeamJoinForm()
    return render(request, "teams/team_join.html", {"form": form, "competition": competition})


@login_required
def team_leave(request):
    competition = get_current_competition()
    if request.method == "POST" and competition:
        try:
            leave_team(user=request.user, competition=competition)
        except TeamActionError as exc:
            messages.error(request, str(exc))
        else:
            log_action(request.user, "team.leave")
            messages.success(request, "You left your team.")
    return redirect("core:dashboard")


@login_required
def team_manage(request):
    competition = get_current_competition()
    membership = TeamMembership.objects.filter(user=request.user, competition=competition).select_related("team").first() if competition else None
    if not membership or membership.team.captain_id != request.user.id:
        messages.error(request, "Only the team captain can manage the team.")
        return redirect("core:dashboard")

    team = membership.team
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "update":
            form = TeamManageForm(request.POST, instance=team)
            if form.is_valid():
                form.save()
                messages.success(request, "Team description updated.")
                return redirect("teams:team_manage")
        elif action == "regenerate_code":
            if competition.team_changes_locked():
                messages.error(request, "Invite codes are locked once the competition starts.")
            else:
                old = team.regenerate_invite_code(created_by=request.user)
                log_action(request.user, "team.regenerate_invite", target=team, metadata={"old_code": old})
                messages.success(request, f"New invite code: {team.invite_code}")
            return redirect("teams:team_manage")
        elif action == "remove_member":
            if competition.team_changes_locked():
                messages.error(request, "Membership is locked once the competition starts. Contact an admin.")
                return redirect("teams:team_manage")
            member_id = request.POST.get("membership_id")
            target = team.memberships.exclude(user=request.user).filter(pk=member_id).first()
            if target:
                log_action(request.user, "team.remove_member", target=target.user)
                target.delete()
                messages.success(request, "Member removed.")
            return redirect("teams:team_manage")
    else:
        form = TeamManageForm(instance=team)

    return render(request, "teams/team_manage.html", {"team": team, "form": form, "competition": competition})


def leaderboard(request):
    from challenges.models import Solve

    competition = get_current_competition()
    teams = leaderboard_queryset(competition) if competition else []
    is_frozen = bool(competition and competition.scoreboard_frozen_at and timezone.now() >= competition.scoreboard_frozen_at)

    activity = []
    if competition:
        cutoff = competition.leaderboard_cutoff()
        activity = (
            Solve.objects.filter(challenge__competition=competition, solved_at__lte=cutoff)
            .select_related("team", "challenge")
            .order_by("-solved_at")[:15]
        )

    return render(
        request,
        "teams/leaderboard.html",
        {"competition": competition, "teams": teams, "is_frozen": is_frozen, "activity": activity},
    )


def leaderboard_rows(request):
    competition = get_current_competition()
    teams = leaderboard_queryset(competition) if competition else []
    return render(request, "teams/_leaderboard_rows.html", {"teams": teams})
