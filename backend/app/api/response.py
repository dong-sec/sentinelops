from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.response_repository import ResponseRepository
from app.schemas.response import (
    ResponseDetailResponse,
    ResponseExecuteRequest,
    ResponseExecuteResponse,
    ResponseListItem,
)
from app.security.dependencies import get_current_user, require_permission
from app.services.response_service import ResponseService


router = APIRouter(prefix="/responses")


def get_response_service(
    session: AsyncSession = Depends(get_db),
) -> ResponseService:
    repository = ResponseRepository(session)
    return ResponseService(repository)


@router.get(
    "",
    response_model=list[ResponseListItem],
    dependencies=[Depends(require_permission("response.read"))],
)
async def get_responses(
    current_user=Depends(get_current_user),
    service: ResponseService = Depends(get_response_service),
):
    return await service.get_all()


@router.get(
    "/{response_id}",
    response_model=ResponseDetailResponse,
    dependencies=[Depends(require_permission("response.read"))],
)
async def get_response(
    response_id: UUID,
    current_user=Depends(get_current_user),
    service: ResponseService = Depends(get_response_service),
):
    response = await service.get_by_id(response_id)

    if response is None:
        raise HTTPException(
            status_code=404,
            detail="Response not found.",
        )

    return response


@router.post(
    "",
    response_model=ResponseExecuteResponse,
    dependencies=[Depends(require_permission("response.execute"))],
)
async def execute_response(
    request: ResponseExecuteRequest,
    current_user=Depends(get_current_user),
    service: ResponseService = Depends(get_response_service),
):
    try:
        return await service.execute_response(
            action=request.action,
            target_type=request.target.type,
            target_value=request.target.value,
            duration_seconds=request.duration_seconds,
            reason=request.reason,
            source_event_id=request.source_event_id,
            user_id=current_user.id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )