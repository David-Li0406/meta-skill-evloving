---
id: caching-strategy
name: "Caching Strategy"
domain: DEV
skill: faion-software-developer
category: "development"
---

# Caching Strategy

## Overview

Caching strategy involves implementing multi-level caching to reduce latency, decrease database load, and improve application scalability. This covers in-memory caching, distributed caching, CDN caching, and cache invalidation patterns.

## When to Use

- High read-to-write ratio data
- Expensive computations that can be reused
- Frequently accessed database queries
- Static assets and API responses
- Session storage and rate limiting

## Key Principles

- **Cache closest to consumer**: Reduce network hops
- **Understand invalidation needs**: Stale data costs vs freshness requirements
- **Size appropriately**: Memory is expensive, cache wisely
- **Monitor hit rates**: Low hit rate = wasted resources
- **Plan for cache failures**: Application must work without cache

## Best Practices

### Multi-Level Caching Architecture

```
Request Flow:
User → CDN → Application Cache → Distributed Cache → Database
          ↓
     L1: Browser/CDN (static assets, API responses)
          ↓
     L2: In-Memory (local application cache)
          ↓
     L3: Distributed Cache (Redis/Memcached)
          ↓
     L4: Database Query Cache
          ↓
     L5: Database
```

### Cache-Aside Pattern (Lazy Loading)

```python
import redis
import json
from functools import wraps
from typing import Optional, Callable
import hashlib

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def cache_aside(
    key_prefix: str,
    ttl: int = 3600,
    key_builder: Optional[Callable] = None
):
    """Cache-aside decorator with customizable key building."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Build cache key
            if key_builder:
                cache_key = f"{key_prefix}:{key_builder(*args, **kwargs)}"
            else:
                key_data = f"{args}:{sorted(kwargs.items())}"
                key_hash = hashlib.md5(key_data.encode()).hexdigest()[:12]
                cache_key = f"{key_prefix}:{key_hash}"

            # Try cache first
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)

            # Cache miss - call function
            result = func(*args, **kwargs)

            # Store in cache
            redis_client.setex(cache_key, ttl, json.dumps(result))

            return result

        # Add cache invalidation method
        wrapper.invalidate = lambda *args, **kwargs: redis_client.delete(
            f"{key_prefix}:{key_builder(*args, **kwargs)}" if key_builder
            else f"{key_prefix}:*"
        )

        return wrapper
    return decorator

# Usage
@cache_aside("user", ttl=1800, key_builder=lambda user_id: user_id)
def get_user(user_id: str) -> dict:
    return db.users.find_one({"_id": user_id})

# Invalidate when user updates
def update_user(user_id: str, data: dict):
    db.users.update_one({"_id": user_id}, {"$set": data})
    get_user.invalidate(user_id)
```

### Write-Through Cache

```python
class WriteThroughCache:
    """Cache that writes to both cache and database synchronously."""

    def __init__(self, redis_client, db, collection_name: str, ttl: int = 3600):
        self.redis = redis_client
        self.collection = db[collection_name]
        self.ttl = ttl
        self.key_prefix = collection_name

    def _cache_key(self, doc_id: str) -> str:
        return f"{self.key_prefix}:{doc_id}"

    def get(self, doc_id: str) -> Optional[dict]:
        # Try cache
        cached = self.redis.get(self._cache_key(doc_id))
        if cached:
            return json.loads(cached)

        # Fallback to DB
        doc = self.collection.find_one({"_id": doc_id})
        if doc:
            self.redis.setex(self._cache_key(doc_id), self.ttl, json.dumps(doc))
        return doc

    def set(self, doc_id: str, data: dict) -> dict:
        # Write to database first
        self.collection.update_one(
            {"_id": doc_id},
            {"$set": data},
            upsert=True
        )

        # Then update cache
        doc = self.collection.find_one({"_id": doc_id})
        self.redis.setex(self._cache_key(doc_id), self.ttl, json.dumps(doc))

        return doc

    def delete(self, doc_id: str):
        self.collection.delete_one({"_id": doc_id})
        self.redis.delete(self._cache_key(doc_id))
```

### Write-Behind (Write-Back) Cache

```python
import asyncio
from collections import defaultdict
from datetime import datetime

class WriteBehindCache:
    """Async write-behind cache with batched DB writes."""

    def __init__(self, redis_client, db, flush_interval: int = 5):
        self.redis = redis_client
        self.db = db
        self.flush_interval = flush_interval
        self.pending_writes = defaultdict(dict)
        self._flush_task = None

    async def start(self):
        self._flush_task = asyncio.create_task(self._flush_loop())

    async def stop(self):
        if self._flush_task:
            self._flush_task.cancel()
            await self._flush_all()

    async def set(self, collection: str, doc_id: str, data: dict):
        # Write to cache immediately
        cache_key = f"{collection}:{doc_id}"
        self.redis.setex(cache_key, 3600, json.dumps(data))

        # Queue for async DB write
        self.pending_writes[collection][doc_id] = {
            "data": data,
            "timestamp": datetime.utcnow()
        }

    async def _flush_loop(self):
        while True:
            await asyncio.sleep(self.flush_interval)
            await self._flush_all()

    async def _flush_all(self):
        for collection, docs in list(self.pending_writes.items()):
            if not docs:
                continue

            # Batch write to DB
            operations = [
                UpdateOne(
                    {"_id": doc_id},
                    {"$set": doc_info["data"]},
                    upsert=True
                )
                for doc_id, doc_info in docs.items()
            ]

            if operations:
                self.db[collection].bulk_write(operations)
                self.pending_writes[collection].clear()
```

### Cache Invalidation Patterns

```python
# Pattern 1: Time-based expiration (TTL)
redis_client.setex("key", 3600, "value")  # Expires in 1 hour

# Pattern 2: Event-based invalidation
class CacheInvalidator:
    def __init__(self, redis_client):
        self.redis = redis_client
        self.pubsub = redis_client.pubsub()

    def invalidate(self, pattern: str):
        """Invalidate all keys matching pattern."""
        keys = self.redis.keys(pattern)
        if keys:
            self.redis.delete(*keys)

    def invalidate_tags(self, *tags: str):
        """Invalidate by tag membership."""
        for tag in tags:
            keys = self.redis.smembers(f"cache:tag:{tag}")
            if keys:
                self.redis.delete(*keys)
                self.redis.delete(f"cache:tag:{tag}")

    def set_with_tags(self, key: str, value: str, ttl: int, tags: list):
        """Set value with tag associations."""
        pipe = self.redis.pipeline()
        pipe.setex(key, ttl, value)
        for tag in tags:
            pipe.sadd(f"cache:tag:{tag}", key)
            pipe.expire(f"cache:tag:{tag}", ttl)
        pipe.execute()

# Usage
invalidator = CacheInvalidator(redis_client)
invalidator.set_with_tags(
    "product:123",
    json.dumps(product),
    3600,
    tags=["products", "category:electronics"]
)

# When category updates, invalidate all related products
invalidator.invalidate_tags("category:electronics")

# Pattern 3: Version-based invalidation
def get_cache_version(entity: str) -> int:
    return int(redis_client.get(f"cache:version:{entity}") or 0)

def increment_cache_version(entity: str):
    redis_client.incr(f"cache:version:{entity}")

def versioned_cache_key(entity: str, id: str) -> str:
    version = get_cache_version(entity)
    return f"{entity}:v{version}:{id}"

# Old cache naturally expires, new cache uses new version
```

### HTTP Caching Headers

```python
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import hashlib

app = FastAPI()

@app.get("/api/products/{product_id}")
async def get_product(product_id: str, response: Response):
    product = get_product_from_db(product_id)

    # Generate ETag from content
    etag = hashlib.md5(json.dumps(product).encode()).hexdigest()

    # Set caching headers
    response.headers["Cache-Control"] = "public, max-age=300, stale-while-revalidate=60"
    response.headers["ETag"] = f'"{etag}"'
    response.headers["Vary"] = "Accept-Encoding"

    return product

@app.get("/api/user/profile")
async def get_profile(response: Response):
    # Private data - don't cache in shared caches
    response.headers["Cache-Control"] = "private, max-age=0, must-revalidate"
    return get_current_user_profile()

# CDN configuration example (Cloudflare)
"""
Cache-Control Directives:
- public: CDN can cache
- private: Only browser can cache
- max-age=N: Fresh for N seconds
- s-maxage=N: CDN-specific max-age
- stale-while-revalidate=N: Serve stale while fetching fresh
- no-cache: Must revalidate before use
- no-store: Never cache
"""
```

### In-Memory Application Cache

```python
from functools import lru_cache
from cachetools import TTLCache, cached
import threading

# Simple LRU cache (process-local, no TTL)
@lru_cache(maxsize=1000)
def expensive_computation(input_data: str) -> str:
    return perform_heavy_calculation(input_data)

# TTL cache with thread safety
cache = TTLCache(maxsize=1000, ttl=300)
cache_lock = threading.Lock()

@cached(cache, lock=cache_lock)
def get_config(key: str) -> dict:
    return load_config_from_db(key)

# Custom cache with warming
class WarmableCache:
    def __init__(self, loader: Callable, ttl: int = 300):
        self.cache = TTLCache(maxsize=10000, ttl=ttl)
        self.loader = loader
        self.lock = threading.Lock()

    def get(self, key: str):
        if key not in self.cache:
            with self.lock:
                if key not in self.cache:
                    self.cache[key] = self.loader(key)
        return self.cache[key]

    def warm(self, keys: list):
        """Pre-populate cache with known hot keys."""
        for key in keys:
            self.cache[key] = self.loader(key)
```

## Anti-patterns

- **Cache everything**: Caching rarely-accessed data wastes memory
- **No expiration**: Data becomes stale indefinitely
- **Cache stampede**: Multiple processes rebuilding cache simultaneously
- **Ignoring cache failures**: Application breaks when cache is down
- **Caching nulls without TTL**: Negative caching without bounds
- **No monitoring**: Can't detect low hit rates or memory issues
- **Over-aggressive invalidation**: Defeats the purpose of caching

## References

- [Redis Caching Patterns](https://redis.io/docs/manual/patterns/)
- [HTTP Caching - MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Caching)
- [Cloudflare Cache Configuration](https://developers.cloudflare.com/cache/)
- [AWS ElastiCache Best Practices](https://docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/BestPractices.html)
