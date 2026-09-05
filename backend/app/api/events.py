from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.events_repository import EventsRepository
from app.schemas.events import (
    EventDetail,
    EventDetection,
    EventListResponse,
    EventRisk,
    EventTimelineItem,
)
from app.security.dependencies import get_current_user
from app.services.events_service import EventsService


router = APIRouter(prefix="/events")


def get_events_service(
    session: AsyncSession = Depends(get_db),
) -> EventsService:
    repository = EventsRepository(session)
    return EventsService(repository)


@router.get("", response_model=EventListResponse)
async def get_events(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    severity: str | None = Query(default=None),
    risk_level: str | None = Query(default=None),
    attack_type: str | None = Query(default=None),
    source_ip: str | None = Query(default=None),
    status: str | None = Query(default=None),
    method: str | None = Query(default=None),
    from_time: datetime | None = Query(default=None, alias="from"),
    to_time: datetime | None = Query(default=None, alias="to"),
    sort_by: str = Query(default="event_time"),
    sort_order: str = Query(default="desc"),
    current_user=Depends(get_current_user),
    service: EventsService = Depends(get_events_service),
):
    try:
        return await service.get_events(
            page=page,
            page_size=page_size,
            severity=severity,
            risk_level=risk_level,
            attack_type=attack_type,
            source_ip=source_ip,
            status=status,
            method=method,
            from_time=from_time,
            to_time=to_time,
            sort_by=sort_by,
            sort_order=sort_order,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


@router.get(
    "/{event_id}/timeline",
    response_model=list[EventTimelineItem],
)
async def get_event_timeline(
    event_id: str,
    current_user=Depends(get_current_user),
    service: EventsService = Depends(get_events_service),
):
    event = await service.get_event(event_id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found.",
        )

    return await service.get_event_timeline(event_id)


@router.get(
    "/{event_id}/detections",
    response_model=list[EventDetection],
)
async def get_event_detections(
    event_id: str,
    current_user=Depends(get_current_user),
    service: EventsService = Depends(get_events_service),
):
    event = await service.get_event(event_id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found.",
        )

    return await service.get_event_detections(event_id)


@router.get(
    "/{event_id}/risk",
    response_model=list[EventRisk],
)
async def get_event_risk(
    event_id: str,
    current_user=Depends(get_current_user),
    service: EventsService = Depends(get_events_service),
):
    event = await service.get_event(event_id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found.",
        )

    return await service.get_event_risk(event_id)

@router.get("/{event_id}", response_model=EventDetail)
async def get_event(
    event_id: str,
    current_user=Depends(get_current_user),
    service: EventsService = Depends(get_events_service),
):
    event = await service.get_event(event_id)

    if event is None:
        raise HTTPException(
            status_code=404,
            detail="Event not found.",
        )

    return event