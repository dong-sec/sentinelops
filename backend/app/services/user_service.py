from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.security.password import hash_password


class UserService:

    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.role_repository = RoleRepository(session)

    async def get_by_id(
        self,
        user_id: UUID,
    ):
        return await self.repository.get_by_id(user_id)

    async def get_by_username(
        self,
        username: str,
    ):
        return await self.repository.get_by_username(username)

    async def create_user(
        self,
        username: str,
        email: str | None,
        password: str,
        role_name: str,
    ) -> User:
        existing_user = await self.repository.get_by_username(username)

        if existing_user:
            raise ValueError("Username already exists.")

        if email:
            existing_email = await self.repository.get_by_email(email)

            if existing_email:
                raise ValueError("Email already exists.")

        role = await self.role_repository.get_by_name(role_name)

        if role is None:
            raise ValueError("Role not found.")

        user = User(
            username=username,
            email=email,
            password_hash=hash_password(password),
            role_id=role.id,
            status="ACTIVE",
        )

        return await self.repository.create(user)