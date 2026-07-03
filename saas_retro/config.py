from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import os


def _parse_bool(value: str, default: bool = False) -> bool:
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default


@dataclass(frozen=True)
class Settings:
    database_url: str
    database_echo: bool = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    database_url = os.getenv(
        "SAAS_RETRO_DB_URL",
        "mysql+pymysql://root:password@127.0.0.1:3306/saas_retro",
    )
    database_echo = _parse_bool(os.getenv("SAAS_RETRO_DB_ECHO", "false"))
    return Settings(database_url=database_url, database_echo=database_echo)
