import csv
import io

from django import forms
from django.contrib import admin, messages
from django.shortcuts import redirect, render
from django.urls import path, reverse
from django.utils.html import format_html

from core.models import log_action

from .models import ApprovedMember, Profile, School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ("name", "short_name")
    search_fields = ("name", "short_name")


class CSVImportForm(forms.Form):
    csv_file = forms.FileField(help_text="Columns: name,email,school")


@admin.register(ApprovedMember)
class ApprovedMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "masked_email", "school", "pending_review", "is_claimed", "imported_at")
    list_filter = ("pending_review", "is_claimed", "school")
    search_fields = ("name", "email")
    readonly_fields = ("invite_token", "claim_link", "is_claimed", "claimed_by", "claimed_at", "imported_at")
    change_list_template = "admin/accounts/approvedmember/change_list.html"
    actions = ["approve_requests"]

    @admin.display(description="Claim link")
    def claim_link(self, obj):
        if not obj.pk:
            return "—"
        url = reverse("accounts:claim_invite", args=[obj.invite_token])
        return format_html('<code>{}</code>', url)

    @admin.action(description="Approve selected access requests")
    def approve_requests(self, request, queryset):
        updated = queryset.filter(pending_review=True).update(pending_review=False)
        for member in queryset:
            log_action(request.user, "membership.approve_request", target=member)
        self.message_user(request, f"Approved {updated} access requests. They can now use their claim link.")

    @admin.display(description="Email")
    def masked_email(self, obj):
        # Member emails are not displayed publicly; mask in the list view too.
        local, _, domain = obj.email.partition("@")
        if len(local) <= 2:
            masked = local[0] + "*" if local else "*"
        else:
            masked = local[0] + "*" * (len(local) - 2) + local[-1]
        return f"{masked}@{domain}"

    def get_urls(self):
        urls = super().get_urls()
        custom = [
            path("import-csv/", self.admin_site.admin_view(self.import_csv), name="accounts_approvedmember_import_csv"),
        ]
        return custom + urls

    def import_csv(self, request):
        if request.method == "POST":
            form = CSVImportForm(request.POST, request.FILES)
            if form.is_valid():
                created, skipped = self._process_csv(request.FILES["csv_file"])
                log_action(request.user, "membership.csv_import", metadata={"created": created, "skipped": skipped})
                messages.success(request, f"Imported {created} new members. Skipped {skipped} (already present).")
                return redirect("admin:accounts_approvedmember_changelist")
        else:
            form = CSVImportForm()
        return render(request, "admin/accounts/approvedmember/import_csv.html", {"form": form, "opts": self.model._meta})

    def _process_csv(self, uploaded_file):
        decoded = uploaded_file.read().decode("utf-8-sig")
        reader = csv.DictReader(io.StringIO(decoded))
        created, skipped = 0, 0
        for row in reader:
            name = (row.get("name") or "").strip()
            email = (row.get("email") or "").strip().lower()
            school_name = (row.get("school") or "").strip()
            if not name or not email:
                skipped += 1
                continue
            if ApprovedMember.objects.filter(email=email).exists():
                skipped += 1
                continue
            school = None
            if school_name:
                school, _ = School.objects.get_or_create(name=school_name)
            ApprovedMember.objects.create(name=name, email=email, school=school)
            created += 1
        return created, skipped


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("display_name", "user", "school", "is_approved", "is_deactivated")
    list_filter = ("is_approved", "is_deactivated", "school")
    search_fields = ("display_name", "user__username", "user__email")
    actions = ["approve_profiles", "deactivate_profiles"]

    @admin.action(description="Approve selected members")
    def approve_profiles(self, request, queryset):
        updated = queryset.update(is_approved=True)
        log_action(request.user, "membership.bulk_approve", metadata={"count": updated})
        self.message_user(request, f"Approved {updated} members.")

    @admin.action(description="Deactivate selected accounts")
    def deactivate_profiles(self, request, queryset):
        updated = queryset.update(is_deactivated=True)
        log_action(request.user, "membership.bulk_deactivate", metadata={"count": updated})
        self.message_user(request, f"Deactivated {updated} accounts.")
