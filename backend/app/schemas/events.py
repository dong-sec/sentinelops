from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EventListItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    timestamp: datetime
    source_ip: str
    attack_type: str | None = None
    severity: str | None = None
    risk_score: int | None = None
    risk_level: str | None = None
    status: str
    response_status: str | None = None


class EventListResponse(BaseModel):
    items: list[EventListItem]
    page: int
    page_size: int
    total: int
    total_pages: int


class EventDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    timestamp: datetime
    source_ip: str
    method: str
    request_uri: str
    protocol: str | None = None
    status_code: int | None = None
    user_agent: str | None = None
    referer: str | None = None
    request_size: int | None = None
    response_size: int | None = None
    response_time_ms: int | None = None
    host: str | None = None
    server_name: str | None = None
    raw_log: str | None = None
    status: str
    created_at: datetime

    attack_type: str | None = None
    rule_name: str | None = None
    detection_severity: str | None = None
    confidence: float | None = None
    evidence: dict | None = None
    detection_description: str | None = None

    risk_score: int | None = None
    risk_level: str | None = None
    calculation_version: str | None = None
    factors: dict | None = None
    calculated_at: datetime | None = None


class EventDetection(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    detection_type: str
    rule_name: str | None = None
    severity: str
    confidence: float | None = None
    evidence: dict | None = None
    description: str | None = None
    detected_at: datetime


class EventRisk(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    source_ip: str
    score: int
    severity: str
    calculation_version: str | None = None
    factors: dict | None = None
    calculated_at: datetime


class EventTimelineItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    timestamp: datetime
    event_type: str
    status: str | None = None
    description: str | None = None