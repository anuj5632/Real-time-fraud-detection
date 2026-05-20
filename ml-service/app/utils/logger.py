import logging
from typing import Optional

from app.config import settings

_configured = False


def _configure_logging() -> None:
    global _configured
    if _configured:
        return

    logging.basicConfig(
        level=settings.log_level.upper(),
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    _configured = True


def get_logger(name: Optional[str] = None) -> logging.Logger:
    _configure_logging()
    return logging.getLogger(name)
