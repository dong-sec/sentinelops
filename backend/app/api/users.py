from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserCreateRequest, UserResponse, UserUpdateRequest
from app.security.dependencies import require_permission
from app.services.user_service import UserService


router = APIRouter(prefix="/users")


def to_user_response(user) -> UserResponse:
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role.name if user.role else "Viewer",
        status=user.status,
    )


@router.get(
    "",
    response_model=list[UserResponse],
)
async def list_users(
    current_user=Depends(require_permission("user.read")),
    session: AsyncSession = Depends(get_db),
):
    service = UserService(session)

    users = await service.get_all()

    return [
        to_user_response(user)
        for user in users
    ]


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    request: UserCreateRequest,
    current_user=Depends(require_permission("user.write")),
    session: AsyncSession = Depends(get_db),
):
    service = UserService(session)

    try:
        user = await service.create_user(
            username=request.username,
            email=request.email,
            password=request.password,
            role_name=request.role,
        )

    except ValueError as exc:
        detail = str(exc)

        if detail == "Username already exists.":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=detail,
            )

        if detail == "Email already exists.":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=detail,
            )

        if detail == "Role not found.":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail,
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )

    return to_user_response(user)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
)
async def get_user(
    user_id: UUID,
    current_user=Depends(require_permission("user.read")),
    session: AsyncSession = Depends(get_db),
):
    service = UserService(session)

    user = await service.get_by_id(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return to_user_response(user)


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
)
async def update_user(
    user_id: UUID,
    request: UserUpdateRequest,
    current_user=Depends(require_permission("user.write")),
    session: AsyncSession = Depends(get_db),
):
    service = UserService(session)

    try:
        user = await service.update_user(
            user_id=user_id,
            username=request.username,
            email=request.email,
            password=request.password,
            role_name=request.role,
        )

    except ValueError as exc:
        detail = str(exc)

        if detail in {
            "Username already exists.",
            "Email already exists.",
        }:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=detail,
            )

        if detail == "User not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail,
            )

        if detail == "Role not found.":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=detail,
            )

        raise

    return to_user_response(user)


@router.post(
    "/{user_id}/disable",
    response_model=UserResponse,
)
async def disable_user(
    user_id: UUID,
    current_user=Depends(require_permission("user.write")),
    session: AsyncSession = Depends(get_db),
):
    service = UserService(session)

    try:
        user = await service.disable_user(user_id)

    except ValueError as exc:
        detail = str(exc)

        if detail == "User not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail,
            )

        if detail == "User already disabled.":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=detail,
            )

        raise

    return to_user_response(user)


@router.post(
    "/{user_id}/enable",
    response_model=UserResponse,
)
async def enable_user(
    user_id: UUID,
    current_user=Depends(require_permission("user.write")),
    session: AsyncSession = Depends(get_db),
):
    service = UserService(session)

    try:
        user = await service.enable_user(user_id)

    except ValueError as exc:
        detail = str(exc)

        if detail == "User not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail,
            )

        if detail == "User already enabled.":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=detail,
            )

        raise

    return to_user_response(user)