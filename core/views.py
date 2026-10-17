import csv
from collections import Counter
from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.utils import timezone

from accounts.models import ApprovedMember
from challenges.models import Challenge, Submission
from competitions.services import get_current_competition
from core.models import AuditLog
from teams.models import Team, TeamMembership
from teams.services import leaderboard_queryset

SCHOOLS = [
    "John Champe High School",
    "Academies of Loudoun",
    "Lightridge High School",
    "Freedom High School",
]


def home(request):
    competition = get_current_competition()
    stats = {
        "participants": 0,
        "teams": 0,
        "challenges": 0,
        "solves": 0,
    }
    if competition:
        stats["teams"] = Team.objects.filter(competition=competition).count()
        stats["challenges"] = Challenge.objects.filter(competition=competition, is_published=True).count()
        stats["solves"] = sum(
            t.solve_count for t in leaderboard_queryset(competition)
        )
        stats["participants"] = TeamMembership.objects.filter(competition=competition).count()

    announcements = []
    if competition:
        announcements = competition.announcements.filter(is_published=True)[:3]

    return render(
        request,
        "core/home.html",
        {
            "competition": competition,
            "stats": stats,
            "schools": SCHOOLS,
            "announcements": announcements,
        },
    )


@login_required
def dashboard(request):
    competition = get_current_competition()
    membership = None
    if competition:
        membership = TeamMembership.objects.filter(user=request.user, competition=competition).select_related("team").first()
    announcements = competition.announcements.filter(is_published=True)[:5] if competition else []
    return render(
        request,
        "core/dashboard.html",
        {"competition": competition, "membership": membership, "announcements": announcements},
    )


def rules(request):
    competition = get_current_competition()
    return render(request, "core/rules.html", {"competition": competition})


def health(request):
    db_ok = True
    try:
        connection.cursor()
    except Exception:
        db_ok = False
    return JsonResponse({"status": "ok" if db_ok else "degraded", "database": db_ok})


@staff_member_required
def admin_overview(request):
    competition = get_current_competition()
    total_users = TeamMembership.objects.filter(competition=competition).count() if competition else 0
    teams = Team.objects.filter(competition=competition).count() if competition else 0
    challenges = Challenge.objects.filter(competition=competition).count() if competition else 0
    published_challenges = Challenge.objects.filter(competition=competition, is_published=True).count() if competition else 0
    solves = Submission.objects.filter(challenge__competition=competition, is_correct=True).count() if competition else 0
    submissions = Submission.objects.filter(challenge__competition=competition).count() if competition else 0
    pending_requests = ApprovedMember.objects.filter(pending_review=True).count()

    recent_audit = AuditLog.objects.all()[:15]

    return render(
        request,
        "core/admin_overview.html",
        {
            "competition": competition,
            "total_users": total_users,
            "teams": teams,
            "challenges": challenges,
            "published_challenges": published_challenges,
            "solves": solves,
            "submissions": submissions,
            "pending_requests": pending_requests,
            "recent_audit": recent_audit,
        },
    )


@staff_member_required
def admin_submission_logs(request):
    competition = get_current_competition()
    qs = Submission.objects.select_related("user", "team", "challenge").order_by("-created_at")
    if competition:
        qs = qs.filter(challenge__competition=competition)

    window_start = timezone.now() - timedelta(minutes=10)
    recent = qs.filter(created_at__gte=window_start, is_correct=False)
    abuse_counter = Counter((s.user_id, s.challenge_id) for s in recent)
    flagged_pairs = {pair for pair, count in abuse_counter.items() if count >= 6}

    submissions = list(qs[:200])
    for s in submissions:
        s.is_flagged = (s.user_id, s.challenge_id) in flagged_pairs

    return render(request, "core/admin_submission_logs.html", {"submissions": submissions, "competition": competition})


@staff_member_required
def admin_export_results(request):
    competition = get_current_competition()
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="nova_ctf_results.csv"'
    writer = csv.writer(response)
    writer.writerow(["rank", "team", "points", "solves", "last_solve_utc"])
    if competition:
        for rank, team in enumerate(leaderboard_queryset(competition), start=1):
            writer.writerow([rank, team.name, team.score, team.solve_count, team.last_solve or ""])
    return response


@staff_member_required
def admin_export_submissions(request):
    competition = get_current_competition()
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="nova_ctf_submissions.csv"'
    writer = csv.writer(response)
    writer.writerow(["timestamp_utc", "user", "team", "challenge", "correct"])
    qs = Submission.objects.select_related("user", "team", "challenge").order_by("created_at")
    if competition:
        qs = qs.filter(challenge__competition=competition)
    for s in qs:
        writer.writerow([s.created_at.isoformat(), s.user.username, s.team.name, s.challenge.title, s.is_correct])
    return response
