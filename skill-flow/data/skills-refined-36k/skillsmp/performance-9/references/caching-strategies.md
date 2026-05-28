# Caching Strategies

When and how to cache effectively.

## When to Cache

### ✅ Good Candidates

- Expensive computations (heavy queries, aggregations)
- Frequently accessed, rarely changed data
- External API responses
- Session data

### ❌ Bad Candidates

- Rapidly changing data
- User-specific data with low reuse
- Security-sensitive data
- Data that must be real-time

## Cache Invalidation Strategies

### Time-Based (TTL)

```python
# Simple but can serve stale data
cache.set("user:123", user_data, ttl=300)  # 5 minutes
```

### Event-Based

```python
# Invalidate on write
def update_user(user_id, data):
    db.update_user(user_id, data)
    cache.delete(f"user:{user_id}")
```

### Write-Through

```python
# Update cache on every write
def update_user(user_id, data):
    db.update_user(user_id, data)
    cache.set(f"user:{user_id}", data)
```

### Cache-Aside (Lazy Loading)

```python
def get_user(user_id):
    # Try cache first
    cached = cache.get(f"user:{user_id}")
    if cached:
        return cached

    # Cache miss: fetch and cache
    user = db.get_user(user_id)
    cache.set(f"user:{user_id}", user, ttl=300)
    return user
```

## Cache Layers

```
Request → CDN → Application Cache → Database Cache → Database
         ↓           ↓                    ↓
      Static      Redis/Memcached    Query Cache
      assets      Session, API       (PostgreSQL)
```

### Layer 1: CDN/Edge Cache

```nginx
# Nginx cache
location /api/products {
    proxy_cache api_cache;
    proxy_cache_valid 200 5m;
    proxy_cache_key "$scheme$request_method$host$request_uri";
    add_header X-Cache-Status $upstream_cache_status;
}
```

### Layer 2: Application Cache (Redis)

```python
import redis

cache = redis.Redis(host='localhost', port=6379)

def get_product(product_id):
    key = f"product:{product_id}"

    # Try cache
    cached = cache.get(key)
    if cached:
        return json.loads(cached)

    # Cache miss
    product = db.get_product(product_id)
    cache.setex(key, 300, json.dumps(product))
    return product
```

### Layer 3: Query Cache

```python
# Django ORM caching
from django.core.cache import cache

def get_active_users():
    key = "active_users_count"
    count = cache.get(key)
    if count is None:
        count = User.objects.filter(is_active=True).count()
        cache.set(key, count, 60)
    return count
```

## Cache Patterns

### Thundering Herd Prevention

```python
import threading

locks = {}

def get_with_lock(key, fetch_func, ttl=300):
    # Try cache first
    value = cache.get(key)
    if value:
        return value

    # Acquire lock for this key
    lock = locks.setdefault(key, threading.Lock())
    with lock:
        # Double-check after acquiring lock
        value = cache.get(key)
        if value:
            return value

        # Fetch and cache
        value = fetch_func()
        cache.set(key, value, ttl)
        return value
```

### Stale-While-Revalidate

```python
def get_with_swr(key, fetch_func, ttl=300, stale_ttl=600):
    cached = cache.get(key)

    if cached:
        # Check if stale
        if cached['expires_at'] < time.time():
            # Return stale, refresh in background
            threading.Thread(target=refresh, args=(key, fetch_func, ttl)).start()
        return cached['value']

    # No cache at all
    value = fetch_func()
    cache.set(key, {'value': value, 'expires_at': time.time() + ttl}, stale_ttl)
    return value
```

## Common Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Caching user-specific data globally | Wrong data shown | Include user ID in key |
| No TTL | Stale data forever | Always set TTL |
| Caching null/empty | Repeated DB hits | Cache "not found" explicitly |
| Large cache values | Memory pressure | Cache references, not full objects |
| No cache warming | Cold start latency | Pre-populate critical data |
