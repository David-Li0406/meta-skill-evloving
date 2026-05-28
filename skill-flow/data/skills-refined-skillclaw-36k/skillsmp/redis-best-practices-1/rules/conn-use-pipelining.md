---
title: Use Pipelining for Multiple Commands
impact: HIGH
impactDescription: reduces latency 5-10x for batched operations
tags: connection, pipeline, performance, batching
---

## Use Pipelining for Multiple Commands

Use pipelining to send multiple commands without waiting for individual responses. This dramatically reduces network round trips and improves throughput. Without pipelining, each command waits for a response before the next is sent.

**Performance Impact:**
- Without pipelining: 100 commands = 100 round trips
- With pipelining: 100 commands = 1 round trip
- Typical improvement: 5-10x faster for batched operations

**Incorrect (sequential commands):**

```python
import redis
r = redis.Redis()

# Anti-pattern: Sequential commands
def get_multiple_users_bad(user_ids):
    users = {}
    for user_id in user_ids:
        users[user_id] = r.hgetall(f"user:{user_id}")  # Round trip per user!
    return users
# 100 users = 100 round trips = 100+ ms (with 1ms RTT each)

# Anti-pattern: Sequential writes
def save_metrics_bad(metrics):
    for metric_name, value in metrics.items():
        r.set(f"metric:{metric_name}", value)  # Round trip per metric!

# Anti-pattern: Setting multiple fields
def update_user_bad(user_id, updates):
    for field, value in updates.items():
        r.hset(f"user:{user_id}", field, value)  # Round trip per field!
```

**Correct (using pipelines):**

```python
import redis
r = redis.Redis()

# Correct 1: Pipeline for multiple reads
def get_multiple_users(user_ids):
    pipe = r.pipeline()
    for user_id in user_ids:
        pipe.hgetall(f"user:{user_id}")
    results = pipe.execute()  # Single round trip!
    return dict(zip(user_ids, results))
# 100 users = 1 round trip = ~1-2ms

# Correct 2: Pipeline for multiple writes
def save_metrics(metrics):
    pipe = r.pipeline()
    for metric_name, value in metrics.items():
        pipe.set(f"metric:{metric_name}", value)
    pipe.execute()

# Correct 3: Use MGET/MSET for strings (built-in batching)
def get_multiple_values(keys):
    return r.mget(keys)  # Single command for multiple keys

def set_multiple_values(mapping):
    return r.mset(mapping)  # Single command

# Correct 4: Pipeline with transactions (MULTI/EXEC)
def transfer_points(from_user, to_user, amount):
    """Atomic transfer using transaction"""
    pipe = r.pipeline(transaction=True)  # Wraps in MULTI/EXEC
    pipe.hincrby(f"user:{from_user}", "points", -amount)
    pipe.hincrby(f"user:{to_user}", "points", amount)
    return pipe.execute()

# Correct 5: Pipeline for mixed operations
def initialize_user(user_id, user_data):
    pipe = r.pipeline()
    pipe.hset(f"user:{user_id}", mapping=user_data)
    pipe.sadd("users:all", user_id)
    pipe.zadd("users:by_created", {user_id: time.time()})
    pipe.expire(f"user:{user_id}:session", 86400)
    pipe.execute()
```

```python
# Chunked pipelining for very large batches
def get_users_chunked(user_ids, chunk_size=1000):
    """Process large batches in chunks to avoid memory issues"""
    all_users = {}

    for i in range(0, len(user_ids), chunk_size):
        chunk = user_ids[i:i + chunk_size]
        pipe = r.pipeline()

        for user_id in chunk:
            pipe.hgetall(f"user:{user_id}")

        results = pipe.execute()

        for user_id, data in zip(chunk, results):
            all_users[user_id] = data

    return all_users

# Pipeline with error handling
def safe_pipeline_execute(operations):
    """Execute pipeline and handle partial failures"""
    pipe = r.pipeline()

    for op in operations:
        getattr(pipe, op['cmd'])(*op['args'])

    results = pipe.execute(raise_on_error=False)

    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"Operation {i} failed: {result}")
            # Handle error for operations[i]

    return results
```

```javascript
// Node.js - Pipelining with ioredis
const Redis = require('ioredis');
const redis = new Redis();

// Pipeline
async function getMultipleUsers(userIds) {
    const pipeline = redis.pipeline();

    userIds.forEach(id => {
        pipeline.hgetall(`user:${id}`);
    });

    const results = await pipeline.exec();
    // results: [[null, {...}], [null, {...}], ...]
    // Each item: [error, result]

    return userIds.reduce((acc, id, i) => {
        acc[id] = results[i][1];
        return acc;
    }, {});
}

// Using multi for transactions
async function transferPoints(fromUser, toUser, amount) {
    const results = await redis.multi()
        .hincrby(`user:${fromUser}`, 'points', -amount)
        .hincrby(`user:${toUser}`, 'points', amount)
        .exec();

    return results;
}
```

```go
// Go - Pipelining with go-redis
import "github.com/redis/go-redis/v9"

func GetMultipleUsers(ctx context.Context, userIDs []string) (map[string]map[string]string, error) {
    pipe := rdb.Pipeline()

    cmds := make(map[string]*redis.MapStringStringCmd)
    for _, id := range userIDs {
        cmds[id] = pipe.HGetAll(ctx, fmt.Sprintf("user:%s", id))
    }

    _, err := pipe.Exec(ctx)
    if err != nil {
        return nil, err
    }

    results := make(map[string]map[string]string)
    for id, cmd := range cmds {
        results[id], _ = cmd.Result()
    }

    return results, nil
}

// Transaction
func TransferPoints(ctx context.Context, from, to string, amount int64) error {
    _, err := rdb.TxPipelined(ctx, func(pipe redis.Pipeliner) error {
        pipe.HIncrBy(ctx, fmt.Sprintf("user:%s", from), "points", -amount)
        pipe.HIncrBy(ctx, fmt.Sprintf("user:%s", to), "points", amount)
        return nil
    })
    return err
}
```

Reference: [Redis Pipelining](https://redis.io/docs/manual/pipelining/)
