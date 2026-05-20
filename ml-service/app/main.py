from fastapi import FastAPI

from app.api.routes import router
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(title=settings.app_name)
app.include_router(router)


@app.on_event("startup")
def on_startup() -> None:
    logger.info("Starting %s", settings.app_name)
