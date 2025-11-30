"""
Database initialization script.
"""
from app.db.base import Base
from app.db.session import engine
from app.models import user, account, transaction, budget, goal, category


def init_db() -> None:
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)

