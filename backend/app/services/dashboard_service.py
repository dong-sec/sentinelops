from datetime import datetime, timedelta, timezone

from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:
    def __init__(self, repository: DashboardRepository):
        self.repository = repository

    async def get_overview(self) -> dict:
        (
            total_events,
            critical_events,
            high_risk_events,
            blocked_ips,
            active_incidents,
            automatic_responses,
            response_failures,
            risk_distribution,
            attack_distribution,
            recent_critical_events,
            service_health,
            recent_responses,
        ) = await self._get_overview_data()

        return {
            "kpi": {
                "total_events": total_events,
                "critical_events": critical_events,
                "high_risk_events": high_risk_events,
                "blocked_ips": blocked_ips,
                "active_incidents": active_incidents,
                "automatic_responses": automatic_responses,
                "response_failures": response_failures,
            },
            "risk_distribution": risk_distribution,
            "attack_distribution": attack_distribution,
            "recent_critical_events": recent_critical_events,
            "service_health": service_health,
            "recent_responses": recent_responses,
        }

    async def _get_overview_data(self):
        return await self._gather_overview_data()

    async def _gather_overview_data(self):
        return (
            await self.repository.get_total_events(),
            await self.repository.get_critical_events(),
            await self.repository.get_high_risk_events(),
            await self.repository.get_blocked_ips(),
            await self.repository.get_active_incidents(),
            await self.repository.get_automatic_responses(),
            await self.repository.get_response_failures(),
            await self.repository.get_risk_distribution(),
            await self.repository.get_attack_distribution(),
            await self.repository.get_recent_critical_events(),
            await self.repository.get_service_health(),
            await self.repository.get_recent_responses(),
        )

    async def get_trends(
        self,
        interval: str,
        from_time: datetime | None = None,
        to_time: datetime | None = None,
    ) -> dict:
        now = datetime.now(timezone.utc)

        if interval == "1h":
            default_from = now - timedelta(hours=1)
        elif interval == "6h":
            default_from = now - timedelta(hours=6)
        elif interval == "24h":
            default_from = now - timedelta(hours=24)
        elif interval == "7d":
            default_from = now - timedelta(days=7)
        elif interval == "30d":
            default_from = now - timedelta(days=30)
        elif interval == "custom":
            if from_time is None or to_time is None:
                raise ValueError(
                    "from_time and to_time are required for custom range."
                )
            default_from = from_time
        else:
            raise ValueError("Unsupported trend interval.")

        if to_time is None:
            to_time = now

        if from_time is None:
            from_time = default_from

        if from_time >= to_time:
            raise ValueError("from_time must be earlier than to_time.")

        points = await self.repository.get_trends(
            interval=interval,
            from_time=from_time,
            to_time=to_time,
        )

        return {
            "interval": interval,
            "points": points,
        }