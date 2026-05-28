# Module Patterns - Independent Module Development

## Overview

FastAPI Enterprise uses a **modular architecture** where each business domain is an independent module. Modules are self-contained with their own routes, models, schemas, services, cache, and migrations.

## Module Structure

```
modules/users/
├── __init__.py                 # Module router export
├── routes/                     # API endpoints
│   ├── __init__.py
│   ├── user.py                 # /api/v1/users
│   └── roles/
│       ├── __init__.py
│       └── role.py             # /api/v1/users/roles
├── models/                     # SQLAlchemy models
│   ├── __init__.py
│   ├── user.py
│   └── role.py
├── schemas/                    # Pydantic schemas
│   ├── __init__.py
│   ├── user.py                 # UserCreate, UserResponse, UserUpdate
│   └── role.py
├── services/                   # Business logic
│   ├── __init__.py
│   ├── user_service.py
│   └── role_service.py
├── cache/                      # Module-specific caching
│   ├── __init__.py
│   └── user_cache.py
├── enums/                      # Module-specific enums
│   ├── __init__.py
│   └── role_type.py
└── alembic/                    # Module-specific migrations
    ├── env.py
    ├── script.py.mako
    └── versions/
        └── 001_create_user_table.py
```

## Creating a New Module

### Using Automation Script
```bash
# Create complete module structure
uv run python scripts/create_module.py --name orders

# Creates:
# - modules/orders/ with all subdirectories
# - Basic CRUD routes
# - Sample model, schema, service
# - Alembic configuration
# - Cache setup
```

### Manual Module Creation

#### Step 1: Module Router (__init__.py)
```python
# modules/orders/__init__.py
from fastapi import APIRouter
from .routes import order, items

router = APIRouter()

# Include sub-routes
router.include_router(order.router, prefix="", tags=["Orders"])
router.include_router(items.router, prefix="/items", tags=["Order Items"])
```

#### Step 2: Routes
```python
# modules/orders/routes/order.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db import get_db
from src.core.logging import logger
from ..schemas.order import OrderCreate, OrderResponse
from ..services.order_service import OrderService

router = APIRouter()

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_data: OrderCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create new order."""
    logger.info("create_order_requested", data=order_data.model_dump())
    
    order = await OrderService.create(db, order_data)
    
    logger.info("order_created", order_id=order.id)
    return order
```

#### Step 3: Models
```python
# modules/orders/models/order.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Order(Base):
    """Order model - module-specific table."""
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False, index=True)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(20), nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

#### Step 4: Schemas
```python
# modules/orders/schemas/order.py
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, Field

class OrderBase(BaseModel):
    """Shared order attributes."""
    total_amount: Decimal = Field(..., ge=0, description="Order total amount")

class OrderCreate(OrderBase):
    """Schema for creating order."""
    pass

class OrderUpdate(BaseModel):
    """Schema for updating order."""
    status: str | None = Field(None, max_length=20)

class OrderResponse(OrderBase):
    """Schema for order response."""
    id: int
    order_number: str
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

#### Step 5: Services
```python
# modules/orders/services/order_service.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.logging import logger
from ..models.order import Order
from ..schemas.order import OrderCreate
from ..cache.order_cache import OrderCache

class OrderService:
    """Order business logic."""
    
    @staticmethod
    async def create(db: AsyncSession, order_data: OrderCreate) -> Order:
        """Create new order with caching."""
        # Generate order number
        order_number = await OrderService._generate_order_number(db)
        
        # Create order
        order = Order(
            order_number=order_number,
            total_amount=order_data.total_amount
        )
        
        db.add(order)
        await db.commit()
        await db.refresh(order)
        
        # Cache the order
        await OrderCache.set(order.id, order)
        
        logger.info("order_created", order_id=order.id, order_number=order_number)
        return order
    
    @staticmethod
    async def get_by_id(db: AsyncSession, order_id: int) -> Order | None:
        """Get order by ID with caching."""
        # Check cache first
        cached_order = await OrderCache.get(order_id)
        if cached_order:
            logger.debug("order_cache_hit", order_id=order_id)
            return cached_order
        
        # Fetch from DB
        result = await db.execute(
            select(Order).where(Order.id == order_id)
        )
        order = result.scalars().first()
        
        # Cache if found
        if order:
            await OrderCache.set(order_id, order)
        
        return order
    
    @staticmethod
    async def _generate_order_number(db: AsyncSession) -> str:
        """Generate unique order number."""
        import uuid
        return f"ORD-{uuid.uuid4().hex[:8].upper()}"
```

#### Step 6: Cache
```python
# modules/orders/cache/order_cache.py
from typing import Any
from src.core.cache import cache_manager
from src.core.logging import logger

class OrderCache:
    """Order-specific caching."""
    
    PREFIX = "orders"
    TTL = 3600  # 1 hour
    
    @staticmethod
    async def get(order_id: int) -> Any | None:
        """Get cached order."""
        key = f"{OrderCache.PREFIX}:{order_id}"
        return await cache_manager.get(key)
    
    @staticmethod
    async def set(order_id: int, order: Any) -> None:
        """Cache order."""
        key = f"{OrderCache.PREFIX}:{order_id}"
        await cache_manager.set(key, order, ttl=OrderCache.TTL)
        logger.debug("order_cached", order_id=order_id, key=key)
    
    @staticmethod
    async def delete(order_id: int) -> None:
        """Invalidate order cache."""
        key = f"{OrderCache.PREFIX}:{order_id}"
        await cache_manager.delete(key)
        logger.debug("order_cache_invalidated", order_id=order_id)
    
    @staticmethod
    async def invalidate_all() -> None:
        """Invalidate all order caches."""
        pattern = f"{OrderCache.PREFIX}:*"
        await cache_manager.delete_pattern(pattern)
        logger.info("all_order_caches_invalidated")
```

## Module Independence Guidelines

### ✅ DO:
1. **Use service layer for inter-module communication**
   ```python
   # In orders module, accessing user data
   from modules.users.services.user_service import UserService
   
   user = await UserService.get_by_id(db, user_id)
   ```

2. **Each module has own database tables**
   ```python
   # modules/orders/models/order.py - orders table
   # modules/users/models/user.py - users table
   ```

3. **Module-specific cache prefixes**
   ```python
   # modules/orders/cache/order_cache.py
   PREFIX = "orders"
   
   # modules/users/cache/user_cache.py
   PREFIX = "users"
   ```

4. **Separate migration histories**
   ```bash
   modules/orders/alembic/versions/001_create_orders.py
   modules/users/alembic/versions/001_create_users.py
   ```

### ❌ DON'T:
1. **Import models from other modules**
   ```python
   # ❌ WRONG
   from modules.users.models.user import User
   
   # ✅ CORRECT
   from modules.users.services.user_service import UserService
   user_data = await UserService.get_by_id(db, user_id)
   ```

2. **Share database tables**
   ```python
   # ❌ WRONG - Don't create ForeignKey to other module's table
   user_id = Column(Integer, ForeignKey("users.id"))
   
   # ✅ CORRECT - Store user_id as regular integer
   user_id = Column(Integer, nullable=False)
   ```

3. **Access other module's cache directly**
   ```python
   # ❌ WRONG
   from modules.users.cache.user_cache import UserCache
   user = await UserCache.get(user_id)
   
   # ✅ CORRECT
   from modules.users.services.user_service import UserService
   user = await UserService.get_by_id(db, user_id)
   ```

## Module Auto-Discovery

### Core Module Loader
```python
# src/core/module_loader.py
from pathlib import Path
from importlib import import_module
from fastapi import FastAPI
from src.core.logging import logger

def discover_modules(app: FastAPI) -> None:
    """Auto-discover and register all modules."""
    modules_dir = Path(__file__).parent.parent.parent / "modules"
    
    if not modules_dir.exists():
        logger.warning("modules_directory_not_found", path=str(modules_dir))
        return
    
    for module_path in sorted(modules_dir.iterdir()):
        if not module_path.is_dir():
            continue
            
        if not (module_path / "__init__.py").exists():
            logger.warning("module_missing_init", module=module_path.name)
            continue
        
        try:
            # Import module
            module = import_module(f"modules.{module_path.name}")
            
            # Check for router
            if not hasattr(module, "router"):
                logger.warning("module_missing_router", module=module_path.name)
                continue
            
            # Register with FastAPI
            app.include_router(
                module.router,
                prefix=f"/api/v1/{module_path.name}",
                tags=[module_path.name.replace('_', ' ').title()]
            )
            
            logger.info("module_registered", 
                       module=module_path.name, 
                       prefix=f"/api/v1/{module_path.name}")
                       
        except Exception as e:
            logger.error("module_registration_failed", 
                        module=module_path.name, 
                        error=str(e))
```

### App Integration
```python
# src/app.py
from fastapi import FastAPI
from src.core.module_loader import discover_modules

app = FastAPI(title="My API")

# Auto-register all modules
discover_modules(app)
```

## Module-Specific Migrations

### Per-Module Alembic Configuration
Each module has its own migration history:

```python
# modules/orders/alembic/env.py
from sqlalchemy import pool
from alembic import context
from src.core.config import settings

# Import module models only
from modules.orders.models.order import Base

target_metadata = Base.metadata

def run_migrations_online():
    """Run migrations in online mode."""
    configuration = context.config
    configuration.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
    
    with context.begin_transaction():
        context.run_migrations()

run_migrations_online()
```

### Running Module Migrations
```bash
# Run migrations for specific module
cd modules/orders/alembic
alembic upgrade head

# Or use automation script
uv run python scripts/run_migrations.py --module orders

# Run all module migrations
uv run python scripts/run_migrations.py --all
```

## Testing Modules

### Module Test Structure
```
tests/
├── unit/
│   ├── test_orders/
│   │   ├── test_order_service.py
│   │   └── test_order_cache.py
│   └── test_users/
│       └── test_user_service.py
└── integration/
    ├── test_orders/
    │   └── test_order_api.py
    └── test_users/
        └── test_user_api.py
```

### Example Unit Test
```python
# tests/unit/test_orders/test_order_service.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from modules.orders.services.order_service import OrderService
from modules.orders.schemas.order import OrderCreate

@pytest.mark.asyncio
async def test_create_order(db_session: AsyncSession):
    """Test order creation."""
    order_data = OrderCreate(total_amount=100.50)
    
    order = await OrderService.create(db_session, order_data)
    
    assert order.id is not None
    assert order.order_number is not None
    assert order.total_amount == 100.50
    assert order.status == "pending"
```

### Example Integration Test
```python
# tests/integration/test_orders/test_order_api.py
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_order_endpoint(client: AsyncClient):
    """Test order creation endpoint."""
    response = await client.post(
        "/api/v1/orders",
        json={"total_amount": 150.75}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["total_amount"] == 150.75
```

## Module Best Practices

### 1. Single Responsibility
Each module handles one business domain:
- ✅ `users` - User management and authentication
- ✅ `orders` - Order processing
- ✅ `products` - Product catalog
- ❌ `users_and_orders` - Too broad

### 2. Clear Boundaries
Define clear module boundaries:
```python
# modules/orders/services/order_service.py
class OrderService:
    @staticmethod
    async def create_order_for_user(db: AsyncSession, user_id: int, ...):
        # Validate user exists (via UserService)
        user = await UserService.get_by_id(db, user_id)
        if not user:
            raise ValueError("User not found")
        
        # Create order (own logic)
        order = await OrderService.create(db, ...)
        return order
```

### 3. Dependency Injection
Use FastAPI's dependency injection:
```python
# modules/orders/routes/order.py
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import get_db

@router.post("")
async def create_order(
    db: AsyncSession = Depends(get_db),  # DB session
    current_user = Depends(get_current_user)  # Auth
):
    ...
```

### 4. Error Handling
Module-specific exceptions:
```python
# modules/orders/exceptions.py
class OrderNotFoundError(Exception):
    """Order not found."""
    pass

class InsufficientStockError(Exception):
    """Insufficient stock for order."""
    pass
```

## Cross-References

- [Project Structure](./project-structure.md) - Complete directory layout
- [Cache Patterns](./cache-patterns.md) - Module-level caching
- [Database Patterns](./database-patterns.md) - Per-module migrations
- [Clean Code Standards](./clean-code-standards.md) - DDD principles
