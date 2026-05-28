# Cache Patterns - Module-Level Caching Strategies

## Overview

FastAPI Enterprise supports both **Redis** (production) and **in-memory** (development) caching with a unified interface. Each module manages its own cache with clear namespace separation.

## Cache Architecture

```
src/core/cache.py               # Central cache manager
│
modules/
├── users/cache/
│   └── user_cache.py          # users:* prefix
├── orders/cache/
│   └── order_cache.py         # orders:* prefix
└── products/cache/
    └── product_cache.py       # products:* prefix
```

## Core Cache Manager

### Setup
```python
# src/core/cache.py
from typing import Any
import json
from redis.asyncio import Redis
from src.core.config import settings
from src.core.logging import logger

class CacheManager:
    """Unified cache manager supporting Redis and in-memory."""
    
    def __init__(self):
        self.redis: Redis | None = None
        self.memory: dict[str, Any] = {}
        self.use_redis = settings.REDIS_URL is not None
    
    async def connect(self):
        """Connect to Redis or use memory cache."""
        if self.use_redis:
            self.redis = await Redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
            logger.info("cache_connected", backend="redis", url=settings.REDIS_URL)
        else:
            logger.info("cache_connected", backend="memory")
    
    async def disconnect(self):
        """Disconnect from Redis."""
        if self.redis:
            await self.redis.close()
            logger.info("cache_disconnected", backend="redis")
    
    async def get(self, key: str) -> Any | None:
        """Get value from cache."""
        try:
            if self.use_redis:
                value = await self.redis.get(key)
                if value:
                    return json.loads(value)
            else:
                return self.memory.get(key)
        except Exception as e:
            logger.error("cache_get_error", key=key, error=str(e))
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL (seconds)."""
        try:
            serialized = json.dumps(value, default=str)
            
            if self.use_redis:
                await self.redis.setex(key, ttl, serialized)
            else:
                self.memory[key] = serialized
            
            logger.debug("cache_set", key=key, ttl=ttl)
            return True
        except Exception as e:
            logger.error("cache_set_error", key=key, error=str(e))
            return False
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache."""
        try:
            if self.use_redis:
                await self.redis.delete(key)
            else:
                self.memory.pop(key, None)
            
            logger.debug("cache_deleted", key=key)
            return True
        except Exception as e:
            logger.error("cache_delete_error", key=key, error=str(e))
            return False
    
    async def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern."""
        try:
            if self.use_redis:
                keys = await self.redis.keys(pattern)
                if keys:
                    deleted = await self.redis.delete(*keys)
                    logger.info("cache_pattern_deleted", pattern=pattern, count=deleted)
                    return deleted
            else:
                keys_to_delete = [k for k in self.memory.keys() if self._match_pattern(k, pattern)]
                for key in keys_to_delete:
                    del self.memory[key]
                logger.info("cache_pattern_deleted", pattern=pattern, count=len(keys_to_delete))
                return len(keys_to_delete)
        except Exception as e:
            logger.error("cache_pattern_delete_error", pattern=pattern, error=str(e))
            return 0
    
    @staticmethod
    def _match_pattern(key: str, pattern: str) -> bool:
        """Simple pattern matching for memory cache."""
        import re
        regex = pattern.replace("*", ".*")
        return re.match(f"^{regex}$", key) is not None
    
    async def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        if self.use_redis:
            return await self.redis.exists(key) > 0
        else:
            return key in self.memory

# Global cache manager instance
cache_manager = CacheManager()
```

### App Integration
```python
# src/app.py
from fastapi import FastAPI
from src.core.cache import cache_manager

app = FastAPI()

@app.on_event("startup")
async def startup():
    """Connect to cache on startup."""
    await cache_manager.connect()

@app.on_event("shutdown")
async def shutdown():
    """Disconnect from cache on shutdown."""
    await cache_manager.disconnect()
```

## Module-Specific Cache

### Basic Cache Pattern
```python
# modules/users/cache/user_cache.py
from typing import Any
from src.core.cache import cache_manager
from src.core.logging import logger

class UserCache:
    """User-specific caching with namespace."""
    
    PREFIX = "users"
    TTL = 3600  # 1 hour default
    
    @staticmethod
    async def get(user_id: int) -> dict | None:
        """Get cached user."""
        key = f"{UserCache.PREFIX}:{user_id}"
        cached = await cache_manager.get(key)
        
        if cached:
            logger.debug("user_cache_hit", user_id=user_id)
        else:
            logger.debug("user_cache_miss", user_id=user_id)
        
        return cached
    
    @staticmethod
    async def set(user_id: int, user_data: dict, ttl: int | None = None) -> None:
        """Cache user data."""
        key = f"{UserCache.PREFIX}:{user_id}"
        ttl = ttl or UserCache.TTL
        
        await cache_manager.set(key, user_data, ttl=ttl)
        logger.debug("user_cached", user_id=user_id, ttl=ttl)
    
    @staticmethod
    async def delete(user_id: int) -> None:
        """Invalidate user cache."""
        key = f"{UserCache.PREFIX}:{user_id}"
        await cache_manager.delete(key)
        logger.debug("user_cache_invalidated", user_id=user_id)
    
    @staticmethod
    async def invalidate_all() -> None:
        """Invalidate all user caches."""
        pattern = f"{UserCache.PREFIX}:*"
        count = await cache_manager.delete_pattern(pattern)
        logger.info("all_user_caches_invalidated", count=count)
```

### Service Integration
```python
# modules/users/services/user_service.py
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import User
from ..cache.user_cache import UserCache
from src.core.logging import logger

class UserService:
    """User service with caching."""
    
    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
        """Get user by ID with cache."""
        # Check cache first
        cached = await UserCache.get(user_id)
        if cached:
            # Reconstruct User object from cached dict
            return User(**cached)
        
        # Fetch from database
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalars().first()
        
        # Cache if found
        if user:
            user_dict = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active
            }
            await UserCache.set(user_id, user_dict)
        
        return user
    
    @staticmethod
    async def update(db: AsyncSession, user_id: int, user_data: dict) -> User:
        """Update user and invalidate cache."""
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        user = result.scalars().first()
        
        if not user:
            raise ValueError("User not found")
        
        # Update user
        for key, value in user_data.items():
            setattr(user, key, value)
        
        await db.commit()
        await db.refresh(user)
        
        # Invalidate cache
        await UserCache.delete(user_id)
        logger.info("user_updated", user_id=user_id)
        
        return user
```

## Cache Decorator Pattern

### Cache Decorator
```python
# src/shared/helpers/cache_decorator.py
from functools import wraps
from typing import Callable
from src.core.cache import cache_manager
from src.core.logging import logger

def cached(prefix: str, ttl: int = 3600, key_func: Callable | None = None):
    """
    Cache decorator for functions.
    
    Args:
        prefix: Cache key prefix
        ttl: Time to live in seconds
        key_func: Function to generate cache key from args
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = f"{prefix}:{key_func(*args, **kwargs)}"
            else:
                # Use first argument as key (usually ID)
                cache_key = f"{prefix}:{args[0] if args else 'default'}"
            
            # Check cache
            cached_result = await cache_manager.get(cache_key)
            if cached_result is not None:
                logger.debug("cache_hit", key=cache_key)
                return cached_result
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Cache result
            if result is not None:
                await cache_manager.set(cache_key, result, ttl=ttl)
                logger.debug("cache_miss_and_set", key=cache_key)
            
            return result
        
        return wrapper
    return decorator
```

### Using Cache Decorator
```python
# modules/products/services/product_service.py
from src.shared.helpers.cache_decorator import cached

class ProductService:
    """Product service with decorator caching."""
    
    @staticmethod
    @cached(prefix="products", ttl=1800)  # 30 minutes
    async def get_by_id(db: AsyncSession, product_id: int) -> dict | None:
        """Get product by ID with automatic caching."""
        result = await db.execute(
            select(Product).where(Product.id == product_id)
        )
        product = result.scalars().first()
        
        if product:
            return {
                "id": product.id,
                "name": product.name,
                "price": float(product.price),
                "stock": product.stock
            }
        return None
    
    @staticmethod
    @cached(
        prefix="products:category",
        ttl=3600,
        key_func=lambda db, category_id: category_id
    )
    async def get_by_category(db: AsyncSession, category_id: int) -> list[dict]:
        """Get products by category with automatic caching."""
        result = await db.execute(
            select(Product).where(Product.category_id == category_id)
        )
        products = result.scalars().all()
        
        return [
            {"id": p.id, "name": p.name, "price": float(p.price)}
            for p in products
        ]
```

## Cache Invalidation Strategies

### 1. Time-Based Expiration (TTL)
```python
# Cache expires after TTL
await UserCache.set(user_id, user_data, ttl=3600)  # 1 hour
```

### 2. Event-Based Invalidation
```python
# Invalidate on update/delete
class UserService:
    @staticmethod
    async def update(db: AsyncSession, user_id: int, data: dict):
        # Update in database
        ...
        
        # Invalidate cache
        await UserCache.delete(user_id)
    
    @staticmethod
    async def delete(db: AsyncSession, user_id: int):
        # Delete from database
        ...
        
        # Invalidate cache
        await UserCache.delete(user_id)
```

### 3. Pattern-Based Invalidation
```python
# Invalidate all related caches
class OrderService:
    @staticmethod
    async def cancel_all_user_orders(db: AsyncSession, user_id: int):
        # Cancel orders in database
        ...
        
        # Invalidate all order caches for user
        pattern = f"orders:user:{user_id}:*"
        await cache_manager.delete_pattern(pattern)
```

### 4. Cache-Aside Pattern
```python
async def get_user_with_orders(db: AsyncSession, user_id: int) -> dict:
    """Get user with orders using cache-aside pattern."""
    # Try cache first
    cache_key = f"users:with_orders:{user_id}"
    cached = await cache_manager.get(cache_key)
    if cached:
        return cached
    
    # Fetch from DB
    user = await UserService.get_by_id(db, user_id)
    orders = await OrderService.get_by_user(db, user_id)
    
    result = {
        "user": user,
        "orders": orders
    }
    
    # Update cache
    await cache_manager.set(cache_key, result, ttl=600)  # 10 minutes
    
    return result
```

## Advanced Caching Patterns

### List Caching
```python
# modules/products/cache/product_cache.py
class ProductCache:
    """Product cache with list support."""
    
    @staticmethod
    async def get_list(category_id: int, page: int = 1, size: int = 20) -> list | None:
        """Get cached product list."""
        key = f"products:list:{category_id}:page:{page}:size:{size}"
        return await cache_manager.get(key)
    
    @staticmethod
    async def set_list(category_id: int, products: list, page: int = 1, size: int = 20):
        """Cache product list."""
        key = f"products:list:{category_id}:page:{page}:size:{size}"
        await cache_manager.set(key, products, ttl=600)  # 10 minutes for lists
```

### Composite Key Caching
```python
class OrderCache:
    """Order cache with composite keys."""
    
    @staticmethod
    async def get_by_user_and_status(user_id: int, status: str) -> list | None:
        """Get cached orders by user and status."""
        key = f"orders:user:{user_id}:status:{status}"
        return await cache_manager.get(key)
    
    @staticmethod
    async def invalidate_user_orders(user_id: int):
        """Invalidate all caches for user's orders."""
        pattern = f"orders:user:{user_id}:*"
        await cache_manager.delete_pattern(pattern)
```

### Counter Caching
```python
class StatsCache:
    """Statistics caching."""
    
    @staticmethod
    async def increment_view_count(product_id: int) -> int:
        """Increment product view counter."""
        key = f"stats:product:{product_id}:views"
        
        if cache_manager.use_redis:
            # Use Redis INCR for atomic increment
            return await cache_manager.redis.incr(key)
        else:
            # Memory cache increment
            current = await cache_manager.get(key) or 0
            new_value = current + 1
            await cache_manager.set(key, new_value, ttl=86400)  # 24 hours
            return new_value
```

## Configuration

### Environment Variables
```bash
# .env
# Redis cache (production)
REDIS_URL=redis://localhost:6379/0

# Or leave empty for memory cache (development)
# REDIS_URL=
```

### Settings
```python
# src/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Cache
    REDIS_URL: str | None = None  # None = memory cache
    CACHE_DEFAULT_TTL: int = 3600  # 1 hour
    
    class Config:
        env_file = ".env"

settings = Settings()
```

## Performance Best Practices

### 1. Use Appropriate TTL
```python
# Short TTL for frequently changing data
await cache_manager.set("stats:live", data, ttl=60)  # 1 minute

# Medium TTL for semi-static data
await cache_manager.set("products:featured", data, ttl=1800)  # 30 minutes

# Long TTL for static data
await cache_manager.set("config:app", data, ttl=86400)  # 24 hours
```

### 2. Cache Expensive Operations
```python
# ✅ CACHE: Complex aggregations
@cached(prefix="analytics:sales", ttl=3600)
async def get_sales_report(db: AsyncSession, start_date, end_date):
    # Expensive query with aggregations
    ...

# ❌ DON'T CACHE: Simple lookups (unless very frequent)
async def get_user_by_id(db: AsyncSession, user_id: int):
    # Simple indexed lookup - caching might not help much
    ...
```

### 3. Namespace Separation
```python
# Clear namespaces prevent key collisions
users:123             # User ID 123
products:123          # Product ID 123
orders:user:123       # Orders for user 123
```

### 4. Monitor Cache Hit Ratio
```python
# Add metrics to cache operations
async def get(key: str) -> Any:
    value = await cache_manager.get(key)
    
    if value:
        metrics.increment("cache.hit")
    else:
        metrics.increment("cache.miss")
    
    return value
```

## Testing Cache

### Mock Cache in Tests
```python
# tests/conftest.py
import pytest
from src.core.cache import cache_manager

@pytest.fixture
async def cache():
    """Provide cache for tests."""
    # Use memory cache for tests
    cache_manager.use_redis = False
    cache_manager.memory = {}
    
    yield cache_manager
    
    # Cleanup
    cache_manager.memory.clear()
```

### Test Cache Operations
```python
# tests/unit/test_cache.py
import pytest
from modules.users.cache.user_cache import UserCache

@pytest.mark.asyncio
async def test_user_cache_set_get(cache):
    """Test user cache operations."""
    user_data = {"id": 1, "username": "test", "email": "test@example.com"}
    
    # Set cache
    await UserCache.set(1, user_data)
    
    # Get cache
    cached = await UserCache.get(1)
    
    assert cached == user_data

@pytest.mark.asyncio
async def test_cache_invalidation(cache):
    """Test cache invalidation."""
    await UserCache.set(1, {"id": 1, "username": "test"})
    await UserCache.delete(1)
    
    cached = await UserCache.get(1)
    assert cached is None
```

## Cross-References

- [Module Patterns](./module-patterns.md) - Module-specific cache usage
- [Database Patterns](./database-patterns.md) - Cache-aside with database
- [Project Structure](./project-structure.md) - Cache directory organization
