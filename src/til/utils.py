from datetime import datetime, timezone
import logging
from pathlib import Path

from til.errors import TilConfigNotFoundError


logger = logging.getLogger(__name__)


def load_env(path: Path) -> dict[str, str]:
    logger.info(f"Loading env from file {path}")

    if not path.is_file():
        logger.error(f"Error loading env from file {path}")
        raise TilConfigNotFoundError(path)

    env_vars = {}
    for line in path.read_text().splitlines():
        if line.strip() != "" and not line.startswith("#"):
            key, _, value = line.strip().partition("=")
            env_vars[key] = value.strip().strip("'\"")
            logger.debug(f"Loaded env var {key}={value}")

    return env_vars


def datetime_now(tz: timezone | None = None) -> datetime:
    tz = tz or timezone.utc
    return datetime.now(tz)


def today() -> datetime.date:
    return datetime_now().date()
