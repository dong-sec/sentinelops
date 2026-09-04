from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DashboardKPI(BaseModel):
    total_events: int
    critical_events: int
    high_risk_events: int
    blocked_ips: int
    active_incidents: int
    automatic_responses: int
    response_failures: int


class RiskDistribution(BaseModel):
    critical: int
    high: int
    medium: int
    low: int


class AttackDistributionItem(BaseModel):
    attack_type: str
    count: int


class RecentCriticalEvent(BaseModel):
    id: str
    timestamp: datetime
    source_ip: str
    attack_type: str | None = None
    severity: str
    status: str


class ServiceHealthItem(BaseModel):
    service_name: str
    status: str
    health_status: str
    cpu_percent: float | None = None
    memory_percent: float | None = None
    disk_percent: float | None = None
    last_check_at: datetime | None = None


class RecentResponse(BaseModel):
    id: str
    response_type: str
    target_ip: str | None = None
    status: str
    created_at: datetime


class DashboardOverview(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    kpi: DashboardKPI
    risk_distribution: RiskDistribution
    attack_distribution: list[AttackDistributionItem]
    recent_critical_events: list[RecentCriticalEvent]
    service_health: list[ServiceHealthItem]
    recent_responses: list[RecentResponse]


class DashboardTrendPoint(BaseModel):
    timestamp: datetime
    events: int
    critical: int
    high: int
    blocked: int


class DashboardTrends(BaseModel):
    interval: str
    points: list[DashboardTrendPoint]