from datetime import datetime
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.audit_repository import AuditRepository
from app.schemas.audit import (
    AuditLogDetailResponse,
    AuditLogListItem,
    AuditRelatedResponse,
)
from app.security.dependencies import get_current_user, require_permission
from app.services.audit_service import AuditService


router = APIRouter(prefix="/audit-logs")


def get_audit_service(
    session: AsyncSession = Depends(get_db),
) -> AuditService:
    repository = AuditRepository(session)
    return AuditService(repository)


@router.get(
    "",
    response_model=list[AuditLogListItem],
    dependencies=[Depends(require_permission("audit.read"))],
)
async def get_audit_logs(
    actor_id: UUID | None = Query(default=None),
    action: str | None = Query(default=None),
    target_type: str | None = Query(default=None),
    result: str | None = Query(default=None),
    source_ip: str | None = Query(default=None),
    from_time: datetime | None = Query(default=None, alias="from"),
    to_time: datetime | None = Query(default=None, alias="to"),
    current_user=Depends(get_current_user),
    service: AuditService = Depends(get_audit_service),
):
    return await service.get_all(
        actor_id=actor_id,
        action=action,
        target_type=target_type,
        result=result,
        source_ip=source_ip,
        from_time=from_time,
        to_time=to_time,
    )


@router.get(
    "/{audit_id}",
    response_model=AuditLogDetailResponse,
    dependencies=[Depends(require_permission("audit.read"))],
)
async def get_audit_log(
    audit_id: UUID,
    current_user=Depends(get_current_user),
    service: AuditService = Depends(get_audit_service),
):
    audit_log = await service.get_by_id(audit_id)

    if audit_log is None:
        raise HTTPException(
            status_code=404,
            detail="Audit log not found.",
        )

    return audit_log