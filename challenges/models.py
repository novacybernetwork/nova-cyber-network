from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify

from competitions.models import Competition
from teams.models import Team


class ChallengeCategory(models.Model):
    name = models.CharField(max_length=60, unique=True)
    slug = models.SlugField(max_length=70, blank=True)
    icon_name = models.CharField(
        max_length=40, default="flag", help_text="Lucide icon name, e.g. 'terminal', 'lock', 'search'."
    )
    description = models.CharField(max_length=255, blank=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "challenge categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:70]
        super().save(*args, **kwargs)


class Challenge(models.Model):
    DIFFICULTY_EASY = "easy"
    DIFFICULTY_MEDIUM = "medium"
    DIFFICULTY_HARD = "hard"
    DIFFICULTY_CHOICES = [
        (DIFFICULTY_EASY, "Easy"),
        (DIFFICULTY_MEDIUM, "Medium"),
        (DIFFICULTY_HARD, "Hard"),
    ]
    DEFAULT_POINTS = {DIFFICULTY_EASY: 100, DIFFICULTY_MEDIUM: 250, DIFFICULTY_HARD: 500}

    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="challenges")
    category = models.ForeignKey(ChallengeCategory, on_delete=models.PROTECT, related_name="challenges")
    title = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, blank=True)
    description = models.TextField(help_text="Full problem statement. Plain text / safe markdown-lite.")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default=DIFFICULTY_EASY)
    points = models.PositiveIntegerField(default=100)

    flag_hash = models.CharField(max_length=255, editable=False)
    case_sensitive = models.BooleanField(default=True)

    is_published = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)
    order = models.PositiveSmallIntegerField(default=0)
    author = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Write-only virtual field used by admin/forms to set a new flag.
    _plain_flag = None

    class Meta:
        ordering = ["category__order", "order", "points"]
        constraints = [
            models.UniqueConstraint(fields=["competition", "slug"], name="unique_challenge_slug_per_competition"),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:140] or "challenge"
        super().save(*args, **kwargs)

    def _normalize(self, value):
        value = value.strip()
        return value if self.case_sensitive else value.lower()

    def set_flag(self, plain_flag):
        self.flag_hash = make_password(self._normalize(plain_flag))

    def check_flag(self, submitted):
        if not submitted:
            return False
        return check_password(self._normalize(submitted), self.flag_hash)

    @property
    def solve_count(self):
        return self.solves.count()

    def is_visible(self, competition=None):
        competition = competition or self.competition
        if not self.is_published or self.is_archived:
            return False
        status = competition.status()
        if status == "upcoming":
            return False
        if status == "ended":
            return competition.challenges_readable_after_end
        return True


class ChallengeAttachment(models.Model):
    """
    References a file checked into the repository (under
    static/challenge_files/) rather than relying on ephemeral uploads,
    since Render's local disk does not persist across deploys/restarts.
    """

    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="attachments")
    display_name = models.CharField(max_length=150)
    relative_path = models.CharField(
        max_length=255, help_text="Path under static/challenge_files/, e.g. 'web-security/leak.har'."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["display_name"]

    def __str__(self):
        return self.display_name


class ChallengeHint(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="hints")
    order = models.PositiveSmallIntegerField(default=0)
    text = models.TextField()
    point_cost = models.PositiveIntegerField(default=0, help_text="Reserved for future dynamic scoring.")

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Hint for {self.challenge.title} (#{self.order})"


class Submission(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="submissions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submissions")
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="submissions")
    submitted_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["team", "challenge", "created_at"]),
            models.Index(fields=["user", "created_at"]),
        ]

    def __str__(self):
        status = "correct" if self.is_correct else "incorrect"
        return f"{self.user.username} -> {self.challenge.title} ({status})"


class Solve(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="solves")
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name="solves")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="solves")
    points_awarded = models.PositiveIntegerField()
    solved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["solved_at"]
        constraints = [
            models.UniqueConstraint(fields=["team", "challenge"], name="one_solve_per_team_per_challenge"),
        ]

    def __str__(self):
        return f"{self.team.name} solved {self.challenge.title}"
