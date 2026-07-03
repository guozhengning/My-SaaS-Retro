from __future__ import annotations

from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from saas_retro.config import get_settings


@lru_cache(maxsize=1)
def create_db_engine() -> Engine:
    settings = get_settings()
    return create_engine(
        settings.database_url,
        echo=settings.database_echo,
        pool_pre_ping=True,
        future=True,
    )


def get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(
        bind=create_db_engine(),
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )


def get_session() -> Session:
    return get_session_factory()()
