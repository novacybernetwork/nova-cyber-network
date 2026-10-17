import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class School(models.Model):
    name = models.CharField(max_length=150, unique=True)
    short_name = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ApprovedMember(models.Model):
    """
    Pre-approved NOVA Cyber Network roster entry, imported by an admin via CSV.
    A matching user must claim the invite before they can participate.
    """

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_members")
    invite_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_claimed = models.BooleanField(default=False)
    pending_review = models.BooleanField(
        default=False,
        help_text="True for self-requested access not yet on the roster. An admin must clear this before the "
        "invite link can be claimed.",
    )
    claimed_by = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_member"
    )
    imported_at = models.DateTimeField(auto_now_add=True)
    claimed_at = models.DateTimeField(null=True, blank=True)
    notes = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} <{self.email}>"

    def mark_claimed(self, user):
        self.is_claimed = True
        self.claimed_by = user
        self.claimed_at = timezone.now()
        self.save(update_fields=["is_claimed", "claimed_by", "claimed_at"])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    display_name = models.CharField(max_length=60)
    school = models.ForeignKey(School, on_delete=models.SET_NULL, null=True, blank=True, related_name="profiles")
    approved_member = models.OneToOneField(
        ApprovedMember, on_delete=models.SET_NULL, null=True, blank=True, related_name="profile"
    )
    is_approved = models.BooleanField(
        default=False, help_text="Whether this member is eligible to participate in competitions."
    )
    is_deactivated = models.BooleanField(default=False)

    class Meta:
        ordering = ["display_name"]

    def __str__(self):
        return self.display_name or self.user.username

    @property
    def date_joined(self):
        return self.user.date_joined

    def current_team_membership(self, competition):
        return self.user.team_memberships.filter(competition=competition).select_related("team").first()
