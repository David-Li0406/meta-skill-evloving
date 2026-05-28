---
title: Configure Appropriate Timeouts
impact: HIGH
impactDescription: prevents hung connections, enables fast failure detection
tags: connection, timeout, performance, reliability
---

## Configure Appropriate Timeouts

Configure appropriate timeouts for connections, reads, and writes. Without timeouts, operations can hang indefinitely during network issues. Too short timeouts cause false failures; too long delays error detection.

**Timeout Types:**
- **Connect timeout**: Time to establish TCP connection
- **Socket/Read timeout**: Time to wait for response
- **Command timeout**: Time for specific operation
- **Pool timeout**: Time to wait for available connection

**Recommended Values:**
- Connect timeout: 5 seconds (longer for cross-region)
- Socket timeout: 1-5 seconds (depends on expected operation time)
- Pool timeout: 1-5 seconds
- Slow operations: Use specific longer timeouts

**Incorrect (no or inappropriate timeouts):**

```python
import redis

# Anti-pattern 1: No timeouts configured
r = redis.Redis(host='localhost', port=6379)
# Default: no socket timeout, operations can hang forever

# Anti-pattern 2: Timeouts too short
r = redis.Redis(
    host='localhost',
    port=6379,
    socket_timeout=0.1  # 100ms - too short for network variance
)
# Results in frequent false timeouts

# Anti-pattern 3: Same timeout for all operations
r = redis.Redis(socket_timeout=1)
# BLPOP with 30s wait will timeout after 1s

# Anti-pattern 4: No connect timeout
# If Redis is down, connection attempts hang for OS default (~120s)
```

**Correct (appropriate timeout configuration):**

```python
import redis

# Correct 1: Configure all timeout types
r = redis.Redis(
    host='localhost',
    port=6379,
    socket_timeout=5,           # Read/write timeout
    socket_connect_timeout=5,    # Connection establishment timeout
    socket_keepalive=True,       # Enable TCP keepalive
    socket_keepalive_options={
        # Linux TCP keepalive options
        1: 60,   # TCP_KEEPIDLE: seconds before keepalive probes
        2: 15,   # TCP_KEEPINTVL: interval between probes
        3: 3     # TCP_KEEPCNT: failed probes before connection drop
    }
)

# Correct 2: Connection pool with timeouts
pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=50,
    socket_timeout=5,
    socket_connect_timeout=5,
    retry_on_timeout=True,
    health_check_interval=30     # Check connection health periodically
)

r = redis.Redis(connection_pool=pool)

# Correct 3: Specific timeout for blocking operations
def wait_for_job(queue, timeout=30):
    """BLPOP with appropriate timeout"""
    # Note: socket_timeout should be > blocking timeout
    result = r.blpop(queue, timeout=timeout)
    return result

# Or create client with longer timeout for blocking ops
r_blocking = redis.Redis(
    host='localhost',
    port=6379,
    socket_timeout=60  # Longer timeout for blocking operations
)

def wait_for_job(queue, timeout=30):
    return r_blocking.blpop(queue, timeout=timeout)

# Correct 4: Async client with timeouts
import redis.asyncio as redis

async_pool = redis.ConnectionPool.from_url(
    "redis://localhost",
    socket_timeout=5,
    socket_connect_timeout=5
)
```

```python
# Timeout strategy by operation type

class RedisClient:
    def __init__(self):
        # Standard operations (fast)
        self.fast = redis.Redis(
            host='localhost',
            port=6379,
            socket_timeout=2,
            socket_connect_timeout=5
        )

        # Blocking operations
        self.blocking = redis.Redis(
            host='localhost',
            port=6379,
            socket_timeout=65,  # > max blocking time + buffer
            socket_connect_timeout=5
        )

        # Slow operations (large scans, etc.)
        self.slow = redis.Redis(
            host='localhost',
            port=6379,
            socket_timeout=30,
            socket_connect_timeout=5
        )

    def get(self, key):
        return self.fast.get(key)

    def blpop(self, key, timeout=60):
        return self.blocking.blpop(key, timeout=timeout)

    def scan_all(self, pattern):
        return list(self.slow.scan_iter(match=pattern))
```

```javascript
// Node.js - ioredis timeouts
const Redis = require('ioredis');

const redis = new Redis({
    host: 'localhost',
    port: 6379,
    connectTimeout: 5000,        // Connection timeout (ms)
    commandTimeout: 5000,        // Per-command timeout (ms)
    enableOfflineQueue: true,    // Queue commands while reconnecting
    maxRetriesPerRequest: 3,
    retryStrategy(times) {
        if (times > 3) return null;  // Stop retrying
        return Math.min(times * 200, 1000);
    }
});

// Blocking operations with specific timeout
async function waitForJob(queue, timeoutSeconds = 30) {
    // BLPOP timeout is in seconds
    return redis.blpop(queue, timeoutSeconds);
}
```

```go
// Go - go-redis timeouts
import "github.com/redis/go-redis/v9"

rdb := redis.NewClient(&redis.Options{
    Addr:         "localhost:6379",
    DialTimeout:  5 * time.Second,  // Connection timeout
    ReadTimeout:  3 * time.Second,  // Socket read timeout
    WriteTimeout: 3 * time.Second,  // Socket write timeout
    PoolTimeout:  4 * time.Second,  // Pool wait timeout
    PoolSize:     50,
    MinIdleConns: 10,
})

// Context timeout for specific operations
func GetWithTimeout(key string, timeout time.Duration) (string, error) {
    ctx, cancel := context.WithTimeout(context.Background(), timeout)
    defer cancel()

    return rdb.Get(ctx, key).Result()
}

// Blocking operation with appropriate timeout
func WaitForJob(ctx context.Context, queue string, timeout time.Duration) ([]string, error) {
    return rdb.BLPop(ctx, timeout, queue).Result()
}
```

```java
// Java - Jedis timeouts
import redis.clients.jedis.JedisPoolConfig;
import redis.clients.jedis.JedisPool;

JedisPoolConfig config = new JedisPoolConfig();
config.setMaxTotal(50);
config.setMaxWaitMillis(5000);  // Pool timeout

// Connection and socket timeouts
JedisPool pool = new JedisPool(
    config,
    "localhost",
    6379,
    5000,  // Connection timeout (ms)
    5000,  // Socket timeout (ms)
    null,  // Password
    0      // Database
);
```

Reference: [Redis Client Handling](https://redis.io/docs/clients/)
