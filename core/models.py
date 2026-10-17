from django.contrib.auth.models import User
from django.db import models


class AuditLog(models.Model):
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="audit_entries")
    action = models.CharField(max_length=100)
    target_repr = models.CharField(max_length=255, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        who = self.actor.username if self.actor else "system"
        return f"[{self.created_at:%Y-%m-%d %H:%M}] {who} - {self.action}"


def log_action(actor, action, target=None, metadata=None, ip_address=None):
    AuditLog.objects.create(
        actor=actor if getattr(actor, "is_authenticated", False) else None,
        action=action,
        target_repr=str(target) if target is not None else "",
        metadata=metadata or {},
        ip_address=ip_address,
    )
