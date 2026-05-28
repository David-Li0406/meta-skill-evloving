---
title: Always Use Connection Pooling
impact: CRITICAL
impactDescription: prevents connection exhaustion, reduces latency 10-100x
tags: connection, pool, performance, resources
---

## Always Use Connection Pooling

Always use connection pooling instead of creating new connections per request. Creating connections is expensive (TCP handshake, authentication, TLS negotiation) and without pooling you'll exhaust available connections under load.

**Connection Costs:**
- TCP handshake: ~1ms local, 10-100ms remote
- TLS negotiation: +10-50ms
- AUTH command: +1 round trip
- Redis max connections: 10,000 by default

**Incorrect (connection per request):**

```python
import redis

# Anti-pattern 1: New connection per request
def get_user_bad(user_id):
    r = redis.Redis(host='localhost', port=6379)  # New connection!
    user = r.hgetall(f"user:{user_id}")
    r.close()  # Connection closed
    return user
# Each call = TCP connect + potentially AUTH + command + close
# Under load: connection exhaustion, high latency

# Anti-pattern 2: Global connection without pool
r = redis.Redis(host='localhost', port=6379)  # Single connection

def get_user(user_id):
    return r.hgetall(f"user:{user_id}")  # All requests share ONE connection
# Problem: No concurrency, connection failure affects all requests
```

```javascript
// Node.js - Anti-pattern
const redis = require('redis');

async function getUserBad(userId) {
    const client = redis.createClient();  // New connection per call!
    await client.connect();
    const user = await client.hGetAll(`user:${userId}`);
    await client.disconnect();
    return user;
}
```

**Correct (connection pooling):**

```python
import redis

# Correct 1: Use ConnectionPool
pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=50,           # Limit connections
    socket_timeout=5,             # Timeout for operations
    socket_connect_timeout=5,     # Timeout for connection
    retry_on_timeout=True,
    health_check_interval=30      # Periodic health checks
)

def get_redis():
    return redis.Redis(connection_pool=pool)

def get_user(user_id):
    r = get_redis()  # Gets connection from pool
    return r.hgetall(f"user:{user_id}")
    # Connection automatically returned to pool

# Correct 2: Using redis-py's built-in pool (simpler)
# Redis() creates a pool internally when decode_responses is used
r = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True,
    max_connections=50,
    socket_timeout=5,
    socket_connect_timeout=5,
    retry_on_timeout=True
)

def get_user(user_id):
    return r.hgetall(f"user:{user_id}")

# Correct 3: With authentication and TLS
pool = redis.ConnectionPool(
    host='redis.example.com',
    port=6380,
    password='your-password',
    ssl=True,
    ssl_cert_reqs='required',
    ssl_ca_certs='/path/to/ca.crt',
    max_connections=50,
    socket_timeout=5
)
```

```python
# Flask/Django integration
from flask import Flask, g
import redis

app = Flask(__name__)

pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    max_connections=50,
    decode_responses=True
)

def get_redis():
    if 'redis' not in g:
        g.redis = redis.Redis(connection_pool=pool)
    return g.redis

@app.route('/user/<user_id>')
def get_user(user_id):
    r = get_redis()
    return r.hgetall(f"user:{user_id}")
```

```python
# Async Python (aioredis / redis-py async)
import redis.asyncio as redis

# Create pool once at startup
pool = redis.ConnectionPool.from_url(
    "redis://localhost:6379",
    max_connections=50,
    decode_responses=True
)

async def get_user(user_id):
    r = redis.Redis(connection_pool=pool)
    return await r.hgetall(f"user:{user_id}")

# Or use connection pool context manager
async def main():
    pool = redis.ConnectionPool.from_url("redis://localhost")
    r = redis.Redis(connection_pool=pool)

    async with r.client() as conn:
        await conn.set("key", "value")

    await pool.disconnect()
```

```javascript
// Node.js - Correct pooling with ioredis
const Redis = require('ioredis');

// ioredis handles pooling internally
const redis = new Redis({
    host: 'localhost',
    port: 6379,
    maxRetriesPerRequest: 3,
    enableReadyCheck: true,
    connectTimeout: 5000,
    // Connection pool settings
    lazyConnect: true,
    keepAlive: 30000,
});

// For multiple connections (e.g., pub/sub)
const redisPub = new Redis();
const redisSub = new Redis();

async function getUser(userId) {
    return redis.hgetall(`user:${userId}`);
}
```

```go
// Go - go-redis handles pooling automatically
import "github.com/redis/go-redis/v9"

var rdb = redis.NewClient(&redis.Options{
    Addr:         "localhost:6379",
    Password:     "",
    DB:           0,
    PoolSize:     50,           // Connection pool size
    MinIdleConns: 10,           // Minimum idle connections
    PoolTimeout:  4 * time.Second,
    DialTimeout:  5 * time.Second,
    ReadTimeout:  3 * time.Second,
    WriteTimeout: 3 * time.Second,
})

func GetUser(ctx context.Context, userID string) (map[string]string, error) {
    return rdb.HGetAll(ctx, fmt.Sprintf("user:%s", userID)).Result()
}
```

```java
// Java - Jedis with connection pool
import redis.clients.jedis.JedisPool;
import redis.clients.jedis.JedisPoolConfig;

JedisPoolConfig poolConfig = new JedisPoolConfig();
poolConfig.setMaxTotal(50);
poolConfig.setMaxIdle(10);
poolConfig.setMinIdle(5);
poolConfig.setTestOnBorrow(true);
poolConfig.setTestOnReturn(true);

JedisPool pool = new JedisPool(poolConfig, "localhost", 6379);

public Map<String, String> getUser(String userId) {
    try (Jedis jedis = pool.getResource()) {  // Auto-returned to pool
        return jedis.hgetAll("user:" + userId);
    }
}
```

Reference: [Redis Connection Handling](https://redis.io/docs/clients/)
