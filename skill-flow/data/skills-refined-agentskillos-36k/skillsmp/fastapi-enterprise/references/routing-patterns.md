# API Routing Patterns

Auto-discovery routing with folder-based structure and auto-generated tags.

## Auto-Discovery System

Routes are automatically discovered from `api/routes/` folder structure and registered with FastAPI.

### Benefits

- **No manual registration**: Add file → route appears
- **Consistent structure**: Folder = URL segment
- **Auto-tags**: OpenAPI tags from folder names
- **Easy refactoring**: Move file = move endpoint

## File Structure to URL Mapping

```
api/routes/
├── health.py                    →  /health
├── metrics.py                   →  /metrics
└── v1/
    ├── user/
    │   ├── profile.py           →  /api/v1/user/profile/*
    │   └── role.py              →  /api/v1/user/role/*
    └── product/
        └── category.py          →  /api/v1/product/category/*
```

**Rule**: `api/routes/{version}/{module}/{service}.py` maps to `/{api_prefix}/{version}/{module}/{service}/*`

## Auto-Registration Logic

### api/routes/__init__.py

```python
"""Auto-discovery and registration of API routes."""

import importlib
import inspect
from pathlib import Path
from fastapi import APIRouter, FastAPI
from core.logging import get_logger
from core.config import settings

logger = get_logger(__name__)


def register_routes(app: FastAPI) -> None:
    """Auto-discover and register all routes."""
    routes_dir = Path(__file__).parent
    
    # Direct endpoints (no version)
    _register_direct_endpoints(app, routes_dir)
    
    # Versioned endpoints
    _register_versioned_endpoints(app, routes_dir)


def _register_direct_endpoints(app: FastAPI, routes_dir: Path) -> None:
    """Register /health, /metrics, etc."""
    for py_file in routes_dir.glob("*.py"):
        if py_file.name.startswith("_"):
            continue
        
        module_name = f"api.routes.{py_file.stem}"
        try:
            module = importlib.import_module(module_name)
            
            for name, obj in inspect.getmembers(module):
                if isinstance(obj, APIRouter):
                    app.include_router(obj)
                    logger.info(f"Registered direct route: {module_name}")
                    break
        except Exception as e:
            logger.error(f"Failed to load route {module_name}: {e}")


def _register_versioned_endpoints(app: FastAPI, routes_dir: Path) -> None:
    """Register /api/v1/..., /api/v2/..., etc."""
    for version_dir in routes_dir.iterdir():
        if not version_dir.is_dir() or version_dir.name.startswith("_"):
            continue
        
        version = version_dir.name
        
        for py_file in version_dir.rglob("*.py"):
            if py_file.name.startswith("_"):
                continue
            
            relative_path = py_file.relative_to(routes_dir)
            module_parts = list(relative_path.parts[:-1]) + [py_file.stem]
            module_name = "api.routes." + ".".join(module_parts)
            
            try:
                module = importlib.import_module(module_name)
                
                for name, obj in inspect.getmembers(module):
                    if isinstance(obj, APIRouter):
                        # Auto-generate tag
                        if not obj.tags:
                            parent_folder = relative_path.parts[-2] if len(relative_path.parts) > 1 else version
                            obj.tags = [parent_folder.capitalize()]
                        
                        # Build prefix
                        prefix_parts = [settings.API_PREFIX, version] + list(relative_path.parts[1:-1]) + [py_file.stem]
                        prefix = "/" + "/".join(filter(None, prefix_parts))
                        
                        app.include_router(obj, prefix=prefix)
                        logger.info(
                            f"Registered route: {module_name}",
                            prefix=prefix,
                            tags=obj.tags,
                        )
                        break
            except Exception as e:
                logger.error(f"Failed to load route {module_name}: {e}")
```

## Creating Endpoints

### Example: User Role Management

File: `api/routes/v1/user/role.py`

```python
"""
User role management endpoints.

Auto-discovered as: /api/v1/user/role/*
Tag: User (auto-generated from parent folder "user")
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import get_db
from core.logging import get_logger
from schemas.user.role import RoleCreate, RoleResponse
from services.user.role import role_service

logger = get_logger(__name__)

# Router will be auto-discovered
router = APIRouter()
# Tag will be auto-generated as "User"


@router.get("/list")
async def list_roles(
    db: AsyncSession = Depends(get_db),
) -> list[RoleResponse]:
    """
    GET /api/v1/user/role/list
    
    List all user roles.
    """
    logger.info("Listing user roles")
    roles = await role_service.get_all(db)
    return roles


@router.post("/add-rule")
async def add_rule(
    role_id: int,
    rule: str,
    db: AsyncSession = Depends(get_db),
) -> RoleResponse:
    """
    POST /api/v1/user/role/add-rule
    
    Add a rule to a role.
    """
    logger.info("Adding rule to role", role_id=role_id, rule=rule)
    
    role = await role_service.add_rule(db, role_id, rule)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    
    return role


@router.delete("/remove-rule")
async def remove_rule(
    role_id: int,
    rule: str,
    db: AsyncSession = Depends(get_db),
):
    """
    DELETE /api/v1/user/role/remove-rule
    
    Remove a rule from a role.
    """
    logger.info("Removing rule from role", role_id=role_id, rule=rule)
    
    success = await role_service.remove_rule(db, role_id, rule)
    if not success:
        raise HTTPException(status_code=404, detail="Role or rule not found")
    
    return {"message": "Rule removed"}
```

Result:
- **Prefix**: `/api/v1/user/role`
- **Tag**: `User`
- **Endpoints**:
  - `GET /api/v1/user/role/list`
  - `POST /api/v1/user/role/add-rule`
  - `DELETE /api/v1/user/role/remove-rule`

## Custom Tags

Override auto-generated tags:

```python
router = APIRouter(tags=["Role Management"])
```

## Direct Endpoints (No Versioning)

For `/health`, `/metrics`, `/status`:

File: `api/routes/health.py`

```python
"""Health check endpoint."""

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """Health check endpoint at /health"""
    return {"status": "healthy"}
```

Registered directly without `/api/v1` prefix.

## API Prefix Configuration

Change global API prefix:

```python
# core/config.py
API_PREFIX: str = "/api"  # or "" for no prefix
```

Affects all versioned routes:
- With `/api`: `/api/v1/user/profile`
- Without: `/v1/user/profile`

## Max Nesting Depth

**Limit**: 3-4 levels deep

✅ **Good**:
```
/api/v1/user/role/add-rule
/api/v1/product/category/list
```

❌ **Too deep**:
```
/api/v1/admin/user/role/permission/grant
```

**Solution**: Flatten structure or use query parameters.

## Multiple Endpoints in One File

Group related endpoints:

```python
# api/routes/v1/user/role.py

@router.get("/list")
async def list_roles(): ...

@router.post("/create")
async def create_role(): ...

@router.put("/{role_id}")
async def update_role(role_id: int): ...

@router.delete("/{role_id}")
async def delete_role(role_id: int): ...
```

All map to `/api/v1/user/role/*`.

## Path Parameters

```python
@router.get("/{role_id}")
async def get_role(role_id: int):
    ...
```

URL: `GET /api/v1/user/role/123`

## Query Parameters

```python
@router.get("/list")
async def list_roles(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
):
    ...
```

URL: `GET /api/v1/user/role/list?skip=0&limit=10&active_only=true`

## Dependencies

### Authentication

```python
from api.dependencies import get_current_user

@router.post("/create")
async def create_role(
    data: RoleCreate,
    current_user = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    ...
```

### Router-Level Dependencies

Apply to all endpoints in router:

```python
router = APIRouter(dependencies=[Depends(get_current_user)])

# Now all endpoints require authentication
@router.get("/list")
async def list_roles(): ...  # Auto-requires auth
```

## Response Models

```python
from schemas.user.role import RoleResponse

@router.get("/{role_id}", response_model=RoleResponse)
async def get_role(role_id: int, db: AsyncSession = Depends(get_db)):
    role = await role_service.get_by_id(db, role_id)
    return role  # Automatically validated and serialized
```

## Status Codes

```python
from fastapi import status

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_role(data: RoleCreate, db: AsyncSession = Depends(get_db)):
    ...

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(role_id: int, db: AsyncSession = Depends(get_db)):
    ...
```

## Error Handling

```python
from fastapi import HTTPException

@router.get("/{role_id}")
async def get_role(role_id: int, db: AsyncSession = Depends(get_db)):
    role = await role_service.get_by_id(db, role_id)
    
    if not role:
        raise HTTPException(
            status_code=404,
            detail=f"Role {role_id} not found"
        )
    
    return role
```

## Testing Routes

```python
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_list_roles():
    response = client.get("/api/v1/user/role/list")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_role():
    response = client.post(
        "/api/v1/user/role/create",
        json={"name": "admin", "permissions": ["read", "write"]}
    )
    assert response.status_code == 201
```

## Next Steps

- [Project Structure](project-structure.md) - Complete folder organization
- [Authentication Patterns](authentication-patterns.md) - Securing routes
- [Clean Code Standards](clean-code-standards.md) - Route organization
