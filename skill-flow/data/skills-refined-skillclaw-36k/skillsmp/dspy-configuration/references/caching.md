# DSPy Caching

Manage cache behavior to improve performance and control costs. This guide covers cache architecture, configuration, and debugging.

## Table of Contents

- [Caching Overview](#caching-overview)
- [Cache Architecture](#cache-architecture)
- [Basic Cache Configuration](#basic-cache-configuration)
- [Custom Cache Implementation](#custom-cache-implementation)
- [Cache Debugging](#cache-debugging)
- [Best Practices](#best-practices)

## Caching Overview

### What is Caching?

DSPy caching stores LM responses to avoid redundant API calls, improving performance and reducing costs.

### Why Use Caching?

- **Performance**: Faster response times for cached results
- **Cost reduction**: Fewer API calls to LM providers
- **Consistency**: Same input always returns same output
- **Debugging**: Replay cached responses for debugging

### Cache Layers

DSPy caching is architected in three distinct layers:

1. **In-memory cache**: Fast access using cachetools.LRUCache
2. **On-disk cache**: Persistent storage using diskcache.FanoutCache
3. **Server-side cache**: Managed by LM provider (e.g., OpenAI, Anthropic)

## Cache Architecture

### In-Memory Cache

Implemented using `cachetools.LRUCache` for fast access to frequently used data.

**Characteristics:**
- Fastest access time
- Limited by memory
- Lost on program restart
- Thread-safe

### On-Disk Cache

Implemented using `diskcache.FanoutCache` for persistent storage.

**Characteristics:**
- Persistent across restarts
- Slower than in-memory cache
- Limited by disk space
- Thread-safe

### Server-Side Cache

Managed by LLM service provider (e.g., OpenAI, Anthropic).

**Characteristics:**
- Provider-managed
- Transparent to user
- May have cost implications
- Provider-specific policies

DSPy does not directly control the server-side prompt cache, but offers users the flexibility to enable, disable, and customize the in-memory and on-disk caches.

## Basic Cache Configuration

### Enable All Caches (Default)

Both in-memory and on-disk caching are enabled by default:

```python
import dspy

# Caching is enabled by default
# No action required to start using the cache
```

### Disable All Caches

Disable both in-memory and on-disk caching:

```python
import dspy

# Configure cache settings
dspy.configure_cache(
    enable_disk_cache=False,
    enable_memory_cache=False,
)
```

### Disable In-Memory Cache Only

```python
import dspy

# Keep disk cache, disable memory cache
dspy.configure_cache(
    enable_memory_cache=False,
    enable_disk_cache=True,
)
```

### Disable On-Disk Cache Only

```python
import dspy

# Keep memory cache, disable disk cache
dspy.configure_cache(
    enable_memory_cache=True,
    enable_disk_cache=False,
)
```

### Configure Custom Disk Cache Directory

```python
import dspy

# Specify custom cache directory
dspy.configure_cache(
    disk_cache_dir="/path/to/custom/cache",
)
```

## Custom Cache Implementation

### Custom Cache Key

Override `cache_key()` method to create custom cache keys:

```python
import dspy
from typing import Dict, Any, Optional
import ujson
from hashlib import sha256

class CustomCache(dspy.clients.Cache):

    def cache_key(
        self,
        request: dict[str, Any],
        ignored_args_for_cache_key: Optional[list[str]] = None
    ) -> str:
        """
        Generate custom cache key.

        This example creates a key based solely on the messages,
        ignoring other parameters.
        """
        messages = request.get("messages", [])
        return sha256(ujson.dumps(messages, sort_keys=True).encode()).hexdigest()

# Configure custom cache
dspy.cache = CustomCache(
    enable_disk_cache=True,
    enable_memory_cache=True,
    disk_cache_dir=dspy.clients.DISK_CACHE_DIR
)
```

### Cache Key with Ignored Arguments

```python
class CustomCache(dspy.clients.Cache):

    def cache_key(
        self,
        request: dict[str, Any],
        ignored_args_for_cache_key: Optional[list[str]] = None
    ) -> str:
        """Generate cache key with ignored arguments."""
        # Get request data
        request_copy = dict(request)

        # Remove ignored arguments from cache key
        if ignored_args_for_cache_key:
            for arg in ignored_args_for_cache_key:
                request_copy.pop(arg, None)

        # Generate key from remaining data
        return sha256(ujson.dumps(request_copy, sort_keys=True).encode()).hexdigest()
```

### Custom Cache with TTL

```python
from datetime import timedelta

class CustomCache(dspy.clients.Cache):

    def __init__(self, ttl=timedelta(hours=1), **kwargs):
        super().__init__(**kwargs)
        self.ttl = ttl

    def get(self, key):
        """Get value from cache with TTL check."""
        value = super().get(key)
        if value and value.get('timestamp'):
            age = datetime.now() - value['timestamp']
            if age > self.ttl:
                # Expired, remove from cache
                self.delete(key)
                return None
        return value.get('data') if value else None

    def set(self, key, value):
        """Set value in cache with timestamp."""
        super().set(key, {
            'data': value,
            'timestamp': datetime.now()
        })
```

## Cache Debugging

### Check Cache Hit Rate

Monitor cache effectiveness by tracking hits and misses:

```python
import dspy

# Create a simple cache monitor
class CacheMonitor:
    def __init__(self):
        self.hits = 0
        self.misses = 0

    def check_cache(self, request):
        """Check if request is in cache."""
        key = dspy.cache.cache_key(request)
        cached = dspy.cache.get(key)

        if cached:
            self.hits += 1
            print(f"Cache HIT: {key[:50]}...")
        else:
            self.misses += 1
            print(f"Cache MISS: {key[:50]}...")

        return cached

    def stats(self):
        """Get cache statistics."""
        total = self.hits + self.misses
        if total == 0:
            return "No cache operations"
        return f"Hits: {self.hits}, Misses: {self.misses}, Hit Rate: {self.hits/total:.2%}"

# Use cache monitor
monitor = CacheMonitor()
cached = monitor.check_cache(request)
print(monitor.stats())
```

### Clear Cache

```python
import dspy

# Clear all cache (memory and disk)
dspy.cache.clear()

# Clear memory cache only
dspy.cache.clear_memory()

# Clear disk cache only
dspy.cache.clear_disk()
```

### Inspect Cache Contents

```python
import dspy

# List all cache keys
all_keys = list(dspy.cache.keys())

# Get specific cached value
key = dspy.cache.cache_key(request)
cached_value = dspy.cache.get(key)

# Check cache size
cache_size = len(all_keys)
print(f"Cache contains {cache_size} entries")
```

## Best Practices

### 1. Enable Caching by Default

```python
# Good: Caching is enabled by default
import dspy

# No action required
response = qa(question="Test")

# Bad: Explicitly disable caching
dspy.configure_cache(
    enable_disk_cache=False,
    enable_memory_cache=False,
)
```

### 2. Use Custom Cache Keys for Complex Requests

```python
# Good: Custom cache key for complex requests
class CustomCache(dspy.clients.Cache):

    def cache_key(self, request, ignored_args_for_cache_key=None):
        # Extract only relevant parts of request
        messages = request.get("messages", [])
        return sha256(ujson.dumps(messages, sort_keys=True).encode()).hexdigest()

# Bad: Default cache key for all arguments
```

### 3. Clear Cache When Changing Programs

```python
# Good: Clear cache after program changes
import dspy

# Modify program
program = MyModifiedProgram()

# Clear cache to avoid stale results
dspy.cache.clear()

# Use modified program
result = program(input="test")
```

### 4. Monitor Cache Hit Rate

```python
# Good: Monitor cache effectiveness
class CacheStats:
    def __init__(self):
        self.hits = 0
        self.misses = 0

    def record_hit(self):
        self.hits += 1

    def record_miss(self):
        self.misses += 1

    def hit_rate(self):
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0

# Use cache stats
stats = CacheStats()
# ... monitor cache operations ...
print(f"Cache hit rate: {stats.hit_rate():.2%}")
```

### 5. Use Disk Cache for Persistent Storage

```python
# Good: Enable disk cache for persistent storage
dspy.configure_cache(
    enable_disk_cache=True,
    disk_cache_dir="/path/to/cache",
)

# Bad: Only use memory cache (lost on restart)
dspy.configure_cache(
    enable_disk_cache=False,
    enable_memory_cache=True,
)
```

## Common Issues and Solutions

### Issue: Cache Not Working

**Problem**: Caching seems to have no effect

**Solution**:
1. Verify caching is enabled (it's enabled by default)
2. Check cache directory has write permissions
3. Verify request is being cached (check cache_key())
4. Check cache size (may be full or expired)

### Issue: Stale Cache Results

**Problem**: Cache returns old, outdated results

**Solution**:
1. Clear cache after program changes
2. Implement TTL (time-to-live) for cache entries
3. Use custom cache keys to include version information
4. Regularly clear cache during development

### Issue: Cache Too Large

**Problem**: Cache consumes too much disk or memory

**Solution**:
1. Disable disk cache if memory is sufficient
2. Implement TTL to expire old entries
3. Regularly clear cache
4. Use custom cache with limited size

### Issue: Cache Keys Collide

**Problem**: Different requests return same cached result

**Solution**:
1. Review custom cache key implementation
2. Ensure all relevant arguments are included in key
3. Add unique identifiers (e.g., model name, timestamp)
4. Test cache key generation with varied inputs
