from django_ratelimit.decorators import ratelimit
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from competitions.services import get_current_competition
from core.models import log_action
from teams.models import TeamMembership

from .forms import FlagSubmitForm
from .models import Challenge, ChallengeCategory, Solve
from .services import submit_flag


def _team_for(request, competition):
    if not competition:
        return None
    membership = TeamMembership.objects.filter(user=request.user, competition=competition).select_related("team").first()
    return membership.team if membership else None


@login_required
def challenge_list(request):
    competition = get_current_competition()
    categories = ChallengeCategory.objects.all()

    if not competition or competition.status() == "upcoming":
        return render(
            request,
            "challenges/challenge_list.html",
            {"competition": competition, "locked": True, "categories": categories, "challenges_by_category": []},
        )

    team = _team_for(request, competition)
    solved_ids = set(Solve.objects.filter(team=team).values_list("challenge_id", flat=True)) if team else set()

    qs = Challenge.objects.filter(competition=competition, is_published=True, is_archived=False).annotate(
        total_solves=Count("solves")
    ).select_related("category")

    category_slug = request.GET.get("category")
    difficulty = request.GET.get("difficulty")
    if category_slug:
        qs = qs.filter(category__slug=category_slug)
    if difficulty:
        qs = qs.filter(difficulty=difficulty)

    challenges_by_category = []
    for category in categories:
        cat_challenges = [c for c in qs if c.category_id == category.id]
        if cat_challenges:
            challenges_by_category.append((category, cat_challenges))

    return render(
        request,
        "challenges/challenge_list.html",
        {
            "competition": competition,
            "locked": False,
            "categories": categories,
            "challenges_by_category": challenges_by_category,
            "solved_ids": solved_ids,
            "selected_category": category_slug,
            "selected_difficulty": difficulty,
        },
    )


@login_required
def challenge_detail(request, slug):
    competition = get_current_competition()
    challenge = get_object_or_404(Challenge, competition=competition, slug=slug)

    if not challenge.is_visible(competition):
        messages.error(request, "That challenge isn't available right now.")
        return redirect("challenges:challenge_list")

    team = _team_for(request, competition)
    is_solved = bool(team and Solve.objects.filter(team=team, challenge=challenge).exists())
    form = FlagSubmitForm()

    return render(
        request,
        "challenges/challenge_detail.html",
        {
            "competition": competition,
            "challenge": challenge,
            "team": team,
            "is_solved": is_solved,
            "form": form,
            "can_submit": competition.accepts_submissions() and team and not is_solved,
        },
    )


@login_required
@ratelimit(key="user", rate="15/m", method="POST", block=True)
def challenge_submit(request, slug):
    competition = get_current_competition()
    challenge = get_object_or_404(Challenge, competition=competition, slug=slug)

    if not challenge.is_visible(competition):
        messages.error(request, "That challenge isn't available right now.")
        return redirect("challenges:challenge_list")

    team = _team_for(request, competition)
    result = None
    form = FlagSubmitForm(request.POST)

    if not team:
        messages.error(request, "Join a team before submitting flags.")
    elif not competition.accepts_submissions():
        messages.error(request, "Flag submissions are currently closed.")
    elif form.is_valid():
        result = submit_flag(team=team, user=request.user, challenge=challenge, submitted_text=form.cleaned_data["flag"])
        log_action(
            request.user,
            "flag.submit",
            target=challenge,
            metadata={"correct": result.correct, "already_solved": result.already_solved},
        )

    is_solved = bool(team and Solve.objects.filter(team=team, challenge=challenge).exists())

    if request.htmx:
        return render(
            request,
            "challenges/_submission_result.html",
            {
                "challenge": challenge,
                "result": result,
                "form": FlagSubmitForm(),
                "is_solved": is_solved,
                "can_submit": competition.accepts_submissions() and team and not is_solved,
            },
        )

    if result:
        if result.already_solved:
            messages.warning(request, result.message)
        elif result.correct:
            messages.success(request, result.message)
        else:
            messages.error(request, result.message)
    return redirect("challenges:challenge_detail", slug=slug)
