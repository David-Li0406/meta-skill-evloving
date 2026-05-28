---
title: Implement Proper Reconnection Logic
impact: HIGH
impactDescription: prevents cascading failures during network issues
tags: connection, resilience, retry, failover
---

## Implement Proper Reconnection Logic

Implement robust reconnection handling for network failures, Redis restarts, and failovers. Without proper retry logic, temporary issues become application outages. Most Redis clients have built-in retry mechanisms - configure them properly.

**Common Failure Scenarios:**
- Network blips (brief disconnection)
- Redis server restart
- Sentinel/Cluster failover
- Connection timeout
- Max connections reached

**Incorrect (no retry handling):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: No error handling
def get_user(user_id):
    return r.hgetall(f"user:{user_id}")  # Crashes on connection error

# Anti-pattern 2: Swallowing all errors
def get_user(user_id):
    try:
        return r.hgetall(f"user:{user_id}")
    except:
        return None  # Silently fails, no retry, hides issues

# Anti-pattern 3: Infinite retry without backoff
def get_user_retry_forever(user_id):
    while True:
        try:
            return r.hgetall(f"user:{user_id}")
        except redis.ConnectionError:
            pass  # Tight loop, hammers Redis
```

**Correct (proper reconnection and retry):**

```python
import redis
from redis.backoff import ExponentialBackoff
from redis.retry import Retry
import time

# Correct 1: Configure client with retry
retry = Retry(ExponentialBackoff(), retries=3)

r = redis.Redis(
    host='localhost',
    port=6379,
    socket_timeout=5,
    socket_connect_timeout=5,
    retry_on_timeout=True,
    retry=retry,
    health_check_interval=30  # Periodic health checks
)

# Correct 2: Manual retry with exponential backoff
def get_with_retry(func, max_retries=3, base_delay=0.1):
    """Execute function with exponential backoff retry"""
    last_exception = None

    for attempt in range(max_retries):
        try:
            return func()
        except (redis.ConnectionError, redis.TimeoutError) as e:
            last_exception = e
            if attempt < max_retries - 1:
                delay = base_delay * (2 ** attempt)  # 0.1, 0.2, 0.4
                time.sleep(delay)
                continue
            raise

    raise last_exception

# Usage
def get_user(user_id):
    return get_with_retry(lambda: r.hgetall(f"user:{user_id}"))

# Correct 3: Circuit breaker pattern
class CircuitBreaker:
    def __init__(self, failure_threshold=5, recovery_timeout=30):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failures = 0
        self.last_failure_time = None
        self.state = "closed"  # closed, open, half-open

    def call(self, func):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half-open"
            else:
                raise Exception("Circuit breaker is open")

        try:
            result = func()
            if self.state == "half-open":
                self.state = "closed"
                self.failures = 0
            return result
        except (redis.ConnectionError, redis.TimeoutError) as e:
            self.failures += 1
            self.last_failure_time = time.time()

            if self.failures >= self.failure_threshold:
                self.state = "open"

            raise

circuit_breaker = CircuitBreaker()

def get_user_safe(user_id):
    return circuit_breaker.call(lambda: r.hgetall(f"user:{user_id}"))
```

```python
# Correct 4: Handling Sentinel failover
from redis.sentinel import Sentinel

sentinel = Sentinel(
    [('sentinel1', 26379), ('sentinel2', 26379), ('sentinel3', 26379)],
    socket_timeout=0.5,
    sentinel_kwargs={'password': 'sentinel-password'}
)

# Get master connection (auto-discovers current master)
master = sentinel.master_for(
    'mymaster',
    socket_timeout=0.5,
    password='redis-password',
    retry_on_timeout=True
)

# Get replica for reads
replica = sentinel.slave_for(
    'mymaster',
    socket_timeout=0.5,
    password='redis-password'
)

def get_user(user_id):
    """Reads from replica, writes to master"""
    return replica.hgetall(f"user:{user_id}")

def update_user(user_id, data):
    """Writes go to master"""
    return master.hset(f"user:{user_id}", mapping=data)
```

```javascript
// Node.js - ioredis with retry
const Redis = require('ioredis');

const redis = new Redis({
    host: 'localhost',
    port: 6379,
    retryStrategy(times) {
        // Exponential backoff with max delay
        const delay = Math.min(times * 50, 2000);
        return delay;
    },
    maxRetriesPerRequest: 3,
    enableReadyCheck: true,
    reconnectOnError(err) {
        // Reconnect on specific errors
        const targetError = 'READONLY';
        if (err.message.includes(targetError)) {
            return true;  // Reconnect for READONLY (failover)
        }
        return false;
    }
});

redis.on('error', (err) => {
    console.error('Redis error:', err);
});

redis.on('reconnecting', () => {
    console.log('Reconnecting to Redis...');
});

// Sentinel support
const redis = new Redis({
    sentinels: [
        { host: 'sentinel1', port: 26379 },
        { host: 'sentinel2', port: 26379 }
    ],
    name: 'mymaster',
    sentinelRetryStrategy(times) {
        return Math.min(times * 10, 1000);
    }
});
```

```go
// Go - go-redis with retry and Sentinel
import "github.com/redis/go-redis/v9"

// With retry
rdb := redis.NewClient(&redis.Options{
    Addr:            "localhost:6379",
    MaxRetries:      3,
    MinRetryBackoff: 8 * time.Millisecond,
    MaxRetryBackoff: 512 * time.Millisecond,
    DialTimeout:     5 * time.Second,
    ReadTimeout:     3 * time.Second,
    WriteTimeout:    3 * time.Second,
    PoolTimeout:     4 * time.Second,
})

// Sentinel
rdb := redis.NewFailoverClient(&redis.FailoverOptions{
    MasterName:    "mymaster",
    SentinelAddrs: []string{"sentinel1:26379", "sentinel2:26379"},
    MaxRetries:    3,
})
```

Reference: [Redis High Availability](https://redis.io/docs/management/sentinel/)
