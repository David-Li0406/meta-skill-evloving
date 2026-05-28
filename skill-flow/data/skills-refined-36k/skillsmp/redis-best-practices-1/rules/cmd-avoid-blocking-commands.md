---
title: Understand Blocking Command Implications
impact: MEDIUM-HIGH
impactDescription: blocking commands tie up connections, require careful handling
tags: commands, blocking, performance, architecture
---

## Understand Blocking Command Implications

Blocking commands (BLPOP, BRPOP, BLMOVE, BRPOPLPUSH, BLMPOP, BZPOPMIN, BZPOPMAX, XREAD with BLOCK) tie up the connection until data arrives or timeout. Use them appropriately with dedicated connections and proper timeouts.

**Blocking Command Characteristics:**
- Connection is blocked and unusable for other operations
- Should use dedicated connections
- Always specify reasonable timeouts
- Useful for worker patterns and message queues

**Incorrect (blocking command misuse):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: Blocking on shared connection
def get_data(key):
    return r.get(key)

def process_jobs():
    while True:
        # This blocks the connection used for get_data!
        job = r.blpop("jobs", timeout=0)  # Blocks forever
        process(job)

# Anti-pattern 2: No timeout
def wait_for_message():
    return r.blpop("messages", timeout=0)  # Blocks forever!
# If producer dies, worker hangs forever

# Anti-pattern 3: Blocking in request handler
def api_handler(request):
    # Don't block in request handlers!
    item = r.blpop("queue", timeout=30)  # Ties up web worker
    return process(item)

# Anti-pattern 4: Wrong timeout for socket
r = redis.Redis(socket_timeout=5)
r.blpop("queue", timeout=30)  # Socket times out before command!
```

**Correct (proper blocking command usage):**

```python
import redis
import threading

# Correct 1: Dedicated connection for blocking operations
class RedisQueues:
    def __init__(self):
        # Regular operations
        self.redis = redis.Redis(
            socket_timeout=5,
            socket_connect_timeout=5
        )
        # Blocking operations - longer socket timeout
        self.redis_blocking = redis.Redis(
            socket_timeout=65,  # > max blocking timeout + buffer
            socket_connect_timeout=5
        )

    def get(self, key):
        return self.redis.get(key)

    def blpop(self, key, timeout=60):
        return self.redis_blocking.blpop(key, timeout=timeout)

# Correct 2: Worker with proper timeout and reconnection
def job_worker(queue_name, process_func):
    """Worker with proper blocking command handling"""
    r = redis.Redis(
        socket_timeout=65,
        retry_on_timeout=True,
        health_check_interval=30
    )

    while True:
        try:
            # Always use timeout, never block forever
            result = r.blpop(queue_name, timeout=30)

            if result:
                queue, data = result
                try:
                    process_func(data)
                except Exception as e:
                    # Log and continue, don't crash worker
                    print(f"Error processing job: {e}")
            # If None, timeout reached, loop again

        except redis.ConnectionError as e:
            print(f"Connection error: {e}, reconnecting...")
            time.sleep(1)

# Correct 3: Multiple queues with priority
def priority_worker():
    """Process high priority queue first"""
    r = redis.Redis(socket_timeout=35)

    while True:
        # BLPOP checks queues in order, blocks until any has data
        result = r.blpop(
            ["queue:high", "queue:medium", "queue:low"],
            timeout=30
        )

        if result:
            queue, job = result
            print(f"Processing from {queue}: {job}")
            process_job(job)

# Correct 4: Non-blocking alternative with polling
def polling_worker(queue_name, poll_interval=0.1):
    """Alternative: poll instead of block"""
    r = redis.Redis(socket_timeout=5)

    while True:
        # Non-blocking pop
        job = r.rpop(queue_name)

        if job:
            process_job(job)
        else:
            # No job available, wait before polling again
            time.sleep(poll_interval)

# Correct 5: Async blocking with timeout
import asyncio
import redis.asyncio as redis

async def async_worker(queue_name):
    r = redis.Redis()

    while True:
        try:
            # Async BLPOP with timeout
            result = await r.blpop(queue_name, timeout=30)
            if result:
                await process_job_async(result[1])
        except asyncio.CancelledError:
            break
        except Exception as e:
            print(f"Worker error: {e}")
            await asyncio.sleep(1)
```

```python
# Correct 6: Stream-based alternative (recommended for new projects)
def stream_worker(stream_name, group_name, consumer_name):
    """Use Streams instead of blocking list operations"""
    r = redis.Redis(socket_timeout=35)

    # Create consumer group if not exists
    try:
        r.xgroup_create(stream_name, group_name, id='0', mkstream=True)
    except redis.ResponseError:
        pass  # Group already exists

    while True:
        # XREADGROUP with blocking
        messages = r.xreadgroup(
            group_name,
            consumer_name,
            {stream_name: '>'},
            count=10,
            block=30000  # 30 seconds in milliseconds
        )

        for stream, stream_messages in (messages or []):
            for msg_id, fields in stream_messages:
                try:
                    process_message(fields)
                    r.xack(stream_name, group_name, msg_id)
                except Exception as e:
                    print(f"Failed to process {msg_id}: {e}")
```

```javascript
// Node.js - Blocking commands
const Redis = require('ioredis');

// Dedicated connection for blocking
const blockingRedis = new Redis({
    commandTimeout: 65000,  // > blocking timeout
});

async function worker(queueName) {
    while (true) {
        try {
            // BLPOP with timeout in seconds
            const result = await blockingRedis.blpop(queueName, 30);

            if (result) {
                const [queue, data] = result;
                await processJob(data);
            }
        } catch (error) {
            console.error('Worker error:', error);
            await new Promise(r => setTimeout(r, 1000));
        }
    }
}
```

Reference: [Redis Blocking Commands](https://redis.io/commands/blpop/)
