from dataclasses import dataclass

from django.db import IntegrityError, transaction

from .models import Challenge, Solve, Submission


class SubmissionError(Exception):
    """Raised when a submission cannot be accepted (closed competition, etc.)."""


@dataclass
class SubmissionResult:
    correct: bool
    already_solved: bool
    message: str


def submit_flag(*, team, user, challenge: Challenge, submitted_text: str) -> SubmissionResult:
    """
    Validate and record a flag submission.

    Correctness is checked against the server-side flag hash only; the
    plaintext flag is never sent to the client. Awarding points happens in
    one atomic transaction guarded by the team+challenge unique constraint,
    so concurrent duplicate submissions cannot double-award points.
    """
    submitted_text = (submitted_text or "")[:255]

    # Fast path: already solved by this team -> no-op, no new Submission row
    # needed for scoring purposes, but we still want the no-op to be cheap.
    if Solve.objects.filter(team=team, challenge=challenge).exists():
        Submission.objects.create(team=team, user=user, challenge=challenge, submitted_text=submitted_text, is_correct=False)
        return SubmissionResult(correct=False, already_solved=True, message="Your team has already solved this challenge.")

    is_correct = challenge.check_flag(submitted_text)

    with transaction.atomic():
        Submission.objects.create(
            team=team, user=user, challenge=challenge, submitted_text=submitted_text, is_correct=is_correct
        )
        if not is_correct:
            return SubmissionResult(correct=False, already_solved=False, message="Incorrect flag. Try again.")

        try:
            with transaction.atomic():
                solve = Solve.objects.create(
                    team=team, challenge=challenge, user=user, points_awarded=challenge.points
                )
        except IntegrityError:
            # Another teammate's concurrent request won the race.
            return SubmissionResult(
                correct=True, already_solved=True, message="Your team has already solved this challenge."
            )

        _apply_team_score(team, solve)

    return SubmissionResult(correct=True, already_solved=False, message=f"Correct! +{challenge.points} points.")


def _apply_team_score(team, solve):
    """
    Lock the team row for the duration of the enclosing transaction so two
    teammates solving different challenges at the same instant can't race
    each other into a lost update on total_points/last_solve_at.
    """
    from teams.models import Team

    locked_team = Team.objects.select_for_update().get(pk=team.pk)
    locked_team.total_points += solve.points_awarded
    locked_team.last_solve_at = solve.solved_at
    locked_team.save(update_fields=["total_points", "last_solve_at"])
