from datetime import datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class EventsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def count_events(
        self,
        severity: str | None = None,
        risk_level: str | None = None,
        attack_type: str | None = None,
        source_ip: str | None = None,
        status: str | None = None,
        method: str | None = None,
        from_time: datetime | None = None,
        to_time: datetime | None = None,
    ) -> int:
        query = """
            SELECT COUNT(DISTINCT se.id)
            FROM security_events se
            LEFT JOIN detections d
                ON d.event_id = se.id
            LEFT JOIN risk_scores rs
                ON rs.event_id = se.id
            WHERE 1 = 1
        """

        params = {}

        if severity is not None:
            query += " AND rs.severity = :severity"
            params["severity"] = severity

        if risk_level is not None:
            query += " AND rs.severity = :risk_level"
            params["risk_level"] = risk_level

        if attack_type is not None:
            query += " AND d.detection_type = :attack_type"
            params["attack_type"] = attack_type

        if source_ip is not None:
            query += " AND se.source_ip = CAST(:source_ip AS inet)"
            params["source_ip"] = source_ip

        if status is not None:
            query += " AND se.event_status = :status"
            params["status"] = status

        if method is not None:
            query += " AND se.method = :method"
            params["method"] = method

        if from_time is not None:
            query += " AND se.event_time >= :from_time"
            params["from_time"] = from_time

        if to_time is not None:
            query += " AND se.event_time <= :to_time"
            params["to_time"] = to_time

        result = await self.session.execute(text(query), params)

        return result.scalar_one()

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
    ) -> list[dict]:
        query = """
            SELECT
                se.id,
                se.event_time AS timestamp,
                se.source_ip,
                d.detection_type AS attack_type,
                rs.severity,
                rs.score AS risk_score,
                rs.severity AS risk_level,
                se.event_status AS status,
                CASE
                    WHEN EXISTS (
                        SELECT 1
                        FROM responses r
                        WHERE r.event_id = se.id
                          AND r.status = 'SUCCESS'
                    )
                    THEN 'SUCCESS'
                    WHEN EXISTS (
                        SELECT 1
                        FROM responses r
                        WHERE r.event_id = se.id
                          AND r.status = 'FAILED'
                    )
                    THEN 'FAILED'
                    ELSE NULL
                END AS response_status
            FROM security_events se
            LEFT JOIN detections d
                ON d.event_id = se.id
            LEFT JOIN risk_scores rs
                ON rs.event_id = se.id
            WHERE 1 = 1
        """

        params = {
            "limit": page_size,
            "offset": (page - 1) * page_size,
        }

        if severity is not None:
            query += " AND rs.severity = :severity"
            params["severity"] = severity

        if risk_level is not None:
            query += " AND rs.severity = :risk_level"
            params["risk_level"] = risk_level

        if attack_type is not None:
            query += " AND d.detection_type = :attack_type"
            params["attack_type"] = attack_type

        if source_ip is not None:
            query += " AND se.source_ip = CAST(:source_ip AS inet)"
            params["source_ip"] = source_ip

        if status is not None:
            query += " AND se.event_status = :status"
            params["status"] = status

        if method is not None:
            query += " AND se.method = :method"
            params["method"] = method

        if from_time is not None:
            query += " AND se.event_time >= :from_time"
            params["from_time"] = from_time

        if to_time is not None:
            query += " AND se.event_time <= :to_time"
            params["to_time"] = to_time

        sort_columns = {
            "event_time": "se.event_time",
            "severity": "rs.severity",
            "risk_score": "rs.score",
            "source_ip": "se.source_ip",
        }

        order_column = sort_columns.get(sort_by, "se.event_time")
        order_direction = "ASC" if sort_order.lower() == "asc" else "DESC"

        query += f"""
            ORDER BY {order_column} {order_direction}, se.id
            LIMIT :limit
            OFFSET :offset
        """

        result = await self.session.execute(text(query), params)

        return [
            {
                "id": str(row.id),
                "timestamp": row.timestamp,
                "source_ip": str(row.source_ip),
                "attack_type": row.attack_type,
                "severity": row.severity,
                "risk_score": row.risk_score,
                "risk_level": row.risk_level,
                "status": row.status,
                "response_status": row.response_status,
            }
            for row in result
        ]

    async def get_event(self, event_id: str) -> dict | None:
        result = await self.session.execute(
            text(
                """
                SELECT
                    se.id,
                    se.event_time AS timestamp,
                    se.source_ip,
                    se.method,
                    se.request_uri,
                    se.protocol,
                    se.status_code,
                    se.user_agent,
                    se.referer,
                    se.request_size,
                    se.response_size,
                    se.response_time_ms,
                    se.host,
                    se.server_name,
                    se.raw_log,
                    se.event_status AS status,
                    se.created_at,
                    d.detection_type AS attack_type,
                    d.rule_name,
                    d.severity AS detection_severity,
                    d.confidence,
                    d.evidence,
                    d.description AS detection_description,
                    rs.score AS risk_score,
                    rs.severity AS risk_level,
                    rs.calculation_version,
                    rs.factors,
                    rs.calculated_at
                FROM security_events se
                LEFT JOIN detections d
                    ON d.event_id = se.id
                LEFT JOIN risk_scores rs
                    ON rs.event_id = se.id
                WHERE se.id = CAST(:event_id AS uuid)
                ORDER BY d.detected_at DESC NULLS LAST,
                         rs.calculated_at DESC NULLS LAST
                LIMIT 1
                """
            ),
            {"event_id": event_id},
        )

        row = result.first()

        if row is None:
            return None

        return {
            "id": str(row.id),
            "timestamp": row.timestamp,
            "source_ip": str(row.source_ip),
            "method": row.method,
            "request_uri": row.request_uri,
            "protocol": row.protocol,
            "status_code": row.status_code,
            "user_agent": row.user_agent,
            "referer": row.referer,
            "request_size": row.request_size,
            "response_size": row.response_size,
            "response_time_ms": row.response_time_ms,
            "host": row.host,
            "server_name": row.server_name,
            "raw_log": row.raw_log,
            "status": row.status,
            "created_at": row.created_at,
            "attack_type": row.attack_type,
            "rule_name": row.rule_name,
            "detection_severity": row.detection_severity,
            "confidence": row.confidence,
            "evidence": row.evidence,
            "detection_description": row.detection_description,
            "risk_score": row.risk_score,
            "risk_level": row.risk_level,
            "calculation_version": row.calculation_version,
            "factors": row.factors,
            "calculated_at": row.calculated_at,
        }

    async def get_event_detections(self, event_id: str) -> list[dict]:
        result = await self.session.execute(
            text(
                """
                SELECT
                    id,
                    detection_type,
                    rule_name,
                    severity,
                    confidence,
                    evidence,
                    description,
                    detected_at
                FROM detections
                WHERE event_id = CAST(:event_id AS uuid)
                ORDER BY detected_at DESC, id
                """
            ),
            {"event_id": event_id},
        )

        return [
            {
                "id": str(row.id),
                "detection_type": row.detection_type,
                "rule_name": row.rule_name,
                "severity": row.severity,
                "confidence": row.confidence,
                "evidence": row.evidence,
                "description": row.description,
                "detected_at": row.detected_at,
            }
            for row in result
        ]

    async def get_event_risk(self, event_id: str) -> list[dict]:
        result = await self.session.execute(
            text(
                """
                SELECT
                    id,
                    source_ip,
                    score,
                    severity,
                    calculation_version,
                    factors,
                    calculated_at
                FROM risk_scores
                WHERE event_id = CAST(:event_id AS uuid)
                ORDER BY calculated_at DESC, id
                """
            ),
            {"event_id": event_id},
        )

        return [
            {
                "id": str(row.id),
                "source_ip": str(row.source_ip),
                "score": row.score,
                "severity": row.severity,
                "calculation_version": row.calculation_version,
                "factors": row.factors,
                "calculated_at": row.calculated_at,
            }
            for row in result
        ]

    async def get_event_timeline(self, event_id: str) -> list[dict]:
        result = await self.session.execute(
            text(
                """
                SELECT
                    event_time AS timestamp,
                    'EVENT' AS event_type,
                    event_status AS status,
                    NULL::text AS description
                FROM security_events
                WHERE id = CAST(:event_id AS uuid)

                UNION ALL

                SELECT
                    detected_at AS timestamp,
                    'DETECTION' AS event_type,
                    severity AS status,
                    description
                FROM detections
                WHERE event_id = CAST(:event_id AS uuid)

                UNION ALL

                SELECT
                    calculated_at AS timestamp,
                    'RISK' AS event_type,
                    severity AS status,
                    NULL::text AS description
                FROM risk_scores
                WHERE event_id = CAST(:event_id AS uuid)

                UNION ALL

                SELECT
                    created_at AS timestamp,
                    'RESPONSE' AS event_type,
                    status,
                    reason AS description
                FROM responses
                WHERE event_id = CAST(:event_id AS uuid)

                ORDER BY timestamp ASC
                """
            ),
            {"event_id": event_id},
        )

        return [
            {
                "timestamp": row.timestamp,
                "event_type": row.event_type,
                "status": row.status,
                "description": row.description,
            }
            for row in result
        ]