"""
FastAPI Application Template with Better Auth Integration

Usage:
1. Copy this file to your project (e.g., app/main.py)
2. Configure database in app/database.py
3. Set environment variables in .env
4. Run: uvicorn app.main:app --reload
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# === CHOOSE YOUR ORM ===

# Option 1: SQLModel
from app.database import create_db_and_tables
# from app.routes import tasks

# Option 2: SQLAlchemy
# from app.database import engine, Base
# Base.metadata.create_all(bind=engine)


# === LIFESPAN ===
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan - startup and shutdown."""
    # Startup
    create_db_and_tables()  # SQLModel
    # Base.metadata.create_all(bind=engine)  # SQLAlchemy
    yield
    # Shutdown (cleanup if needed)


# === APPLICATION ===
app = FastAPI(
    title="My API",
    description="FastAPI application with Better Auth authentication",
    version="1.0.0",
    lifespan=lifespan,
)


# === CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev server
        # Add your production domains:
        # "https://your-domain.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === ROUTES ===
# Include your routers here
# app.include_router(tasks.router)


# === HEALTH CHECK ===
@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


# === EXAMPLE PROTECTED ROUTE ===
from app.auth import User, get_current_user
from fastapi import Depends


@app.get("/api/me")
async def get_me(user: User = Depends(get_current_user)):
    """Get current user information."""
    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
    }
