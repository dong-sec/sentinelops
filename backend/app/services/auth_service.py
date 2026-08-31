from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repository import UserRepository
from app.security.jwt import create_access_token
from app.security.password import verify_password


class AuthService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = UserRepository(session)

    async def authenticate(
        self,
        username: str,
        password: str,
    ):
        user = await self.repository.get_by_username(username)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password.",
            )

        if user.status != "ACTIVE":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password.",
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password.",
            )

        await self.repository.update_last_login(user)

        role_name = user.role.name if user.role else "Viewer"

        token, expires_at = create_access_token(
            user_id=user.id,
            username=user.username,
            role=role_name,
        )

        await self.session.commit()

        return user, token, expires_at