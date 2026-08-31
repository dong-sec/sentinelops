from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.auth import LoginRequest
from app.security.dependencies import get_current_user
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth")


@router.post("/login")
async def login(
    request: LoginRequest,
    session: AsyncSession = Depends(get_db),
):
    service = AuthService(session)

    user, token, expires_at = await service.authenticate(
        username=request.username,
        password=request.password,
    )

    role_name = user.role.name if user.role else "Viewer"

    return {
        "success": True,
        "data": {
            "user": {
                "id": str(user.id),
                "username": user.username,
                "role": role_name,
            },
            "session": {
                "access_token": token,
                "token_type": "bearer",
                "expires_at": expires_at,
            },
        },
        "meta": {},
    }


@router.get("/me")
async def current_user(
    user=Depends(get_current_user),
):
    role_name = user.role.name if user.role else "Viewer"

    permissions = []

    if user.role:
        permissions = [
            permission.code
            for permission in user.role.permissions
        ]

    return {
        "success": True,
        "data": {
            "id": str(user.id),
            "username": user.username,
            "role": role_name,
            "permissions": permissions,
        },
        "meta": {},
    }


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(
    user=Depends(get_current_user),
):
    return {
        "success": True,
        "data": None,
        "meta": {},
    }