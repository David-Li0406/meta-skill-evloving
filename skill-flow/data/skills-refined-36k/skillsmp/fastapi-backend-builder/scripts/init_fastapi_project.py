#!/usr/bin/env python3
"""
FastAPI Project Initializer

This script creates a complete FastAPI project structure with all necessary files.

Usage:
    python init_fastapi_project.py <project_name> [--path <path>]

Examples:
    python init_fastapi_project.py my_api
    python init_fastapi_project.py my_api --path ./backend
"""

import sys
import os
from pathlib import Path
from typing import Optional


def create_directory(path: Path) -> None:
    """Create directory if it doesn't exist."""
    path.mkdir(parents=True, exist_ok=True)
    print(f"✅ Created directory: {path}")


def create_file(path: Path, content: str) -> None:
    """Create file with content."""
    path.write_text(content)
    print(f"✅ Created file: {path}")


def init_fastapi_project(project_name: str, base_path: Optional[str] = None) -> None:
    """Initialize a FastAPI project structure."""
    
    # Determine project root
    if base_path:
        project_root = Path(base_path) / project_name
    else:
        project_root = Path(project_name)
    
    if project_root.exists():
        print(f"❌ Error: Project directory already exists: {project_root}")
        sys.exit(1)
    
    print(f"🚀 Initializing FastAPI project: {project_name}")
    print(f"   Location: {project_root.absolute()}")
    print()
    
    # Create directory structure
    create_directory(project_root)
    create_directory(project_root / "app")
    create_directory(project_root / "app" / "models")
    create_directory(project_root / "app" / "routers")
    create_directory(project_root / "app" / "services")
    create_directory(project_root / "app" / "repositories")
    create_directory(project_root / "app" / "utils")
    create_directory(project_root / "app" / "middleware")
    create_directory(project_root / "tests")
    
    # Create __init__.py files
    init_files = [
        project_root / "app" / "__init__.py",
        project_root / "app" / "models" / "__init__.py",
        project_root / "app" / "routers" / "__init__.py",
        project_root / "app" / "services" / "__init__.py",
        project_root / "app" / "repositories" / "__init__.py",
        project_root / "app" / "utils" / "__init__.py",
        project_root / "app" / "middleware" / "__init__.py",
        project_root / "tests" / "__init__.py",
    ]
    
    for init_file in init_files:
        create_file(init_file, "")
    
    # Create main.py
    main_content = '''"""
FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

app = FastAPI(
    title=settings.APP_NAME,
    description="A FastAPI application",
    version="1.0.0",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
# from .routers import users, items
# app.include_router(users.router)
# app.include_router(items.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to the API"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
'''
    create_file(project_root / "app" / "main.py", main_content)
    
    # Create config.py
    config_content = '''"""
Application configuration.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings."""
    
    # App settings
    APP_NAME: str = "FastAPI Application"
    DEBUG: bool = False
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./test.db"
    
    # Security settings
    SECRET_KEY: str = "your-secret-key-change-this"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
'''
    create_file(project_root / "app" / "config.py", config_content)
    
    # Create dependencies.py
    dependencies_content = '''"""
Dependency injection functions.
"""
from typing import Generator
from sqlalchemy.orm import Session
from .models.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
'''
    create_file(project_root / "app" / "dependencies.py", dependencies_content)
    
    # Create database.py
    database_content = '''"""
Database configuration and base.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from ..config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)
'''
    create_file(project_root / "app" / "models" / "database.py", database_content)
    
    # Create schemas.py
    schemas_content = '''"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class HealthCheck(BaseModel):
    """Health check response."""
    status: str


class Message(BaseModel):
    """Generic message response."""
    message: str
'''
    create_file(project_root / "app" / "models" / "schemas.py", schemas_content)
    
    # Create requirements.txt
    requirements_content = '''fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
sqlalchemy==2.0.23
alembic==1.13.0
python-dotenv==1.0.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
pytest==7.4.3
httpx==0.25.2
'''
    create_file(project_root / "requirements.txt", requirements_content)
    
    # Create .env.example
    env_example_content = '''# Application settings
APP_NAME=FastAPI Application
DEBUG=False

# Database
DATABASE_URL=sqlite:///./test.db

# Security
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
ALLOWED_ORIGINS=["http://localhost:3000"]
'''
    create_file(project_root / ".env.example", env_example_content)
    
    # Create .gitignore
    gitignore_content = '''# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.venv

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Database
*.db
*.sqlite
*.sqlite3

# Logs
*.log

# Testing
.pytest_cache/
.coverage
htmlcov/

# OS
.DS_Store
Thumbs.db
'''
    create_file(project_root / ".gitignore", gitignore_content)
    
    # Create README.md
    readme_content = f'''# {project_name}

A FastAPI application.

## Setup

### 1. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

### 4. Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
{project_name}/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration
│   ├── dependencies.py      # Dependency injection
│   ├── models/              # Data models & schemas
│   │   ├── __init__.py
│   │   ├── database.py      # Database setup
│   │   └── schemas.py       # Pydantic schemas
│   ├── routers/             # API route handlers
│   │   └── __init__.py
│   ├── services/            # Business logic
│   │   └── __init__.py
│   ├── repositories/        # Data access
│   │   └── __init__.py
│   ├── utils/               # Utilities
│   │   └── __init__.py
│   └── middleware/          # Custom middleware
│       └── __init__.py
├── tests/                   # Test suite
├── requirements.txt         # Dependencies
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Development

### Adding a new router

1. Create router file in `app/routers/`:

```python
from fastapi import APIRouter

router = APIRouter(prefix="/items", tags=["items"])

@router.get("/")
async def get_items():
    return {"items": []}
```

2. Include router in `app/main.py`:

```python
from .routers import items

app.include_router(items.router)
```

### Running tests

```bash
pytest
```

## Production

Update `.env` with production values and use a production server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## License

Add your license here.
'''
    create_file(project_root / "README.md", readme_content)
    
    # Create test file
    test_content = '''"""
Test main application.
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
'''
    create_file(project_root / "tests" / "test_main.py", test_content)
    
    print()
    print(f"✅ FastAPI project '{project_name}' initialized successfully!")
    print()
    print("Next steps:")
    print(f"1. cd {project_name}")
    print("2. python -m venv venv")
    print("3. source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print("4. pip install -r requirements.txt")
    print("5. cp .env.example .env")
    print("6. uvicorn app.main:app --reload")
    print()
    print("📚 API Documentation will be available at:")
    print("   http://localhost:8000/docs")
    print("   http://localhost:8000/redoc")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python init_fastapi_project.py <project_name> [--path <path>]")
        print()
        print("Examples:")
        print("  python init_fastapi_project.py my_api")
        print("  python init_fastapi_project.py my_api --path ./backend")
        sys.exit(1)
    
    project_name = sys.argv[1]
    base_path = None
    
    if len(sys.argv) == 4 and sys.argv[2] == "--path":
        base_path = sys.argv[3]
    
    init_fastapi_project(project_name, base_path)


if __name__ == "__main__":
    main()
