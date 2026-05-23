from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import settings
from app.dependencies import close_providers
from app.middleware.rate_limit import RateLimitMiddleware
from app.routers.health import router as health_router
from app.routers.translate import router as translate_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await close_providers()


def create_app() -> FastAPI:
    app = FastAPI(title="Screenshot Translation API", version="0.1.0", lifespan=lifespan)
    app.add_middleware(
        RateLimitMiddleware,
        max_requests=settings.rate_limit_per_minute,
        window_seconds=60,
    )
    app.include_router(health_router)
    app.include_router(translate_router)
    return app


app = create_app()
