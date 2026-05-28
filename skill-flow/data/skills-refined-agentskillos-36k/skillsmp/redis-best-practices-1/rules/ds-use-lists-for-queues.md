---
title: Use Lists for Queues and Stacks
impact: HIGH
impactDescription: O(1) push/pop, blocking operations for workers
tags: data-structures, list, queue, stack, messaging
---

## Use Lists for Queues and Stacks

Use Redis Lists for implementing queues (FIFO), stacks (LIFO), and capped collections. Lists support O(1) push/pop operations at both ends and blocking variants for efficient worker patterns.

**Incorrect (polling or wrong data structure):**

```python
import redis
import time
import json
r = redis.Redis()

# Anti-pattern 1: Using Set for ordered processing
r.sadd("jobs", json.dumps({"id": 1, "task": "send_email"}))
# Sets have no order guarantee, can't process FIFO

# Anti-pattern 2: Polling with sleep
while True:
    job = r.get("next_job")
    if job:
        process(job)
        r.delete("next_job")
    else:
        time.sleep(0.1)  # Wasteful polling, adds latency

# Anti-pattern 3: Using sorted set for simple queue
r.zadd("queue", {json.dumps(job): time.time()})
# Overhead of maintaining scores when FIFO is all you need
```

**Correct (using Lists):**

```python
import redis
import json
r = redis.Redis()

# Basic queue (FIFO) - push left, pop right
def enqueue(queue_name, item):
    """Add item to queue"""
    r.lpush(queue_name, json.dumps(item))

def dequeue(queue_name):
    """Remove and return oldest item"""
    item = r.rpop(queue_name)
    return json.loads(item) if item else None

# Stack (LIFO) - push and pop from same end
def push_stack(stack_name, item):
    r.lpush(stack_name, json.dumps(item))

def pop_stack(stack_name):
    item = r.lpop(stack_name)
    return json.loads(item) if item else None

# Producer
r.lpush("jobs:email", json.dumps({
    "to": "user@example.com",
    "subject": "Welcome!"
}))

# Consumer - non-blocking
job = r.rpop("jobs:email")

# Consumer - blocking (waits for item, no polling!)
# This is the recommended pattern for workers
job = r.brpop("jobs:email", timeout=30)  # Wait up to 30 seconds
# Returns: (b'jobs:email', b'{"to": "user@..."}') or None on timeout

# Multiple queues with priority - check high priority first
job = r.brpop(["jobs:high", "jobs:medium", "jobs:low"], timeout=30)
```

```python
# Reliable queue pattern - items moved to processing list
import redis
import json
import uuid

r = redis.Redis()

def reliable_dequeue(queue_name, processing_name):
    """
    Move item atomically from queue to processing list.
    If worker crashes, item is still in processing list for recovery.
    """
    # BLMOVE (Redis 6.2+): blocking move from source to destination
    # Replaces deprecated BRPOPLPUSH
    item = r.blmove(queue_name, processing_name, timeout=30, src="RIGHT", dest="LEFT")
    # For Redis < 6.2, use: r.brpoplpush(queue_name, processing_name, timeout=30)
    return json.loads(item) if item else None

def complete_job(processing_name, item):
    """Remove item from processing list after successful completion"""
    r.lrem(processing_name, 1, json.dumps(item))

def recover_stuck_jobs(processing_name, queue_name):
    """Move stuck jobs back to queue (run periodically)"""
    # In production, track timestamps to only recover old items
    while True:
        # LMOVE (Redis 6.2+) replaces deprecated RPOPLPUSH
        item = r.lmove(processing_name, queue_name, src="RIGHT", dest="LEFT")
        # For Redis < 6.2, use: r.rpoplpush(processing_name, queue_name)
        if not item:
            break
```

```python
# Capped list - keep only N most recent items
import redis
r = redis.Redis()

def add_to_activity_feed(user_id, activity):
    """Add activity and keep only last 100 items"""
    key = f"activity:{user_id}"
    pipe = r.pipeline()
    pipe.lpush(key, json.dumps(activity))
    pipe.ltrim(key, 0, 99)  # Keep only first 100 (indices 0-99)
    pipe.execute()

def get_recent_activity(user_id, count=20):
    """Get N most recent activities"""
    return r.lrange(f"activity:{user_id}", 0, count - 1)
```

```javascript
// Node.js
const redis = require('redis');
const client = redis.createClient();

// Enqueue
await client.lPush('jobs', JSON.stringify({ task: 'process_order' }));

// Blocking dequeue (worker pattern)
const result = await client.brPop('jobs', 30); // 30 second timeout
if (result) {
    const job = JSON.parse(result.element);
    // process job
}

// Multiple queues with priority
const result = await client.brPop(['jobs:high', 'jobs:low'], 30);
```

```go
// Go
import "github.com/redis/go-redis/v9"

rdb := redis.NewClient(&redis.Options{Addr: "localhost:6379"})

// Enqueue
rdb.LPush(ctx, "jobs", `{"task": "send_email"}`)

// Blocking dequeue
result, err := rdb.BRPop(ctx, 30*time.Second, "jobs").Result()
if err != redis.Nil {
    job := result[1] // result[0] is key name, result[1] is value
}
```

Reference: [Redis Lists](https://redis.io/docs/data-types/lists/)
