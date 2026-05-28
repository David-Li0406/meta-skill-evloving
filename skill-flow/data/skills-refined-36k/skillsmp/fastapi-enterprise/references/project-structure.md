# FastAPI Enterprise Project Structure - Modular Architecture

## Critical Requirements

### 1. Project Name Subdirectory
All project files **MUST** be inside a subdirectory named after the project:
```
workspace/
└── my_project/                 # ← Project name directory
    ├── src/
    │   └── app.py              # Main app
    ├── modules/                # Independent modules
    ├── core/                   # Shared core
    └── pyproject.toml          # UV project config
```

**Why?** Clean workspace organization, prevents root directory clutter with alembic/, .env, etc.

### 2. app.py in src/ Directory
`app.py` **MUST** be in `src/` subdirectory:
```
my_project/
└── src/
    └── app.py                  # ← Main FastAPI application
```

**Why?** Separates source code from configuration files, follows modern Python conventions.

### 3. UV + pyproject.toml (Modern Python)
Use **UV** for dependency management with `pyproject.toml`:
```bash
# Initialize project
uv init my_project
cd my_project

# Add dependencies
uv add fastapi uvicorn sqlalchemy asyncpg

# Sync dependencies
uv sync

# Run application
uv run uvicorn src.app:app --reload

# Export for legacy systems
uv export --format requirements-txt > requirements.txt
```

**Why?** 
- UV is 10-100x faster than pip
- pyproject.toml is modern Python standard (PEP 518, 621)
- Lockfile ensures reproducible builds
- Can still generate requirements.txt when needed

### 4. Maximum Route Nesting: 3-4 Levels
Route paths should have **maximum 3-4 levels** of nesting:
- ✅ Good: `/api/v1/users/roles/add-rule` (5 segments total, 3 levels after v1)
- ✅ Good: `/api/v1/products/categories` (4 segments)
- ❌ Bad: `/api/v1/users/roles/permissions/groups/add` (7 segments - too deep)

### 5. Modular Architecture
Each module is **completely independent** with its own:
- Routes (API endpoints)
- Models (database tables)
- Schemas (Pydantic validation)
- Services (business logic)
- Cache (module-specific caching)
- Migrations (Alembic per module)

**Why?**
- Team can work on different modules simultaneously
- Easy to add/remove modules without affecting others
- Clear ownership and responsibility boundaries
- Scales better for large applications

## Complete Directory Structure

```
my_project/                         # Project name directory
├── pyproject.toml                  # UV project configuration
├── uv.lock                         # UV lock file
├── .env.example                    # Environment variable template
├── .gitignore
├── README.md
│
├── src/                            # Source code root
│   ├── __init__.py
│   ├── app.py                      # Main FastAPI application
│   │
│   ├── core/                       # Core functionality (shared across modules)
│   │   ├── __init__.py
│   │   ├── logging.py              # Structlog configuration
│   │   ├── config.py               # Pydantic settings from environment
│   │   ├── db.py                   # Central DB session factory
│   │   ├── cache.py                # Central cache manager (Redis/Memory)
│   │   ├── httpx_client.py         # Central HTTP client
│   │   └── module_loader.py        # Auto-discovery for modules
│   │
│   ├── middleware/                 # Global middleware
│   │   ├── __init__.py
│   │   ├── conversation_middleware.py  # UUID tracking
│   │   ├── logging_middleware.py       # Request/response logging
│   │   └── auth_middleware.py          # Optional Keycloak/RBAC
│   │
│   ├── shared/                     # Shared utilities across modules
│   │   ├── __init__.py
│   │   ├── enums/
│   │   │   ├── __init__.py
│   │   │   └── common.py
│   │   └── helpers/
│   │       ├── __init__.py
│   │       ├── datetime_utils.py
│   │       └── validation_utils.py
│   │
│   └── routes/                     # Core routes (health, metrics, docs)
│       ├── __init__.py
│       ├── health.py               # GET /health
│       └── metrics.py              # GET /metrics
│
├── modules/                        # Independent modules
│   │
│   ├── users/                      # User management module
│   │   ├── __init__.py
│   │   ├── routes/                 # Module-specific routes
│   │   │   ├── __init__.py
│   │   │   ├── user.py             # GET/POST /api/v1/users
│   │   │   └── roles/
│   │   │       ├── __init__.py
│   │   │       └── role.py         # /api/v1/users/roles/*
│   │   ├── models/                 # Module-specific models
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   └── role.py
│   │   ├── schemas/                # Module-specific schemas
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   └── role.py
│   │   ├── services/               # Module business logic
│   │   │   ├── __init__.py
│   │   │   ├── user_service.py
│   │   │   └── role_service.py
│   │   ├── cache/                  # Module-specific cache
│   │   │   ├── __init__.py
│   │   │   └── user_cache.py
│   │   ├── enums/                  # Module-specific enums
│   │   │   ├── __init__.py
│   │   │   └── role_type.py
│   │   └── alembic/                # Module-specific migrations
│   │       ├── env.py
│   │       ├── script.py.mako
│   │       └── versions/
│   │
│   └── products/                   # Product management module
│       ├── __init__.py
│       ├── routes/
│       │   ├── __init__.py
│       │   ├── product.py          # /api/v1/products
│       │   └── category.py         # /api/v1/products/categories
│       ├── models/
│       │   ├── __init__.py
│       │   ├── product.py
│       │   └── category.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   ├── product.py
│       │   └── category.py
│       ├── services/
│       │   ├── __init__.py
│       │   ├── product_service.py
│       │   └── category_service.py
│       ├── cache/
│       │   ├── __init__.py
│       │   └── product_cache.py
│       ├── enums/
│       │   ├── __init__.py
│       │   └── product_status.py
│       └── alembic/
│           ├── env.py
│           ├── script.py.mako
│           └── versions/
│
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   ├── test_users/
│   │   │   ├── test_user_service.py
│   │   │   └── test_role_service.py
│   │   └── test_products/
│   │       └── test_product_service.py
│   └── integration/
│       ├── test_users/
│       │   └── test_user_api.py
│       └── test_products/
│           └── test_product_api.py
│
├── scripts/                        # Development automation scripts
│   ├── create_module.py            # Create new independent module
│   ├── create_endpoint.py          # Add endpoint to existing module
│   └── run_migrations.py           # Run migrations for all modules
│
└── config/                         # YAML configuration files
    ├── development.yml
    └── production.yml
```

## Module Independence Rules

### Each Module Must:
1. **Be self-contained**: All code for a feature lives in one module directory
2. **Own its data**: Module has its own models and migration history
3. **Manage its cache**: Module-specific cache keys and invalidation
4. **Register routes**: Auto-discovered by core.module_loader
5. **Have clear boundaries**: Inter-module communication via services only

### Modules Must NOT:
1. ❌ Import models from other modules
2. ❌ Share database tables (except through shared core)
3. ❌ Directly access other module's cache
4. ❌ Register routes in other modules

### Inter-Module Communication:
```python
# ✅ CORRECT: Via service layer
from modules.users.services.user_service import UserService
user = await UserService.get_by_id(user_id)

# ❌ WRONG: Direct model import
from modules.users.models.user import User  # DON'T DO THIS
```

## Auto-Discovery Mechanism

### Module Registration
Modules are automatically discovered by `core.module_loader`:

```python
# src/core/module_loader.py
def discover_modules(app: FastAPI):
    """Auto-discover and register all modules."""
    modules_dir = Path(__file__).parent.parent.parent / "modules"
    
    for module_path in modules_dir.iterdir():
        if module_path.is_dir() and (module_path / "__init__.py").exists():
            # Import module router
            router_module = import_module(f"modules.{module_path.name}.routes")
            
            # Register with FastAPI
            app.include_router(
                router_module.router,
                prefix=f"/api/v1/{module_path.name}",
                tags=[module_path.name.title()]
            )
```

### Module __init__.py Structure
Each module must export a router:

```python
# modules/users/__init__.py
from fastapi import APIRouter
from .routes import user, roles

router = APIRouter()

# Include sub-routes
router.include_router(user.router, prefix="", tags=["Users"])
router.include_router(roles.router, prefix="/roles", tags=["User Roles"])
```

## File Organization Standards

### 1. Import Order
```python
# Standard library
import os
from datetime import datetime

# Third-party
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Core
from src.core.db import get_db
from src.core.cache import cache_manager

# Shared
from src.shared.helpers.datetime_utils import utc_now

# Current module
from .models.user import User
from .schemas.user import UserCreate
from .services.user_service import UserService
```

### 2. File Naming Conventions
- **Models**: Singular noun (`user.py`, `product.py`)
- **Schemas**: Match model name (`user.py` contains `UserCreate`, `UserResponse`)
- **Services**: `{model}_service.py` (`user_service.py`)
- **Routes**: Match resource (`user.py` for `/users` endpoint)
- **Cache**: `{model}_cache.py` (`user_cache.py`)

### 3. Class Naming Conventions
- **Models**: PascalCase, singular (`User`, `Product`)
- **Schemas**: PascalCase with suffix (`UserCreate`, `UserResponse`, `UserUpdate`)
- **Services**: PascalCase with suffix (`UserService`, `ProductService`)
- **Enums**: PascalCase (`RoleType`, `ProductStatus`)

## Configuration Management

### Environment-Based Configuration
All configuration comes from environment variables via `core.config.py`:

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    PROJECT_NAME: str
    API_VERSION: str = "v1"
    
    # Database
    DATABASE_URL: str
    
    # Cache
    REDIS_URL: str | None = None  # None = memory cache
    
    # External configs
    CONFIG_ENV: str = "development"  # Switches development.yml/production.yml
    
    class Config:
        env_file = ".env"
```

### YAML for External APIs
Use YAML files for external service configurations:

```yaml
# config/development.yml
external_apis:
  payment_gateway:
    base_url: "https://sandbox.payment.com"
    api_key: "${PAYMENT_API_KEY}"  # From environment
    timeout: 30
```

## Cross-References

- [Module Patterns](./module-patterns.md) - Detailed module development guide
- [Cache Patterns](./cache-patterns.md) - Module-level caching strategies
- [Routing Patterns](./routing-patterns.md) - Auto-discovery routing details
- [Database Patterns](./database-patterns.md) - Per-module migrations
- [Clean Code Standards](./clean-code-standards.md) - DDD principles
