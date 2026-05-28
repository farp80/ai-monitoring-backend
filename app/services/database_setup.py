from app.database import Base, engine

# Ensure SQLAlchemy models are registered before metadata operations.
from app.models import user  # noqa: F401


def ensure_database_schema() -> None:
    """Create missing tables (works for SQLite and Neon Postgres)."""
    Base.metadata.create_all(bind=engine)
