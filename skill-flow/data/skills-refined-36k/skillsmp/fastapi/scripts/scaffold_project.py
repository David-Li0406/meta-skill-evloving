#!/usr/bin/env python3
"""
FastAPI Project Scaffolding Script

Generates different types of FastAPI projects with proper structure and boilerplate.

Usage:
    python scaffold_project.py <project_name> --type <project_type> [options]

Project Types:
    - simple-api: Basic REST API with CRUD operations
    - microservice: Microservice with health checks and service discovery
    - fullstack: Full-stack app with frontend integration
    - ml-api: ML/AI API with model serving capabilities

Options:
    --database: Database type (postgresql, mysql, sqlite, mongodb)
    --docker: Include Docker configuration
    --testing: Include pytest testing setup
    --path: Output path (default: current directory)

Examples:
    python scaffold_project.py my-api --type simple-api --database postgresql
    python scaffold_project.py ml-service --type ml-api --database mongodb --docker
"""

import sys
import argparse
from pathlib import Path
from typing import Dict, List


PROJECT_TYPES = {
    'simple-api': 'Simple REST API',
    'microservice': 'Microservice Architecture',
    'fullstack': 'Full-stack Application',
    'ml-api': 'ML/AI API Service'
}

DATABASES = ['postgresql', 'mysql', 'sqlite', 'mongodb']


def create_directory_structure(base_path: Path, project_type: str) -> Dict[str, Path]:
    """Create the base directory structure for the project."""
    dirs = {
        'root': base_path,
        'app': base_path / 'app',
        'api': base_path / 'app' / 'api',
        'core': base_path / 'app' / 'core',
        'models': base_path / 'app' / 'models',
        'schemas': base_path / 'app' / 'schemas',
        'services': base_path / 'app' / 'services',
        'tests': base_path / 'tests',
    }

    # Add additional directories based on project type
    if project_type == 'ml-api':
        dirs['ml'] = base_path / 'app' / 'ml'
        dirs['ml_models'] = base_path / 'models'

    if project_type == 'fullstack':
        dirs['static'] = base_path / 'app' / 'static'
        dirs['templates'] = base_path / 'app' / 'templates'

    # Create all directories
    for dir_path in dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)
        # Create __init__.py for Python packages
        if 'app' in str(dir_path) and dir_path != dirs['root']:
            (dir_path / '__init__.py').touch()

    return dirs


def generate_main_file(project_type: str, database: str = None) -> str:
    """Generate the main FastAPI application file."""
    return f'''from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="{PROJECT_TYPES[project_type]}"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(router.api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {{"message": "Welcome to {{settings.PROJECT_NAME}}", "version": settings.VERSION}}


@app.get("/health")
async def health_check():
    return {{"status": "healthy"}}
'''


def generate_config_file(database: str = None) -> str:
    """Generate configuration file."""
    db_url = ""
    if database == 'postgresql':
        db_url = "postgresql://user:password@localhost/dbname"
    elif database == 'mysql':
        db_url = "mysql://user:password@localhost/dbname"
    elif database == 'sqlite':
        db_url = "sqlite:///./app.db"
    elif database == 'mongodb':
        db_url = "mongodb://localhost:27017/dbname"

    return f'''from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Project"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Database
    DATABASE_URL: str = "{db_url}"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
'''


def generate_router_file(project_type: str) -> str:
    """Generate API router file."""
    routes = '''from fastapi import APIRouter
from app.api.endpoints import items

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(items.router, prefix="/items", tags=["items"])
'''

    if project_type == 'ml-api':
        routes += '''api_router.include_router(predictions.router, prefix="/predict", tags=["predictions"])
'''

    return routes


def generate_items_endpoint() -> str:
    """Generate example items CRUD endpoint."""
    return '''from typing import List
from fastapi import APIRouter, HTTPException
from app.schemas.item import Item, ItemCreate, ItemUpdate

router = APIRouter()

# In-memory storage (replace with database in production)
items_db = {}
item_id_counter = 1


@router.get("/", response_model=List[Item])
async def list_items():
    """List all items."""
    return list(items_db.values())


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    """Get item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]


@router.post("/", response_model=Item, status_code=201)
async def create_item(item: ItemCreate):
    """Create a new item."""
    global item_id_counter
    new_item = Item(id=item_id_counter, **item.model_dump())
    items_db[item_id_counter] = new_item
    item_id_counter += 1
    return new_item


@router.put("/{item_id}", response_model=Item)
async def update_item(item_id: int, item: ItemUpdate):
    """Update an existing item."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    stored_item = items_db[item_id]
    update_data = item.model_dump(exclude_unset=True)
    updated_item = stored_item.model_copy(update=update_data)
    items_db[item_id] = updated_item
    return updated_item


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int):
    """Delete an item."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
'''


def generate_item_schema() -> str:
    """Generate Pydantic schemas for items."""
    return '''from pydantic import BaseModel, Field
from typing import Optional


class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    tax: Optional[float] = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    tax: Optional[float] = None


class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True
'''


def generate_requirements(database: str = None, include_testing: bool = False) -> str:
    """Generate requirements.txt file."""
    reqs = [
        "fastapi[standard]==0.115.0",
        "pydantic==2.9.0",
        "pydantic-settings==2.6.0",
        "uvicorn[standard]==0.32.0",
    ]

    if database == 'postgresql':
        reqs.extend(["sqlalchemy==2.0.35", "psycopg2-binary==2.9.10", "alembic==1.14.0"])
    elif database == 'mysql':
        reqs.extend(["sqlalchemy==2.0.35", "pymysql==1.1.1", "alembic==1.14.0"])
    elif database == 'sqlite':
        reqs.extend(["sqlalchemy==2.0.35", "alembic==1.14.0"])
    elif database == 'mongodb':
        reqs.extend(["motor==3.6.0", "beanie==1.27.0"])

    if include_testing:
        reqs.extend(["pytest==8.3.0", "pytest-asyncio==0.24.0", "httpx==0.27.0"])

    return "\n".join(reqs) + "\n"


def generate_dockerfile() -> str:
    """Generate Dockerfile."""
    return '''FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
'''


def generate_docker_compose(database: str = None) -> str:
    """Generate docker-compose.yml."""
    compose = '''version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
    depends_on:
'''

    if database == 'postgresql':
        compose += '''      - postgres
    volumes:
      - .:/app

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=dbname
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
'''
    elif database == 'mongodb':
        compose += '''      - mongodb
    volumes:
      - .:/app

  mongodb:
    image: mongo:7
    ports:
      - "27017:27017"
    environment:
      - MONGO_INITDB_DATABASE=dbname
    volumes:
      - mongodb_data:/data/db

volumes:
  mongodb_data:
'''
    else:
        compose += '''    volumes:
      - .:/app
'''

    return compose


def generate_gitignore() -> str:
    """Generate .gitignore file."""
    return '''# Python
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

# FastAPI
.env
.env.local
*.db
*.sqlite

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/

# Docker
*.log
'''


def generate_env_template(database: str = None) -> str:
    """Generate .env.template file."""
    content = '''# FastAPI Configuration
PROJECT_NAME=My FastAPI Project
VERSION=1.0.0
API_V1_STR=/api/v1

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Database
'''

    if database == 'postgresql':
        content += 'DATABASE_URL=postgresql://user:password@localhost/dbname\n'
    elif database == 'mysql':
        content += 'DATABASE_URL=mysql://user:password@localhost/dbname\n'
    elif database == 'sqlite':
        content += 'DATABASE_URL=sqlite:///./app.db\n'
    elif database == 'mongodb':
        content += 'DATABASE_URL=mongodb://localhost:27017/dbname\n'

    return content


def generate_readme(project_name: str, project_type: str, database: str = None) -> str:
    """Generate README.md file."""
    return f'''# {project_name}

{PROJECT_TYPES[project_type]} built with FastAPI.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment:
```bash
cp .env.template .env
# Edit .env with your configuration
```

4. Run the application:
```bash
fastapi dev app/main.py
```

The API will be available at http://localhost:8000
Interactive API docs at http://localhost:8000/docs

## Project Structure

```
{project_name}/
├── app/
│   ├── api/           # API routes
│   ├── core/          # Configuration
│   ├── models/        # Database models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic
│   └── main.py        # Application entry point
├── tests/             # Test files
├── requirements.txt   # Dependencies
└── .env.template      # Environment template
```

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/v1/items` - List items
- `POST /api/v1/items` - Create item
- `GET /api/v1/items/{{id}}` - Get item
- `PUT /api/v1/items/{{id}}` - Update item
- `DELETE /api/v1/items/{{id}}` - Delete item

## Development

Run with auto-reload:
```bash
fastapi dev app/main.py
```

Run tests:
```bash
pytest
```

## Docker

Build and run with Docker:
```bash
docker-compose up --build
```
'''


def scaffold_project(args):
    """Main function to scaffold the project."""
    project_name = args.name
    project_type = args.type
    database = args.database
    include_docker = args.docker
    include_testing = args.testing
    output_path = Path(args.path) / project_name

    print(f"Creating {PROJECT_TYPES[project_type]}: {project_name}")
    print(f"Location: {output_path}")

    # Create directory structure
    dirs = create_directory_structure(output_path, project_type)
    print(f"  Created directory structure")

    # Generate and write main.py
    (dirs['app'] / 'main.py').write_text(generate_main_file(project_type, database), encoding='utf-8')

    # Generate and write config.py
    (dirs['core'] / 'config.py').write_text(generate_config_file(database), encoding='utf-8')

    # Create API router structure
    (dirs['api'] / '__init__.py').touch()
    (dirs['api'] / 'router.py').write_text(generate_router_file(project_type), encoding='utf-8')

    # Create endpoints directory
    endpoints_dir = dirs['api'] / 'endpoints'
    endpoints_dir.mkdir(exist_ok=True)
    (endpoints_dir / '__init__.py').touch()
    (endpoints_dir / 'items.py').write_text(generate_items_endpoint(), encoding='utf-8')

    # Generate schemas
    (dirs['schemas'] / 'item.py').write_text(generate_item_schema(), encoding='utf-8')

    # Generate requirements.txt
    (output_path / 'requirements.txt').write_text(generate_requirements(database, include_testing), encoding='utf-8')

    # Generate .gitignore
    (output_path / '.gitignore').write_text(generate_gitignore(), encoding='utf-8')

    # Generate .env.template
    (output_path / '.env.template').write_text(generate_env_template(database), encoding='utf-8')

    # Generate README.md
    (output_path / 'README.md').write_text(generate_readme(project_name, project_type, database), encoding='utf-8')

    # Generate Docker files if requested
    if include_docker:
        (output_path / 'Dockerfile').write_text(generate_dockerfile(), encoding='utf-8')
        (output_path / 'docker-compose.yml').write_text(generate_docker_compose(database), encoding='utf-8')
        print(f"  Added Docker configuration")

    print(f"\n  Project '{project_name}' created successfully!")
    print(f"\nNext steps:")
    print(f"  cd {project_name}")
    print(f"  python -m venv venv")
    print(f"  source venv/bin/activate  # On Windows: venv\\Scripts\\activate")
    print(f"  pip install -r requirements.txt")
    print(f"  cp .env.template .env")
    print(f"  fastapi dev app/main.py")


def main():
    parser = argparse.ArgumentParser(description='Scaffold FastAPI projects')
    parser.add_argument('name', help='Project name')
    parser.add_argument('--type', choices=list(PROJECT_TYPES.keys()),
                       default='simple-api', help='Project type')
    parser.add_argument('--database', choices=DATABASES,
                       help='Database type')
    parser.add_argument('--docker', action='store_true',
                       help='Include Docker configuration')
    parser.add_argument('--testing', action='store_true',
                       help='Include pytest testing setup')
    parser.add_argument('--path', default='.',
                       help='Output path (default: current directory)')

    args = parser.parse_args()
    scaffold_project(args)


if __name__ == "__main__":
    main()
