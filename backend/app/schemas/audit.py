from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, field_validator


class AuditLogListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    actor_user_id: UUID | None = None
    action: str
    target_type: str | None = None
    target_id: UUID | None = None
    result: str
    reason: str | None = None
    source_ip: str | None = None
    correlation_id: UUID | None = None
    created_at: datetime

    @field_validator("source_ip", mode="before")
    @classmethod
    def normalize_source_ip(cls, value):
        if value is None:
            return None

        return str(value)


class AuditLogDetailResponse(AuditLogListItem):
    before_data: dict | None = None
    after_data: dict | None = None


class AuditRelatedResponse(BaseModel):
    audit_logs: list[AuditLogListItem]