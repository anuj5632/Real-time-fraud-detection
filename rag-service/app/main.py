from __future__ import annotations

import logging

from fastapi import FastAPI

from app.api.routes import router as api_router
from app.config import get_settings


def create_app() -> FastAPI:
	settings = get_settings()
	logging.basicConfig(level=logging.INFO)

	app = FastAPI(title=settings.app_name)
	app.include_router(api_router, prefix=settings.api_prefix)
	return app


app = create_app()
