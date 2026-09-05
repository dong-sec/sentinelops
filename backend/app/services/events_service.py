from datetime import datetime

from app.repositories.events_repository import EventsRepository


class EventsService:
    def __init__(self, repository: EventsRepository):
        self.repository = repository

    async def get_events(
        self,
        page: int = 1,
        page_size: int = 20,
        severity: str | None = None,
        risk_level: str | None = None,
        attack_type: str | None = None,
        source_ip: str | None = None,
        status: str | None = None,
        method: str | None = None,
        from_time: datetime | None = None,
        to_time: datetime | None = None,
        sort_by: str = "event_time",
        sort_order: str = "desc",
    ) -> dict:
        if page < 1:
            raise ValueError("page must be greater than or equal to 1.")

        if page_size < 1 or page_size > 100:
            raise ValueError("page_size must be between 1 and 100.")

        if sort_by not in {
            "event_time",
            "severity",
            "risk_score",
            "source_ip",
        }:
            raise ValueError("Unsupported sort_by.")

        if sort_order.lower() not in {"asc", "desc"}:
            raise ValueError("sort_order must be asc or desc.")

        if from_time is not None and to_time is not None:
            if from_time >= to_time:
                raise ValueError("from_time must be earlier than to_time.")

        total = await self.repository.count_events(
            severity=severity,
            risk_level=risk_level,
            attack_type=attack_type,
            source_ip=source_ip,
            status=status,
            method=method,
            from_time=from_time,
            to_time=to_time,
        )

        items = await self.repository.get_events(
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

        total_pages = (total + page_size - 1) // page_size

        return {
            "items": items,
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
        }

    async def get_event(self, event_id: str) -> dict | None:
        return await self.repository.get_event(event_id)

    async def get_event_detections(self, event_id: str) -> list[dict]:
        return await self.repository.get_event_detections(event_id)

    async def get_event_risk(self, event_id: str) -> list[dict]:
        return await self.repository.get_event_risk(event_id)

    async def get_event_timeline(self, event_id: str) -> list[dict]:
        return await self.repository.get_event_timeline(event_id)