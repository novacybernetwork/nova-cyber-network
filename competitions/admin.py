from django.contrib import admin
from django.utils import timezone

from core.models import log_action

from .models import Announcement, Competition


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "status_display",
        "start_time",
        "end_time",
        "is_published",
        "registration_open",
        "submissions_paused",
    )
    list_filter = ("is_published", "registration_open", "submissions_paused")
    search_fields = ("name",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("name", "slug", "tagline", "description")}),
        ("Schedule (UTC)", {"fields": ("start_time", "end_time", "team_lock_time")}),
        (
            "Controls",
            {
                "fields": (
                    "is_published",
                    "registration_open",
                    "max_team_size",
                    "submissions_paused",
                    "scoreboard_frozen_at",
                    "challenges_readable_after_end",
                )
            },
        ),
        ("Rules & contact", {"fields": ("rules_text", "contact_email")}),
        ("Metadata", {"fields": ("created_at", "updated_at")}),
    )
    actions = ["pause_submissions", "resume_submissions", "freeze_scoreboard_now", "unfreeze_scoreboard"]

    @admin.display(description="Status")
    def status_display(self, obj):
        return obj.status().title()

    @admin.action(description="Pause flag submissions")
    def pause_submissions(self, request, queryset):
        queryset.update(submissions_paused=True)
        for c in queryset:
            log_action(request.user, "competition.pause_submissions", target=c)
        self.message_user(request, "Submissions paused for selected competitions.")

    @admin.action(description="Resume flag submissions")
    def resume_submissions(self, request, queryset):
        queryset.update(submissions_paused=False)
        for c in queryset:
            log_action(request.user, "competition.resume_submissions", target=c)
        self.message_user(request, "Submissions resumed for selected competitions.")

    @admin.action(description="Freeze scoreboard now")
    def freeze_scoreboard_now(self, request, queryset):
        now = timezone.now()
        queryset.update(scoreboard_frozen_at=now)
        for c in queryset:
            log_action(request.user, "competition.freeze_scoreboard", target=c, metadata={"at": now.isoformat()})
        self.message_user(request, "Scoreboard frozen at current time.")

    @admin.action(description="Unfreeze scoreboard")
    def unfreeze_scoreboard(self, request, queryset):
        queryset.update(scoreboard_frozen_at=None)
        for c in queryset:
            log_action(request.user, "competition.unfreeze_scoreboard", target=c)
        self.message_user(request, "Scoreboard unfrozen.")


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "competition", "is_published", "created_by", "created_at")
    list_filter = ("competition", "is_published")
    search_fields = ("title", "body")
    readonly_fields = ("created_by", "created_at")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        log_action(request.user, "announcement.publish" if obj.is_published else "announcement.save", target=obj)
