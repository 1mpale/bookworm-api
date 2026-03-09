# Copyright 2024 BookWorm Inc. All rights reserved.

"""FastAPI application entry point."""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from modules.shared.__config.logging_config import setup_logging
from modules.shared.setup import initialize
from modules.shared.services.auth.jwt_middleware import JwtMiddleware
from modules.shared.services.rate_limiter import RateLimitMiddleware
from workers.api.routes import (
    book_router,
    review_router,
    search_router,
    collection_router,
    export_router,
    health_router,
    admin_router,
)

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    """Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance.
    """
    setup_logging()
    initialize()

    app = FastAPI(
        title="BookWorm API",
        description="Book management and recommendation platform",
        version="1.1.0",
    )

    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RateLimitMiddleware)
    app.add_middleware(JwtMiddleware)

    # Routes
    app.include_router(health_router.router)
    app.include_router(book_router.router, prefix="/api/v1")
    app.include_router(review_router.router, prefix="/api/v1")
    app.include_router(search_router.router, prefix="/api/v1")
    app.include_router(collection_router.router, prefix="/api/v1")
    app.include_router(export_router.router, prefix="/api/v1")
    app.include_router(admin_router.router, prefix="/api/v1")

    logger.info("BookWorm API initialized")
    return app


app = create_app()
