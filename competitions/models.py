import zoneinfo

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

EVENT_TZ = zoneinfo.ZoneInfo(getattr(settings, "EVENT_TIME_ZONE", "America/New_York"))


class Competition(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    tagline = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)

    start_time = models.DateTimeField(help_text="Stored in UTC. Competition becomes live at this instant.")
    end_time = models.DateTimeField(
        help_text="Stored in UTC. Submissions close at this instant (exclusive upper bound)."
    )

    is_published = models.BooleanField(default=False, help_text="Visible to the public landing page.")
    registration_open = models.BooleanField(default=True, help_text="Whether team creation/joining is allowed.")
    team_lock_time = models.DateTimeField(
        null=True, blank=True, help_text="After this time, team membership changes require admin approval."
    )
    max_team_size = models.PositiveSmallIntegerField(default=5)

    submissions_paused = models.BooleanField(
        default=False, help_text="Manual kill-switch: pause flag submissions regardless of schedule."
    )
    scoreboard_frozen_at = models.DateTimeField(
        null=True, blank=True, help_text="If set, the public leaderboard only reflects solves up to this instant."
    )
    challenges_readable_after_end = models.BooleanField(
        default=True, help_text="Allow participants to keep reading challenges after the event ends."
    )

    rules_text = models.TextField(
        blank=True, help_text="One rule per line. Rendered as a numbered list on the Rules page."
    )
    contact_email = models.EmailField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_time"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:170]
        super().save(*args, **kwargs)

    # --- state machine -------------------------------------------------
    def status(self, now=None):
        now = now or timezone.now()
        if now < self.start_time:
            return "upcoming"
        if now < self.end_time:
            return "live"
        return "ended"

    def is_live(self, now=None):
        return self.status(now) == "live"

    def has_ended(self, now=None):
        return self.status(now) == "ended"

    def accepts_submissions(self, now=None):
        return self.is_live(now) and not self.submissions_paused

    def team_changes_locked(self, now=None):
        now = now or timezone.now()
        if self.team_lock_time and now >= self.team_lock_time:
            return True
        return self.is_live(now) or self.has_ended(now)

    def rules_list(self):
        return [line.strip() for line in self.rules_text.splitlines() if line.strip()]

    def leaderboard_cutoff(self, now=None):
        """Timestamp up to which solves should count, honoring a scoreboard freeze."""
        now = now or timezone.now()
        if self.scoreboard_frozen_at and now >= self.scoreboard_frozen_at:
            return self.scoreboard_frozen_at
        return now

    @property
    def start_time_local(self):
        return self.start_time.astimezone(EVENT_TZ)

    @property
    def end_time_local(self):
        return self.end_time.astimezone(EVENT_TZ)


class Announcement(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="announcements")
    title = models.CharField(max_length=150)
    body = models.TextField()
    is_published = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        "auth.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="announcements"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
