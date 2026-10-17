from django.contrib import admin

from core.models import log_action

from .models import Team, TeamInvite, TeamMembership


class TeamMembershipInline(admin.TabularInline):
    model = TeamMembership
    extra = 0
    autocomplete_fields = ["user"]
    readonly_fields = ("joined_at",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "competition", "captain", "member_count", "total_points", "is_disqualified")
    list_filter = ("competition", "is_disqualified")
    search_fields = ("name", "captain__username")
    readonly_fields = ("invite_code", "total_points", "last_solve_at", "created_at")
    inlines = [TeamMembershipInline]
    actions = ["disqualify_teams", "requalify_teams"]

    @admin.action(description="Disqualify selected teams")
    def disqualify_teams(self, request, queryset):
        updated = queryset.update(is_disqualified=True)
        for team in queryset:
            log_action(request.user, "team.disqualify", target=team)
        self.message_user(request, f"Disqualified {updated} teams.")

    @admin.action(description="Re-qualify selected teams")
    def requalify_teams(self, request, queryset):
        updated = queryset.update(is_disqualified=False, disqualified_reason="")
        for team in queryset:
            log_action(request.user, "team.requalify", target=team)
        self.message_user(request, f"Re-qualified {updated} teams.")


@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "team", "competition", "role", "joined_at")
    list_filter = ("competition", "role")
    search_fields = ("user__username", "team__name")
    autocomplete_fields = ["user", "team"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        log_action(request.user, "team.membership_admin_edit", target=obj)


@admin.register(TeamInvite)
class TeamInviteAdmin(admin.ModelAdmin):
    list_display = ("team", "code", "created_by", "created_at", "revoked_at")
    list_filter = ("team__competition",)
    search_fields = ("team__name", "code")
