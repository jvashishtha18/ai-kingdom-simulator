import logging
import sys
from app.core.config import settings

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)


def setup_logger() -> None:
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=LOG_FORMAT,
        handlers=[logging.StreamHandler(sys.stdout)],
        force= True,
    )


logger = logging.getLogger("ai_kingdom")