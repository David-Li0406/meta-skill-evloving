---
title: Always Set TTL on Cache Keys
impact: CRITICAL
impactDescription: prevents memory leaks and stale data
tags: keys, ttl, expiration, cache, memory
---

## Always Set TTL on Cache Keys

Always set an expiration (TTL) on cache keys and temporary data. Without TTLs, keys accumulate indefinitely, causing memory exhaustion and serving stale data. This is one of the most common Redis anti-patterns.

**Incorrect (no expiration):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: Cache without TTL
def get_user_profile(user_id):
    cache_key = f"cache:user:{user_id}"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)

    profile = fetch_from_database(user_id)
    r.set(cache_key, json.dumps(profile))  # NO TTL - stays forever!
    return profile

# Anti-pattern 2: Session without expiration
r.hset(f"session:{token}", mapping={"user_id": "123", "created": "..."})
# Session stays forever even after logout

# Anti-pattern 3: Rate limit counter without TTL
r.incr(f"ratelimit:{user_id}")  # Counter grows forever

# Anti-pattern 4: Temporary data without cleanup
r.set(f"upload:progress:{upload_id}", "50%")  # Never cleaned up
```

**Correct (always set TTL):**

```python
import redis
r = redis.Redis()

# Correct 1: Cache with TTL
def get_user_profile(user_id, cache_ttl=3600):  # 1 hour default
    cache_key = f"cache:user:{user_id}"
    cached = r.get(cache_key)
    if cached:
        return json.loads(cached)

    profile = fetch_from_database(user_id)
    r.setex(cache_key, cache_ttl, json.dumps(profile))  # TTL in seconds
    # Or: r.set(cache_key, json.dumps(profile), ex=cache_ttl)
    return profile

# Correct 2: Session with expiration
SESSION_TTL = 86400  # 24 hours

def create_session(user_id, token):
    key = f"session:{token}"
    r.hset(key, mapping={"user_id": user_id, "created": time.time()})
    r.expire(key, SESSION_TTL)

# Or use pipeline for atomicity
def create_session_atomic(user_id, token):
    key = f"session:{token}"
    pipe = r.pipeline()
    pipe.hset(key, mapping={"user_id": user_id, "created": time.time()})
    pipe.expire(key, SESSION_TTL)
    pipe.execute()

# Correct 3: Rate limiter with TTL
def check_rate_limit(user_id, max_requests=100, window_seconds=60):
    key = f"ratelimit:{user_id}"
    current = r.incr(key)
    if current == 1:
        r.expire(key, window_seconds)  # Set TTL on first increment
    return current <= max_requests

# Or use atomic SETEX pattern
def rate_limit_atomic(user_id, window_seconds=60):
    key = f"ratelimit:{user_id}:{int(time.time() // window_seconds)}"
    current = r.incr(key)
    if current == 1:
        r.expire(key, window_seconds * 2)  # Extra buffer for clock drift
    return current

# Correct 4: Temporary data with TTL
r.setex(f"upload:progress:{upload_id}", 3600, "50%")  # Expires in 1 hour

# Correct 5: Refresh TTL on access (sliding expiration)
def get_session(token):
    key = f"session:{token}"
    session = r.hgetall(key)
    if session:
        r.expire(key, SESSION_TTL)  # Refresh TTL on each access
    return session
```

```python
# TTL best practices by data type

CACHE_TTLS = {
    "user_profile": 3600,        # 1 hour - changes rarely
    "product_details": 300,      # 5 minutes - moderate updates
    "inventory_count": 60,       # 1 minute - changes frequently
    "search_results": 120,       # 2 minutes - expensive to compute
    "config": 3600,              # 1 hour - rarely changes
    "session": 86400,            # 24 hours
    "rate_limit": 60,            # 1 minute window
    "one_time_token": 600,       # 10 minutes
    "password_reset": 3600,      # 1 hour
    "email_verification": 86400, # 24 hours
}

def cache_with_ttl(key, value, data_type):
    ttl = CACHE_TTLS.get(data_type, 3600)  # Default 1 hour
    r.setex(key, ttl, value)
```

```python
# Check and fix keys without TTL (maintenance script)
import redis
r = redis.Redis()

def find_keys_without_ttl(pattern="cache:*", sample_size=1000):
    """Find cached keys that have no TTL set"""
    keys_without_ttl = []
    count = 0

    for key in r.scan_iter(match=pattern, count=100):
        ttl = r.ttl(key)
        if ttl == -1:  # -1 means no expiration
            keys_without_ttl.append(key)

        count += 1
        if count >= sample_size:
            break

    return keys_without_ttl

def fix_missing_ttls(pattern="cache:*", default_ttl=3600):
    """Add TTL to keys that don't have one"""
    fixed = 0
    for key in r.scan_iter(match=pattern, count=100):
        if r.ttl(key) == -1:
            r.expire(key, default_ttl)
            fixed += 1
    return fixed
```

```javascript
// Node.js
const redis = require('redis');
const client = redis.createClient();

// Set with TTL
await client.setEx('cache:user:123', 3600, JSON.stringify(userData));

// Or using set with options
await client.set('cache:user:123', JSON.stringify(userData), { EX: 3600 });

// Hash with TTL (use pipeline)
const multi = client.multi();
multi.hSet('session:token', { userId: '123' });
multi.expire('session:token', 86400);
await multi.exec();
```

Reference: [Redis EXPIRE Command](https://redis.io/commands/expire/)
