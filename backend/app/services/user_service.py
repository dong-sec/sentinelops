from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository
from app.security.password import hash_password


class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = UserRepository(session)
        self.role_repository = RoleRepository(session)

    async def get_all(self):
        return await self.repository.get_all()

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

    async def update_user(
        self,
        user_id: UUID,
        username: str | None = None,
        email: str | None = None,
        password: str | None = None,
        role_name: str | None = None,
    ) -> User:
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise ValueError("User not found.")

        if username is not None and username != user.username:
            existing_user = await self.repository.get_by_username(username)

            if existing_user:
                raise ValueError("Username already exists.")

            user.username = username

        if email is not None and email != user.email:
            existing_email = await self.repository.get_by_email(email)

            if existing_email:
                raise ValueError("Email already exists.")

            user.email = email

        if password is not None:
            user.password_hash = hash_password(password)

        if role_name is not None:
            role = await self.role_repository.get_by_name(role_name)

            if role is None:
                raise ValueError("Role not found.")

            user.role_id = role.id

        try:
            user = await self.repository.update(user)
            await self.session.commit()

            return await self.repository.get_by_id(user.id)

        except Exception:
            await self.session.rollback()
            raise

    async def disable_user(
        self,
        user_id: UUID,
    ) -> User:
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise ValueError("User not found.")

        if user.status == "DISABLED":
            raise ValueError("User already disabled.")

        try:
            user = await self.repository.disable(user)

            await self.session.commit()

            return await self.repository.get_by_id(user.id)

        except Exception:
            await self.session.rollback()
            raise

    async def enable_user(
        self,
        user_id: UUID,
    ) -> User:
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise ValueError("User not found.")

        if user.status == "ACTIVE":
            raise ValueError("User already enabled.")

        try:
            user = await self.repository.enable(user)

            await self.session.commit()

            return await self.repository.get_by_id(user.id)

        except Exception:
            await self.session.rollback()
            raise

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

        try:
            user = await self.repository.create(user)
            await self.session.commit()

            return await self.repository.get_by_id(user.id)

        except Exception:
            await self.session.rollback()
            raise