from datetime import datetime
from uuid import UUID

from app.models.audit import AuditLog
from app.repositories.audit_repository import AuditRepository


class AuditService:

    def __init__(self, repository: AuditRepository):
        self.repository = repository

    async def get_all(
        self,
        actor_id: UUID | None = None,
        action: str | None = None,
        target_type: str | None = None,
        result: str | None = None,
        source_ip: str | None = None,
        from_time: datetime | None = None,
        to_time: datetime | None = None,
    ) -> list[AuditLog]:
        return await self.repository.get_all(
            actor_id=actor_id,
            action=action,
            target_type=target_type,
            result=result,
            source_ip=source_ip,
            from_time=from_time,
            to_time=to_time,
        )

    async def get_by_id(
        self,
        audit_id: UUID,
    ) -> AuditLog | None:
        return await self.repository.get_by_id(audit_id)

    async def create(
        self,
        actor_user_id: UUID | None,
        action: str,
        target_type: str | None,
        target_id: UUID | None,
        result: str,
        reason: str | None = None,
        source_ip: str | None = None,
        before_data: dict | None = None,
        after_data: dict | None = None,
        correlation_id: UUID | None = None,
    ) -> AuditLog:
        audit_log = AuditLog(
            actor_user_id=actor_user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            result=result,
            reason=reason,
            source_ip=source_ip,
            before_data=before_data,
            after_data=after_data,
            correlation_id=correlation_id,
        )

        return await self.repository.create(audit_log)