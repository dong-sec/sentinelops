from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PolicyRuleRequest(BaseModel):
    field: str = Field(min_length=1, max_length=100)
    operator: str = Field(min_length=1, max_length=50)
    value: str = Field(min_length=1)
    logical_operator: str = Field(
        default="AND",
        pattern="^(AND|OR)$",
    )


class PolicyCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    enabled: bool = True
    priority: int = Field(default=100, ge=1)
    action: str = Field(min_length=1, max_length=100)
    duration_seconds: int | None = Field(default=None, ge=0)
    rules: list[PolicyRuleRequest] = Field(default_factory=list)


class PolicyUpdateRequest(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    description: str | None = None
    enabled: bool | None = None
    priority: int | None = Field(default=None, ge=1)
    action: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    duration_seconds: int | None = Field(default=None, ge=0)
    rules: list[PolicyRuleRequest] | None = None


class PolicyRuleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    field: str
    operator: str
    value: str
    logical_operator: str


class PolicyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: str | None
    enabled: bool
    priority: int
    action: str
    duration_seconds: int | None
    created_by: UUID | None
    updated_by: UUID | None
    created_at: object
    updated_at: object
    rules: list[PolicyRuleResponse]


class PolicyValidationRequest(BaseModel):
    condition: dict = Field(default_factory=dict)
    action: dict = Field(default_factory=dict)


class PolicyValidationResponse(BaseModel):
    valid: bool
    warnings: list[str] = Field(default_factory=list)