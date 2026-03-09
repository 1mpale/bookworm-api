"""Repository for audit log data access."""

import logging
from typing import Any, Optional

from modules.shared.models.orm.models.django_audit_log import DjangoAuditLog

logger = logging.getLogger(__name__)


class AuditRepository:
    """Data access layer for audit logs.

    Provides read and write operations for the audit log.
    Audit log entries are immutable — no update or delete operations.
    """

    def log_action(
        self,
        action: str,
        resource_type: str,
        resource_id: Optional[int] = None,
        user_id: Optional[int] = None,
        details: Optional[dict[str, Any]] = None,
        ip_address: Optional[str] = None,
    ) -> DjangoAuditLog:
        """Create an audit log entry.

        Args:
            action: The action performed (e.g., 'book.create', 'user.login').
            resource_type: Type of resource affected.
            resource_id: ID of the affected resource.
            user_id: ID of the user who performed the action.
            details: Additional context as JSON.
            ip_address: Client IP address.

        Returns:
            The created audit log entry.
        """
        entry = DjangoAuditLog.objects.create(
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            user_id=user_id,
            details=details,
            ip_address=ip_address,
        )
        logger.debug("Audit log: %s %s/%s", action, resource_type, resource_id)
        return entry

    def list_entries(
        self,
        page: int = 1,
        page_size: int = 50,
        action: Optional[str] = None,
        user_id: Optional[int] = None,
        resource_type: Optional[str] = None,
    ) -> tuple[list[DjangoAuditLog], int]:
        """List audit log entries with filters.

        Args:
            page: Page number.
            page_size: Items per page.
            action: Optional action filter.
            user_id: Optional user filter.
            resource_type: Optional resource type filter.

        Returns:
            Tuple of (entries list, total count).
        """
        queryset = DjangoAuditLog.objects.all()

        if action:
            queryset = queryset.filter(action=action)
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        if resource_type:
            queryset = queryset.filter(resource_type=resource_type)

        total = queryset.count()
        offset = (page - 1) * page_size
        entries = list(queryset[offset : offset + page_size])

        return entries, total
