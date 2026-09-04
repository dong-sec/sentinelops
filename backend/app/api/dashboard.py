from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.dashboard_repository import DashboardRepository
from app.schemas.dashboard import DashboardOverview, DashboardTrends
from app.security.dependencies import get_current_user
from app.services.dashboard_service import DashboardService


router = APIRouter(prefix="/dashboard")


def get_dashboard_service(
    session: AsyncSession = Depends(get_db),
) -> DashboardService:
    repository = DashboardRepository(session)
    return DashboardService(repository)


@router.get("/overview", response_model=DashboardOverview)
async def get_overview(
    current_user=Depends(get_current_user),
    service: DashboardService = Depends(get_dashboard_service),
):
    return await service.get_overview()


@router.get("/trends", response_model=DashboardTrends)
async def get_trends(
    range: str = Query(
        default="1h",
        pattern="^(1h|6h|24h|7d|30d|custom)$",
    ),
    from_time: datetime | None = Query(default=None, alias="from"),
    to_time: datetime | None = Query(default=None, alias="to"),
    current_user=Depends(get_current_user),
    service: DashboardService = Depends(get_dashboard_service),
):
    try:
        return await service.get_trends(
            interval=range,
            from_time=from_time,
            to_time=to_time,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )