---
title: Use Hashes for Object Storage
impact: CRITICAL
impactDescription: reduces memory 50-90%, enables partial updates
tags: data-structures, hash, memory, objects
---

## Use Hashes for Object Storage

Store related fields together in a Hash instead of multiple String keys. Hashes are memory-efficient (Redis optimizes small hashes with ziplist encoding) and support partial field updates without reading the entire object.

**Incorrect (multiple keys per object):**

```python
# Anti-pattern: One key per field = memory overhead + multiple round trips
import redis
r = redis.Redis()

# Storing user data as separate keys
r.set("user:123:name", "John Doe")
r.set("user:123:email", "john@example.com")
r.set("user:123:age", "30")
r.set("user:123:city", "New York")

# Reading requires multiple commands
name = r.get("user:123:name")
email = r.get("user:123:email")
age = r.get("user:123:age")
# 3 round trips = 3x network latency
# Plus: each key has ~50 bytes overhead
```

```javascript
// Node.js - Same anti-pattern
const redis = require('redis');
const client = redis.createClient();

await client.set('user:123:name', 'John Doe');
await client.set('user:123:email', 'john@example.com');
await client.set('user:123:age', '30');
```

**Correct (Hash for object):**

```python
# Best practice: Single Hash holds all fields
import redis
r = redis.Redis()

# Store all fields in one Hash
r.hset("user:123", mapping={
    "name": "John Doe",
    "email": "john@example.com",
    "age": "30",
    "city": "New York"
})

# Single round trip for all fields
user = r.hgetall("user:123")
# Returns: {b'name': b'John Doe', b'email': b'john@example.com', ...}

# Get specific fields only
name, email = r.hmget("user:123", "name", "email")

# Partial update without reading entire object
r.hset("user:123", "email", "newemail@example.com")

# Increment numeric field atomically
r.hincrby("user:123", "login_count", 1)
```

```javascript
// Node.js - Correct pattern
const redis = require('redis');
const client = redis.createClient();

// Store as Hash
await client.hSet('user:123', {
    name: 'John Doe',
    email: 'john@example.com',
    age: '30'
});

// Get all fields
const user = await client.hGetAll('user:123');

// Get specific fields
const [name, email] = await client.hmGet('user:123', ['name', 'email']);

// Partial update
await client.hSet('user:123', 'email', 'newemail@example.com');
```

```go
// Go - Correct pattern
import "github.com/redis/go-redis/v9"

rdb := redis.NewClient(&redis.Options{Addr: "localhost:6379"})

// Store as Hash
rdb.HSet(ctx, "user:123", map[string]interface{}{
    "name":  "John Doe",
    "email": "john@example.com",
    "age":   "30",
})

// Get all fields
user, _ := rdb.HGetAll(ctx, "user:123").Result()
```

Reference: [Redis Hashes](https://redis.io/docs/data-types/hashes/)
