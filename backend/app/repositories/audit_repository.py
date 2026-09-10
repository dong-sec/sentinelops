from datetime import datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit import AuditLog


class AuditRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

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
        query = select(AuditLog)

        if actor_id is not None:
            query = query.where(
                AuditLog.actor_user_id == actor_id
            )

        if action is not None:
            query = query.where(
                AuditLog.action == action
            )

        if target_type is not None:
            query = query.where(
                AuditLog.target_type == target_type
            )

        if result is not None:
            query = query.where(
                AuditLog.result == result
            )

        if source_ip is not None:
            query = query.where(
                AuditLog.source_ip == source_ip
            )

        if from_time is not None:
            query = query.where(
                AuditLog.created_at >= from_time
            )

        if to_time is not None:
            query = query.where(
                AuditLog.created_at <= to_time
            )

        query = query.order_by(
            AuditLog.created_at.desc()
        )

        result_data = await self.session.execute(query)

        return list(result_data.scalars().all())

    async def get_by_id(
        self,
        audit_id: UUID,
    ) -> AuditLog | None:
        result = await self.session.execute(
            select(AuditLog).where(
                AuditLog.id == audit_id
            )
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        audit_log: AuditLog,
    ) -> AuditLog:
        self.session.add(audit_log)

        await self.session.flush()
        await self.session.refresh(audit_log)

        return audit_log