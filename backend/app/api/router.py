from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.users import router as users_router
from app.api.dashboard import router as dashboard_router
from app.api.search import router as search_router
from app.api.events import router as events_router
from app.api.policy import router as policy_router


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(dashboard_router)
api_router.include_router(search_router)
api_router.include_router(events_router)
api_router.include_router(policy_router)