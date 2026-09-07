from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class SearchRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def count_events(self, q: str) -> int:
        query = """
            SELECT COUNT(DISTINCT se.id)
            FROM security_events se
            LEFT JOIN detections d
                ON d.event_id = se.id
            WHERE
                CAST(se.id AS text) ILIKE :q
                OR CAST(se.source_ip AS text) ILIKE :q
                OR se.request_uri ILIKE :q
                OR COALESCE(d.detection_type, '') ILIKE :q
                OR COALESCE(se.user_agent, '') ILIKE :q
                OR COALESCE(d.rule_name, '') ILIKE :q
        """

        result = await self.session.execute(
            text(query),
            {"q": f"%{q}%"},
        )

        return result.scalar_one()

    async def search_events(
        self,
        q: str,
        page: int = 1,
        page_size: int = 20,
    ) -> list[dict]:
        query = """
            SELECT DISTINCT ON (se.id)
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
            WHERE
                CAST(se.id AS text) ILIKE :q
                OR CAST(se.source_ip AS text) ILIKE :q
                OR se.request_uri ILIKE :q
                OR COALESCE(d.detection_type, '') ILIKE :q
                OR COALESCE(se.user_agent, '') ILIKE :q
                OR COALESCE(d.rule_name, '') ILIKE :q
            ORDER BY
                se.id,
                d.detected_at DESC NULLS LAST,
                rs.calculated_at DESC NULLS LAST
        """

        result = await self.session.execute(
            text(query),
            {
                "q": f"%{q}%",
            },
        )

        rows = list(result)

        offset = (page - 1) * page_size
        rows = rows[offset : offset + page_size]

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
            for row in rows
        ]