from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.response import Response, ResponseStep


class ResponseRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> list[Response]:
        result = await self.session.execute(
            select(Response)
            .options(
                selectinload(Response.steps)
            )
            .order_by(
                Response.created_at.desc(),
            )
        )

        return list(result.scalars().unique().all())

    async def get_by_id(
        self,
        response_id: UUID,
    ) -> Response | None:
        result = await self.session.execute(
            select(Response)
            .options(
                selectinload(Response.steps)
            )
            .where(Response.id == response_id)
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        response: Response,
    ) -> Response:
        self.session.add(response)

        await self.session.flush()
        await self.session.refresh(response)

        return response

    async def create_step(
        self,
        step: ResponseStep,
    ) -> ResponseStep:
        self.session.add(step)

        await self.session.flush()
        await self.session.refresh(step)

        return step