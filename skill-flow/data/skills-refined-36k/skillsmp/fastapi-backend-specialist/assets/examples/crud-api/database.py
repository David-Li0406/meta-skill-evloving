"""
Database Configuration for CRUD API Example
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL - using SQLite for simplicity
# For PostgreSQL: postgresql://user:password@localhost/dbname
# For MySQL: mysql://user:password@localhost/dbname
SQLALCHEMY_DATABASE_URL = "sqlite:///./crud_example.db"

# Create engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # Only needed for SQLite
)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


# Dependency
def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
