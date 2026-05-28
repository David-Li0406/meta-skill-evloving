---
title: Keep Key Names Reasonably Short
impact: MEDIUM
impactDescription: saves memory with millions of keys
tags: keys, memory, optimization, naming
---

## Keep Key Names Reasonably Short

Balance readability with memory efficiency in key names. While clarity is important, excessively long keys waste memory - especially significant when you have millions of keys. Each key name is stored in memory for every instance.

**Memory Impact:**
- Key name overhead: ~50 bytes per key (internal structures) + key length
- 10 million keys with 50-char names vs 20-char names = ~300MB difference
- Short IDs (numeric or short UUIDs) are more efficient than long UUIDs

**Incorrect (overly verbose keys):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: Overly verbose naming
r.set("user_account_profile_information_for_user_id_123", "{...}")
# 48 characters for key name!

# Anti-pattern 2: Full UUIDs when not necessary
r.set("user:550e8400-e29b-41d4-a716-446655440000:profile", "{...}")
# UUID adds 36 characters

# Anti-pattern 3: Redundant information
r.set("redis_cache_key_for_user_data_user_123", "{...}")
# "redis_cache_key_for" adds nothing useful

# Anti-pattern 4: Environment in every key
r.set("production_application_myapp_service_users_user_123", "{...}")
# Use separate Redis instances/databases instead
```

**Correct (balanced key names):**

```python
import redis
r = redis.Redis()

# Good: Short but clear
r.hset("u:123", mapping={"name": "John"})           # User
r.hset("p:456", mapping={"title": "Widget"})        # Product
r.set("s:abc123", "session_data")                   # Session
r.set("c:u:123:cart", "{...}")                      # Cart

# Good: Readable abbreviations
r.hset("usr:123", mapping={"name": "John"})         # User
r.hset("prod:456", mapping={"title": "Widget"})     # Product
r.set("sess:abc123", "session_data")                # Session
r.set("ord:789", "{...}")                           # Order

# Good: Full words for less frequent keys (config, etc.)
r.hset("config:app", mapping={"timeout": "30"})     # Config is fine
r.set("feature:dark_mode", "enabled")               # Feature flags

# ID optimization: Use numeric IDs or short IDs
# Instead of: user:550e8400-e29b-41d4-a716-446655440000
# Use: user:123 (auto-increment) or user:7bx9k2 (short ID)

# Short ID generation example
import base64
import struct

def short_id(numeric_id):
    """Convert numeric ID to short base64 string"""
    packed = struct.pack('>Q', numeric_id).lstrip(b'\x00')
    return base64.urlsafe_b64encode(packed).rstrip(b'=').decode()

# short_id(123456) -> "AeJA"
# short_id(9999999) -> "mJj_"
```

```python
# Abbreviation conventions (document in your team)
ABBREVIATIONS = {
    "user": "u",
    "product": "p",
    "order": "o",
    "session": "s",
    "cart": "c",
    "inventory": "inv",
    "category": "cat",
    "transaction": "tx",
    "notification": "notif",
}

# Or slightly longer for readability
ABBREVIATIONS = {
    "user": "usr",
    "product": "prod",
    "order": "ord",
    "session": "sess",
    "cart": "cart",
    "inventory": "inv",
    "category": "cat",
}
```

```python
# Memory calculation example
import redis
r = redis.Redis()

# Check memory usage of a key
r.set("user_profile_information:123", "x" * 100)
r.set("u:123", "x" * 100)

# Use MEMORY USAGE command (Redis 4.0+)
long_key_mem = r.memory_usage("user_profile_information:123")
short_key_mem = r.memory_usage("u:123")

print(f"Long key: {long_key_mem} bytes")   # ~180 bytes
print(f"Short key: {short_key_mem} bytes") # ~150 bytes
# Difference of 30 bytes * 10M keys = 300MB
```

```javascript
// Node.js - Key builder with abbreviations
const PREFIXES = {
    user: 'u',
    product: 'p',
    order: 'o',
    session: 's'
};

function key(type, id, ...rest) {
    const prefix = PREFIXES[type] || type;
    return [prefix, id, ...rest].join(':');
}

// Usage
key('user', 123);                    // "u:123"
key('user', 123, 'profile');         // "u:123:profile"
key('product', 456);                 // "p:456"
```

**When to use longer names:**
- Configuration keys (few in number)
- Keys used for debugging/monitoring
- When the domain requires specific clarity
- When key count is small (< 100,000)

Reference: [Redis Memory Optimization](https://redis.io/docs/management/optimization/memory-optimization/)
