---
title: Use Memory-Efficient Data Encodings
impact: MEDIUM-HIGH
impactDescription: can reduce memory usage 50-90% for small objects
tags: memory, optimization, encoding, ziplist
---

## Use Memory-Efficient Data Encodings

Redis automatically uses memory-efficient encodings (ziplist, intset, listpack) for small data structures. Keep collections small to benefit from these optimizations, and tune thresholds if needed.

**Internal Encodings:**
- **Strings**: int (for integers), embstr (≤44 bytes), raw
- **Lists**: listpack (small), quicklist (large)
- **Sets**: intset (integers only), listpack (small), hashtable
- **Hashes**: listpack (small), hashtable
- **Sorted Sets**: listpack (small), skiplist

**Encoding Thresholds (Redis 7+):**
- `hash-max-listpack-entries`: 512 (switch to hashtable above)
- `hash-max-listpack-value`: 64 bytes
- `list-max-listpack-size`: -2 (8KB per node)
- `set-max-intset-entries`: 512
- `set-max-listpack-entries`: 128
- `zset-max-listpack-entries`: 128
- `zset-max-listpack-value`: 64 bytes

**Incorrect (wasting memory):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: Storing numbers as strings
r.set("counter", "12345")  # Stored as string
# Better: let Redis store as int

# Anti-pattern 2: Large hash fields preventing listpack
r.hset("user:123", "bio", "A" * 1000)  # 1000 bytes > 64 byte threshold
# Forces hash to use hashtable encoding (more memory)

# Anti-pattern 3: Many small separate keys instead of hash
for i in range(1000):
    r.set(f"setting:{i}", "value")
# Each key has ~50 bytes overhead
# 1000 keys = 50KB overhead

# Anti-pattern 4: Using hash for large collection
for i in range(10000):
    r.hset("big_hash", f"field:{i}", "value")
# Exceeds listpack threshold, uses more memory per field
```

**Correct (memory-efficient patterns):**

```python
import redis
r = redis.Redis()

# Correct 1: Store integers efficiently
r.set("counter", 12345)  # Redis stores as integer internally
r.incr("counter")  # Efficient integer operations

# Check encoding
encoding = r.object("encoding", "counter")
print(f"counter encoding: {encoding}")  # Should be "int"

# Correct 2: Keep hash values small for listpack
def store_user_efficient(user_id, user_data):
    """Store user with small field values"""
    # Keep field values under 64 bytes
    r.hset(f"user:{user_id}", mapping={
        "name": user_data["name"][:64],  # Truncate if needed
        "email": user_data["email"][:64],
        "age": user_data["age"],  # Integer stored efficiently
    })

    # Store large content separately
    if len(user_data.get("bio", "")) > 64:
        r.set(f"user:{user_id}:bio", user_data["bio"])

# Correct 3: Use hash bucketing for many small values
def set_bucketed(prefix, key, value, bucket_size=100):
    """
    Store in hash buckets instead of individual keys.
    Reduces per-key overhead significantly.
    """
    bucket = hash(key) % bucket_size
    r.hset(f"{prefix}:bucket:{bucket}", key, value)

def get_bucketed(prefix, key, bucket_size=100):
    bucket = hash(key) % bucket_size
    return r.hget(f"{prefix}:bucket:{bucket}", key)

# Example: 1M settings
# Without bucketing: 1M keys * ~50 bytes overhead = ~50MB overhead
# With 100 buckets: 100 hashes with ~10K fields each = minimal overhead

# Correct 4: Use intset for integer-only sets
r.sadd("user_ids", 1, 2, 3, 4, 5)  # Stored as intset (very compact)
encoding = r.object("encoding", "user_ids")
print(f"user_ids encoding: {encoding}")  # Should be "intset"

# Correct 5: Keep sorted sets small for listpack
# Under 128 elements with values < 64 bytes uses listpack
r.zadd("top_users", {"user1": 100, "user2": 95, "user3": 90})
encoding = r.object("encoding", "top_users")
print(f"top_users encoding: {encoding}")  # Should be "listpack"
```

```python
# Memory analysis tools

def analyze_key_memory(key):
    """Analyze memory usage of a key"""
    key_type = r.type(key).decode()
    encoding = r.object("encoding", key)
    memory = r.memory_usage(key)
    idle_time = r.object("idletime", key)

    info = {
        "key": key,
        "type": key_type,
        "encoding": encoding.decode() if encoding else None,
        "memory_bytes": memory,
        "idle_seconds": idle_time,
    }

    # Add type-specific info
    if key_type == "hash":
        info["field_count"] = r.hlen(key)
    elif key_type == "list":
        info["length"] = r.llen(key)
    elif key_type == "set":
        info["cardinality"] = r.scard(key)
    elif key_type == "zset":
        info["cardinality"] = r.zcard(key)
    elif key_type == "string":
        info["string_length"] = r.strlen(key)

    return info

def find_inefficient_encodings(sample_size=1000):
    """Find keys using less efficient encodings"""
    inefficient = []

    for key in r.scan_iter(count=100):
        if len(inefficient) >= sample_size:
            break

        key_type = r.type(key).decode()
        encoding = r.object("encoding", key)

        if encoding:
            encoding = encoding.decode()
            # Flag potentially inefficient encodings
            if key_type == "hash" and encoding == "hashtable":
                field_count = r.hlen(key)
                if field_count < 512:
                    inefficient.append({
                        "key": key.decode(),
                        "type": key_type,
                        "encoding": encoding,
                        "fields": field_count,
                        "reason": "Hash with <512 fields using hashtable"
                    })

    return inefficient
```

```bash
# Redis configuration for memory efficiency
# redis.conf

# Hash encoding thresholds
hash-max-listpack-entries 512
hash-max-listpack-value 64

# List encoding
list-max-listpack-size -2  # 8 KB max size

# Set encoding
set-max-intset-entries 512
set-max-listpack-entries 128
set-max-listpack-value 64

# Sorted Set encoding
zset-max-listpack-entries 128
zset-max-listpack-value 64

# Check current settings
redis-cli CONFIG GET hash-max-*
redis-cli CONFIG GET list-max-*
redis-cli CONFIG GET set-max-*
redis-cli CONFIG GET zset-max-*
```

Reference: [Redis Memory Optimization](https://redis.io/docs/management/optimization/memory-optimization/)
