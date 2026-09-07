from uuid import UUID

from app.models.response import Response, ResponseStep
from app.repositories.response_repository import ResponseRepository


class ResponseService:

    def __init__(self, repository: ResponseRepository):
        self.repository = repository

    async def get_all(self) -> list[Response]:
        return await self.repository.get_all()

    async def get_by_id(
        self,
        response_id: UUID,
    ) -> Response | None:
        return await self.repository.get_by_id(response_id)

    async def execute_response(
        self,
        action: str,
        target_type: str,
        target_value: str,
        duration_seconds: int | None,
        reason: str | None,
        source_event_id: UUID | None,
        user_id: UUID,
    ) -> Response:
        response = Response(
            event_id=source_event_id,
            initiated_by=user_id,
            response_type=action,
            target_ip=target_value if target_type == "ip" else None,
            status="PENDING",
            reason=reason,
        )

        response = await self.repository.create(response)

        step = ResponseStep(
            response_id=response.id,
            step_order=1,
            step_type="VALIDATION",
            status="PENDING",
            message="Response validation queued.",
            metadata_={
                "target_type": target_type,
                "duration_seconds": duration_seconds,
            },
        )

        await self.repository.create_step(step)

        await self.repository.session.commit()

        return await self.repository.get_by_id(response.id)