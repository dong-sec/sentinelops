from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class DashboardRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_total_events(self) -> int:
        result = await self.session.execute(
            text("""
                SELECT COUNT(*)
                FROM security_events
            """)
        )
        return result.scalar_one()

    async def get_critical_events(self) -> int:
        result = await self.session.execute(
            text("""
                SELECT COUNT(*)
                FROM risk_scores
                WHERE severity = 'CRITICAL'
            """)
        )
        return result.scalar_one()

    async def get_high_risk_events(self) -> int:
        result = await self.session.execute(
            text("""
                SELECT COUNT(*)
                FROM risk_scores
                WHERE severity IN ('HIGH', 'CRITICAL')
            """)
        )
        return result.scalar_one()

    async def get_blocked_ips(self) -> int:
        result = await self.session.execute(
            text("""
                SELECT COUNT(*)
                FROM ip_lists
                WHERE list_type = 'BLACKLIST'
                  AND enabled = TRUE
                  AND (
                      expires_at IS NULL
                      OR expires_at > NOW()
                  )
            """)
        )
        return result.scalar_one()

    async def get_active_incidents(self) -> int:
        result = await self.session.execute(
            text("""
                SELECT COUNT(*)
                FROM incidents
                WHERE status NOT IN ('RESOLVED', 'CLOSED')
            """)
        )
        return result.scalar_one()

    async def get_automatic_responses(self) -> int:
        result = await self.session.execute(
            text("""
                SELECT COUNT(*)
                FROM responses
                WHERE initiated_by IS NULL
                  AND status = 'SUCCESS'
            """)
        )
        return result.scalar_one()

    async def get_response_failures(self) -> int:
        result = await self.session.execute(
            text("""
                SELECT COUNT(*)
                FROM responses
                WHERE status = 'FAILED'
            """)
        )
        return result.scalar_one()

    async def get_risk_distribution(self) -> dict:
        result = await self.session.execute(
            text("""
                SELECT
                    severity,
                    COUNT(*) AS count
                FROM risk_scores
                GROUP BY severity
            """)
        )

        distribution = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        }

        for severity, count in result.all():
            distribution[severity.lower()] = count

        return distribution

    async def get_attack_distribution(self) -> list[dict]:
        result = await self.session.execute(
            text("""
                SELECT
                    detection_type AS attack_type,
                    COUNT(*) AS count
                FROM detections
                GROUP BY detection_type
                ORDER BY count DESC, detection_type
            """)
        )

        return [
            {
                "attack_type": row.attack_type,
                "count": row.count,
            }
            for row in result
        ]

    async def get_recent_critical_events(self, limit: int = 10) -> list[dict]:
        result = await self.session.execute(
            text("""
                SELECT
                    se.id,
                    se.event_time AS timestamp,
                    se.source_ip,
                    d.detection_type AS attack_type,
                    rs.severity,
                    se.event_status AS status
                FROM security_events se
                JOIN risk_scores rs
                  ON rs.event_id = se.id
                LEFT JOIN detections d
                  ON d.event_id = se.id
                WHERE rs.severity = 'CRITICAL'
                ORDER BY se.event_time DESC
                LIMIT :limit
            """),
            {"limit": limit},
        )

        return [
            {
                "id": str(row.id),
                "timestamp": row.timestamp,
                "source_ip": str(row.source_ip),
                "attack_type": row.attack_type,
                "severity": row.severity,
                "status": row.status,
            }
            for row in result
        ]

    async def get_service_health(self) -> list[dict]:
        result = await self.session.execute(
            text("""
                SELECT
                    service_name,
                    status,
                    health_status,
                    cpu_percent,
                    memory_percent,
                    disk_percent,
                    last_check_at
                FROM service_statuses
                ORDER BY service_name
            """)
        )

        return [
            {
                "service_name": row.service_name,
                "status": row.status,
                "health_status": row.health_status,
                "cpu_percent": row.cpu_percent,
                "memory_percent": row.memory_percent,
                "disk_percent": row.disk_percent,
                "last_check_at": row.last_check_at,
            }
            for row in result
        ]

    async def get_recent_responses(self, limit: int = 10) -> list[dict]:
        result = await self.session.execute(
            text("""
                SELECT
                    id,
                    response_type,
                    target_ip,
                    status,
                    created_at
                FROM responses
                ORDER BY created_at DESC
                LIMIT :limit
            """),
            {"limit": limit},
        )

        return [
            {
                "id": str(row.id),
                "response_type": row.response_type,
                "target_ip": str(row.target_ip) if row.target_ip is not None else None,
                "status": row.status,
                "created_at": row.created_at,
            }
            for row in result
        ]

    async def get_trends(
        self,
        interval: str,
        from_time,
        to_time,
    ) -> list[dict]:
        if interval == "custom":
            bucket_interval = "1 hour"
        else:
            interval_map = {
                "1h": "1 hour",
                "6h": "1 hour",
                "24h": "1 hour",
                "7d": "1 hour",
                "30d": "1 hour",
            }

            bucket_interval = interval_map.get(interval)

            if bucket_interval is None:
                raise ValueError("Unsupported trend interval.")

        result = await self.session.execute(
            text("""
                WITH time_buckets AS (
                    SELECT generate_series(
                        :from_time,
                        :to_time,
                        INTERVAL '1 hour'
                    ) AS timestamp
                ),
                event_counts AS (
                    SELECT
                        date_trunc('hour', event_time) AS timestamp,
                        COUNT(*) AS events
                    FROM security_events
                    WHERE event_time >= :from_time
                      AND event_time <= :to_time
                    GROUP BY date_trunc('hour', event_time)
                ),
                critical_counts AS (
                    SELECT
                        date_trunc('hour', calculated_at) AS timestamp,
                        COUNT(*) AS critical
                    FROM risk_scores
                    WHERE severity = 'CRITICAL'
                      AND calculated_at >= :from_time
                      AND calculated_at <= :to_time
                    GROUP BY date_trunc('hour', calculated_at)
                ),
                high_counts AS (
                    SELECT
                        date_trunc('hour', calculated_at) AS timestamp,
                        COUNT(*) AS high
                    FROM risk_scores
                    WHERE severity = 'HIGH'
                      AND calculated_at >= :from_time
                      AND calculated_at <= :to_time
                    GROUP BY date_trunc('hour', calculated_at)
                ),
                blocked_counts AS (
                    SELECT
                        date_trunc('hour', created_at) AS timestamp,
                        COUNT(*) AS blocked
                    FROM responses
                    WHERE status = 'SUCCESS'
                      AND created_at >= :from_time
                      AND created_at <= :to_time
                    GROUP BY date_trunc('hour', created_at)
                )
                SELECT
                    tb.timestamp,
                    COALESCE(ec.events, 0) AS events,
                    COALESCE(cc.critical, 0) AS critical,
                    COALESCE(hc.high, 0) AS high,
                    COALESCE(bc.blocked, 0) AS blocked
                FROM time_buckets tb
                LEFT JOIN event_counts ec
                  ON ec.timestamp = tb.timestamp
                LEFT JOIN critical_counts cc
                  ON cc.timestamp = tb.timestamp
                LEFT JOIN high_counts hc
                  ON hc.timestamp = tb.timestamp
                LEFT JOIN blocked_counts bc
                  ON bc.timestamp = tb.timestamp
                ORDER BY tb.timestamp
            """),
            {
                "from_time": from_time,
                "to_time": to_time,
            },
        )

        return [
            {
                "timestamp": row.timestamp,
                "events": row.events,
                "critical": row.critical,
                "high": row.high,
                "blocked": row.blocked,
            }
            for row in result
        ]