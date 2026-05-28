---
title: Implement Distributed Locks Correctly
impact: HIGH
impactDescription: prevents race conditions in distributed systems
tags: commands, locks, distributed, concurrency, redlock
---

## Implement Distributed Locks Correctly

Implement distributed locks using the single-instance SET NX pattern or Redlock algorithm for multi-instance deployments. Incorrect lock implementations lead to race conditions, deadlocks, or lock safety violations.

**Lock Requirements:**
1. **Mutual exclusion**: Only one client can hold the lock
2. **Deadlock-free**: Lock eventually releases (TTL)
3. **Fault-tolerant**: Lock works even if client crashes
4. **Identity**: Only the owner can release the lock

**Incorrect (unsafe lock implementations):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: SETNX without TTL
def acquire_lock_bad(lock_name):
    if r.setnx(lock_name, "1"):  # No TTL!
        return True
    return False
# If client crashes, lock is held forever (deadlock)

# Anti-pattern 2: Separate SETNX and EXPIRE (race condition)
def acquire_lock_bad2(lock_name, ttl):
    if r.setnx(lock_name, "1"):
        r.expire(lock_name, ttl)  # Race: might crash between these!
        return True
    return False

# Anti-pattern 3: No owner identity
def release_lock_bad(lock_name):
    r.delete(lock_name)  # Anyone can release!
# Client A acquires lock, takes long, lock expires
# Client B acquires lock
# Client A finishes, deletes B's lock!

# Anti-pattern 4: Check-then-delete race condition
def release_lock_bad2(lock_name, owner):
    if r.get(lock_name) == owner:  # Check
        r.delete(lock_name)  # Delete - race condition!
    # Lock could expire and be reacquired between check and delete
```

**Correct (safe lock implementation):**

```python
import redis
import uuid
import time
r = redis.Redis()

# Correct 1: SET with NX and EX (atomic acquire)
def acquire_lock(lock_name, owner, ttl_seconds=10):
    """
    Acquire lock atomically with SET NX EX.
    Returns True if lock acquired, False otherwise.
    """
    result = r.set(
        lock_name,
        owner,
        nx=True,     # Only set if not exists
        ex=ttl_seconds  # Expire after TTL
    )
    return result is True

# Correct 2: Lua script for safe release (atomic check-and-delete)
RELEASE_LOCK_SCRIPT = """
if redis.call("GET", KEYS[1]) == ARGV[1] then
    return redis.call("DEL", KEYS[1])
else
    return 0
end
"""
release_lock_script = r.register_script(RELEASE_LOCK_SCRIPT)

def release_lock(lock_name, owner):
    """Release lock only if we own it (atomic operation)"""
    return release_lock_script(keys=[lock_name], args=[owner]) == 1

# Correct 3: Lock with auto-renewal (for long operations)
EXTEND_LOCK_SCRIPT = """
if redis.call("GET", KEYS[1]) == ARGV[1] then
    return redis.call("PEXPIRE", KEYS[1], ARGV[2])
else
    return 0
end
"""
extend_lock_script = r.register_script(EXTEND_LOCK_SCRIPT)

def extend_lock(lock_name, owner, ttl_ms):
    """Extend lock TTL if we still own it"""
    return extend_lock_script(keys=[lock_name], args=[owner, ttl_ms]) == 1

# Correct 4: Full lock class implementation
class RedisLock:
    def __init__(self, redis_client, name, ttl_seconds=10):
        self.redis = redis_client
        self.name = f"lock:{name}"
        self.ttl = ttl_seconds
        self.owner = str(uuid.uuid4())
        self._release_script = self.redis.register_script(RELEASE_LOCK_SCRIPT)
        self._extend_script = self.redis.register_script(EXTEND_LOCK_SCRIPT)

    def acquire(self, blocking=True, timeout=None):
        """Acquire the lock, optionally blocking until available"""
        start = time.time()

        while True:
            if self.redis.set(self.name, self.owner, nx=True, ex=self.ttl):
                return True

            if not blocking:
                return False

            if timeout and (time.time() - start) >= timeout:
                return False

            time.sleep(0.1)  # Small delay before retry

    def release(self):
        """Release the lock if we own it"""
        return self._release_script(keys=[self.name], args=[self.owner]) == 1

    def extend(self, additional_time=None):
        """Extend lock TTL"""
        ttl_ms = (additional_time or self.ttl) * 1000
        return self._extend_script(keys=[self.name], args=[self.owner, ttl_ms]) == 1

    def __enter__(self):
        if not self.acquire():
            raise Exception(f"Could not acquire lock: {self.name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

# Usage
with RedisLock(r, "my-resource", ttl_seconds=30) as lock:
    # Critical section
    process_resource()

# Or manual usage
lock = RedisLock(r, "my-resource")
if lock.acquire(blocking=True, timeout=5):
    try:
        process_resource()
    finally:
        lock.release()
```

```python
# Correct 5: Redlock for distributed Redis (multiple masters)
# Use when you have multiple independent Redis masters for HA

from redlock import Redlock

# Initialize with multiple Redis instances
dlm = Redlock([
    {"host": "redis1", "port": 6379},
    {"host": "redis2", "port": 6379},
    {"host": "redis3", "port": 6379},
])

# Acquire lock (majority must agree)
lock = dlm.lock("my-resource", 10000)  # 10 second TTL

if lock:
    try:
        # Critical section
        process_resource()
    finally:
        dlm.unlock(lock)
else:
    print("Could not acquire lock")
```

```javascript
// Node.js - Distributed lock
const Redis = require('ioredis');
const redis = new Redis();

const RELEASE_SCRIPT = `
if redis.call("GET", KEYS[1]) == ARGV[1] then
    return redis.call("DEL", KEYS[1])
else
    return 0
end
`;

class RedisLock {
    constructor(redis, name, ttlSeconds = 10) {
        this.redis = redis;
        this.name = `lock:${name}`;
        this.ttl = ttlSeconds;
        this.owner = crypto.randomUUID();
    }

    async acquire(timeout = 0) {
        const start = Date.now();

        while (true) {
            const result = await this.redis.set(
                this.name,
                this.owner,
                'NX',
                'EX',
                this.ttl
            );

            if (result === 'OK') return true;
            if (timeout === 0) return false;
            if (Date.now() - start >= timeout * 1000) return false;

            await new Promise(r => setTimeout(r, 100));
        }
    }

    async release() {
        const result = await this.redis.eval(
            RELEASE_SCRIPT,
            1,
            this.name,
            this.owner
        );
        return result === 1;
    }
}

// Usage
const lock = new RedisLock(redis, 'my-resource');
if (await lock.acquire(5)) {
    try {
        await processResource();
    } finally {
        await lock.release();
    }
}
```

Reference: [Distributed Locks with Redis](https://redis.io/docs/manual/patterns/distributed-locks/)
