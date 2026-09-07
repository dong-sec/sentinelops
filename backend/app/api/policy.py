from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.policy import (
    PolicyCreateRequest,
    PolicyResponse,
    PolicyUpdateRequest,
    PolicyValidationRequest,
    PolicyValidationResponse,
)
from app.security.dependencies import require_permission
from app.services.policy_service import PolicyService


router = APIRouter(prefix="/policies")


@router.post(
    "/validate",
    response_model=PolicyValidationResponse,
)
async def validate_policy(
    request: PolicyValidationRequest,
    current_user=Depends(require_permission("policy.write")),
    session: AsyncSession = Depends(get_db),
):
    service = PolicyService(session)

    valid, warnings = await service.validate_policy(
        condition=request.condition,
        action=request.action,
    )

    return PolicyValidationResponse(
        valid=valid,
        warnings=warnings,
    )

@router.get(
    "",
    response_model=list[PolicyResponse],
)
async def list_policies(
    current_user=Depends(require_permission("policy.read")),
    session: AsyncSession = Depends(get_db),
):
    service = PolicyService(session)

    return await service.get_all()


@router.post(
    "",
    response_model=PolicyResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_policy(
    request: PolicyCreateRequest,
    current_user=Depends(require_permission("policy.write")),
    session: AsyncSession = Depends(get_db),
):
    service = PolicyService(session)

    try:
        return await service.create_policy(
            name=request.name,
            description=request.description,
            enabled=request.enabled,
            priority=request.priority,
            action=request.action,
            duration_seconds=request.duration_seconds,
            rules=[
                rule.model_dump()
                for rule in request.rules
            ],
            user_id=current_user.id,
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        )


@router.post(
    "/{policy_id}/enable",
    response_model=PolicyResponse,
)
async def enable_policy(
    policy_id: UUID,
    current_user=Depends(require_permission("policy.write")),
    session: AsyncSession = Depends(get_db),
):
    service = PolicyService(session)

    try:
        return await service.enable_policy(
            policy_id=policy_id,
            user_id=current_user.id,
        )

    except ValueError as exc:
        detail = str(exc)

        if detail == "Policy not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail,
            )

        if detail == "Policy already enabled.":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=detail,
            )

        raise


@router.post(
    "/{policy_id}/disable",
    response_model=PolicyResponse,
)
async def disable_policy(
    policy_id: UUID,
    current_user=Depends(require_permission("policy.write")),
    session: AsyncSession = Depends(get_db),
):
    service = PolicyService(session)

    try:
        return await service.disable_policy(
            policy_id=policy_id,
            user_id=current_user.id,
        )

    except ValueError as exc:
        detail = str(exc)

        if detail == "Policy not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail,
            )

        if detail == "Policy already disabled.":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=detail,
            )

        raise


@router.get(
    "/{policy_id}",
    response_model=PolicyResponse,
)
async def get_policy(
    policy_id: UUID,
    current_user=Depends(require_permission("policy.read")),
    session: AsyncSession = Depends(get_db),
):
    service = PolicyService(session)

    policy = await service.get_by_id(policy_id)

    if policy is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Policy not found.",
        )

    return policy


@router.patch(
    "/{policy_id}",
    response_model=PolicyResponse,
)
async def update_policy(
    policy_id: UUID,
    request: PolicyUpdateRequest,
    current_user=Depends(require_permission("policy.write")),
    session: AsyncSession = Depends(get_db),
):
    service = PolicyService(session)

    try:
        return await service.update_policy(
            policy_id=policy_id,
            name=request.name,
            description=request.description,
            enabled=request.enabled,
            priority=request.priority,
            action=request.action,
            duration_seconds=request.duration_seconds,
            rules=(
                [
                    rule.model_dump()
                    for rule in request.rules
                ]
                if request.rules is not None
                else None
            ),
            user_id=current_user.id,
        )

    except ValueError as exc:
        detail = str(exc)

        if detail == "Policy not found.":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail,
            )

        if detail == "Policy name already exists.":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=detail,
            )

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )

        
@router.delete(
    "/{policy_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_policy(
    policy_id: UUID,
    current_user=Depends(require_permission("policy.write")),
    session: AsyncSession = Depends(get_db),
):
    service = PolicyService(session)

    try:
        await service.delete_policy(policy_id)

    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )