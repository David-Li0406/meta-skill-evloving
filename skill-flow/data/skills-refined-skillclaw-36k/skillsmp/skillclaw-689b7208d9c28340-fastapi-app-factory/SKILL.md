---
name: fastapi-app-factory
description: Use this skill when you need to create a FastAPI application factory with lifespan management, middleware, pagination, and router configuration.
---

# FastAPI Application Factory

## Overview

This skill covers creating the FastAPI application factory pattern with proper lifespan management, middleware registration, pagination setup, and router configuration.

## Create main.py

Create `src/app/main.py`:

```python
import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app.api import api_router
from app.config import settings
from app.database import engine
from app.exception_handlers import register_exception_handlers
from app.logging import setup_logging
from app.middleware import CorrelationIdMiddleware

# Setup logging before anything else
setup_logging()

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan context manager.

    Handles startup and shutdown events:
    - Startup: Log application start, initialize resources
    - Shutdown: Close database connections, cleanup resources
    """
    # Startup
    logger.info(
        "Starting application",
        extra={
            "app_name": settings.app_name,
            "debug": settings.debug,
        },
    )

    yield

    # Shutdown
    logger.info("Shutting down application")
    await engine.dispose()
    logger.info("Database connections closed")

def create_app() -> FastAPI:
    """
    Application factory function.

    Creates and configures the FastAPI application with:
    - Lifespan management
    - Exception handlers
    - Middleware (correlation ID)
    - Pagination support
    - API routers

    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title=settings.app_name,
        debug=settings.debug,
        lifespan=lifespan,
        openapi_url="/api/openapi.json" if settings.debug else None,
        docs_url="/api/docs" if settings.debug else None,
        redoc_url="/api/redoc" if settings.debug else None,
    )

    # Register exception handlers
    register_exception_handlers(app)

    # Add middleware (order matters - first added = outermost)
    app.add_middleware(CorrelationIdMiddleware)

    # Add pagination support
    add_pagination(app)

    # Include API routers
    app.include_router(api_router)

    return app
```