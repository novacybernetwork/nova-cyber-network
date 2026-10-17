import secrets
import string

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from competitions.models import Competition


def generate_invite_code(length=8):
    alphabet = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


class Team(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="teams")
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    captain = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="captained_teams"
    )
    invite_code = models.CharField(max_length=16, unique=True, blank=True)

    total_points = models.PositiveIntegerField(default=0)
    last_solve_at = models.DateTimeField(null=True, blank=True)

    is_disqualified = models.BooleanField(default=False)
    disqualified_reason = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-total_points", "last_solve_at"]
        constraints = [
            models.UniqueConstraint(fields=["competition", "name"], name="unique_team_name_per_competition"),
            models.UniqueConstraint(fields=["competition", "slug"], name="unique_team_slug_per_competition"),
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:100] or "team"
        if not self.invite_code:
            self.invite_code = self._unique_invite_code()
        super().save(*args, **kwargs)

    @staticmethod
    def _unique_invite_code():
        for _ in range(25):
            code = generate_invite_code()
            if not Team.objects.filter(invite_code=code).exists():
                return code
        raise RuntimeError("Could not generate a unique invite code")

    def regenerate_invite_code(self, created_by=None):
        old_code = self.invite_code
        self.invite_code = self._unique_invite_code()
        self.save(update_fields=["invite_code"])
        TeamInvite.objects.filter(team=self, revoked_at__isnull=True).update(revoked_at=timezone.now())
        TeamInvite.objects.create(team=self, code=self.invite_code, created_by=created_by)
        return old_code

    @property
    def member_count(self):
        return self.memberships.count()

    def is_full(self):
        return self.member_count >= self.competition.max_team_size


class TeamMembership(models.Model):
    ROLE_CAPTAIN = "captain"
    ROLE_MEMBER = "member"
    ROLE_CHOICES = [(ROLE_CAPTAIN, "Captain"), (ROLE_MEMBER, "Member")]

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="memberships")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="team_memberships")
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="team_memberships")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["joined_at"]
        constraints = [
            models.UniqueConstraint(fields=["competition", "user"], name="one_active_membership_per_user_per_competition"),
        ]

    def __str__(self):
        return f"{self.user.username} -> {self.team.name}"


class TeamInvite(models.Model):
    """Audit trail of invite codes issued for a team (rotation history)."""

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="invite_history")
    code = models.CharField(max_length=16)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.team.name}:{self.code}"
