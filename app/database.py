from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import get_settings

settings = get_settings()

if not settings.database_url.strip():
    raise RuntimeError(
        "DATABASE_URL is missing or empty. Set it in your environment "
        "(or use `railway run ...` to inject Railway variables locally)."
    )

def _normalize_database_url(url: str) -> str:
    """Use psycopg v3 (installed) instead of SQLAlchemy's default psycopg2 driver."""
    if url.startswith("postgres://"):
        return "postgresql+psycopg://" + url[len("postgres://") :]
    if url.startswith("postgresql://"):
        return "postgresql+psycopg://" + url[len("postgresql://") :]
    return url


database_url = _normalize_database_url(settings.database_url)

if database_url.startswith("sqlite"):
    Path("data").mkdir(parents=True, exist_ok=True)

connect_args = (
    {"check_same_thread": False}
    if database_url.startswith("sqlite")
    else {}
)

engine_kwargs = {"connect_args": connect_args}
if database_url.startswith("postgresql"):
    # Neon may close idle TLS connections; pre_ping/recycle avoids stale sockets.
    engine_kwargs.update(
        {
            "pool_pre_ping": True,
            "pool_recycle": 300,
            "pool_size": 5,
            "max_overflow": 10,
        }
    )

engine = create_engine(database_url, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
