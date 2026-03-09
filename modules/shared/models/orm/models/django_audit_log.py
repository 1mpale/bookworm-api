# Copyright 2024 BookWorm Inc. All rights reserved.

"""Django ORM model for audit logs."""

from django.db import models


class DjangoAuditLog(models.Model):
    """Audit log database model.

    Tracks all significant system events for compliance and debugging.
    Immutable — records are never updated or deleted.
    """

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    user_id = models.IntegerField(null=True, blank=True, db_index=True)
    action = models.CharField(max_length=100, db_index=True)
    resource_type = models.CharField(max_length=100)
    resource_id = models.IntegerField(null=True, blank=True)
    details = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        db_table = "audit_logs"
        ordering = ["-timestamp"]

    def __str__(self) -> str:
        return f"[{self.timestamp}] {self.action} on {self.resource_type}"

    __all__ = ["DjangoAuditLog"]
