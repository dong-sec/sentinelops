from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ResponseStepResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    step_order: int
    step_type: str
    status: str
    message: str | None = None
    metadata: dict | None = Field(
        default=None,
        validation_alias="metadata_",
    )
    started_at: datetime | None = None
    completed_at: datetime | None = None

    @field_validator("metadata", mode="before")
    @classmethod
    def normalize_metadata(cls, value):
        if value is None:
            return None

        if isinstance(value, dict):
            return value

        return dict(value)


class ResponseListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    event_id: UUID | None = None
    policy_id: UUID | None = None
    initiated_by: UUID | None = None
    response_type: str
    target_ip: str | None = None
    status: str
    reason: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None
    created_at: datetime

    @field_validator("target_ip", mode="before")
    @classmethod
    def normalize_target_ip(cls, value):
        if value is None:
            return None

        return str(value)


class ResponseDetailResponse(ResponseListItem):
    steps: list[ResponseStepResponse] = Field(default_factory=list)


class ResponseTargetRequest(BaseModel):
    type: str = Field(min_length=1, max_length=50)
    value: str = Field(min_length=1)


class ResponseExecuteRequest(BaseModel):
    action: str = Field(min_length=1, max_length=50)
    target: ResponseTargetRequest
    duration_seconds: int | None = Field(
        default=None,
        ge=0,
    )
    reason: str | None = None
    source_event_id: UUID | None = None


class ResponseExecuteResponse(ResponseDetailResponse):
    pass