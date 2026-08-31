from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.role import Role
from app.models.user import User


class UserRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:
        result = await self.session.execute(
            select(User)
            .options(
                selectinload(User.role).selectinload(
                    Role.permissions
                )
            )
            .where(User.id == user_id)
        )

        return result.scalar_one_or_none()

    async def get_by_username(
        self,
        username: str,
    ) -> User | None:
        result = await self.session.execute(
            select(User)
            .options(
                selectinload(User.role).selectinload(
                    Role.permissions
                )
            )
            .where(User.username == username)
        )

        return result.scalar_one_or_none()

    async def get_by_email(
        self,
        email: str,
    ) -> User | None:
        result = await self.session.execute(
            select(User)
            .options(
                selectinload(User.role).selectinload(
                    Role.permissions
                )
            )
            .where(User.email == email)
        )

        return result.scalar_one_or_none()

    async def create(
        self,
        user: User,
    ) -> User:
        self.session.add(user)

        await self.session.flush()
        await self.session.refresh(user)

        return user

    async def update_last_login(
        self,
        user: User,
    ) -> None:
        user.last_login_at = datetime.now(timezone.utc)

        await self.session.flush()