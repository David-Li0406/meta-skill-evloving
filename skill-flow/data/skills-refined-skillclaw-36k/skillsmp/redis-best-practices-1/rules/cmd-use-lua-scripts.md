---
title: Use Lua Scripts for Complex Atomic Operations
impact: HIGH
impactDescription: true atomicity, reduced round trips, server-side logic
tags: commands, lua, atomicity, performance, scripting
---

## Use Lua Scripts for Complex Atomic Operations

Use Lua scripts for operations that need true atomicity with conditional logic. Unlike MULTI/EXEC, Lua scripts can read values and make decisions atomically. Scripts run entirely on the server, reducing network round trips.

**Lua vs MULTI/EXEC:**
- MULTI/EXEC: Queue commands, execute together, but can't use results of one command in another
- Lua: Full programming logic, read values, make decisions, all atomic

**When to Use Lua:**
- Conditional operations (if X then Y)
- Read-modify-write patterns
- Complex atomic operations
- Rate limiting with sliding windows
- Distributed locks

**Incorrect (non-atomic conditional logic):**

```python
import redis
r = redis.Redis()

# Anti-pattern: Check-then-act is not atomic
def acquire_lock_bad(lock_name, owner, timeout):
    if not r.exists(lock_name):  # Check
        r.setex(lock_name, timeout, owner)  # Set - race condition!
        return True
    return False

# Anti-pattern: Conditional increment
def increment_if_less_than_bad(key, max_val):
    current = int(r.get(key) or 0)  # Read
    if current < max_val:  # Decide
        r.incr(key)  # Modify - race condition!
        return True
    return False
```

**Correct (using Lua scripts):**

```python
import redis
r = redis.Redis()

# Correct 1: Rate limiter with sliding window
RATE_LIMIT_SCRIPT = """
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

-- Remove old entries
redis.call('ZREMRANGEBYSCORE', key, '-inf', now - window)

-- Count current entries
local count = redis.call('ZCARD', key)

if count < limit then
    -- Add new entry
    redis.call('ZADD', key, now, now .. ':' .. math.random())
    redis.call('EXPIRE', key, window)
    return 1  -- Allowed
else
    return 0  -- Rate limited
end
"""

# Register script (returns SHA for EVALSHA)
rate_limit = r.register_script(RATE_LIMIT_SCRIPT)

def is_allowed(user_id, limit=100, window=60):
    """Check if request is allowed under rate limit"""
    import time
    key = f"ratelimit:{user_id}"
    now = time.time()
    result = rate_limit(keys=[key], args=[limit, window, now])
    return result == 1

# Correct 2: Distributed lock with Lua
LOCK_SCRIPT = """
local key = KEYS[1]
local owner = ARGV[1]
local ttl = tonumber(ARGV[2])

if redis.call('EXISTS', key) == 0 then
    redis.call('SET', key, owner, 'PX', ttl)
    return 1
end
return 0
"""

UNLOCK_SCRIPT = """
local key = KEYS[1]
local owner = ARGV[1]

if redis.call('GET', key) == owner then
    redis.call('DEL', key)
    return 1
end
return 0
"""

acquire_lock = r.register_script(LOCK_SCRIPT)
release_lock = r.register_script(UNLOCK_SCRIPT)

def with_lock(lock_name, owner, ttl_ms=5000):
    """Context manager for distributed lock"""
    class LockContext:
        def __enter__(self):
            result = acquire_lock(keys=[lock_name], args=[owner, ttl_ms])
            if result != 1:
                raise Exception("Could not acquire lock")
            return self

        def __exit__(self, *args):
            release_lock(keys=[lock_name], args=[owner])

    return LockContext()

# Usage
import uuid
owner = str(uuid.uuid4())
with with_lock("my-resource", owner):
    # Critical section
    do_something()

# Correct 3: Atomic increment with limit
INCREMENT_IF_BELOW = """
local key = KEYS[1]
local max = tonumber(ARGV[1])
local current = tonumber(redis.call('GET', key) or '0')

if current < max then
    return redis.call('INCR', key)
end
return -1
"""

increment_below = r.register_script(INCREMENT_IF_BELOW)

def safe_increment(key, max_value):
    result = increment_below(keys=[key], args=[max_value])
    return result if result != -1 else None

# Correct 4: Compare and swap
CAS_SCRIPT = """
local key = KEYS[1]
local expected = ARGV[1]
local new_value = ARGV[2]

local current = redis.call('GET', key)
if current == expected then
    redis.call('SET', key, new_value)
    return 1
end
return 0
"""

compare_and_swap = r.register_script(CAS_SCRIPT)

def cas(key, expected, new_value):
    """Atomic compare-and-swap"""
    return compare_and_swap(keys=[key], args=[expected, new_value]) == 1

# Correct 5: Batch get with fallback
GET_OR_SET = """
local key = KEYS[1]
local default = ARGV[1]
local ttl = tonumber(ARGV[2])

local value = redis.call('GET', key)
if value then
    return value
end

redis.call('SET', key, default, 'EX', ttl)
return default
"""

get_or_set = r.register_script(GET_OR_SET)
```

```python
# Script management best practices

class RedisScripts:
    """Centralized Lua script management"""

    def __init__(self, redis_client):
        self.r = redis_client
        self._scripts = {}

    def register(self, name, script):
        """Register and cache script"""
        self._scripts[name] = self.r.register_script(script)

    def __getattr__(self, name):
        """Get registered script"""
        if name in self._scripts:
            return self._scripts[name]
        raise AttributeError(f"Script '{name}' not registered")

# Usage
scripts = RedisScripts(r)
scripts.register('rate_limit', RATE_LIMIT_SCRIPT)
scripts.register('acquire_lock', LOCK_SCRIPT)

# Call scripts
scripts.rate_limit(keys=['ratelimit:user1'], args=[100, 60, time.time()])
```

```javascript
// Node.js - Lua scripts with ioredis
const Redis = require('ioredis');
const redis = new Redis();

// Define scripts
redis.defineCommand('rateLimit', {
    numberOfKeys: 1,
    lua: `
        local key = KEYS[1]
        local limit = tonumber(ARGV[1])
        local window = tonumber(ARGV[2])
        local now = tonumber(ARGV[3])

        redis.call('ZREMRANGEBYSCORE', key, '-inf', now - window)
        local count = redis.call('ZCARD', key)

        if count < limit then
            redis.call('ZADD', key, now, now .. ':' .. math.random())
            redis.call('EXPIRE', key, window)
            return 1
        end
        return 0
    `
});

// Use defined command
async function isAllowed(userId, limit = 100, window = 60) {
    const key = `ratelimit:${userId}`;
    const now = Date.now() / 1000;
    const result = await redis.rateLimit(key, limit, window, now);
    return result === 1;
}
```

Reference: [Redis Lua Scripting](https://redis.io/docs/manual/programmability/eval-intro/)
