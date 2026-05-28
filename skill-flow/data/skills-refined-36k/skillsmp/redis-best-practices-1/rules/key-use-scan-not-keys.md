---
title: Use SCAN Instead of KEYS in Production
impact: CRITICAL
impactDescription: KEYS blocks Redis for seconds/minutes with large datasets
tags: keys, commands, performance, production
---

## Use SCAN Instead of KEYS in Production

Never use the `KEYS` command in production. It scans the entire keyspace in a single blocking operation, freezing Redis for seconds or even minutes with large datasets. Use `SCAN` for cursor-based iteration instead.

**Why KEYS is Dangerous:**
- O(n) where n is total keys in database (not just matches)
- Blocks Redis completely during execution
- 1 million keys ≈ 1 second block; 100 million keys ≈ minutes
- Can trigger cascading failures in distributed systems

**Incorrect (using KEYS):**

```python
import redis
r = redis.Redis()

# NEVER DO THIS IN PRODUCTION
# Anti-pattern 1: Finding keys by pattern
user_keys = r.keys("user:*")  # Blocks entire Redis!

# Anti-pattern 2: Counting keys
session_count = len(r.keys("session:*"))  # Terrible!

# Anti-pattern 3: Deleting by pattern
for key in r.keys("cache:old:*"):  # Double terrible!
    r.delete(key)

# Anti-pattern 4: In application code
def get_all_users():
    keys = r.keys("user:*")  # Production disaster waiting
    return [r.hgetall(k) for k in keys]

# Anti-pattern 5: Finding expired/orphan keys
temp_keys = r.keys("temp:*")  # Blocks production
```

**Correct (using SCAN):**

```python
import redis
r = redis.Redis()

# Correct 1: Iterate with SCAN (cursor-based, non-blocking)
def find_keys_by_pattern(pattern, count=100):
    """
    Non-blocking key iteration using SCAN.
    count is a hint - Redis may return more or fewer.
    """
    keys = []
    cursor = 0

    while True:
        cursor, batch = r.scan(cursor, match=pattern, count=count)
        keys.extend(batch)
        if cursor == 0:  # Iteration complete
            break

    return keys

# Correct 2: Using scan_iter (Python wrapper)
def find_keys_iter(pattern):
    """Pythonic iterator over SCAN results"""
    for key in r.scan_iter(match=pattern, count=100):
        yield key

# Usage
for key in r.scan_iter(match="user:*", count=100):
    print(key)

# Correct 3: Count keys without blocking (approximate is OK)
def count_keys_by_pattern(pattern, sample_size=10000):
    """Count keys matching pattern without blocking"""
    count = 0
    for _ in r.scan_iter(match=pattern, count=100):
        count += 1
        if count >= sample_size:
            # For large sets, return estimate
            break
    return count

# Or use INFO for total key count (instant)
info = r.info("keyspace")
# Returns: {'db0': {'keys': 1234567, 'expires': 123456, 'avg_ttl': 3600000}}

# Correct 4: Delete by pattern safely
def delete_by_pattern(pattern, batch_size=100):
    """Delete keys matching pattern in batches"""
    deleted = 0

    # Use SCAN to find keys, delete in batches
    pipe = r.pipeline()
    batch = []

    for key in r.scan_iter(match=pattern, count=100):
        batch.append(key)

        if len(batch) >= batch_size:
            pipe.delete(*batch)
            pipe.execute()
            deleted += len(batch)
            batch = []
            pipe = r.pipeline()

    # Delete remaining
    if batch:
        pipe.delete(*batch)
        pipe.execute()
        deleted += len(batch)

    return deleted

# Correct 5: Process keys in batches
def process_all_users(batch_size=100):
    """Process users without blocking Redis"""
    batch = []

    for key in r.scan_iter(match="user:*", count=100):
        batch.append(key)

        if len(batch) >= batch_size:
            # Process batch
            users = [r.hgetall(k) for k in batch]
            yield users
            batch = []

    if batch:
        users = [r.hgetall(k) for k in batch]
        yield users
```

```python
# SCAN for different data types

# SSCAN - scan Set members
def get_all_set_members(key):
    members = []
    cursor = 0
    while True:
        cursor, batch = r.sscan(key, cursor, count=100)
        members.extend(batch)
        if cursor == 0:
            break
    return members

# HSCAN - scan Hash fields
def get_all_hash_fields(key):
    fields = {}
    cursor = 0
    while True:
        cursor, batch = r.hscan(key, cursor, count=100)
        fields.update(batch)
        if cursor == 0:
            break
    return fields

# ZSCAN - scan Sorted Set members
def get_all_zset_members(key):
    members = []
    cursor = 0
    while True:
        cursor, batch = r.zscan(key, cursor, count=100)
        members.extend(batch)
        if cursor == 0:
            break
    return members
```

```javascript
// Node.js - SCAN iteration
const redis = require('redis');
const client = redis.createClient();

// Using scanIterator (Node Redis v4+)
async function findKeysByPattern(pattern) {
    const keys = [];
    for await (const key of client.scanIterator({ MATCH: pattern, COUNT: 100 })) {
        keys.push(key);
    }
    return keys;
}

// Delete by pattern
async function deleteByPattern(pattern) {
    let deleted = 0;
    const batch = [];

    for await (const key of client.scanIterator({ MATCH: pattern, COUNT: 100 })) {
        batch.push(key);
        if (batch.length >= 100) {
            await client.del(batch);
            deleted += batch.length;
            batch.length = 0;
        }
    }

    if (batch.length > 0) {
        await client.del(batch);
        deleted += batch.length;
    }

    return deleted;
}
```

```python
# Only safe use of KEYS: local development/debugging
# Even then, prefer SCAN

# In redis-cli for debugging (NOT production):
# KEYS user:* (only if you know dataset is small)
# SCAN 0 MATCH user:* COUNT 10 (safer)
# DBSIZE (get total key count)
```

Reference: [Redis SCAN Command](https://redis.io/commands/scan/)
