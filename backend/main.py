"""FastAPI application entrypoint.

Configures CORS, middleware, and routers.
"""

from contextlib import asynccontextmanager

from backend.app.api.router import router
from backend.app.core.config import settings
from backend.app.core.logging import RequestIdMiddleware, setup_logging
from backend.app.core.rate_limit import limiter
from backend.app.db.database import create_tables
from backend.app.services.inference import initialize_inference_service
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for startup and shutdown."""
    # Setup logging
    setup_logging(settings.log_level)

    # Initialize services
    initialize_inference_service()

    # Initialize database tables
    await create_tables()

    yield
    # Shutdown logic if needed


app = FastAPI(
    title="AgriVision API",
    description="Tomato disease diagnosis API",
    version="1.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middleware
app.add_middleware(RequestIdMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(router)


@app.get("/")
async def root():
    """Describe the API and direct operators to its documentation."""
    return {"message": "AgriVision API is running. See /docs for API documentation."}
