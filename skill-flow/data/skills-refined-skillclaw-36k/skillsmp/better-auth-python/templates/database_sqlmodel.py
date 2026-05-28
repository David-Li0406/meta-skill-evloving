"""
SQLModel Database Configuration Template

Usage:
1. Copy this file to your project as app/database.py
2. Set DATABASE_URL environment variable
3. Import get_session in your routes
"""

import os
from typing import Generator
from sqlmodel import SQLModel, create_engine, Session

# === CONFIGURATION ===
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# SQLite requires check_same_thread=False
connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=True,  # Set to False in production
)


# === DATABASE INITIALIZATION ===
def create_db_and_tables():
    """Create all tables defined in SQLModel models."""
    SQLModel.metadata.create_all(engine)


# === SESSION DEPENDENCY ===
def get_session() -> Generator[Session, None, None]:
    """FastAPI dependency to get database session.

    Usage:
        @app.get("/items")
        def get_items(session: Session = Depends(get_session)):
            return session.exec(select(Item)).all()
    """
    with Session(engine) as session:
        yield session
