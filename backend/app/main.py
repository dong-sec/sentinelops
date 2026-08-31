from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.router import api_router
from app.core.config import settings
from app.core.database import close_database
from app.core.logging import configure_logging
from app.core.redis import close_redis
from app.middleware.request_id import RequestIDMiddleware


configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

    await close_database()
    await close_redis()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

app.add_middleware(RequestIDMiddleware)

app.include_router(api_router)
