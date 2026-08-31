from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.security.jwt import decode_access_token

from app.models.permission import Permission
from app.models.role import Role

bearer_scheme = HTTPBearer()

def require_permission(permission_code: str):

    async def permission_checker(
        current_user=Depends(get_current_user),
    ):
        role = current_user.role

        if role is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions.",
            )

        permission_codes = {
            permission.code
            for permission in role.permissions
        }

        if permission_code not in permission_codes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions.",
            )

        return current_user

    return permission_checker

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    session: AsyncSession = Depends(get_db),
):
    try:
        payload = decode_access_token(
            credentials.credentials
        )

        user_id = UUID(payload["sub"])

    except (ValueError, KeyError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials.",
        )

    repository = UserRepository(session)

    user = await repository.get_by_id(user_id)

    if user is None or user.status != "ACTIVE":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials.",
        )

    return user