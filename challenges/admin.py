from pathlib import Path

from django import forms
from django.conf import settings
from django.contrib import admin

from core.models import log_action

from .models import Challenge, ChallengeAttachment, ChallengeCategory, ChallengeHint, Solve, Submission

ATTACHMENTS_ROOT = Path(settings.BASE_DIR) / "static" / "challenge_files"


def _available_attachment_files():
    if not ATTACHMENTS_ROOT.exists():
        return []
    return sorted(
        str(p.relative_to(ATTACHMENTS_ROOT))
        for p in ATTACHMENTS_ROOT.rglob("*")
        if p.is_file()
    )


class ChallengeAttachmentForm(forms.ModelForm):
    relative_path = forms.ChoiceField(
        choices=(),
        help_text="Files checked into static/challenge_files/. Add a file to the repo to make it selectable here.",
    )

    class Meta:
        model = ChallengeAttachment
        fields = ["display_name", "relative_path"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = [(f, f) for f in _available_attachment_files()]
        current = self.instance.relative_path if self.instance and self.instance.pk else None
        if current and current not in dict(choices):
            choices.insert(0, (current, f"{current} (missing from repo)"))
        self.fields["relative_path"].choices = choices


class ChallengeAttachmentInline(admin.TabularInline):
    model = ChallengeAttachment
    form = ChallengeAttachmentForm
    extra = 0


class ChallengeHintInline(admin.TabularInline):
    model = ChallengeHint
    extra = 0


class ChallengeAdminForm(forms.ModelForm):
    plain_flag = forms.CharField(
        required=False,
        label="Flag",
        help_text="Enter to set/replace the flag (e.g. NOVA{example_flag}). Leave blank to keep the current flag.",
        widget=forms.TextInput(attrs={"autocomplete": "off"}),
    )

    class Meta:
        model = Challenge
        exclude = ["flag_hash"]

    def clean(self):
        cleaned = super().clean()
        if not self.instance.pk and not cleaned.get("plain_flag"):
            self.add_error("plain_flag", "A flag is required when creating a new challenge.")
        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        plain_flag = self.cleaned_data.get("plain_flag")
        if plain_flag:
            instance.set_flag(plain_flag)
        if commit:
            instance.save()
        return instance


@admin.register(ChallengeCategory)
class ChallengeCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "icon_name", "order")
    ordering = ["order", "name"]


@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    form = ChallengeAdminForm
    list_display = (
        "title",
        "competition",
        "category",
        "difficulty",
        "points",
        "solve_count",
        "is_published",
        "is_archived",
    )
    list_filter = ("competition", "category", "difficulty", "is_published", "is_archived")
    search_fields = ("title", "description")
    inlines = [ChallengeHintInline, ChallengeAttachmentInline]
    actions = ["publish_challenges", "unpublish_challenges", "archive_challenges"]
    fieldsets = (
        (None, {"fields": ("competition", "category", "title", "slug", "author")}),
        ("Content", {"fields": ("description", "difficulty", "points")}),
        ("Flag", {"fields": ("plain_flag", "case_sensitive")}),
        ("Visibility", {"fields": ("is_published", "is_archived", "order")}),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        log_action(request.user, "challenge.save", target=obj, metadata={"published": obj.is_published})

    @admin.action(description="Publish selected challenges")
    def publish_challenges(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f"Published {updated} challenges.")

    @admin.action(description="Unpublish selected challenges")
    def unpublish_challenges(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f"Unpublished {updated} challenges.")

    @admin.action(description="Archive selected challenges")
    def archive_challenges(self, request, queryset):
        updated = queryset.update(is_archived=True, is_published=False)
        self.message_user(request, f"Archived {updated} challenges.")


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("user", "team", "challenge", "is_correct", "created_at")
    list_filter = ("is_correct", "challenge__competition", "challenge")
    search_fields = ("user__username", "team__name", "challenge__title")
    readonly_fields = [f.name for f in Submission._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Solve)
class SolveAdmin(admin.ModelAdmin):
    list_display = ("team", "challenge", "user", "points_awarded", "solved_at")
    list_filter = ("challenge__competition", "challenge")
    search_fields = ("team__name", "challenge__title", "user__username")
    readonly_fields = [f.name for f in Solve._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
