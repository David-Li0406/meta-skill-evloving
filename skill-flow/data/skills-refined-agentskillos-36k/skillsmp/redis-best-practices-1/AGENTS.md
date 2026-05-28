# Redis Best Practices

**Version 1.0.0**
Redis
January 2026

> **Note:**
> This document is primarily for agents and LLMs to follow when maintaining,
> generating, or refactoring Redis application code.

---

## Abstract

Performance optimization and best practices guide for Redis applications, ordered by impact. Contains rules for data structures, key design, connection management, commands & patterns, memory management, persistence, clustering & high availability, and performance monitoring.

---

## Table of Contents

1. [Data Structures](#1-data-structures) — **CRITICAL**
   - 1.1 [Choose the Right Data Structure](#11-choose-the-right-data-structure)
   - 1.2 [Use Hashes for Object Storage](#12-use-hashes-for-object-storage)
   - 1.3 [Use Lists for Queues and Stacks](#13-use-lists-for-queues-and-stacks)
   - 1.4 [Use Sets for Unique Collections](#14-use-sets-for-unique-collections)
   - 1.5 [Use Sorted Sets for Rankings and Time-Series](#15-use-sorted-sets-for-rankings-and-time-series)
   - 1.6 [Use Streams for Event Logs and Messaging](#16-use-streams-for-event-logs-and-messaging)
2. [Key Design](#2-key-design) — **CRITICAL**
   - 2.1 [Avoid Large Keys and Values](#21-avoid-large-keys-and-values)
   - 2.2 [Design Keys Around Access Patterns](#22-design-keys-around-access-patterns)
   - 2.3 [Keep Key Names Reasonably Short](#23-keep-key-names-reasonably-short)
   - 2.4 [Always Set TTL on Cache Keys](#24-always-set-ttl-on-cache-keys)
   - 2.5 [Use Colon-Separated Key Namespacing](#25-use-colon-separated-key-namespacing)
   - 2.6 [Use SCAN Instead of KEYS in Production](#26-use-scan-instead-of-keys-in-production)
3. [Connection Management](#3-connection-management) — **HIGH**
   - 3.1 [Configure Appropriate Timeouts](#31-configure-appropriate-timeouts)
   - 3.2 [Use Dedicated Connections for Pub/Sub](#32-use-dedicated-connections-for-pub-sub)
   - 3.3 [Implement Proper Reconnection Logic](#33-implement-proper-reconnection-logic)
   - 3.4 [Always Use Connection Pooling](#34-always-use-connection-pooling)
   - 3.5 [Use Pipelining for Multiple Commands](#35-use-pipelining-for-multiple-commands)
4. [Commands & Patterns](#4-commands-patterns) — **HIGH**
   - 4.1 [Understand Blocking Command Implications](#41-understand-blocking-command-implications)
   - 4.2 [Never Use KEYS Command in Production](#42-never-use-keys-command-in-production)
   - 4.3 [Implement Distributed Locks Correctly](#43-implement-distributed-locks-correctly)
   - 4.4 [Use Batch Operations for Multiple Keys](#44-use-batch-operations-for-multiple-keys)
   - 4.5 [Use Lua Scripts for Complex Atomic Operations](#45-use-lua-scripts-for-complex-atomic-operations)
   - 4.6 [Use MULTI/EXEC for Atomic Operations](#46-use-multi-exec-for-atomic-operations)
5. [Memory Management](#5-memory-management) — **MEDIUM-HIGH**
   - 5.1 [Choose Appropriate Eviction Policy](#51-choose-appropriate-eviction-policy)
   - 5.2 [Always Configure maxmemory Limit](#52-always-configure-maxmemory-limit)
   - 5.3 [Monitor and Handle Memory Fragmentation](#53-monitor-and-handle-memory-fragmentation)
   - 5.4 [Use Memory-Efficient Data Encodings](#54-use-memory-efficient-data-encodings)
   - 5.5 [Enable Lazy Freeing for Large Deletions](#55-enable-lazy-freeing-for-large-deletions)
6. [Persistence](#6-persistence) — **MEDIUM**
   - 6.1 [Configure AOF Rewrite Properly](#61-configure-aof-rewrite-properly)
   - 6.2 [Configure Appropriate fsync Policy](#62-configure-appropriate-fsync-policy)
   - 6.3 [Regularly Test Backup Recovery](#63-regularly-test-backup-recovery)
   - 6.4 [Understand RDB vs AOF Persistence](#64-understand-rdb-vs-aof-persistence)
   - 6.5 [Use RDB for Backups and Disaster Recovery](#65-use-rdb-for-backups-and-disaster-recovery)
7. [Clustering & High Availability](#7-clustering-high-availability) — **MEDIUM**
   - 7.1 [Handle MOVED and ASK Redirects](#71-handle-moved-and-ask-redirects)
   - 7.2 [Plan Cluster Resharding Carefully](#72-plan-cluster-resharding-carefully)
   - 7.3 [Understand Redis Cluster Hash Slots](#73-understand-redis-cluster-hash-slots)
   - 7.4 [Offload Reads to Replicas](#74-offload-reads-to-replicas)
   - 7.5 [Use Sentinel for High Availability](#75-use-sentinel-for-high-availability)
8. [Performance & Monitoring](#8-performance-monitoring) — **LOW-MEDIUM**
   - 8.1 [Use redis-benchmark Correctly](#81-use-redis-benchmark-correctly)
   - 8.2 [Track and Diagnose Latency Issues](#82-track-and-diagnose-latency-issues)
   - 8.3 [Track Memory Usage and Trends](#83-track-memory-usage-and-trends)
   - 8.4 [Use INFO Command for Comprehensive Stats](#84-use-info-command-for-comprehensive-stats)
   - 8.5 [Monitor Slow Commands with SLOWLOG](#85-monitor-slow-commands-with-slowlog)

---

## 1. Data Structures

**Impact: CRITICAL**

### 1.1 Choose the Right Data Structure

**Impact: CRITICAL** (wrong type can cause 10-100x performance degradation)

## Choose the Right Data Structure

Redis offers multiple data structures, each optimized for specific access patterns. Choosing the wrong type leads to inefficient operations, excessive memory usage, or inability to perform needed queries.

**Data Structure Selection Guide:**

| Use Case | Data Structure | Key Operations |
|----------|---------------|----------------|
| Simple key-value | String | GET, SET, INCR |
| Object with fields | Hash | HGET, HSET, HGETALL |
| Unique items, membership | Set | SADD, SISMEMBER, SINTER |
| Ranked items, leaderboards | Sorted Set | ZADD, ZRANGE, ZRANK |
| Queue, stack, timeline | List | LPUSH, RPOP, LRANGE |
| Event log, messaging | Stream | XADD, XREAD, XRANGE |
| Boolean flags, bitmaps | String (bitwise) | SETBIT, GETBIT, BITCOUNT |
| Approximate counting | HyperLogLog | PFADD, PFCOUNT |

**Incorrect (using wrong data type):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: Using String for a collection
# Storing a list of user's favorite items as JSON
import json
favorites = ["item1", "item2", "item3"]
r.set("user:123:favorites", json.dumps(favorites))

# To add an item, must read-modify-write (not atomic!)
current = json.loads(r.get("user:123:favorites"))
current.append("item4")
r.set("user:123:favorites", json.dumps(current))
# Race condition if two clients do this simultaneously!

# Anti-pattern 2: Using List when you need uniqueness
r.rpush("user:123:tags", "python")
r.rpush("user:123:tags", "python")  # Duplicate allowed!

# Anti-pattern 3: Using Hash for ranking
r.hset("leaderboard", "player1", 100)
r.hset("leaderboard", "player2", 200)
# Cannot efficiently get "top 10 players" - must fetch all and sort in app
```

**Correct (matching type to use case):**

```python
import redis
r = redis.Redis()

# Correct 1: Use Set for unique collections
r.sadd("user:123:favorites", "item1", "item2", "item3")
r.sadd("user:123:favorites", "item4")  # Atomic add
r.sadd("user:123:favorites", "item1")  # Ignored - already exists
# Check membership in O(1)
is_favorite = r.sismember("user:123:favorites", "item2")

# Correct 2: Use Set for tags (unique)
r.sadd("user:123:tags", "python", "redis", "python")  # python only stored once
tags = r.smembers("user:123:tags")

# Correct 3: Use Sorted Set for leaderboard
r.zadd("leaderboard", {"player1": 100, "player2": 200, "player3": 150})
# Get top 10 players efficiently
top_10 = r.zrevrange("leaderboard", 0, 9, withscores=True)
# Get player's rank
rank = r.zrevrank("leaderboard", "player1")

# Correct 4: Use List for queue/timeline
r.lpush("notifications:123", "New message from Bob")
r.lpush("notifications:123", "Your order shipped")
# Get latest 10 notifications
recent = r.lrange("notifications:123", 0, 9)
# Pop oldest notification (FIFO queue)
oldest = r.rpop("notifications:123")

# Correct 5: Use Stream for event log
r.xadd("events:orders", {"action": "created", "order_id": "456"})
r.xadd("events:orders", {"action": "paid", "order_id": "456"})
# Read events, supports consumer groups
events = r.xrange("events:orders", "-", "+")
```

```javascript
// Node.js examples
const redis = require('redis');
const client = redis.createClient();

// Set for unique items
await client.sAdd('user:123:favorites', ['item1', 'item2']);
const isFavorite = await client.sIsMember('user:123:favorites', 'item1');

// Sorted Set for leaderboard
await client.zAdd('leaderboard', [
    { score: 100, value: 'player1' },
    { score: 200, value: 'player2' }
]);
const top10 = await client.zRange('leaderboard', 0, 9, { REV: true });

// List for queue
await client.lPush('queue:jobs', JSON.stringify({ task: 'send_email' }));
const job = await client.rPop('queue:jobs');
```

Reference: [Redis Data Types](https://redis.io/docs/data-types/)

### 1.2 Use Hashes for Object Storage

**Impact: CRITICAL** (reduces memory 50-90%, enables partial updates)

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

### 1.3 Use Lists for Queues and Stacks

**Impact: HIGH** (O(1) push/pop, blocking operations for workers)

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

### 1.4 Use Sets for Unique Collections

**Impact: HIGH** (O(1) membership checks, automatic deduplication)

## Use Sets for Unique Collections

Use Redis Sets when you need unique collections with fast membership testing, intersection, union, or difference operations. Sets provide O(1) add/remove/check operations and automatic deduplication.

**Incorrect (manual uniqueness handling):**

```python
import redis
import json
r = redis.Redis()

# Anti-pattern 1: Using a List and checking for duplicates
def add_follower_bad(user_id, follower_id):
    key = f"followers:{user_id}"
    # Must fetch entire list to check for duplicates
    followers = r.lrange(key, 0, -1)
    if follower_id.encode() not in followers:
        r.rpush(key, follower_id)
    # O(n) operation, race conditions possible

# Anti-pattern 2: Using JSON string
followers = json.loads(r.get("followers:123") or "[]")
if "user456" not in followers:
    followers.append("user456")
    r.set("followers:123", json.dumps(followers))
# Not atomic, race condition, O(n) check

# Anti-pattern 3: Finding common followers requires app logic
followers_a = set(json.loads(r.get("followers:A") or "[]"))
followers_b = set(json.loads(r.get("followers:B") or "[]"))
common = followers_a & followers_b  # Done in application memory
```

**Correct (using Sets):**

```python
import redis
r = redis.Redis()

# Add followers - duplicates automatically ignored
r.sadd("followers:123", "user456", "user789", "user101")
r.sadd("followers:123", "user456")  # No effect - already exists

# Check if someone is a follower - O(1)
is_following = r.sismember("followers:123", "user456")  # True

# Get follower count - O(1)
count = r.scard("followers:123")  # 3

# Get all followers
all_followers = r.smembers("followers:123")

# Remove a follower - O(1)
r.srem("followers:123", "user789")

# Set operations - done in Redis, not application
# Common followers (intersection)
common = r.sinter("followers:userA", "followers:userB")

# All unique followers of both (union)
all_unique = r.sunion("followers:userA", "followers:userB")

# Followers of A but not B (difference)
only_a = r.sdiff("followers:userA", "followers:userB")

# Store result of set operation
r.sinterstore("common:A:B", "followers:userA", "followers:userB")

# Random follower (useful for sampling)
random_follower = r.srandmember("followers:123")
random_3 = r.srandmember("followers:123", 3)

# Pop random member (remove and return)
removed = r.spop("followers:123")
```

```javascript
// Node.js
const redis = require('redis');
const client = redis.createClient();

// Add to set
await client.sAdd('followers:123', ['user456', 'user789']);

// Check membership
const isFollowing = await client.sIsMember('followers:123', 'user456');

// Set operations
const common = await client.sInter(['followers:A', 'followers:B']);
const all = await client.sUnion(['followers:A', 'followers:B']);
```

```python
# Real-world example: Online users tracking
import redis
import time

r = redis.Redis()

def user_online(user_id):
    """Mark user as online"""
    r.sadd("users:online", user_id)
    # Also track in time-bucketed set for "online in last 5 min"
    bucket = int(time.time() // 300)  # 5-minute buckets
    r.sadd(f"users:online:{bucket}", user_id)
    r.expire(f"users:online:{bucket}", 600)  # Expire after 10 min

def user_offline(user_id):
    """Mark user as offline"""
    r.srem("users:online", user_id)

def get_online_count():
    """Get count of online users"""
    return r.scard("users:online")

def is_user_online(user_id):
    """Check if specific user is online"""
    return r.sismember("users:online", user_id)

def get_online_friends(user_id):
    """Get intersection of user's friends who are online"""
    return r.sinter(f"friends:{user_id}", "users:online")
```

Reference: [Redis Sets](https://redis.io/docs/data-types/sets/)

### 1.5 Use Sorted Sets for Rankings and Time-Series

**Impact: HIGH** (O(log n) ranked operations, efficient range queries)

## Use Sorted Sets for Rankings and Time-Series

Use Redis Sorted Sets (ZSETs) when you need ordered data with scores, such as leaderboards, priority queues, rate limiters, or time-series data. Sorted Sets maintain elements in score order with O(log n) insertions and O(log n + m) range queries.

**Incorrect (sorting in application):**

```python
import redis
import json
r = redis.Redis()

# Anti-pattern 1: Storing scores in Hash and sorting in app
r.hset("leaderboard", mapping={
    "player1": 1500,
    "player2": 2300,
    "player3": 1800
})
# To get top 10, must fetch ALL players and sort
all_players = r.hgetall("leaderboard")
sorted_players = sorted(all_players.items(), key=lambda x: int(x[1]), reverse=True)
top_10 = sorted_players[:10]
# O(n log n) in app + transfers ALL data over network

# Anti-pattern 2: Using List with manual sorting
r.rpush("scores", json.dumps({"player": "p1", "score": 100}))
# Cannot efficiently find rank or get top N without fetching all

# Anti-pattern 3: Time-series in List
r.lpush("events", json.dumps({"ts": 1234567890, "value": 42}))
# Cannot query by time range efficiently
```

**Correct (using Sorted Sets):**

```python
import redis
import time
r = redis.Redis()

# Leaderboard - score is the ranking metric
r.zadd("leaderboard", {
    "player1": 1500,
    "player2": 2300,
    "player3": 1800,
    "player4": 2100
})

# Update score (or add new player)
r.zadd("leaderboard", {"player1": 1600})

# Increment score atomically
r.zincrby("leaderboard", 50, "player1")  # player1 now has 1650

# Get top 10 (highest scores first)
top_10 = r.zrevrange("leaderboard", 0, 9, withscores=True)
# Returns: [(b'player2', 2300.0), (b'player4', 2100.0), ...]

# Get bottom 10 (lowest scores first)
bottom_10 = r.zrange("leaderboard", 0, 9, withscores=True)

# Get player's rank (0-indexed, highest = 0)
rank = r.zrevrank("leaderboard", "player1")  # Returns position

# Get player's score
score = r.zscore("leaderboard", "player1")

# Get players with scores in range
mid_tier = r.zrangebyscore("leaderboard", 1500, 2000, withscores=True)

# Count players in score range
count = r.zcount("leaderboard", 1500, 2000)

# Remove player
r.zrem("leaderboard", "player3")
```

```python
# Time-series data using Sorted Sets (score = timestamp)
import redis
import time

r = redis.Redis()

def record_metric(metric_name, value):
    """Record a metric value with current timestamp"""
    ts = time.time()
    # Use timestamp as score, value as member
    # Include timestamp in member to allow duplicate values
    r.zadd(f"metrics:{metric_name}", {f"{ts}:{value}": ts})

def get_metrics_in_range(metric_name, start_ts, end_ts):
    """Get metrics between two timestamps"""
    return r.zrangebyscore(
        f"metrics:{metric_name}",
        start_ts,
        end_ts,
        withscores=True
    )

def get_recent_metrics(metric_name, seconds=3600):
    """Get metrics from the last N seconds"""
    now = time.time()
    return r.zrangebyscore(
        f"metrics:{metric_name}",
        now - seconds,
        now,
        withscores=True
    )

def cleanup_old_metrics(metric_name, max_age_seconds=86400):
    """Remove metrics older than max_age"""
    cutoff = time.time() - max_age_seconds
    r.zremrangebyscore(f"metrics:{metric_name}", "-inf", cutoff)
```

```python
# Rate limiter using Sorted Sets (sliding window)
import redis
import time

r = redis.Redis()

def is_rate_limited(user_id, max_requests=100, window_seconds=60):
    """
    Sliding window rate limiter.
    Returns True if user should be rate limited.
    """
    key = f"ratelimit:{user_id}"
    now = time.time()
    window_start = now - window_seconds

    pipe = r.pipeline()
    # Remove old entries outside window
    pipe.zremrangebyscore(key, "-inf", window_start)
    # Count requests in window
    pipe.zcard(key)
    # Add current request
    pipe.zadd(key, {f"{now}": now})
    # Set expiry on key
    pipe.expire(key, window_seconds)

    results = pipe.execute()
    request_count = results[1]

    return request_count >= max_requests
```

```javascript
// Node.js
const redis = require('redis');
const client = redis.createClient();

// Add to leaderboard
await client.zAdd('leaderboard', [
    { score: 1500, value: 'player1' },
    { score: 2300, value: 'player2' }
]);

// Get top 10
const top10 = await client.zRange('leaderboard', 0, 9, {
    REV: true,
    WITHSCORES: true
});

// Get rank
const rank = await client.zRevRank('leaderboard', 'player1');
```

Reference: [Redis Sorted Sets](https://redis.io/docs/data-types/sorted-sets/)

### 1.6 Use Streams for Event Logs and Messaging

**Impact: HIGH** (persistent messaging with consumer groups, at-least-once delivery)

## Use Streams for Event Logs and Messaging

Use Redis Streams for event sourcing, activity logs, and reliable messaging. Streams provide persistent, append-only logs with consumer groups for distributed processing, explicit message acknowledgment, and at-least-once delivery semantics.

**When to use Streams vs Lists vs Pub/Sub:**
- **Streams**: Persistent messages, consumer groups, replay capability, acknowledgments
- **Lists**: Simple queues, no need for consumer groups or replay
- **Pub/Sub**: Fire-and-forget, no persistence, real-time only

**Incorrect (using Pub/Sub or Lists for persistent messaging):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: Pub/Sub for persistent messaging
# Messages are lost if no subscriber is listening!
r.publish("events", '{"type": "order_created", "id": 123}')
# If consumer is down, message is gone forever

# Anti-pattern 2: List without consumer groups
# Only one consumer can process each message
# No acknowledgment tracking
r.lpush("events", '{"type": "order_created", "id": 123}')
job = r.rpop("events")  # If process crashes, job is lost

# Anti-pattern 3: Polling for new events
while True:
    events = r.lrange("events", last_index, -1)
    # Must track position manually, no consumer group support
```

**Correct (using Streams):**

```python
import redis
r = redis.Redis()

# Add events to stream (returns auto-generated ID like "1234567890123-0")
event_id = r.xadd("events:orders", {
    "type": "order_created",
    "order_id": "12345",
    "customer_id": "cust_789",
    "total": "99.99"
})
print(f"Event ID: {event_id}")  # e.g., b'1704067200000-0'

# Add with custom ID (use * for auto-generate)
r.xadd("events:orders", {"type": "order_paid", "order_id": "12345"}, id="*")

# Read events (simple, from beginning)
events = r.xrange("events:orders", "-", "+")  # All events
events = r.xrange("events:orders", "-", "+", count=10)  # First 10

# Read events from specific ID onwards
events = r.xrange("events:orders", "1704067200000-0", "+")

# Read new events only (blocking)
# ">" means only new messages not yet delivered
events = r.xread({"events:orders": "$"}, block=5000)  # Block 5 seconds
```

```python
# Consumer Groups - distributed processing with acknowledgments
import redis
r = redis.Redis()

STREAM = "events:orders"
GROUP = "order-processors"
CONSUMER = "worker-1"

# Create consumer group (run once, idempotent with mkstream)
try:
    r.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
except redis.ResponseError as e:
    if "BUSYGROUP" not in str(e):
        raise  # Group already exists is OK

# Read messages for this consumer group
# ">" means only messages never delivered to any consumer in this group
messages = r.xreadgroup(
    GROUP,
    CONSUMER,
    {STREAM: ">"},
    count=10,
    block=5000  # Block for 5 seconds if no messages
)

# Process messages
for stream_name, stream_messages in messages:
    for message_id, fields in stream_messages:
        try:
            # Process the event
            print(f"Processing {message_id}: {fields}")

            # Acknowledge successful processing
            r.xack(STREAM, GROUP, message_id)
        except Exception as e:
            # Don't ack - message will be re-delivered
            print(f"Failed to process {message_id}: {e}")

# Check pending messages (not yet acknowledged)
pending = r.xpending(STREAM, GROUP)
print(f"Pending messages: {pending}")

# Claim stuck messages (from dead consumers)
# Messages pending > 60 seconds, move to this consumer
stuck = r.xautoclaim(STREAM, GROUP, CONSUMER, min_idle_time=60000, start_id="0")
```

```python
# Full worker implementation
import redis
import signal
import sys

r = redis.Redis()
running = True

def shutdown(signum, frame):
    global running
    running = False

signal.signal(signal.SIGTERM, shutdown)
signal.signal(signal.SIGINT, shutdown)

STREAM = "events:orders"
GROUP = "order-processors"
CONSUMER = f"worker-{os.getpid()}"

# Ensure group exists
try:
    r.xgroup_create(STREAM, GROUP, id="0", mkstream=True)
except redis.ResponseError:
    pass

while running:
    # First, check for pending messages (recovery)
    pending = r.xreadgroup(GROUP, CONSUMER, {STREAM: "0"}, count=10)

    # Then read new messages
    if not pending or not pending[0][1]:
        messages = r.xreadgroup(GROUP, CONSUMER, {STREAM: ">"}, count=10, block=1000)
    else:
        messages = pending

    if messages:
        for _, stream_messages in messages:
            for msg_id, fields in stream_messages:
                try:
                    process_event(fields)
                    r.xack(STREAM, GROUP, msg_id)
                except Exception as e:
                    log_error(f"Failed: {msg_id}", e)
```

```javascript
// Node.js
const redis = require('redis');
const client = redis.createClient();

// Add to stream
await client.xAdd('events:orders', '*', {
    type: 'order_created',
    order_id: '12345'
});

// Create consumer group
try {
    await client.xGroupCreate('events:orders', 'processors', '0', { MKSTREAM: true });
} catch (e) {
    // Group exists
}

// Read with consumer group
const messages = await client.xReadGroup('processors', 'worker-1', [
    { key: 'events:orders', id: '>' }
], { COUNT: 10, BLOCK: 5000 });

// Acknowledge
await client.xAck('events:orders', 'processors', messageId);
```

Reference: [Redis Streams](https://redis.io/docs/data-types/streams/)

---

## 2. Key Design

**Impact: CRITICAL**

### 2.1 Avoid Large Keys and Values

**Impact: CRITICAL** (large keys block Redis, cause timeouts and memory issues)

## Avoid Large Keys and Values

Keep individual key values under reasonable size limits. Large keys (>1MB) can block Redis during operations, cause network timeouts, and lead to memory fragmentation. Redis is single-threaded, so a slow operation blocks everything.

**Size Guidelines:**
- Strings: Keep under 1MB, ideally under 100KB
- Lists/Sets/Hashes: Keep under 10,000 elements, ideally under 1,000
- Avoid keys that grow unbounded

**Incorrect (large or unbounded keys):**

```python
import redis
import json
r = redis.Redis()

# Anti-pattern 1: Storing large blobs
large_file = open("report.pdf", "rb").read()  # 50MB file
r.set("report:latest", large_file)  # Blocks Redis!

# Anti-pattern 2: Unbounded list growth
def log_activity(user_id, activity):
    r.lpush(f"activity:{user_id}", json.dumps(activity))
    # List grows forever - could have millions of entries!

# Anti-pattern 3: Large hash with all users
r.hset("all_users", user_id, json.dumps(user_data))
# Single key contains ALL users - deleting it blocks Redis

# Anti-pattern 4: Storing entire query results
search_results = database.query("SELECT * FROM products")  # 100K rows
r.set("cache:all_products", json.dumps(search_results))

# Anti-pattern 5: Large JSON documents
user_with_history = {
    "id": 123,
    "profile": {...},
    "orders": [...],      # 5000 orders
    "activities": [...],  # 100K activities
    "messages": [...],    # 50K messages
}
r.set(f"user:{user_id}:full", json.dumps(user_with_history))
```

**Correct (bounded and chunked storage):**

```python
import redis
import json
r = redis.Redis()

# Correct 1: Store large files externally, cache metadata
def store_report(report_id, file_data):
    # Store file in S3/blob storage
    s3_url = upload_to_s3(file_data)

    # Store only metadata in Redis
    r.hset(f"report:{report_id}", mapping={
        "url": s3_url,
        "size": len(file_data),
        "created": time.time()
    })

# Correct 2: Cap list size
def log_activity(user_id, activity, max_entries=1000):
    key = f"activity:{user_id}"
    pipe = r.pipeline()
    pipe.lpush(key, json.dumps(activity))
    pipe.ltrim(key, 0, max_entries - 1)  # Keep only last N entries
    pipe.execute()

# Correct 3: Shard large collections
def add_user(user_id, user_data):
    # Shard users across multiple keys
    shard = int(user_id) % 100  # 100 shards
    r.hset(f"users:shard:{shard}", user_id, json.dumps(user_data))

def get_user(user_id):
    shard = int(user_id) % 100
    data = r.hget(f"users:shard:{shard}", user_id)
    return json.loads(data) if data else None

# Correct 4: Paginated caching
def cache_search_results(query_hash, results, page_size=100):
    """Store results in pages"""
    for i in range(0, len(results), page_size):
        page = i // page_size
        page_results = results[i:i + page_size]
        r.setex(
            f"search:{query_hash}:page:{page}",
            3600,
            json.dumps(page_results)
        )
    # Store total count
    r.setex(f"search:{query_hash}:total", 3600, len(results))

def get_search_page(query_hash, page=0):
    """Get specific page of results"""
    return json.loads(r.get(f"search:{query_hash}:page:{page}") or "[]")

# Correct 5: Separate large collections
def store_user(user_id, user_data):
    # Core user data in hash
    r.hset(f"user:{user_id}", mapping={
        "name": user_data["name"],
        "email": user_data["email"]
    })

    # Orders in separate capped list
    if "orders" in user_data:
        for order in user_data["orders"][-100:]:  # Last 100 only
            r.lpush(f"user:{user_id}:orders", json.dumps(order))
        r.ltrim(f"user:{user_id}:orders", 0, 99)

    # Activity in sorted set (auto-truncate old)
    # Store recent activity with timestamp scores
```

```python
# Monitor and find large keys
def find_large_keys(sample_size=10000, threshold_bytes=10000):
    """Find keys larger than threshold"""
    large_keys = []

    for key in r.scan_iter(count=100):
        if len(large_keys) >= sample_size:
            break

        try:
            mem = r.memory_usage(key)
            if mem and mem > threshold_bytes:
                key_type = r.type(key).decode()
                large_keys.append({
                    "key": key.decode(),
                    "type": key_type,
                    "memory_bytes": mem,
                    "memory_mb": round(mem / 1024 / 1024, 2)
                })
        except:
            pass

    return sorted(large_keys, key=lambda x: x["memory_bytes"], reverse=True)

# Check specific key size
def check_key_size(key):
    """Get detailed size info for a key"""
    key_type = r.type(key).decode()
    memory = r.memory_usage(key)

    info = {
        "key": key,
        "type": key_type,
        "memory_bytes": memory,
    }

    if key_type == "list":
        info["length"] = r.llen(key)
    elif key_type == "set":
        info["cardinality"] = r.scard(key)
    elif key_type == "zset":
        info["cardinality"] = r.zcard(key)
    elif key_type == "hash":
        info["fields"] = r.hlen(key)
    elif key_type == "string":
        info["string_length"] = r.strlen(key)

    return info
```

```javascript
// Node.js - Safe large value handling
const redis = require('redis');
const client = redis.createClient();

// Chunked storage for large values
async function setLargeValue(key, value, chunkSize = 500000) {
    const chunks = [];
    for (let i = 0; i < value.length; i += chunkSize) {
        chunks.push(value.slice(i, i + chunkSize));
    }

    const multi = client.multi();
    chunks.forEach((chunk, i) => {
        multi.set(`${key}:chunk:${i}`, chunk);
    });
    multi.set(`${key}:chunks`, chunks.length.toString());
    await multi.exec();
}

async function getLargeValue(key) {
    const chunkCount = parseInt(await client.get(`${key}:chunks`));
    const chunks = await Promise.all(
        Array.from({ length: chunkCount }, (_, i) =>
            client.get(`${key}:chunk:${i}`)
        )
    );
    return chunks.join('');
}
```

Reference: [Redis Memory Optimization](https://redis.io/docs/management/optimization/memory-optimization/)

### 2.2 Design Keys Around Access Patterns

**Impact: HIGH** (enables efficient queries without secondary indexes)

## Design Keys Around Access Patterns

Design your key structure around how you'll query the data, not just how it's structured in your source system. Redis doesn't have secondary indexes by default, so your key design determines what queries are efficient.

**Key Questions to Ask:**
1. How will I look up this data? (by user ID? by email? by date?)
2. What queries need to be fast?
3. What relationships need to be traversed?

**Incorrect (designing for storage, not access):**

```python
import redis
import json
r = redis.Redis()

# Anti-pattern 1: Only storing by primary key
r.hset("user:123", mapping={
    "id": "123",
    "email": "john@example.com",
    "username": "johndoe"
})
# Problem: Can't look up user by email or username efficiently
# Must scan all users to find by email!

# Anti-pattern 2: Storing relationships only one direction
r.sadd("user:123:followers", "456", "789")
# Problem: Can't answer "who does user 456 follow?"

# Anti-pattern 3: Timestamp in key without range query support
r.set("event:2024-01-15T10:30:00:abc123", json.dumps(event))
# Problem: Can't efficiently get "events between 10am and 11am"

# Anti-pattern 4: Nested data without index
r.hset("order:789", mapping={
    "customer_id": "123",
    "status": "pending",
    "items": json.dumps([...])
})
# Problem: Can't find "all pending orders" or "orders for customer 123"
```

**Correct (designing for access patterns):**

```python
import redis
import json
r = redis.Redis()

# Correct 1: Create lookup indexes for alternate keys
def create_user(user_data):
    user_id = user_data["id"]

    # Primary storage
    r.hset(f"user:{user_id}", mapping={
        "email": user_data["email"],
        "username": user_data["username"],
        "name": user_data["name"]
    })

    # Index by email (for login lookup)
    r.set(f"user:email:{user_data['email']}", user_id)

    # Index by username (for profile lookup)
    r.set(f"user:username:{user_data['username']}", user_id)

def get_user_by_email(email):
    user_id = r.get(f"user:email:{email}")
    if user_id:
        return r.hgetall(f"user:{user_id.decode()}")
    return None

def get_user_by_username(username):
    user_id = r.get(f"user:username:{username}")
    if user_id:
        return r.hgetall(f"user:{user_id.decode()}")
    return None

# Correct 2: Bidirectional relationships
def follow_user(follower_id, followed_id):
    """Create bidirectional follow relationship"""
    pipe = r.pipeline()
    pipe.sadd(f"user:{followed_id}:followers", follower_id)
    pipe.sadd(f"user:{follower_id}:following", followed_id)
    pipe.execute()

def get_followers(user_id):
    return r.smembers(f"user:{user_id}:followers")

def get_following(user_id):
    return r.smembers(f"user:{user_id}:following")

def get_mutual_followers(user_a, user_b):
    """Friends who follow both users"""
    return r.sinter(f"user:{user_a}:followers", f"user:{user_b}:followers")

# Correct 3: Time-series with sorted sets for range queries
def log_event(event_type, event_data):
    timestamp = time.time()
    event_id = f"{timestamp}:{uuid.uuid4().hex[:8]}"

    # Store event data
    r.hset(f"event:{event_id}", mapping=event_data)
    r.expire(f"event:{event_id}", 86400 * 7)  # 7 days

    # Index by time for range queries
    r.zadd(f"events:{event_type}", {event_id: timestamp})

def get_events_in_range(event_type, start_time, end_time):
    """Get events between two timestamps"""
    event_ids = r.zrangebyscore(
        f"events:{event_type}",
        start_time,
        end_time
    )
    return [r.hgetall(f"event:{eid.decode()}") for eid in event_ids]

# Correct 4: Secondary indexes for queryable fields
def create_order(order_data):
    order_id = order_data["id"]
    customer_id = order_data["customer_id"]
    status = order_data["status"]

    # Primary storage
    r.hset(f"order:{order_id}", mapping={
        "customer_id": customer_id,
        "status": status,
        "total": order_data["total"],
        "created": time.time()
    })

    # Index: orders by customer
    r.sadd(f"customer:{customer_id}:orders", order_id)

    # Index: orders by status
    r.sadd(f"orders:status:{status}", order_id)

def get_customer_orders(customer_id):
    order_ids = r.smembers(f"customer:{customer_id}:orders")
    return [r.hgetall(f"order:{oid.decode()}") for oid in order_ids]

def get_pending_orders():
    order_ids = r.smembers("orders:status:pending")
    return [r.hgetall(f"order:{oid.decode()}") for oid in order_ids]

def update_order_status(order_id, old_status, new_status):
    """Update status and maintain index consistency"""
    pipe = r.pipeline()
    pipe.hset(f"order:{order_id}", "status", new_status)
    pipe.srem(f"orders:status:{old_status}", order_id)
    pipe.sadd(f"orders:status:{new_status}", order_id)
    pipe.execute()
```

```python
# Common access pattern solutions

# Pattern: "Get recent N items for a user"
# Solution: Sorted set with timestamp scores
r.zadd(f"user:{user_id}:activity", {activity_id: timestamp})
recent = r.zrevrange(f"user:{user_id}:activity", 0, 9)  # Last 10

# Pattern: "Check if item exists in collection"
# Solution: Set with O(1) membership check
r.sadd(f"user:{user_id}:likes", item_id)
is_liked = r.sismember(f"user:{user_id}:likes", item_id)

# Pattern: "Get items by multiple criteria"
# Solution: Set intersection
# Users who like Python AND are in San Francisco
r.sinter("likes:python", "location:san_francisco")

# Pattern: "Leaderboard with user's rank"
# Solution: Sorted set
r.zadd("leaderboard", {user_id: score})
rank = r.zrevrank("leaderboard", user_id)
score = r.zscore("leaderboard", user_id)

# Pattern: "Tag-based queries"
# Solution: Sets per tag + intersection/union
r.sadd("tag:python", "article:1", "article:5")
r.sadd("tag:redis", "article:1", "article:3")
python_and_redis = r.sinter("tag:python", "tag:redis")
```

Reference: [Redis Patterns](https://redis.io/docs/manual/patterns/)

### 2.3 Keep Key Names Reasonably Short

**Impact: MEDIUM** (saves memory with millions of keys)

## Keep Key Names Reasonably Short

Balance readability with memory efficiency in key names. While clarity is important, excessively long keys waste memory - especially significant when you have millions of keys. Each key name is stored in memory for every instance.

**Memory Impact:**
- Key name overhead: ~50 bytes per key (internal structures) + key length
- 10 million keys with 50-char names vs 20-char names = ~300MB difference
- Short IDs (numeric or short UUIDs) are more efficient than long UUIDs

**Incorrect (overly verbose keys):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: Overly verbose naming
r.set("user_account_profile_information_for_user_id_123", "{...}")
# 48 characters for key name!

# Anti-pattern 2: Full UUIDs when not necessary
r.set("user:550e8400-e29b-41d4-a716-446655440000:profile", "{...}")
# UUID adds 36 characters

# Anti-pattern 3: Redundant information
r.set("redis_cache_key_for_user_data_user_123", "{...}")
# "redis_cache_key_for" adds nothing useful

# Anti-pattern 4: Environment in every key
r.set("production_application_myapp_service_users_user_123", "{...}")
# Use separate Redis instances/databases instead
```

**Correct (balanced key names):**

```python
import redis
r = redis.Redis()

# Good: Short but clear
r.hset("u:123", mapping={"name": "John"})           # User
r.hset("p:456", mapping={"title": "Widget"})        # Product
r.set("s:abc123", "session_data")                   # Session
r.set("c:u:123:cart", "{...}")                      # Cart

# Good: Readable abbreviations
r.hset("usr:123", mapping={"name": "John"})         # User
r.hset("prod:456", mapping={"title": "Widget"})     # Product
r.set("sess:abc123", "session_data")                # Session
r.set("ord:789", "{...}")                           # Order

# Good: Full words for less frequent keys (config, etc.)
r.hset("config:app", mapping={"timeout": "30"})     # Config is fine
r.set("feature:dark_mode", "enabled")               # Feature flags

# ID optimization: Use numeric IDs or short IDs
# Instead of: user:550e8400-e29b-41d4-a716-446655440000
# Use: user:123 (auto-increment) or user:7bx9k2 (short ID)

# Short ID generation example
import base64
import struct

def short_id(numeric_id):
    """Convert numeric ID to short base64 string"""
    packed = struct.pack('>Q', numeric_id).lstrip(b'\x00')
    return base64.urlsafe_b64encode(packed).rstrip(b'=').decode()

# short_id(123456) -> "AeJA"
# short_id(9999999) -> "mJj_"
```

```python
# Abbreviation conventions (document in your team)
ABBREVIATIONS = {
    "user": "u",
    "product": "p",
    "order": "o",
    "session": "s",
    "cart": "c",
    "inventory": "inv",
    "category": "cat",
    "transaction": "tx",
    "notification": "notif",
}

# Or slightly longer for readability
ABBREVIATIONS = {
    "user": "usr",
    "product": "prod",
    "order": "ord",
    "session": "sess",
    "cart": "cart",
    "inventory": "inv",
    "category": "cat",
}
```

```python
# Memory calculation example
import redis
r = redis.Redis()

# Check memory usage of a key
r.set("user_profile_information:123", "x" * 100)
r.set("u:123", "x" * 100)

# Use MEMORY USAGE command (Redis 4.0+)
long_key_mem = r.memory_usage("user_profile_information:123")
short_key_mem = r.memory_usage("u:123")

print(f"Long key: {long_key_mem} bytes")   # ~180 bytes
print(f"Short key: {short_key_mem} bytes") # ~150 bytes
# Difference of 30 bytes * 10M keys = 300MB
```

```javascript
// Node.js - Key builder with abbreviations
const PREFIXES = {
    user: 'u',
    product: 'p',
    order: 'o',
    session: 's'
};

function key(type, id, ...rest) {
    const prefix = PREFIXES[type] || type;
    return [prefix, id, ...rest].join(':');
}

// Usage
key('user', 123);                    // "u:123"
key('user', 123, 'profile');         // "u:123:profile"
key('product', 456);                 // "p:456"
```

**When to use longer names:**
- Configuration keys (few in number)
- Keys used for debugging/monitoring
- When the domain requires specific clarity
- When key count is small (< 100,000)

Reference: [Redis Memory Optimization](https://redis.io/docs/management/optimization/memory-optimization/)

### 2.4 Always Set TTL on Cache Keys

**Impact: CRITICAL** (prevents memory leaks and stale data)

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

### 2.5 Use Colon-Separated Key Namespacing

**Impact: CRITICAL** (enables organization, scanning, and multi-tenancy)

## Use Colon-Separated Key Namespacing

Use colons (`:`) to create hierarchical key namespaces. This convention enables logical organization, efficient pattern scanning, and clear separation between different data types and entities.

**Naming Convention Pattern:**
```
object-type:id:field
tenant:object-type:id
service:environment:object-type:id
```

**Incorrect (flat or inconsistent naming):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: No namespace - collisions likely
r.set("123", "John Doe")  # What is 123? User? Order? Product?
r.set("settings", "{...}")  # Whose settings?

# Anti-pattern 2: Inconsistent separators
r.set("user_123_profile", "{...}")
r.set("user-123-sessions", "{...}")
r.set("user.123.preferences", "{...}")
# Cannot use SCAN patterns effectively

# Anti-pattern 3: Verbose redundant naming
r.set("application_myapp_production_user_data_user_id_123", "{...}")
# Wastes memory, hard to read

# Anti-pattern 4: No object type prefix
r.set("123:profile", "{...}")
r.set("123:orders", "{...}")
# Is 123 a user? customer? merchant?
```

**Correct (consistent colon-separated namespacing):**

```python
import redis
r = redis.Redis()

# Pattern: object-type:id[:field]
r.hset("user:123", mapping={"name": "John", "email": "john@example.com"})
r.set("user:123:session", "session_token_abc")
r.sadd("user:123:roles", "admin", "editor")
r.zadd("user:123:activity", {"login": 1704067200})

# Pattern: object-type:id for relationships
r.sadd("user:123:followers", "user:456", "user:789")
r.sadd("user:123:following", "user:456")

# Multi-tenant pattern: tenant:object-type:id
r.hset("tenant:acme:user:123", mapping={"name": "John"})
r.hset("tenant:globex:user:123", mapping={"name": "Jane"})

# Service/environment pattern
r.set("myapp:prod:config:feature_flags", "{...}")
r.set("myapp:staging:config:feature_flags", "{...}")

# Scan by pattern (find all users)
for key in r.scan_iter(match="user:*", count=100):
    print(key)

# Scan tenant-specific data
for key in r.scan_iter(match="tenant:acme:*", count=100):
    print(key)

# Delete all sessions for a user (carefully!)
for key in r.scan_iter(match="user:123:session:*"):
    r.delete(key)
```

```python
# Real-world examples of good key naming

# E-commerce application
"product:12345"                      # Product hash
"product:12345:inventory"            # Stock count
"product:12345:reviews"              # Review list
"category:electronics:products"       # Set of product IDs
"cart:user:789"                      # Shopping cart hash
"order:abc123"                       # Order hash
"order:abc123:items"                 # Order line items

# Session management
"session:token:xyz789"               # Session data
"session:user:123:tokens"            # Set of user's session tokens

# Caching with versioning
"cache:v1:user:123:profile"          # Versioned cache key
"cache:v2:user:123:profile"          # New cache version

# Rate limiting
"ratelimit:api:user:123"             # Per-user rate limit
"ratelimit:api:ip:192.168.1.1"       # Per-IP rate limit

# Feature flags
"feature:dark_mode:enabled"          # Global feature
"feature:dark_mode:users"            # Set of users with feature
"feature:dark_mode:percentage"       # Rollout percentage

# Queues
"queue:emails:pending"               # Pending email jobs
"queue:emails:processing"            # Jobs being processed
"queue:emails:failed"                # Failed jobs for retry
```

```javascript
// Node.js - Key naming utilities
const redis = require('redis');
const client = redis.createClient();

// Helper function for consistent key generation
function key(...parts) {
    return parts.join(':');
}

// Usage
const userKey = key('user', userId);                    // "user:123"
const sessionKey = key('user', userId, 'session');      // "user:123:session"
const tenantKey = key('tenant', tenantId, 'user', id);  // "tenant:acme:user:123"

await client.hSet(key('user', '123'), { name: 'John' });
await client.set(key('user', '123', 'session'), 'token');
```

Reference: [Redis Key Naming Conventions](https://redis.io/docs/manual/patterns/)

### 2.6 Use SCAN Instead of KEYS in Production

**Impact: CRITICAL** (KEYS blocks Redis for seconds/minutes with large datasets)

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

---

## 3. Connection Management

**Impact: HIGH**

### 3.1 Configure Appropriate Timeouts

**Impact: HIGH** (prevents hung connections, enables fast failure detection)

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

### 3.2 Use Dedicated Connections for Pub/Sub

**Impact: MEDIUM-HIGH** (Pub/Sub blocks connection, can't be shared)

## Use Dedicated Connections for Pub/Sub

Use separate, dedicated connections for Pub/Sub subscribers. Once a connection enters subscribe mode, it can only execute subscribe/unsubscribe commands. Sharing a Pub/Sub connection with regular commands will fail or block.

**Why Dedicated Connections:**
- SUBSCRIBE puts connection in special mode
- Can only run SUBSCRIBE, PSUBSCRIBE, UNSUBSCRIBE, PUNSUBSCRIBE, PING, QUIT
- Regular commands (GET, SET, etc.) are not allowed
- Messages arrive asynchronously on the subscribed connection

**Incorrect (sharing Pub/Sub connection):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: Using same client for subscribe and commands
pubsub = r.pubsub()
pubsub.subscribe('channel1')

# This will fail or behave unexpectedly
r.get('some_key')  # May interfere with pub/sub
r.set('key', 'value')

# Anti-pattern 2: Subscribing in request handler
def handle_request(request):
    pubsub = r.pubsub()
    pubsub.subscribe('updates')
    # Creates new subscription per request - resource leak!

# Anti-pattern 3: Blocking subscribe in main thread
def start_app():
    pubsub = r.pubsub()
    pubsub.subscribe('events')
    for message in pubsub.listen():  # Blocks forever!
        process(message)
    # App can't do anything else
```

**Correct (dedicated Pub/Sub connections):**

```python
import redis
import threading

# Separate clients for regular operations and pub/sub
redis_client = redis.Redis(host='localhost', port=6379)
redis_pubsub = redis.Redis(host='localhost', port=6379)

# Correct 1: Dedicated pubsub in separate thread
class PubSubHandler:
    def __init__(self, channels):
        self.redis = redis.Redis(host='localhost', port=6379)
        self.pubsub = self.redis.pubsub()
        self.channels = channels
        self.thread = None

    def message_handler(self, message):
        if message['type'] == 'message':
            channel = message['channel'].decode()
            data = message['data'].decode()
            print(f"Received on {channel}: {data}")
            # Process message here

    def start(self):
        self.pubsub.subscribe(**{ch: self.message_handler for ch in self.channels})
        self.thread = self.pubsub.run_in_thread(sleep_time=0.001)

    def stop(self):
        if self.thread:
            self.thread.stop()
        self.pubsub.close()

# Usage
handler = PubSubHandler(['notifications', 'updates'])
handler.start()

# Main thread can still use regular Redis client
redis_client.set('key', 'value')
redis_client.get('key')

# Correct 2: Pattern subscription with dedicated connection
def start_pattern_subscriber():
    r = redis.Redis()  # Dedicated connection
    pubsub = r.pubsub()

    # Subscribe to pattern
    pubsub.psubscribe('events:*')

    for message in pubsub.listen():
        if message['type'] == 'pmessage':
            pattern = message['pattern'].decode()
            channel = message['channel'].decode()
            data = message['data'].decode()
            print(f"Pattern {pattern}, Channel {channel}: {data}")

# Run in separate thread
thread = threading.Thread(target=start_pattern_subscriber, daemon=True)
thread.start()

# Correct 3: Async pub/sub with separate connection
import asyncio
import redis.asyncio as redis

async def subscriber(channels):
    """Async subscriber with dedicated connection"""
    r = redis.Redis()
    pubsub = r.pubsub()

    await pubsub.subscribe(*channels)

    async for message in pubsub.listen():
        if message['type'] == 'message':
            await process_message(message)

async def publisher():
    """Publisher uses regular connection"""
    r = redis.Redis()
    while True:
        await r.publish('notifications', 'Hello!')
        await asyncio.sleep(1)

async def main():
    # Run subscriber and publisher concurrently
    await asyncio.gather(
        subscriber(['notifications']),
        publisher()
    )
```

```python
# Correct 4: Publisher pattern (separate from subscribers)
class EventBus:
    def __init__(self):
        # Publisher connection (for sending)
        self.publisher = redis.Redis(host='localhost', port=6379)
        # Subscriber connections (for receiving)
        self.subscribers = {}

    def publish(self, channel, message):
        """Publish message - uses regular connection"""
        self.publisher.publish(channel, message)

    def subscribe(self, channel, callback):
        """Create dedicated subscriber for channel"""
        r = redis.Redis(host='localhost', port=6379)
        pubsub = r.pubsub()
        pubsub.subscribe(channel)

        def listener():
            for msg in pubsub.listen():
                if msg['type'] == 'message':
                    callback(msg['data'])

        thread = threading.Thread(target=listener, daemon=True)
        thread.start()
        self.subscribers[channel] = (pubsub, thread)

    def unsubscribe(self, channel):
        if channel in self.subscribers:
            pubsub, thread = self.subscribers[channel]
            pubsub.unsubscribe(channel)
            pubsub.close()
            del self.subscribers[channel]
```

```javascript
// Node.js - Separate connections for pub/sub
const Redis = require('ioredis');

// Regular operations
const redis = new Redis();

// Dedicated subscriber connection
const subscriber = new Redis();

// Dedicated publisher connection (optional, can share with redis)
const publisher = new Redis();

subscriber.subscribe('notifications', 'updates', (err, count) => {
    console.log(`Subscribed to ${count} channels`);
});

subscriber.on('message', (channel, message) => {
    console.log(`Received ${message} from ${channel}`);
});

// Regular operations on separate connection
await redis.set('key', 'value');
await redis.get('key');

// Publish (can use redis or publisher)
await publisher.publish('notifications', 'Hello!');
```

```go
// Go - Dedicated pub/sub connection
import "github.com/redis/go-redis/v9"

// Regular client
rdb := redis.NewClient(&redis.Options{Addr: "localhost:6379"})

// Dedicated pub/sub (creates separate connection internally)
pubsub := rdb.Subscribe(ctx, "notifications", "updates")

// Receive messages in goroutine
go func() {
    ch := pubsub.Channel()
    for msg := range ch {
        fmt.Printf("Received %s from %s\n", msg.Payload, msg.Channel)
    }
}()

// Regular operations continue
rdb.Set(ctx, "key", "value", 0)

// Publish
rdb.Publish(ctx, "notifications", "Hello!")
```

Reference: [Redis Pub/Sub](https://redis.io/docs/manual/pubsub/)

### 3.3 Implement Proper Reconnection Logic

**Impact: HIGH** (prevents cascading failures during network issues)

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

### 3.4 Always Use Connection Pooling

**Impact: CRITICAL** (prevents connection exhaustion, reduces latency 10-100x)

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

### 3.5 Use Pipelining for Multiple Commands

**Impact: HIGH** (reduces latency 5-10x for batched operations)

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

---

## 4. Commands & Patterns

**Impact: HIGH**

### 4.1 Understand Blocking Command Implications

**Impact: MEDIUM-HIGH** (blocking commands tie up connections, require careful handling)

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

### 4.2 Never Use KEYS Command in Production

**Impact: CRITICAL** (KEYS blocks entire Redis server, causes outages)

## Never Use KEYS Command in Production

The KEYS command scans the entire keyspace in a single blocking operation. With millions of keys, it can freeze Redis for seconds or minutes, causing cascading failures. Always use SCAN for pattern matching in production.

**See also:** [key-use-scan-not-keys](./key-use-scan-not-keys.md) for detailed SCAN patterns.

**Why KEYS is Dangerous:**
- O(n) complexity where n = ALL keys in database
- Single-threaded blocking operation
- 1M keys ≈ 1 second block
- 100M keys ≈ minutes of blocking
- Affects ALL clients, not just the caller

**Incorrect:**

```python
import redis
r = redis.Redis()

# NEVER DO THIS IN PRODUCTION
keys = r.keys("user:*")  # Blocks entire Redis!
keys = r.keys("cache:*")  # Disaster waiting to happen
keys = r.keys("*")  # Worst case - scans everything
```

**Correct:**

```python
import redis
r = redis.Redis()

# Use SCAN iterator
for key in r.scan_iter(match="user:*", count=100):
    process(key)

# Or collect into list
keys = list(r.scan_iter(match="user:*", count=100))
```

Reference: [Redis SCAN vs KEYS](https://redis.io/commands/scan/)

### 4.3 Implement Distributed Locks Correctly

**Impact: HIGH** (prevents race conditions in distributed systems)

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

### 4.4 Use Batch Operations for Multiple Keys

**Impact: HIGH** (reduces round trips by 90%+, improves throughput)

## Use Batch Operations for Multiple Keys

Use Redis batch commands (MGET, MSET, HMGET, etc.) when operating on multiple keys. Each round trip adds network latency; batch operations combine multiple operations into a single round trip.

**Batch Commands:**
- `MGET key1 key2 ...` - Get multiple string values
- `MSET key1 val1 key2 val2 ...` - Set multiple strings
- `HMGET key field1 field2 ...` - Get multiple hash fields
- `HMSET key field1 val1 ...` - Set multiple hash fields (deprecated, use HSET)
- `SADD key member1 member2 ...` - Add multiple set members
- `LPUSH key val1 val2 ...` - Push multiple list values
- `DEL key1 key2 ...` - Delete multiple keys

**Incorrect (individual operations):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: Loop of GETs
def get_users_bad(user_ids):
    users = {}
    for user_id in user_ids:
        users[user_id] = r.get(f"user:{user_id}")  # N round trips!
    return users
# 100 users = 100 round trips = 100+ ms

# Anti-pattern 2: Loop of SETs
def cache_products_bad(products):
    for product in products:
        r.set(f"product:{product['id']}", json.dumps(product))
# 1000 products = 1000 round trips

# Anti-pattern 3: Getting hash fields one at a time
def get_user_details_bad(user_id):
    name = r.hget(f"user:{user_id}", "name")
    email = r.hget(f"user:{user_id}", "email")
    age = r.hget(f"user:{user_id}", "age")
    return {"name": name, "email": email, "age": age}
# 3 round trips instead of 1
```

**Correct (using batch operations):**

```python
import redis
import json
r = redis.Redis()

# Correct 1: MGET for multiple keys
def get_users(user_ids):
    """Get multiple users in single round trip"""
    keys = [f"user:{uid}" for uid in user_ids]
    values = r.mget(keys)  # Single round trip!
    return {
        uid: json.loads(v) if v else None
        for uid, v in zip(user_ids, values)
    }
# 100 users = 1 round trip = ~1ms

# Correct 2: MSET for multiple keys
def cache_products(products, ttl=3600):
    """Cache multiple products efficiently"""
    # MSET for bulk insert
    mapping = {
        f"product:{p['id']}": json.dumps(p)
        for p in products
    }
    r.mset(mapping)  # Single round trip

    # If TTL needed, use pipeline
    pipe = r.pipeline()
    for key in mapping.keys():
        pipe.expire(key, ttl)
    pipe.execute()

# Or use SETEX in pipeline for set + TTL
def cache_products_with_ttl(products, ttl=3600):
    pipe = r.pipeline()
    for product in products:
        key = f"product:{product['id']}"
        pipe.setex(key, ttl, json.dumps(product))
    pipe.execute()

# Correct 3: HMGET for multiple hash fields
def get_user_details(user_id):
    """Get multiple hash fields in single call"""
    fields = ["name", "email", "age", "city"]
    values = r.hmget(f"user:{user_id}", fields)  # Single round trip
    return dict(zip(fields, values))

# Or get all fields
def get_user_all(user_id):
    return r.hgetall(f"user:{user_id}")

# Correct 4: HSET with mapping for multiple fields
def update_user(user_id, updates):
    """Update multiple hash fields"""
    r.hset(f"user:{user_id}", mapping=updates)  # Single round trip

# Correct 5: Batch delete
def delete_user_cache(user_ids):
    """Delete multiple keys"""
    keys = [f"cache:user:{uid}" for uid in user_ids]
    if keys:
        r.delete(*keys)  # Single round trip

# Correct 6: Batch add to set
def add_tags_to_product(product_id, tags):
    """Add multiple tags in single call"""
    r.sadd(f"product:{product_id}:tags", *tags)  # Single round trip

# Correct 7: Batch push to list
def add_notifications(user_id, notifications):
    """Add multiple notifications"""
    r.lpush(f"notifications:{user_id}", *[json.dumps(n) for n in notifications])
```

```python
# Combining batch operations with pipeline for complex scenarios

def sync_user_data(users):
    """Efficiently sync multiple users with multiple data types"""
    pipe = r.pipeline()

    for user in users:
        user_id = user['id']

        # User profile (hash)
        pipe.hset(f"user:{user_id}", mapping={
            "name": user['name'],
            "email": user['email']
        })

        # User's roles (set)
        if user.get('roles'):
            pipe.delete(f"user:{user_id}:roles")  # Clear existing
            pipe.sadd(f"user:{user_id}:roles", *user['roles'])

        # Email index
        pipe.set(f"user:email:{user['email']}", user_id)

    pipe.execute()  # All operations in one round trip


def get_dashboard_data(user_id):
    """Fetch all dashboard data efficiently"""
    pipe = r.pipeline()

    # Queue multiple reads
    pipe.hgetall(f"user:{user_id}")
    pipe.smembers(f"user:{user_id}:roles")
    pipe.zrevrange(f"user:{user_id}:activity", 0, 9, withscores=True)
    pipe.lrange(f"user:{user_id}:notifications", 0, 4)
    pipe.get(f"user:{user_id}:unread_count")

    # Execute all at once
    results = pipe.execute()

    return {
        "profile": results[0],
        "roles": results[1],
        "recent_activity": results[2],
        "notifications": results[3],
        "unread_count": int(results[4] or 0)
    }
```

```javascript
// Node.js - Batch operations
const Redis = require('ioredis');
const redis = new Redis();

// MGET
async function getUsers(userIds) {
    const keys = userIds.map(id => `user:${id}`);
    const values = await redis.mget(keys);
    return Object.fromEntries(
        userIds.map((id, i) => [id, values[i] ? JSON.parse(values[i]) : null])
    );
}

// MSET
async function cacheProducts(products) {
    const args = products.flatMap(p => [`product:${p.id}`, JSON.stringify(p)]);
    await redis.mset(...args);
}

// Pipeline for mixed operations
async function getDashboard(userId) {
    const results = await redis.pipeline()
        .hgetall(`user:${userId}`)
        .smembers(`user:${userId}:roles`)
        .zrevrange(`user:${userId}:activity`, 0, 9, 'WITHSCORES')
        .exec();

    return {
        profile: results[0][1],
        roles: results[1][1],
        activity: results[2][1]
    };
}
```

Reference: [Redis MGET](https://redis.io/commands/mget/), [Redis Pipelining](https://redis.io/docs/manual/pipelining/)

### 4.5 Use Lua Scripts for Complex Atomic Operations

**Impact: HIGH** (true atomicity, reduced round trips, server-side logic)

## Use Lua Scripts for Complex Atomic Operations

Use Lua scripts for operations that need true atomicity with conditional logic. Unlike MULTI/EXEC, Lua scripts can read values and make decisions atomically. Scripts run entirely on the server, reducing network round trips.

**Lua vs MULTI/EXEC:**
- MULTI/EXEC: Queue commands, execute together, but can't use results of one command in another
- Lua: Full programming logic, read values, make decisions, all atomic

**When to Use Lua:**
- Conditional operations (if X then Y)
- Read-modify-write patterns
- Complex atomic operations
- Rate limiting with sliding windows
- Distributed locks

**Incorrect (non-atomic conditional logic):**

```python
import redis
r = redis.Redis()

# Anti-pattern: Check-then-act is not atomic
def acquire_lock_bad(lock_name, owner, timeout):
    if not r.exists(lock_name):  # Check
        r.setex(lock_name, timeout, owner)  # Set - race condition!
        return True
    return False

# Anti-pattern: Conditional increment
def increment_if_less_than_bad(key, max_val):
    current = int(r.get(key) or 0)  # Read
    if current < max_val:  # Decide
        r.incr(key)  # Modify - race condition!
        return True
    return False
```

**Correct (using Lua scripts):**

```python
import redis
r = redis.Redis()

# Correct 1: Rate limiter with sliding window
RATE_LIMIT_SCRIPT = """
local key = KEYS[1]
local limit = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local now = tonumber(ARGV[3])

-- Remove old entries
redis.call('ZREMRANGEBYSCORE', key, '-inf', now - window)

-- Count current entries
local count = redis.call('ZCARD', key)

if count < limit then
    -- Add new entry
    redis.call('ZADD', key, now, now .. ':' .. math.random())
    redis.call('EXPIRE', key, window)
    return 1  -- Allowed
else
    return 0  -- Rate limited
end
"""

# Register script (returns SHA for EVALSHA)
rate_limit = r.register_script(RATE_LIMIT_SCRIPT)

def is_allowed(user_id, limit=100, window=60):
    """Check if request is allowed under rate limit"""
    import time
    key = f"ratelimit:{user_id}"
    now = time.time()
    result = rate_limit(keys=[key], args=[limit, window, now])
    return result == 1

# Correct 2: Distributed lock with Lua
LOCK_SCRIPT = """
local key = KEYS[1]
local owner = ARGV[1]
local ttl = tonumber(ARGV[2])

if redis.call('EXISTS', key) == 0 then
    redis.call('SET', key, owner, 'PX', ttl)
    return 1
end
return 0
"""

UNLOCK_SCRIPT = """
local key = KEYS[1]
local owner = ARGV[1]

if redis.call('GET', key) == owner then
    redis.call('DEL', key)
    return 1
end
return 0
"""

acquire_lock = r.register_script(LOCK_SCRIPT)
release_lock = r.register_script(UNLOCK_SCRIPT)

def with_lock(lock_name, owner, ttl_ms=5000):
    """Context manager for distributed lock"""
    class LockContext:
        def __enter__(self):
            result = acquire_lock(keys=[lock_name], args=[owner, ttl_ms])
            if result != 1:
                raise Exception("Could not acquire lock")
            return self

        def __exit__(self, *args):
            release_lock(keys=[lock_name], args=[owner])

    return LockContext()

# Usage
import uuid
owner = str(uuid.uuid4())
with with_lock("my-resource", owner):
    # Critical section
    do_something()

# Correct 3: Atomic increment with limit
INCREMENT_IF_BELOW = """
local key = KEYS[1]
local max = tonumber(ARGV[1])
local current = tonumber(redis.call('GET', key) or '0')

if current < max then
    return redis.call('INCR', key)
end
return -1
"""

increment_below = r.register_script(INCREMENT_IF_BELOW)

def safe_increment(key, max_value):
    result = increment_below(keys=[key], args=[max_value])
    return result if result != -1 else None

# Correct 4: Compare and swap
CAS_SCRIPT = """
local key = KEYS[1]
local expected = ARGV[1]
local new_value = ARGV[2]

local current = redis.call('GET', key)
if current == expected then
    redis.call('SET', key, new_value)
    return 1
end
return 0
"""

compare_and_swap = r.register_script(CAS_SCRIPT)

def cas(key, expected, new_value):
    """Atomic compare-and-swap"""
    return compare_and_swap(keys=[key], args=[expected, new_value]) == 1

# Correct 5: Batch get with fallback
GET_OR_SET = """
local key = KEYS[1]
local default = ARGV[1]
local ttl = tonumber(ARGV[2])

local value = redis.call('GET', key)
if value then
    return value
end

redis.call('SET', key, default, 'EX', ttl)
return default
"""

get_or_set = r.register_script(GET_OR_SET)
```

```python
# Script management best practices

class RedisScripts:
    """Centralized Lua script management"""

    def __init__(self, redis_client):
        self.r = redis_client
        self._scripts = {}

    def register(self, name, script):
        """Register and cache script"""
        self._scripts[name] = self.r.register_script(script)

    def __getattr__(self, name):
        """Get registered script"""
        if name in self._scripts:
            return self._scripts[name]
        raise AttributeError(f"Script '{name}' not registered")

# Usage
scripts = RedisScripts(r)
scripts.register('rate_limit', RATE_LIMIT_SCRIPT)
scripts.register('acquire_lock', LOCK_SCRIPT)

# Call scripts
scripts.rate_limit(keys=['ratelimit:user1'], args=[100, 60, time.time()])
```

```javascript
// Node.js - Lua scripts with ioredis
const Redis = require('ioredis');
const redis = new Redis();

// Define scripts
redis.defineCommand('rateLimit', {
    numberOfKeys: 1,
    lua: `
        local key = KEYS[1]
        local limit = tonumber(ARGV[1])
        local window = tonumber(ARGV[2])
        local now = tonumber(ARGV[3])

        redis.call('ZREMRANGEBYSCORE', key, '-inf', now - window)
        local count = redis.call('ZCARD', key)

        if count < limit then
            redis.call('ZADD', key, now, now .. ':' .. math.random())
            redis.call('EXPIRE', key, window)
            return 1
        end
        return 0
    `
});

// Use defined command
async function isAllowed(userId, limit = 100, window = 60) {
    const key = `ratelimit:${userId}`;
    const now = Date.now() / 1000;
    const result = await redis.rateLimit(key, limit, window, now);
    return result === 1;
}
```

Reference: [Redis Lua Scripting](https://redis.io/docs/manual/programmability/eval-intro/)

### 4.6 Use MULTI/EXEC for Atomic Operations

**Impact: HIGH** (prevents race conditions, ensures data consistency)

## Use MULTI/EXEC for Atomic Operations

Use Redis transactions (MULTI/EXEC) when multiple commands must execute atomically. Without transactions, concurrent clients can interleave operations, causing race conditions and data corruption.

**What MULTI/EXEC Provides:**
- All commands execute sequentially without interruption
- Other clients' commands never interleave
- Either all commands execute or none (if EXEC fails)
- Note: No rollback on command errors within transaction

**Incorrect (race condition prone):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: Check-then-act without atomicity
def transfer_funds_bad(from_acct, to_acct, amount):
    # Race condition! Another client can modify between these calls
    balance = int(r.get(f"balance:{from_acct}") or 0)
    if balance >= amount:
        r.decrby(f"balance:{from_acct}", amount)  # Not atomic!
        r.incrby(f"balance:{to_acct}", amount)
        return True
    return False

# Anti-pattern 2: Increment after check
def increment_if_below_max_bad(key, max_value):
    current = int(r.get(key) or 0)
    if current < max_value:
        r.incr(key)  # Race: might exceed max!
        return True
    return False

# Anti-pattern 3: Read-modify-write without lock
def update_json_bad(key, updates):
    data = json.loads(r.get(key) or '{}')
    data.update(updates)  # Another client might update between read and write
    r.set(key, json.dumps(data))
```

**Correct (using transactions):**

```python
import redis
r = redis.Redis()

# Correct 1: Pipeline with transaction=True (MULTI/EXEC)
def transfer_funds(from_acct, to_acct, amount):
    """Atomic transfer using transaction"""
    pipe = r.pipeline(transaction=True)  # Wraps in MULTI/EXEC
    pipe.decrby(f"balance:{from_acct}", amount)
    pipe.incrby(f"balance:{to_acct}", amount)
    results = pipe.execute()
    return results

# Correct 2: WATCH for optimistic locking
def transfer_funds_with_check(from_acct, to_acct, amount):
    """Transfer with balance check using WATCH"""
    from_key = f"balance:{from_acct}"
    to_key = f"balance:{to_acct}"

    with r.pipeline() as pipe:
        while True:
            try:
                # Watch the source account for changes
                pipe.watch(from_key)

                # Check balance (outside transaction)
                balance = int(pipe.get(from_key) or 0)
                if balance < amount:
                    pipe.unwatch()
                    return False  # Insufficient funds

                # Start transaction
                pipe.multi()
                pipe.decrby(from_key, amount)
                pipe.incrby(to_key, amount)
                pipe.execute()  # Executes atomically
                return True

            except redis.WatchError:
                # Another client modified the key, retry
                continue

# Correct 3: Atomic increment with limit
def increment_with_limit(key, max_value, expire=None):
    """Atomic increment that respects maximum value"""
    # Use Lua script for true atomicity (see cmd-use-lua-scripts)
    lua_script = """
    local current = tonumber(redis.call('GET', KEYS[1]) or '0')
    if current < tonumber(ARGV[1]) then
        redis.call('INCR', KEYS[1])
        if ARGV[2] then
            redis.call('EXPIRE', KEYS[1], ARGV[2])
        end
        return current + 1
    end
    return -1
    """
    result = r.eval(lua_script, 1, key, max_value, expire or '')
    return result if result != -1 else None

# Correct 4: Bulk operations atomically
def create_user_atomic(user_id, user_data):
    """Create user with all related data atomically"""
    pipe = r.pipeline(transaction=True)

    # All these execute as one atomic operation
    pipe.hset(f"user:{user_id}", mapping=user_data)
    pipe.set(f"user:email:{user_data['email']}", user_id)
    pipe.sadd("users:all", user_id)
    pipe.zadd("users:by_created", {user_id: time.time()})

    results = pipe.execute()
    return all(results)
```

```javascript
// Node.js - Transactions with ioredis
const Redis = require('ioredis');
const redis = new Redis();

// Basic transaction
async function transferFunds(fromAcct, toAcct, amount) {
    const results = await redis.multi()
        .decrby(`balance:${fromAcct}`, amount)
        .incrby(`balance:${toAcct}`, amount)
        .exec();

    return results;
}

// WATCH for optimistic locking
async function transferWithCheck(fromAcct, toAcct, amount) {
    const fromKey = `balance:${fromAcct}`;

    await redis.watch(fromKey);

    const balance = parseInt(await redis.get(fromKey)) || 0;
    if (balance < amount) {
        await redis.unwatch();
        return false;
    }

    try {
        const results = await redis.multi()
            .decrby(fromKey, amount)
            .incrby(`balance:${toAcct}`, amount)
            .exec();

        return results !== null;  // null if WATCH failed
    } catch (e) {
        return false;
    }
}
```

```go
// Go - Transactions with go-redis
func TransferFunds(ctx context.Context, from, to string, amount int64) error {
    _, err := rdb.TxPipelined(ctx, func(pipe redis.Pipeliner) error {
        pipe.DecrBy(ctx, fmt.Sprintf("balance:%s", from), amount)
        pipe.IncrBy(ctx, fmt.Sprintf("balance:%s", to), amount)
        return nil
    })
    return err
}

// WATCH for optimistic locking
func TransferWithCheck(ctx context.Context, from, to string, amount int64) error {
    fromKey := fmt.Sprintf("balance:%s", from)
    toKey := fmt.Sprintf("balance:%s", to)

    return rdb.Watch(ctx, func(tx *redis.Tx) error {
        balance, err := tx.Get(ctx, fromKey).Int64()
        if err != nil && err != redis.Nil {
            return err
        }
        if balance < amount {
            return errors.New("insufficient funds")
        }

        _, err = tx.TxPipelined(ctx, func(pipe redis.Pipeliner) error {
            pipe.DecrBy(ctx, fromKey, amount)
            pipe.IncrBy(ctx, toKey, amount)
            return nil
        })
        return err
    }, fromKey)
}
```

Reference: [Redis Transactions](https://redis.io/docs/manual/transactions/)

---

## 5. Memory Management

**Impact: MEDIUM-HIGH**

### 5.1 Choose Appropriate Eviction Policy

**Impact: CRITICAL** (wrong policy causes data loss or OOM errors)

## Choose Appropriate Eviction Policy

Configure the right `maxmemory-policy` for your use case. The eviction policy determines which keys Redis removes when memory limit is reached. Wrong policy can cause important data loss or OOM errors blocking writes.

**Available Policies:**
| Policy | Behavior | Use Case |
|--------|----------|----------|
| `noeviction` | Return error on writes | When data loss is unacceptable |
| `allkeys-lru` | Evict least recently used | General caching |
| `allkeys-lfu` | Evict least frequently used | Caching with popularity |
| `volatile-lru` | LRU among keys with TTL | Mixed cache + persistent data |
| `volatile-lfu` | LFU among keys with TTL | Mixed with popularity |
| `allkeys-random` | Random eviction | When all keys equal priority |
| `volatile-random` | Random among keys with TTL | Mixed, no preference |
| `volatile-ttl` | Evict shortest TTL first | When TTL indicates priority |

**Incorrect (wrong policy for use case):**

```bash
# Anti-pattern 1: noeviction for cache
# redis.conf
maxmemory 2gb
maxmemory-policy noeviction  # Writes fail when full!
# Result: Application errors when cache is full

# Anti-pattern 2: volatile-* when no keys have TTL
maxmemory-policy volatile-lru
# If no keys have TTL, behaves like noeviction!
# Result: OOM errors even though eviction is configured

# Anti-pattern 3: allkeys-* when some data must persist
maxmemory-policy allkeys-lru
# Will evict ANY key including important non-cache data
# Result: Critical data randomly deleted
```

**Correct (policy matches use case):**

```bash
# Correct 1: Pure cache - use allkeys-lru or allkeys-lfu
# redis.conf
maxmemory 4gb
maxmemory-policy allkeys-lru  # General caching
# OR
maxmemory-policy allkeys-lfu  # Better for skewed access patterns

# Correct 2: Cache + persistent data - use volatile-*
# Set TTL on cache keys, no TTL on persistent keys
maxmemory 4gb
maxmemory-policy volatile-lru
# Only keys with TTL are evicted

# Correct 3: Session store - volatile-ttl
maxmemory 2gb
maxmemory-policy volatile-ttl
# Sessions expiring soonest are evicted first

# Correct 4: Primary database (no eviction acceptable)
maxmemory 8gb
maxmemory-policy noeviction
# Application must handle OOM errors gracefully
```

```python
import redis
r = redis.Redis()

# Correct 1: Verify eviction policy matches your needs
def verify_eviction_config():
    """Check that eviction policy is appropriate"""
    info = r.info("memory")
    policy = info.get("maxmemory_policy", "unknown")
    max_mem = info.get("maxmemory", 0)

    print(f"maxmemory: {max_mem}")
    print(f"maxmemory-policy: {policy}")

    if policy == "noeviction":
        print("WARNING: noeviction policy - writes will fail when memory full")

    if policy.startswith("volatile"):
        # Check if we actually have keys with TTL
        all_keys = r.dbsize()
        with_ttl = check_keys_with_ttl_sample()
        if with_ttl < all_keys * 0.1:
            print(f"WARNING: volatile policy but only {with_ttl}/{all_keys} keys have TTL")

def check_keys_with_ttl_sample(sample_size=1000):
    """Sample keys to estimate how many have TTL"""
    count = 0
    with_ttl = 0

    for key in r.scan_iter(count=100):
        ttl = r.ttl(key)
        if ttl > 0:  # Has TTL (not -1 = no TTL, not -2 = doesn't exist)
            with_ttl += 1
        count += 1
        if count >= sample_size:
            break

    return with_ttl

# Correct 2: Cache pattern with volatile-lru
# Set TTL on cache keys, persistent keys have no TTL
def cache_set(key, value, ttl=3600):
    """Cache with TTL (eligible for eviction)"""
    r.setex(f"cache:{key}", ttl, value)

def persist_set(key, value):
    """Persistent data without TTL (protected from volatile eviction)"""
    r.set(f"data:{key}", value)  # No TTL = protected with volatile-* policy

# Correct 3: Handle eviction in application
def get_or_compute(key, compute_func, ttl=3600):
    """
    Cache pattern that handles evicted keys gracefully.
    If key was evicted, recompute and cache again.
    """
    value = r.get(key)
    if value is None:
        value = compute_func()
        r.setex(key, ttl, value)
    return value

# Correct 4: Monitor eviction
def get_eviction_stats():
    """Monitor key evictions"""
    info = r.info("stats")
    return {
        "evicted_keys": info.get("evicted_keys", 0),
        "keyspace_hits": info.get("keyspace_hits", 0),
        "keyspace_misses": info.get("keyspace_misses", 0),
    }

def alert_on_eviction_rate(threshold_per_second=100):
    """Alert if eviction rate is too high"""
    stats1 = get_eviction_stats()
    time.sleep(1)
    stats2 = get_eviction_stats()

    eviction_rate = stats2["evicted_keys"] - stats1["evicted_keys"]
    if eviction_rate > threshold_per_second:
        print(f"HIGH EVICTION RATE: {eviction_rate}/sec")
        return True
    return False
```

```bash
# Runtime policy change
redis-cli CONFIG SET maxmemory-policy allkeys-lru

# Check eviction statistics
redis-cli INFO stats | grep evicted

# Tune eviction sampling (higher = more accurate, slightly slower)
redis-cli CONFIG SET maxmemory-samples 10
```

```python
# Policy selection decision tree

def recommend_eviction_policy(
    is_pure_cache: bool,
    has_ttl_on_cache_keys: bool,
    has_persistent_data: bool,
    access_pattern: str  # "uniform" or "skewed"
):
    """Recommend eviction policy based on use case"""

    if not is_pure_cache and has_persistent_data:
        if has_ttl_on_cache_keys:
            # Mixed: cache (with TTL) + persistent (no TTL)
            if access_pattern == "skewed":
                return "volatile-lfu"
            return "volatile-lru"
        else:
            # Must use noeviction if can't lose data
            return "noeviction"

    # Pure cache
    if access_pattern == "skewed":
        return "allkeys-lfu"  # Frequently accessed items kept
    return "allkeys-lru"  # Recently accessed items kept

# Examples:
# Pure cache: allkeys-lru or allkeys-lfu
# Session store: volatile-ttl (shortest TTL evicted first)
# Mixed workload: volatile-lru (only cache keys have TTL)
# Database: noeviction (handle OOM in app)
```

Reference: [Redis Eviction Policies](https://redis.io/docs/manual/eviction/)

### 5.2 Always Configure maxmemory Limit

**Impact: CRITICAL** (prevents OOM crashes, enables predictable behavior)

## Always Configure maxmemory Limit

Always set a `maxmemory` limit for Redis. Without it, Redis uses unlimited memory and will be killed by the OS OOM killer when it exhausts system memory, causing data loss and outages.

**Why maxmemory is Critical:**
- Without limit: Redis grows until OS kills it
- OOM killer: Abrupt termination, no graceful handling
- Data loss: Unsaved data is lost
- Cascading failure: Dependent services fail

**Recommended Settings:**
- Set maxmemory to 75-80% of available RAM
- Leave room for OS, persistence operations, and fork()
- Configure appropriate eviction policy

**Incorrect (no memory limit):**

```bash
# redis.conf - Anti-pattern: no maxmemory set
# maxmemory <bytes>  # Commented out or missing
# Redis will use unlimited memory!

# Anti-pattern: maxmemory too high
maxmemory 64gb  # On a 64GB machine - no room for OS!
```

```python
import redis
r = redis.Redis()

# Anti-pattern: No monitoring for memory pressure
def cache_data(key, value):
    r.set(key, value)  # Keep adding without checking memory
```

**Correct (configure maxmemory):**

```bash
# redis.conf - Production configuration

# Set maxmemory to ~75% of available RAM
# For 8GB machine:
maxmemory 6gb

# For 32GB machine:
maxmemory 24gb

# Must also set eviction policy (see memory-choose-eviction-policy)
maxmemory-policy allkeys-lru

# Optional: memory samples for eviction accuracy
maxmemory-samples 10
```

```bash
# Set at runtime via CLI
redis-cli CONFIG SET maxmemory 6gb
redis-cli CONFIG SET maxmemory-policy allkeys-lru

# Verify settings
redis-cli CONFIG GET maxmemory
redis-cli CONFIG GET maxmemory-policy

# Check current memory usage
redis-cli INFO memory
```

```python
import redis
r = redis.Redis()

# Correct 1: Check memory before operations
def check_memory_health():
    """Check if Redis has sufficient memory"""
    info = r.info("memory")
    used = info['used_memory']
    max_mem = info.get('maxmemory', 0)

    if max_mem == 0:
        print("WARNING: maxmemory not configured!")
        return False

    usage_pct = (used / max_mem) * 100
    print(f"Memory usage: {usage_pct:.1f}% ({used / 1024 / 1024:.1f}MB / {max_mem / 1024 / 1024:.1f}MB)")

    if usage_pct > 90:
        print("WARNING: Memory usage critical!")
        return False

    return True

# Correct 2: Graceful handling of memory pressure
def safe_cache_set(key, value, ttl=3600):
    """Set with memory-aware error handling"""
    try:
        r.setex(key, ttl, value)
        return True
    except redis.ResponseError as e:
        if "OOM" in str(e):
            # Handle OOM - Redis maxmemory reached with noeviction
            print(f"Redis OOM: Cannot write {key}")
            return False
        raise

# Correct 3: Memory monitoring and alerting
def get_memory_stats():
    """Get detailed memory statistics"""
    info = r.info("memory")
    return {
        "used_memory": info["used_memory"],
        "used_memory_human": info["used_memory_human"],
        "used_memory_peak": info["used_memory_peak"],
        "used_memory_peak_human": info["used_memory_peak_human"],
        "maxmemory": info.get("maxmemory", 0),
        "maxmemory_human": info.get("maxmemory_human", "0B"),
        "maxmemory_policy": info.get("maxmemory_policy", "noeviction"),
        "mem_fragmentation_ratio": info.get("mem_fragmentation_ratio", 0),
        "used_memory_rss": info.get("used_memory_rss", 0),
    }

def alert_on_high_memory(threshold_pct=85):
    """Alert if memory usage exceeds threshold"""
    stats = get_memory_stats()
    max_mem = stats["maxmemory"]

    if max_mem == 0:
        raise ValueError("maxmemory not configured - critical!")

    usage_pct = (stats["used_memory"] / max_mem) * 100

    if usage_pct >= threshold_pct:
        return {
            "alert": True,
            "message": f"Redis memory at {usage_pct:.1f}%",
            "used": stats["used_memory_human"],
            "max": stats["maxmemory_human"],
        }
    return {"alert": False}
```

```python
# Docker/Kubernetes configuration

# Docker Compose
"""
services:
  redis:
    image: redis:7
    command: redis-server --maxmemory 2gb --maxmemory-policy allkeys-lru
    deploy:
      resources:
        limits:
          memory: 3g  # Container limit > maxmemory (for fork/persistence)
"""

# Kubernetes ConfigMap
"""
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-config
data:
  redis.conf: |
    maxmemory 2gb
    maxmemory-policy allkeys-lru
    maxmemory-samples 10
"""
```

```javascript
// Node.js - Memory monitoring
const Redis = require('ioredis');
const redis = new Redis();

async function checkMemoryHealth() {
    const info = await redis.info('memory');
    const lines = info.split('\r\n');
    const stats = {};

    lines.forEach(line => {
        const [key, value] = line.split(':');
        if (key && value) stats[key] = value;
    });

    const used = parseInt(stats.used_memory);
    const max = parseInt(stats.maxmemory || '0');

    if (max === 0) {
        console.warn('maxmemory not configured!');
        return false;
    }

    const usagePct = (used / max) * 100;
    console.log(`Memory: ${usagePct.toFixed(1)}%`);

    return usagePct < 90;
}
```

Reference: [Redis Memory Management](https://redis.io/docs/management/optimization/memory-optimization/)

### 5.3 Monitor and Handle Memory Fragmentation

**Impact: MEDIUM-HIGH** (high fragmentation wastes 20-50% memory)

## Monitor and Handle Memory Fragmentation

Monitor memory fragmentation ratio and take action when it's too high. Fragmentation occurs when Redis allocates and frees memory repeatedly, leaving gaps. High fragmentation wastes memory and can cause OOM even with available space.

**Fragmentation Ratio:**
- `mem_fragmentation_ratio = used_memory_rss / used_memory`
- **< 1.0**: Redis using swap (very bad!)
- **1.0 - 1.5**: Healthy
- **> 1.5**: Moderate fragmentation
- **> 2.0**: High fragmentation, action needed

**Causes of Fragmentation:**
- Frequent key creation/deletion
- Variable-size updates
- Large deletions followed by small writes
- Long-running instances without restarts

**Incorrect (ignoring fragmentation):**

```python
import redis
r = redis.Redis()

# Anti-pattern: Not monitoring fragmentation
def check_memory_bad():
    info = r.info("memory")
    print(f"Used memory: {info['used_memory_human']}")
    # Missing fragmentation check!

# Anti-pattern: Assuming used_memory is all that matters
def has_memory_available_bad(needed_bytes):
    info = r.info("memory")
    max_mem = info.get("maxmemory", 0)
    used = info["used_memory"]
    return (max_mem - used) > needed_bytes
# Wrong! RSS (actual memory) could be much higher due to fragmentation
```

**Correct (monitoring and handling fragmentation):**

```python
import redis
r = redis.Redis()

# Correct 1: Monitor fragmentation ratio
def check_memory_health():
    """Comprehensive memory health check including fragmentation"""
    info = r.info("memory")

    used = info["used_memory"]
    rss = info["used_memory_rss"]
    frag_ratio = info["mem_fragmentation_ratio"]
    frag_bytes = info.get("mem_fragmentation_bytes", rss - used)

    health = {
        "used_memory": info["used_memory_human"],
        "used_memory_rss": info["used_memory_rss_human"],
        "fragmentation_ratio": frag_ratio,
        "fragmentation_bytes": frag_bytes,
        "status": "healthy"
    }

    if frag_ratio < 1.0:
        health["status"] = "critical"
        health["issue"] = "Using swap memory!"
    elif frag_ratio > 2.0:
        health["status"] = "warning"
        health["issue"] = f"High fragmentation: {frag_ratio:.2f}"
        health["wasted_memory"] = f"{frag_bytes / 1024 / 1024:.1f} MB"
    elif frag_ratio > 1.5:
        health["status"] = "moderate"
        health["issue"] = f"Moderate fragmentation: {frag_ratio:.2f}"

    return health

def alert_on_fragmentation(threshold=1.5):
    """Alert when fragmentation exceeds threshold"""
    info = r.info("memory")
    frag_ratio = info["mem_fragmentation_ratio"]

    if frag_ratio < 1.0:
        return {
            "alert": "CRITICAL",
            "message": "Redis is using swap! Performance severely degraded.",
            "ratio": frag_ratio
        }
    elif frag_ratio > threshold:
        frag_bytes = info.get("mem_fragmentation_bytes", 0)
        return {
            "alert": "WARNING",
            "message": f"Memory fragmentation at {frag_ratio:.2f}",
            "ratio": frag_ratio,
            "wasted_mb": frag_bytes / 1024 / 1024
        }

    return {"alert": None}

# Correct 2: Check if active defragmentation is running
def check_defrag_status():
    """Check active defragmentation status"""
    info = r.info("memory")
    return {
        "active_defrag_running": info.get("active_defrag_running", 0),
        "active_defrag_hits": info.get("active_defrag_hits", 0),
        "active_defrag_misses": info.get("active_defrag_misses", 0),
        "active_defrag_key_hits": info.get("active_defrag_key_hits", 0),
        "active_defrag_key_misses": info.get("active_defrag_key_misses", 0),
    }
```

```bash
# Enable active defragmentation (Redis 4.0+)
# redis.conf

# Enable active defrag (off by default)
activedefrag yes

# Start defrag when fragmentation > 10%
active-defrag-ignore-bytes 100mb
active-defrag-threshold-lower 10

# Stop when fragmentation < 5%
active-defrag-threshold-upper 100

# CPU effort (1-25% of idle CPU)
active-defrag-cycle-min 1
active-defrag-cycle-max 25

# Max scan per cycle (reduce for latency-sensitive workloads)
active-defrag-max-scan-fields 1000
```

```python
# Correct 3: Enable/configure defrag at runtime
def configure_defragmentation():
    """Enable and configure active defragmentation"""
    # Enable active defrag
    r.config_set("activedefrag", "yes")

    # Start defrag when fragmentation exceeds 10%
    r.config_set("active-defrag-threshold-lower", "10")

    # Aggressive defrag above 50% fragmentation
    r.config_set("active-defrag-threshold-upper", "50")

    # CPU usage for defrag (1-25% of idle CPU)
    r.config_set("active-defrag-cycle-min", "5")
    r.config_set("active-defrag-cycle-max", "25")

    # Ignore if fragmented memory < 100MB
    r.config_set("active-defrag-ignore-bytes", "104857600")

def disable_defragmentation():
    """Disable defrag during performance-critical periods"""
    r.config_set("activedefrag", "no")

# Correct 4: Manual defrag trigger (Redis 7.2+)
def trigger_manual_defrag():
    """Trigger one-time defragmentation"""
    try:
        r.execute_command("MEMORY", "DEFRAG")
        print("Manual defragmentation triggered")
    except redis.ResponseError as e:
        print(f"Defrag not available: {e}")
```

```python
# Correct 5: Strategies to prevent fragmentation

def prevent_fragmentation_tips():
    """Best practices to minimize fragmentation"""
    return """
    1. Use consistent value sizes when possible
    2. Set TTL on temporary keys (automatic cleanup)
    3. Use UNLINK instead of DEL for large keys (async delete)
    4. Consider periodic restarts for long-running instances
    5. Enable active defragmentation for write-heavy workloads
    6. Monitor fragmentation ratio in your metrics
    """

# Use UNLINK for large key deletion
def delete_large_key(key):
    """Delete key asynchronously to reduce blocking and fragmentation"""
    r.unlink(key)  # Non-blocking delete
    # vs r.delete(key) which blocks

# Batch delete with UNLINK
def delete_keys_by_pattern(pattern):
    """Delete keys matching pattern using async UNLINK"""
    pipe = r.pipeline()
    count = 0

    for key in r.scan_iter(match=pattern, count=100):
        pipe.unlink(key)
        count += 1

        if count % 1000 == 0:
            pipe.execute()
            pipe = r.pipeline()

    if count % 1000 != 0:
        pipe.execute()

    return count
```

```bash
# Monitor fragmentation from CLI
redis-cli INFO memory | grep frag

# Output:
# mem_fragmentation_ratio:1.23
# mem_fragmentation_bytes:12345678

# Memory doctor (Redis 4.0+)
redis-cli MEMORY DOCTOR

# Detailed memory stats
redis-cli MEMORY STATS
```

Reference: [Redis Active Defragmentation](https://redis.io/docs/management/optimization/memory-optimization/#active-defragmentation)

### 5.4 Use Memory-Efficient Data Encodings

**Impact: MEDIUM-HIGH** (can reduce memory usage 50-90% for small objects)

## Use Memory-Efficient Data Encodings

Redis automatically uses memory-efficient encodings (ziplist, intset, listpack) for small data structures. Keep collections small to benefit from these optimizations, and tune thresholds if needed.

**Internal Encodings:**
- **Strings**: int (for integers), embstr (≤44 bytes), raw
- **Lists**: listpack (small), quicklist (large)
- **Sets**: intset (integers only), listpack (small), hashtable
- **Hashes**: listpack (small), hashtable
- **Sorted Sets**: listpack (small), skiplist

**Encoding Thresholds (Redis 7+):**
- `hash-max-listpack-entries`: 512 (switch to hashtable above)
- `hash-max-listpack-value`: 64 bytes
- `list-max-listpack-size`: -2 (8KB per node)
- `set-max-intset-entries`: 512
- `set-max-listpack-entries`: 128
- `zset-max-listpack-entries`: 128
- `zset-max-listpack-value`: 64 bytes

**Incorrect (wasting memory):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: Storing numbers as strings
r.set("counter", "12345")  # Stored as string
# Better: let Redis store as int

# Anti-pattern 2: Large hash fields preventing listpack
r.hset("user:123", "bio", "A" * 1000)  # 1000 bytes > 64 byte threshold
# Forces hash to use hashtable encoding (more memory)

# Anti-pattern 3: Many small separate keys instead of hash
for i in range(1000):
    r.set(f"setting:{i}", "value")
# Each key has ~50 bytes overhead
# 1000 keys = 50KB overhead

# Anti-pattern 4: Using hash for large collection
for i in range(10000):
    r.hset("big_hash", f"field:{i}", "value")
# Exceeds listpack threshold, uses more memory per field
```

**Correct (memory-efficient patterns):**

```python
import redis
r = redis.Redis()

# Correct 1: Store integers efficiently
r.set("counter", 12345)  # Redis stores as integer internally
r.incr("counter")  # Efficient integer operations

# Check encoding
encoding = r.object("encoding", "counter")
print(f"counter encoding: {encoding}")  # Should be "int"

# Correct 2: Keep hash values small for listpack
def store_user_efficient(user_id, user_data):
    """Store user with small field values"""
    # Keep field values under 64 bytes
    r.hset(f"user:{user_id}", mapping={
        "name": user_data["name"][:64],  # Truncate if needed
        "email": user_data["email"][:64],
        "age": user_data["age"],  # Integer stored efficiently
    })

    # Store large content separately
    if len(user_data.get("bio", "")) > 64:
        r.set(f"user:{user_id}:bio", user_data["bio"])

# Correct 3: Use hash bucketing for many small values
def set_bucketed(prefix, key, value, bucket_size=100):
    """
    Store in hash buckets instead of individual keys.
    Reduces per-key overhead significantly.
    """
    bucket = hash(key) % bucket_size
    r.hset(f"{prefix}:bucket:{bucket}", key, value)

def get_bucketed(prefix, key, bucket_size=100):
    bucket = hash(key) % bucket_size
    return r.hget(f"{prefix}:bucket:{bucket}", key)

# Example: 1M settings
# Without bucketing: 1M keys * ~50 bytes overhead = ~50MB overhead
# With 100 buckets: 100 hashes with ~10K fields each = minimal overhead

# Correct 4: Use intset for integer-only sets
r.sadd("user_ids", 1, 2, 3, 4, 5)  # Stored as intset (very compact)
encoding = r.object("encoding", "user_ids")
print(f"user_ids encoding: {encoding}")  # Should be "intset"

# Correct 5: Keep sorted sets small for listpack
# Under 128 elements with values < 64 bytes uses listpack
r.zadd("top_users", {"user1": 100, "user2": 95, "user3": 90})
encoding = r.object("encoding", "top_users")
print(f"top_users encoding: {encoding}")  # Should be "listpack"
```

```python
# Memory analysis tools

def analyze_key_memory(key):
    """Analyze memory usage of a key"""
    key_type = r.type(key).decode()
    encoding = r.object("encoding", key)
    memory = r.memory_usage(key)
    idle_time = r.object("idletime", key)

    info = {
        "key": key,
        "type": key_type,
        "encoding": encoding.decode() if encoding else None,
        "memory_bytes": memory,
        "idle_seconds": idle_time,
    }

    # Add type-specific info
    if key_type == "hash":
        info["field_count"] = r.hlen(key)
    elif key_type == "list":
        info["length"] = r.llen(key)
    elif key_type == "set":
        info["cardinality"] = r.scard(key)
    elif key_type == "zset":
        info["cardinality"] = r.zcard(key)
    elif key_type == "string":
        info["string_length"] = r.strlen(key)

    return info

def find_inefficient_encodings(sample_size=1000):
    """Find keys using less efficient encodings"""
    inefficient = []

    for key in r.scan_iter(count=100):
        if len(inefficient) >= sample_size:
            break

        key_type = r.type(key).decode()
        encoding = r.object("encoding", key)

        if encoding:
            encoding = encoding.decode()
            # Flag potentially inefficient encodings
            if key_type == "hash" and encoding == "hashtable":
                field_count = r.hlen(key)
                if field_count < 512:
                    inefficient.append({
                        "key": key.decode(),
                        "type": key_type,
                        "encoding": encoding,
                        "fields": field_count,
                        "reason": "Hash with <512 fields using hashtable"
                    })

    return inefficient
```

```bash
# Redis configuration for memory efficiency
# redis.conf

# Hash encoding thresholds
hash-max-listpack-entries 512
hash-max-listpack-value 64

# List encoding
list-max-listpack-size -2  # 8 KB max size

# Set encoding
set-max-intset-entries 512
set-max-listpack-entries 128
set-max-listpack-value 64

# Sorted Set encoding
zset-max-listpack-entries 128
zset-max-listpack-value 64

# Check current settings
redis-cli CONFIG GET hash-max-*
redis-cli CONFIG GET list-max-*
redis-cli CONFIG GET set-max-*
redis-cli CONFIG GET zset-max-*
```

Reference: [Redis Memory Optimization](https://redis.io/docs/management/optimization/memory-optimization/)

### 5.5 Enable Lazy Freeing for Large Deletions

**Impact: MEDIUM** (prevents blocking during large key deletions)

## Enable Lazy Freeing for Large Deletions

Use `UNLINK` instead of `DEL` for large keys, and enable lazy freeing options. Deleting large keys (millions of elements) blocks Redis for seconds. Lazy freeing moves memory reclamation to background threads.

**Commands:**
- `DEL`: Synchronous delete (blocks Redis)
- `UNLINK`: Asynchronous delete (returns immediately, memory freed in background)

**Lazy Freeing Options:**
- `lazyfree-lazy-eviction`: Async eviction when maxmemory reached
- `lazyfree-lazy-expire`: Async deletion of expired keys
- `lazyfree-lazy-server-del`: Async for implicit deletions (RENAME, etc.)
- `lazyfree-lazy-user-del`: Make DEL behave like UNLINK
- `lazyfree-lazy-user-flush`: Async FLUSHALL/FLUSHDB

**Incorrect (blocking deletions):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: DEL on large key
r.delete("huge_set")  # Blocks Redis if set has millions of members!

# Anti-pattern 2: Mass deletion blocking
def clear_cache_bad():
    for key in r.scan_iter(match="cache:*"):
        r.delete(key)  # Each delete might block

# Anti-pattern 3: FLUSHDB without ASYNC
r.flushdb()  # Blocks entire database clear

# Anti-pattern 4: RENAME that deletes large key
r.rename("new_data", "old_large_data")  # Implicitly deletes old_large_data, blocks!
```

**Correct (non-blocking deletions):**

```python
import redis
r = redis.Redis()

# Correct 1: Use UNLINK for potentially large keys
def delete_key_safe(key):
    """Delete key without blocking Redis"""
    r.unlink(key)  # Returns immediately, memory freed in background

# Correct 2: Use UNLINK for batch deletions
def clear_cache_safe(pattern="cache:*", batch_size=1000):
    """Delete keys matching pattern without blocking"""
    pipe = r.pipeline()
    count = 0

    for key in r.scan_iter(match=pattern, count=100):
        pipe.unlink(key)  # Use UNLINK, not DELETE
        count += 1

        if count % batch_size == 0:
            pipe.execute()
            pipe = r.pipeline()

    if count % batch_size != 0:
        pipe.execute()

    return count

# Correct 3: Async flush
def flush_database_safe():
    """Flush database without blocking"""
    r.flushdb(asynchronous=True)  # Non-blocking flush

def flush_all_safe():
    """Flush all databases without blocking"""
    r.flushall(asynchronous=True)

# Correct 4: Check key size before choosing delete method
def smart_delete(key, size_threshold=10000):
    """Use UNLINK for large keys, DEL for small ones"""
    key_type = r.type(key).decode()

    # Estimate size based on type
    if key_type == "string":
        size = r.strlen(key)
    elif key_type == "list":
        size = r.llen(key)
    elif key_type == "set":
        size = r.scard(key)
    elif key_type == "zset":
        size = r.zcard(key)
    elif key_type == "hash":
        size = r.hlen(key)
    else:
        size = 0

    if size > size_threshold:
        r.unlink(key)  # Async for large keys
    else:
        r.delete(key)  # Sync is fine for small keys
```

```bash
# Enable lazy freeing in redis.conf
# redis.conf

# Async eviction when maxmemory is reached
lazyfree-lazy-eviction yes

# Async deletion of expired keys
lazyfree-lazy-expire yes

# Async for implicit deletions (RENAME overwriting, etc.)
lazyfree-lazy-server-del yes

# Make DEL behave like UNLINK (Redis 6.0+)
lazyfree-lazy-user-del yes

# Async FLUSHALL and FLUSHDB
lazyfree-lazy-user-flush yes

# Number of threads for lazy freeing (Redis 6.0+)
# Default is 1, increase for heavy deletion workloads
io-threads 4
io-threads-do-reads yes
```

```python
# Correct 5: Configure lazy freeing at runtime
def configure_lazy_free():
    """Enable lazy freeing options"""
    configs = [
        ("lazyfree-lazy-eviction", "yes"),
        ("lazyfree-lazy-expire", "yes"),
        ("lazyfree-lazy-server-del", "yes"),
        ("lazyfree-lazy-user-del", "yes"),
        ("lazyfree-lazy-user-flush", "yes"),
    ]

    for key, value in configs:
        try:
            r.config_set(key, value)
            print(f"Set {key} = {value}")
        except redis.ResponseError as e:
            print(f"Could not set {key}: {e}")

def check_lazy_free_config():
    """Check current lazy free settings"""
    settings = {}
    for key in [
        "lazyfree-lazy-eviction",
        "lazyfree-lazy-expire",
        "lazyfree-lazy-server-del",
        "lazyfree-lazy-user-del",
        "lazyfree-lazy-user-flush",
    ]:
        try:
            value = r.config_get(key)
            settings[key] = value.get(key, "unknown")
        except:
            settings[key] = "not supported"

    return settings
```

```python
# Correct 6: Handle large data structure cleanup
def cleanup_large_sorted_set(key, keep_count=1000):
    """
    Trim sorted set to keep only top N elements.
    Uses ZREMRANGEBYRANK which can be slow for large sets.
    Consider chunked approach for very large sets.
    """
    current_size = r.zcard(key)

    if current_size <= keep_count:
        return 0

    # Remove elements beyond keep_count (from the bottom)
    # ZREMRANGEBYRANK removes by index, 0 is lowest score
    removed = r.zremrangebyrank(key, 0, -(keep_count + 1))
    return removed

def cleanup_large_list(key, max_length=10000):
    """Keep only the most recent max_length items in a list"""
    r.ltrim(key, 0, max_length - 1)

def expire_instead_of_delete(key, expire_seconds=1):
    """
    Alternative to immediate delete: set short TTL.
    Key will be deleted asynchronously by Redis expiry mechanism.
    """
    r.expire(key, expire_seconds)
```

```javascript
// Node.js
const Redis = require('ioredis');
const redis = new Redis();

// Use UNLINK for large keys
async function deleteKeySafe(key) {
    await redis.unlink(key);
}

// Batch delete with UNLINK
async function clearCacheSafe(pattern) {
    const stream = redis.scanStream({ match: pattern, count: 100 });
    const pipeline = redis.pipeline();
    let count = 0;

    for await (const keys of stream) {
        for (const key of keys) {
            pipeline.unlink(key);
            count++;

            if (count % 1000 === 0) {
                await pipeline.exec();
                pipeline = redis.pipeline();
            }
        }
    }

    await pipeline.exec();
    return count;
}

// Async flush
await redis.flushdb('ASYNC');
```

Reference: [Redis Lazy Freeing](https://redis.io/docs/management/optimization/memory-optimization/#lazy-freeing)

---

## 6. Persistence

**Impact: MEDIUM**

### 6.1 Configure AOF Rewrite Properly

**Impact: MEDIUM** (prevents AOF from growing unbounded, manages disk usage)

## Configure AOF Rewrite Properly

Configure automatic AOF rewriting to prevent the AOF file from growing unbounded. Rewriting compacts the AOF by generating the minimal set of commands to recreate the current dataset.

**Why AOF Rewriting:**
- AOF grows with every write operation
- Old/overwritten data remains in file
- Rewrite creates minimal command set
- Reduces disk usage and restart time

**Rewrite Triggers:**
- Automatic: Based on size percentage growth
- Manual: `BGREWRITEAOF` command

**Incorrect (no or poor rewrite config):**

```bash
# Anti-pattern 1: No automatic rewrite
# redis.conf
appendonly yes
auto-aof-rewrite-percentage 0  # Disabled!
# AOF grows forever, fills disk

# Anti-pattern 2: Rewrite too aggressive
auto-aof-rewrite-percentage 10
auto-aof-rewrite-min-size 1mb
# Rewrites constantly, causes overhead

# Anti-pattern 3: Never rewriting manually
# File grows to 100GB, restart takes hours
```

**Correct (proper rewrite configuration):**

```bash
# Correct 1: Recommended automatic rewrite settings
# redis.conf
appendonly yes
appendfsync everysec

# Rewrite when AOF is 100% larger than after last rewrite
auto-aof-rewrite-percentage 100

# Don't rewrite unless AOF is at least 64MB
auto-aof-rewrite-min-size 64mb

# Use RDB preamble for faster loading (Redis 4.0+)
aof-use-rdb-preamble yes

# Don't fsync during rewrite (faster, slightly less safe)
no-appendfsync-on-rewrite no  # 'yes' for better performance

# Truncate incomplete AOF on load rather than error
aof-load-truncated yes
```

```python
import redis
r = redis.Redis()

# Monitor AOF size and rewrite status
def check_aof_status():
    """Check AOF file status"""
    info = r.info("persistence")

    if not info.get("aof_enabled"):
        return {"enabled": False}

    current_size = info.get("aof_current_size", 0)
    base_size = info.get("aof_base_size", 0)

    # Calculate growth percentage
    if base_size > 0:
        growth_pct = ((current_size - base_size) / base_size) * 100
    else:
        growth_pct = 0

    return {
        "enabled": True,
        "current_size_mb": current_size / 1024 / 1024,
        "base_size_mb": base_size / 1024 / 1024,
        "growth_percentage": growth_pct,
        "rewrite_in_progress": info.get("aof_rewrite_in_progress", 0) == 1,
        "rewrite_scheduled": info.get("aof_rewrite_scheduled", 0) == 1,
        "last_rewrite_time_sec": info.get("aof_last_rewrite_time_sec", -1),
    }

# Trigger manual rewrite
def trigger_aof_rewrite(wait=True):
    """Trigger background AOF rewrite"""
    info = r.info("persistence")
    if info.get("aof_rewrite_in_progress"):
        print("Rewrite already in progress")
        return False

    print("Triggering BGREWRITEAOF...")
    r.bgrewriteaof()

    if wait:
        while True:
            info = r.info("persistence")
            if not info.get("aof_rewrite_in_progress"):
                break
            time.sleep(1)
            print(".", end="", flush=True)

        print("\nRewrite complete")
        return info.get("aof_last_bgrewrite_status") == "ok"

    return True

# Alert on large AOF growth
def alert_on_aof_growth(threshold_pct=150):
    """Alert if AOF has grown significantly since last rewrite"""
    status = check_aof_status()

    if not status.get("enabled"):
        return {"alert": False, "reason": "AOF not enabled"}

    if status["growth_percentage"] > threshold_pct:
        return {
            "alert": True,
            "message": f"AOF grown {status['growth_percentage']:.0f}% since last rewrite",
            "current_size_mb": status["current_size_mb"],
            "base_size_mb": status["base_size_mb"],
            "recommendation": "Consider manual BGREWRITEAOF or check auto-rewrite settings"
        }

    return {"alert": False}
```

```python
# Schedule rewrite during low-traffic periods
import schedule
import time

def maintenance_rewrite():
    """Perform AOF rewrite during maintenance window"""
    status = check_aof_status()

    # Only rewrite if significant growth
    if status.get("growth_percentage", 0) > 50:
        print(f"AOF growth: {status['growth_percentage']:.0f}%, triggering rewrite")
        trigger_aof_rewrite(wait=True)
    else:
        print(f"AOF growth: {status['growth_percentage']:.0f}%, skipping rewrite")

# Schedule for 3 AM daily
schedule.every().day.at("03:00").do(maintenance_rewrite)

# Or run manually during maintenance
# trigger_aof_rewrite(wait=True)
```

```bash
# Check AOF rewrite settings at runtime
redis-cli CONFIG GET auto-aof-rewrite-*

# Modify rewrite threshold
redis-cli CONFIG SET auto-aof-rewrite-percentage 100
redis-cli CONFIG SET auto-aof-rewrite-min-size 67108864  # 64MB

# Manual rewrite
redis-cli BGREWRITEAOF

# Monitor rewrite progress
redis-cli INFO persistence | grep aof_rewrite
```

```python
# Correct: Handle no-appendfsync-on-rewrite trade-off
def configure_aof_rewrite_safety(prioritize_performance=False):
    """
    Configure AOF rewrite behavior.

    no-appendfsync-on-rewrite:
    - 'yes': Don't fsync during rewrite (faster, may lose up to 30s on crash)
    - 'no': Continue fsync during rewrite (safer, may cause latency)
    """
    if prioritize_performance:
        # Faster rewrites, but may lose data if crash during rewrite
        r.config_set("no-appendfsync-on-rewrite", "yes")
        print("Set no-appendfsync-on-rewrite=yes (faster, less safe)")
    else:
        # Safer, but may have latency spikes during rewrite
        r.config_set("no-appendfsync-on-rewrite", "no")
        print("Set no-appendfsync-on-rewrite=no (safer, may have latency)")

# Verify AOF integrity
def verify_aof():
    """Check AOF file for corruption"""
    import subprocess

    config = r.config_get("dir")
    aof_dir = config.get("dir", "/var/lib/redis")

    # Redis 7+ uses appendonlydir
    aof_path = os.path.join(aof_dir, "appendonlydir")
    if not os.path.exists(aof_path):
        aof_path = os.path.join(aof_dir, "appendonly.aof")

    result = subprocess.run(
        ["redis-check-aof", "--fix", aof_path],
        capture_output=True,
        text=True
    )

    return result.returncode == 0, result.stdout
```

Reference: [Redis AOF Rewrite](https://redis.io/docs/management/persistence/#log-rewriting)

### 6.2 Configure Appropriate fsync Policy

**Impact: HIGH** (balances durability vs write performance)

## Configure Appropriate fsync Policy

Choose the right `appendfsync` policy for AOF based on your durability requirements. The fsync policy determines when data is actually written to disk, affecting both data safety and performance.

**fsync Policies:**
| Policy | Behavior | Data Loss Risk | Performance |
|--------|----------|----------------|-------------|
| `always` | fsync after every write | None | Slowest (~50% impact) |
| `everysec` | fsync every second | Up to 1 second | Good (recommended) |
| `no` | OS decides when to flush | Seconds to minutes | Fastest |

**Incorrect (mismatched policy and requirements):**

```bash
# Anti-pattern 1: 'always' for non-critical cache
appendonly yes
appendfsync always  # Unnecessary for cache, kills performance

# Anti-pattern 2: 'no' for important data
appendonly yes
appendfsync no  # Could lose significant data on crash
# OS might buffer for 30+ seconds

# Anti-pattern 3: Enabling AOF without understanding trade-offs
appendonly yes
# Missing appendfsync directive - defaults to 'everysec' but not explicit
```

**Correct (policy matches requirements):**

```bash
# Correct 1: Financial/transactional data - maximum durability
# redis.conf
appendonly yes
appendfsync always
# Every write is immediately durable
# Accept ~50% write performance reduction

# Correct 2: General application data - balanced (RECOMMENDED)
# redis.conf
appendonly yes
appendfsync everysec
# At most 1 second of data loss
# Minimal performance impact

# Correct 3: Session store - performance priority
# Sessions can be regenerated, prioritize speed
# redis.conf
appendonly yes
appendfsync no
# Fastest AOF writes, OS handles flushing
# OR: Just use RDB snapshots

# Correct 4: Hybrid - RDB for restarts, AOF for durability
# redis.conf
save 900 1
save 300 10
save 60 10000

appendonly yes
appendfsync everysec
aof-use-rdb-preamble yes  # Faster AOF loading
```

```python
import redis
r = redis.Redis()

# Monitor AOF health
def check_aof_health():
    """Check AOF persistence health"""
    info = r.info("persistence")

    if not info.get("aof_enabled"):
        return {"enabled": False}

    return {
        "enabled": True,
        "current_size_mb": info.get("aof_current_size", 0) / 1024 / 1024,
        "base_size_mb": info.get("aof_base_size", 0) / 1024 / 1024,
        "pending_rewrite": info.get("aof_rewrite_scheduled", 0) == 1,
        "rewrite_in_progress": info.get("aof_rewrite_in_progress", 0) == 1,
        "last_rewrite_time_sec": info.get("aof_last_rewrite_time_sec", -1),
        "last_write_status": info.get("aof_last_write_status", "unknown"),
        "buffer_size": info.get("aof_buffer_length", 0),
    }

# Change fsync policy at runtime (use with caution)
def set_fsync_policy(policy):
    """
    Change AOF fsync policy.
    Valid values: 'always', 'everysec', 'no'
    """
    if policy not in ['always', 'everysec', 'no']:
        raise ValueError(f"Invalid policy: {policy}")

    r.config_set("appendfsync", policy)
    return r.config_get("appendfsync")

# Temporarily relax fsync during bulk operations
def bulk_import_with_relaxed_fsync(import_func):
    """
    Temporarily use 'no' fsync during bulk import.
    WARNING: Data may be lost if Redis crashes during import.
    """
    original_policy = r.config_get("appendfsync").get("appendfsync")

    try:
        # Relax fsync for bulk import
        r.config_set("appendfsync", "no")

        # Perform bulk import
        import_func()

        # Force AOF rewrite to persist everything
        r.bgrewriteaof()

    finally:
        # Restore original policy
        r.config_set("appendfsync", original_policy)
```

```bash
# Monitor AOF during operation
redis-cli INFO persistence | grep aof

# Example output:
# aof_enabled:1
# aof_rewrite_in_progress:0
# aof_rewrite_scheduled:0
# aof_last_rewrite_time_sec:2
# aof_current_rewrite_time_sec:-1
# aof_last_bgrewrite_status:ok
# aof_last_write_status:ok
# aof_current_size:1234567
# aof_base_size:1000000
# aof_pending_rewrite:0
# aof_buffer_length:0
```

```python
# Performance benchmarking different fsync policies
def benchmark_fsync_policies():
    """
    Benchmark write performance with different fsync policies.
    Run on test instance only!
    """
    import time
    results = {}

    for policy in ['always', 'everysec', 'no']:
        r.config_set("appendfsync", policy)
        time.sleep(0.1)  # Let setting take effect

        # Benchmark
        start = time.time()
        pipe = r.pipeline()
        for i in range(10000):
            pipe.set(f"bench:{i}", f"value{i}")
        pipe.execute()
        elapsed = time.time() - start

        results[policy] = {
            "writes": 10000,
            "time_sec": elapsed,
            "writes_per_sec": 10000 / elapsed
        }

        # Cleanup
        for i in range(10000):
            r.delete(f"bench:{i}")

    return results

# Typical results:
# 'always': ~5,000 writes/sec (slowest)
# 'everysec': ~50,000 writes/sec (good balance)
# 'no': ~70,000 writes/sec (fastest)
```

Reference: [Redis AOF Configuration](https://redis.io/docs/management/persistence/#append-only-file)

### 6.3 Regularly Test Backup Recovery

**Impact: HIGH** (untested backups are not backups)

## Regularly Test Backup Recovery

Regularly test restoring from backups. Untested backups are not backups - you won't know if they work until you need them. Automate recovery testing to verify backup integrity and document restoration procedures.

**What to Test:**
- RDB file loads correctly
- AOF file replays correctly
- Data integrity after restore
- Recovery time (RTO) meets requirements
- Documented procedure is accurate

**Incorrect (no recovery testing):**

```bash
# Anti-pattern 1: Assuming backups work
# "We run BGSAVE every hour, we're safe"
# But never tested if those backups actually restore

# Anti-pattern 2: Testing only once
# "We tested recovery during initial setup"
# Configuration changes, data grows, backups may no longer work

# Anti-pattern 3: No documented procedure
# Only one person knows how to restore
# They're on vacation when disaster strikes
```

**Correct (regular recovery testing):**

```python
import redis
import subprocess
import tempfile
import shutil
import os
import time

# Correct 1: Automated backup verification
def verify_rdb_backup(backup_path):
    """
    Verify RDB backup can be loaded by starting test Redis instance.
    """
    # Use redis-check-rdb for quick validation
    result = subprocess.run(
        ["redis-check-rdb", backup_path],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return {
            "valid": False,
            "error": result.stderr,
            "check": "redis-check-rdb"
        }

    # For thorough testing, actually load the backup
    return load_and_verify_backup(backup_path)

def load_and_verify_backup(backup_path):
    """
    Load backup in isolated Redis instance and verify.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        # Copy backup to temp directory
        shutil.copy(backup_path, os.path.join(tmpdir, "dump.rdb"))

        # Start isolated Redis instance
        port = 16379  # Different port to avoid conflicts
        process = subprocess.Popen([
            "redis-server",
            "--port", str(port),
            "--dir", tmpdir,
            "--dbfilename", "dump.rdb",
            "--appendonly", "no",
            "--daemonize", "no"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            time.sleep(2)  # Wait for startup

            # Connect and verify
            test_redis = redis.Redis(port=port)

            # Check basic connectivity
            test_redis.ping()

            # Get key count
            key_count = test_redis.dbsize()

            # Sample some keys to verify data
            sample_keys = list(test_redis.scan_iter(count=10))[:10]
            samples = []
            for key in sample_keys:
                key_type = test_redis.type(key).decode()
                samples.append({"key": key.decode(), "type": key_type})

            return {
                "valid": True,
                "key_count": key_count,
                "sample_keys": samples,
                "check": "full_load_test"
            }

        finally:
            process.terminate()
            process.wait()

# Correct 2: Scheduled recovery test
def scheduled_recovery_test(backup_dir="/backups/redis"):
    """
    Automated recovery test for cron/scheduler.
    """
    # Find latest backup
    backups = sorted([
        f for f in os.listdir(backup_dir)
        if f.endswith('.rdb')
    ], reverse=True)

    if not backups:
        return {"success": False, "error": "No backups found"}

    latest = os.path.join(backup_dir, backups[0])
    result = verify_rdb_backup(latest)

    # Log results
    log_entry = {
        "timestamp": time.time(),
        "backup_file": backups[0],
        "verification_result": result
    }

    # Alert on failure
    if not result.get("valid"):
        send_alert(f"Backup verification failed: {result}")

    return log_entry
```

```bash
#!/bin/bash
# Correct 3: Recovery test script

set -e

BACKUP_DIR="/backups/redis"
TEST_PORT=16379
LOG_FILE="/var/log/redis-recovery-test.log"

echo "$(date): Starting recovery test" >> $LOG_FILE

# Find latest backup
LATEST_BACKUP=$(ls -t ${BACKUP_DIR}/*.rdb 2>/dev/null | head -1)

if [ -z "$LATEST_BACKUP" ]; then
    echo "$(date): ERROR - No backups found" >> $LOG_FILE
    exit 1
fi

echo "$(date): Testing backup: $LATEST_BACKUP" >> $LOG_FILE

# Validate with redis-check-rdb
if ! redis-check-rdb "$LATEST_BACKUP" >> $LOG_FILE 2>&1; then
    echo "$(date): ERROR - Backup failed validation" >> $LOG_FILE
    # Send alert
    exit 1
fi

# Create temp directory
TEMP_DIR=$(mktemp -d)
cp "$LATEST_BACKUP" "$TEMP_DIR/dump.rdb"

# Start test instance
redis-server --port $TEST_PORT --dir "$TEMP_DIR" --daemonize yes

sleep 3

# Verify
KEY_COUNT=$(redis-cli -p $TEST_PORT DBSIZE | grep -oP '\d+')
PING=$(redis-cli -p $TEST_PORT PING)

# Shutdown test instance
redis-cli -p $TEST_PORT SHUTDOWN NOSAVE 2>/dev/null || true

# Cleanup
rm -rf "$TEMP_DIR"

if [ "$PING" == "PONG" ] && [ "$KEY_COUNT" -gt 0 ]; then
    echo "$(date): SUCCESS - Backup verified, $KEY_COUNT keys" >> $LOG_FILE
    exit 0
else
    echo "$(date): ERROR - Verification failed" >> $LOG_FILE
    exit 1
fi
```

```python
# Correct 4: Document and automate the full procedure
RECOVERY_PROCEDURE = """
# Redis Disaster Recovery Procedure

## Prerequisites
- Access to backup storage (S3/NFS/local)
- Redis installed on target server
- Network access to application servers

## Recovery Steps

### 1. Stop Current Redis (if running)
```bash
redis-cli SHUTDOWN SAVE  # or NOSAVE if corrupted
```

### 2. Backup Current Data (if any)
```bash
mv /var/lib/redis/dump.rdb /var/lib/redis/dump.rdb.corrupted
mv /var/lib/redis/appendonlydir /var/lib/redis/appendonlydir.corrupted
```

### 3. Download Backup
```bash
# From S3
aws s3 cp s3://bucket/redis/dump_YYYYMMDD.rdb /var/lib/redis/dump.rdb

# Or from NFS
cp /backups/redis/dump_YYYYMMDD.rdb /var/lib/redis/dump.rdb
```

### 4. Set Permissions
```bash
chown redis:redis /var/lib/redis/dump.rdb
chmod 660 /var/lib/redis/dump.rdb
```

### 5. Start Redis
```bash
systemctl start redis
# or
redis-server /etc/redis/redis.conf
```

### 6. Verify Recovery
```bash
redis-cli PING  # Should return PONG
redis-cli DBSIZE  # Check key count
redis-cli INFO persistence  # Verify persistence status
```

### 7. Verify Application
- Test application connectivity
- Check critical data exists
- Monitor for errors

## Rollback
If recovery fails, restore from older backup or contact support.

## Contacts
- Primary: ops-team@company.com
- Escalation: infrastructure@company.com
"""

def print_recovery_procedure():
    print(RECOVERY_PROCEDURE)

# Correct 5: Measure Recovery Time
def measure_recovery_time(backup_path, target_port=16379):
    """Measure how long recovery takes (RTO)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        shutil.copy(backup_path, os.path.join(tmpdir, "dump.rdb"))

        start_time = time.time()

        process = subprocess.Popen([
            "redis-server",
            "--port", str(target_port),
            "--dir", tmpdir,
            "--daemonize", "no"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        try:
            # Wait for Redis to be ready
            test_redis = redis.Redis(port=target_port)
            while True:
                try:
                    if test_redis.ping():
                        break
                except:
                    pass
                time.sleep(0.1)

            recovery_time = time.time() - start_time
            key_count = test_redis.dbsize()

            return {
                "recovery_time_seconds": recovery_time,
                "key_count": key_count,
                "backup_size_mb": os.path.getsize(backup_path) / 1024 / 1024
            }

        finally:
            process.terminate()
            process.wait()
```

Reference: [Redis Backup and Restore](https://redis.io/docs/management/persistence/)

### 6.4 Understand RDB vs AOF Persistence

**Impact: CRITICAL** (wrong choice can cause data loss or performance issues)

## Understand RDB vs AOF Persistence

Choose the right persistence strategy based on your durability requirements and performance constraints. RDB and AOF have different trade-offs, and you can use both together.

**RDB (Redis Database Backup):**
- Point-in-time snapshots
- Compact single-file backups
- Faster restarts
- Can lose data since last snapshot
- Good for: Backups, disaster recovery, replication

**AOF (Append Only File):**
- Logs every write operation
- More durable (configurable fsync)
- Larger files, slower restarts
- Can lose data based on fsync policy
- Good for: Durability-critical applications

**Comparison:**
| Aspect | RDB | AOF |
|--------|-----|-----|
| Durability | Minutes of data loss | Seconds/none |
| File size | Compact | Larger |
| Restart speed | Fast | Slower |
| Write performance | Periodic impact | Continuous (small) |
| Best for | Backups | Durability |

**Incorrect (misunderstanding persistence):**

```bash
# Anti-pattern 1: No persistence for production data
# redis.conf
save ""  # RDB disabled
appendonly no  # AOF disabled
# All data lost on restart!

# Anti-pattern 2: AOF with no fsync (cache behavior)
appendonly yes
appendfsync no  # OS decides when to flush - can lose seconds of data
# Might as well use RDB if durability doesn't matter

# Anti-pattern 3: RDB only for critical data
save 900 1     # Save every 15 min if 1 key changed
save 300 10    # Save every 5 min if 10 keys changed
save 60 10000  # Save every 60s if 10000 keys changed
# With heavy writes, might lose up to 15 minutes of data!
```

**Correct (choose based on requirements):**

```bash
# Correct 1: Cache only (no persistence needed)
# Data can be regenerated, performance is priority
# redis.conf
save ""
appendonly no

# Correct 2: Moderate durability (RDB + AOF everysec)
# Balance of durability and performance
# redis.conf
save 900 1
save 300 10
save 60 10000

appendonly yes
appendfsync everysec  # Lose at most 1 second of data
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# Correct 3: Maximum durability (AOF always)
# Critical financial/transactional data
# redis.conf
appendonly yes
appendfsync always  # Fsync after every write - slowest but safest
# Note: Significant performance impact

# Correct 4: Recommended production setup
# RDB for backups + AOF for durability
# redis.conf
save 900 1
save 300 10
save 60 10000
rdbcompression yes
rdbchecksum yes

appendonly yes
appendfsync everysec
no-appendfsync-on-rewrite no  # Safer, but may impact latency during rewrite
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
aof-use-rdb-preamble yes  # Hybrid: RDB for fast load + AOF for recent ops
```

```python
import redis
r = redis.Redis()

# Check current persistence configuration
def check_persistence_config():
    """Get current persistence settings"""
    config = {}

    # RDB settings
    rdb_save = r.config_get("save")
    config["rdb"] = {
        "save_rules": rdb_save.get("save", ""),
        "compression": r.config_get("rdbcompression").get("rdbcompression"),
        "checksum": r.config_get("rdbchecksum").get("rdbchecksum"),
    }

    # AOF settings
    config["aof"] = {
        "enabled": r.config_get("appendonly").get("appendonly"),
        "fsync_policy": r.config_get("appendfsync").get("appendfsync"),
        "rewrite_percentage": r.config_get("auto-aof-rewrite-percentage").get("auto-aof-rewrite-percentage"),
        "rewrite_min_size": r.config_get("auto-aof-rewrite-min-size").get("auto-aof-rewrite-min-size"),
    }

    # Persistence status
    info = r.info("persistence")
    config["status"] = {
        "rdb_last_save_time": info.get("rdb_last_save_time"),
        "rdb_last_bgsave_status": info.get("rdb_last_bgsave_status"),
        "aof_enabled": info.get("aof_enabled"),
        "aof_last_rewrite_time_sec": info.get("aof_last_rewrite_time_sec"),
        "aof_current_size": info.get("aof_current_size"),
    }

    return config

# Verify persistence is working
def verify_persistence_health():
    """Check if persistence is healthy"""
    info = r.info("persistence")
    issues = []

    # Check RDB
    if info.get("rdb_last_bgsave_status") != "ok":
        issues.append(f"RDB save failed: {info.get('rdb_last_bgsave_status')}")

    rdb_age = time.time() - info.get("rdb_last_save_time", 0)
    if rdb_age > 3600:  # > 1 hour
        issues.append(f"RDB snapshot is {rdb_age/3600:.1f} hours old")

    # Check AOF
    if info.get("aof_enabled"):
        if info.get("aof_last_write_status") != "ok":
            issues.append(f"AOF write failed: {info.get('aof_last_write_status')}")

        if info.get("aof_rewrite_in_progress"):
            issues.append("AOF rewrite in progress")

    return {"healthy": len(issues) == 0, "issues": issues}
```

```python
# Decision guide for persistence
def recommend_persistence(
    is_cache_only: bool,
    max_acceptable_data_loss_seconds: int,
    write_throughput: str,  # "low", "medium", "high"
    restart_time_critical: bool
):
    """Recommend persistence configuration"""

    if is_cache_only:
        return {
            "recommendation": "No persistence",
            "config": {"save": "", "appendonly": "no"},
            "rationale": "Data can be regenerated, no persistence needed"
        }

    if max_acceptable_data_loss_seconds == 0:
        return {
            "recommendation": "AOF with appendfsync always",
            "config": {
                "appendonly": "yes",
                "appendfsync": "always",
                "save": "900 1 300 10 60 10000"  # Keep RDB for backups
            },
            "rationale": "Zero data loss required. Note: ~50% write performance impact",
            "warning": "High write throughput may be impacted significantly"
        }

    if max_acceptable_data_loss_seconds <= 1:
        return {
            "recommendation": "AOF with appendfsync everysec",
            "config": {
                "appendonly": "yes",
                "appendfsync": "everysec",
                "save": "900 1 300 10 60 10000",
                "aof-use-rdb-preamble": "yes"
            },
            "rationale": "At most 1 second data loss, good performance"
        }

    # More tolerant of data loss
    return {
        "recommendation": "RDB snapshots",
        "config": {
            "save": "900 1 300 10 60 10000",
            "appendonly": "no"
        },
        "rationale": f"Acceptable data loss, RDB provides good backup"
    }
```

Reference: [Redis Persistence](https://redis.io/docs/management/persistence/)

### 6.5 Use RDB for Backups and Disaster Recovery

**Impact: HIGH** (enables fast restores and offsite backups)

## Use RDB for Backups and Disaster Recovery

Use RDB snapshots for backups, replication seeding, and disaster recovery. RDB files are compact, easy to transfer, and enable fast restores. Always have a backup strategy even if using AOF for durability.

**RDB Benefits for Backups:**
- Single compact file
- Easy to copy/transfer
- Fast restore (faster than AOF replay)
- Perfect for point-in-time recovery
- Good for seeding replicas

**Incorrect (no backup strategy):**

```bash
# Anti-pattern 1: Relying only on AOF, no RDB
save ""  # No RDB snapshots
appendonly yes
# AOF is for durability, not ideal for backups:
# - Larger files
# - Slower to restore
# - Can't easily transfer

# Anti-pattern 2: No automated backup copies
save 60 1000
# RDB saved but:
# - Not copied offsite
# - No retention policy
# - No backup verification

# Anti-pattern 3: Backing up from primary during high load
# Causes fork() overhead on primary
```

**Correct (proper backup strategy):**

```bash
# Correct 1: Enable RDB with appropriate schedule
# redis.conf
save 900 1        # Every 15 min if >= 1 key changed
save 300 10       # Every 5 min if >= 10 keys changed
save 60 10000     # Every 1 min if >= 10000 keys changed

rdbcompression yes  # Compress with LZF
rdbchecksum yes     # Add CRC64 checksum for integrity
dbfilename dump.rdb
dir /var/lib/redis/

# Correct 2: Also enable AOF for durability
appendonly yes
appendfsync everysec
aof-use-rdb-preamble yes  # Hybrid: RDB + AOF tail
```

```python
import redis
import shutil
import os
from datetime import datetime

r = redis.Redis()

# Correct 3: Trigger manual backup
def create_backup():
    """Trigger RDB snapshot and wait for completion"""
    # Get last save time before triggering
    info = r.info("persistence")
    last_save = info["rdb_last_save_time"]

    # Trigger background save
    r.bgsave()

    # Wait for save to complete
    while True:
        info = r.info("persistence")
        if info["rdb_last_save_time"] > last_save:
            if info["rdb_last_bgsave_status"] == "ok":
                return True
            else:
                raise Exception(f"BGSAVE failed: {info['rdb_last_bgsave_status']}")
        time.sleep(0.5)

# Correct 4: Copy RDB to backup location
def backup_rdb(backup_dir="/backups/redis"):
    """Copy RDB file to backup location with timestamp"""
    # Get RDB file location
    config = r.config_get("dir", "dbfilename")
    rdb_dir = config.get("dir", "/var/lib/redis")
    rdb_file = config.get("dbfilename", "dump.rdb")
    source = os.path.join(rdb_dir, rdb_file)

    if not os.path.exists(source):
        raise FileNotFoundError(f"RDB file not found: {source}")

    # Create timestamped backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest = os.path.join(backup_dir, f"dump_{timestamp}.rdb")

    os.makedirs(backup_dir, exist_ok=True)
    shutil.copy2(source, dest)

    return dest

# Correct 5: Full backup procedure
def perform_backup(backup_dir="/backups/redis"):
    """Complete backup procedure"""
    print("1. Triggering BGSAVE...")
    create_backup()

    print("2. Copying RDB file...")
    backup_path = backup_rdb(backup_dir)

    print("3. Verifying backup...")
    # Verify file size is reasonable
    size = os.path.getsize(backup_path)
    info = r.info("persistence")
    expected_size = info.get("rdb_last_cow_size", 0)

    print(f"Backup complete: {backup_path} ({size / 1024 / 1024:.1f} MB)")
    return backup_path
```

```bash
#!/bin/bash
# Correct 6: Backup script for cron

REDIS_DIR="/var/lib/redis"
BACKUP_DIR="/backups/redis"
RETENTION_DAYS=7
S3_BUCKET="s3://mycompany-backups/redis"

# Trigger BGSAVE
redis-cli BGSAVE

# Wait for save to complete
while [ "$(redis-cli LASTSAVE)" == "$LAST_SAVE" ]; do
    sleep 1
done

# Copy RDB with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
cp ${REDIS_DIR}/dump.rdb ${BACKUP_DIR}/dump_${TIMESTAMP}.rdb

# Optional: Upload to S3
aws s3 cp ${BACKUP_DIR}/dump_${TIMESTAMP}.rdb ${S3_BUCKET}/

# Cleanup old backups
find ${BACKUP_DIR} -name "dump_*.rdb" -mtime +${RETENTION_DAYS} -delete

echo "Backup completed: dump_${TIMESTAMP}.rdb"
```

```python
# Correct 7: Backup from replica (recommended for production)
def backup_from_replica(replica_host, replica_port=6379):
    """
    Take backups from replica to avoid impacting primary.
    Fork for BGSAVE can cause latency spike on primary.
    """
    replica = redis.Redis(host=replica_host, port=replica_port)

    # Verify this is actually a replica
    info = replica.info("replication")
    if info["role"] != "slave":
        raise Exception("Target is not a replica!")

    # Check replication lag
    lag = info.get("master_repl_offset", 0) - info.get("slave_repl_offset", 0)
    if lag > 1000000:  # 1MB lag threshold
        print(f"Warning: Replica lag is {lag} bytes")

    # Trigger backup on replica
    replica.bgsave()

    # Wait and copy...
    print("Backup triggered on replica")
```

```python
# Correct 8: Verify backup integrity
def verify_backup(backup_path):
    """Verify RDB backup file integrity"""
    import subprocess

    # Use redis-check-rdb tool
    result = subprocess.run(
        ["redis-check-rdb", backup_path],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"Backup verified: {backup_path}")
        return True
    else:
        print(f"Backup corrupted: {result.stderr}")
        return False
```

Reference: [Redis RDB Persistence](https://redis.io/docs/management/persistence/#rdb-advantages)

---

## 7. Clustering & High Availability

**Impact: MEDIUM**

### 7.1 Handle MOVED and ASK Redirects

**Impact: MEDIUM-HIGH** (required for cluster operations and resharding)

## Handle MOVED and ASK Redirects

Understand and properly handle MOVED and ASK redirects in Redis Cluster. These redirects tell clients to contact a different node for a key. Most client libraries handle this automatically, but understanding them helps debugging and performance tuning.

**Redirect Types:**
- **MOVED**: Slot permanently moved to another node (update client's slot map)
- **ASK**: Slot being migrated, ask target node once (don't update map)

**When They Occur:**
- MOVED: After resharding completes, client's slot map is stale
- ASK: During active resharding, key being migrated

**Incorrect (not handling redirects):**

```python
import redis

# Anti-pattern 1: Using regular Redis client for cluster
r = redis.Redis(host='node1', port=6379)
r.get('key')  # Gets MOVED error, doesn't know how to handle

# Anti-pattern 2: Not refreshing slot map
# Client has stale slot information
# Gets MOVED errors repeatedly, poor performance

# Anti-pattern 3: Ignoring redirect errors
try:
    r.get('key')
except redis.ResponseError as e:
    pass  # Silently fails, data not retrieved
```

**Correct (proper redirect handling):**

```python
from redis.cluster import RedisCluster

# Correct 1: Use cluster-aware client (handles redirects automatically)
rc = RedisCluster(
    host='node1',
    port=6379,
    decode_responses=True,
    # Automatically handle MOVED/ASK
    skip_full_coverage_check=True,  # For clusters not covering all 16384 slots
)

# Operations just work - client handles redirects
rc.get('key')  # If MOVED, client updates slot map and retries
rc.set('key', 'value')  # Automatic redirect handling

# Correct 2: Monitor redirect frequency (indicates resharding or stale map)
def get_cluster_redirect_stats():
    """Check if there are many redirects (indicates issues)"""
    # Note: This varies by client library
    # redis-py-cluster tracks some stats internally
    nodes = rc.get_nodes()
    stats = []

    for node in nodes:
        try:
            info = rc.get_redis_connection(node).info('stats')
            stats.append({
                'node': f"{node.host}:{node.port}",
                'total_commands': info.get('total_commands_processed', 0),
            })
        except:
            pass

    return stats

# Correct 3: Force slot map refresh after known topology change
def refresh_cluster_slots():
    """Refresh the client's slot mapping"""
    # Most clients do this automatically on MOVED
    rc.cluster_slots()  # Fetches current slot mapping

# Correct 4: Handle resharding gracefully
def get_with_retry(key, max_retries=3):
    """Get with explicit redirect handling for debugging"""
    for attempt in range(max_retries):
        try:
            return rc.get(key)
        except redis.exceptions.ResponseError as e:
            error_msg = str(e)
            if 'MOVED' in error_msg:
                # Slot permanently moved - client should update mapping
                print(f"MOVED redirect (attempt {attempt + 1})")
                # redis-py-cluster handles this automatically
                continue
            elif 'ASK' in error_msg:
                # Slot being migrated - need to ASK target node
                print(f"ASK redirect during migration (attempt {attempt + 1})")
                continue
            elif 'CLUSTERDOWN' in error_msg:
                # Cluster is down or in failed state
                print("Cluster is down!")
                raise
            else:
                raise
    raise Exception(f"Failed after {max_retries} retries")
```

```python
# Correct 5: Manual redirect handling (for custom clients)
def handle_redirect_manually(command, *args):
    """
    Example of manual redirect handling.
    Most clients do this automatically.
    """
    import re

    try:
        # Try executing on current node
        return current_node.execute_command(command, *args)

    except redis.ResponseError as e:
        error = str(e)

        # Handle MOVED: -MOVED 3999 127.0.0.1:6381
        if error.startswith('MOVED'):
            match = re.match(r'MOVED (\d+) ([\w.]+):(\d+)', error)
            if match:
                slot, host, port = match.groups()
                # Update slot mapping
                update_slot_map(int(slot), host, int(port))
                # Retry on correct node
                target_node = get_node(host, int(port))
                return target_node.execute_command(command, *args)

        # Handle ASK: -ASK 3999 127.0.0.1:6381
        elif error.startswith('ASK'):
            match = re.match(r'ASK (\d+) ([\w.]+):(\d+)', error)
            if match:
                slot, host, port = match.groups()
                # Don't update slot map (migration in progress)
                target_node = get_node(host, int(port))
                # Must send ASKING before the command
                target_node.execute_command('ASKING')
                return target_node.execute_command(command, *args)

        raise
```

```javascript
// Node.js - ioredis handles redirects automatically
const Redis = require('ioredis');

const cluster = new Redis.Cluster([
    { host: 'node1', port: 6379 }
], {
    // Redirect handling options
    maxRedirections: 16,  // Max redirects before giving up
    retryDelayOnClusterDown: 100,  // Wait before retry when cluster down
    retryDelayOnFailover: 100,  // Wait during failover
    retryDelayOnTryAgain: 100,  // Wait on TRYAGAIN error

    // Refresh slot mapping
    slotsRefreshTimeout: 2000,
    slotsRefreshInterval: 5000,  // Periodic refresh
});

// Events for monitoring
cluster.on('ready', () => console.log('Cluster ready'));
cluster.on('node error', (err, node) => {
    console.log(`Node ${node.options.host}:${node.options.port} error:`, err);
});
cluster.on('refresh', () => console.log('Slot mapping refreshed'));

// Operations automatically follow redirects
await cluster.set('key', 'value');
const value = await cluster.get('key');
```

```python
# Correct 6: Monitor cluster health during resharding
def check_cluster_health():
    """Check if cluster is healthy or resharding"""
    try:
        cluster_info = rc.cluster_info()
        state = cluster_info.get('cluster_state')

        result = {
            'state': state,
            'healthy': state == 'ok',
            'slots_assigned': cluster_info.get('cluster_slots_assigned'),
            'slots_ok': cluster_info.get('cluster_slots_ok'),
            'slots_pfail': cluster_info.get('cluster_slots_pfail'),
            'slots_fail': cluster_info.get('cluster_slots_fail'),
            'known_nodes': cluster_info.get('cluster_known_nodes'),
        }

        # Check for migrating slots (resharding in progress)
        nodes = rc.get_nodes()
        migrating = 0
        importing = 0

        for node in nodes:
            try:
                node_info = rc.get_redis_connection(node).cluster_nodes()
                migrating += node_info.count('migrating')
                importing += node_info.count('importing')
            except:
                pass

        result['resharding_in_progress'] = migrating > 0 or importing > 0

        return result

    except Exception as e:
        return {'healthy': False, 'error': str(e)}
```

Reference: [Redis Cluster Redirections](https://redis.io/docs/reference/cluster-spec/#redirection-and-resharding)

### 7.2 Plan Cluster Resharding Carefully

**Impact: MEDIUM** (improper resharding can cause data loss or outages)

## Plan Cluster Resharding Carefully

Plan and execute cluster resharding carefully. Resharding moves hash slots between nodes and can impact performance during migration. Follow best practices to minimize impact and avoid data loss.

**When Resharding is Needed:**
- Adding nodes to scale out
- Removing nodes to scale in
- Rebalancing uneven data distribution
- Hardware replacement

**Resharding Impact:**
- Increased latency during slot migration
- ASK redirects during migration
- Memory usage spikes on source and target
- Network bandwidth consumption

**Incorrect (dangerous resharding practices):**

```bash
# Anti-pattern 1: Resharding without backup
redis-cli --cluster reshard node1:6379  # No backup first!

# Anti-pattern 2: Moving too many slots at once
redis-cli --cluster reshard node1:6379 \
    --cluster-from xxx --cluster-to yyy \
    --cluster-slots 8192  # Half the cluster at once!

# Anti-pattern 3: Resharding during peak traffic
# Running reshard during business hours

# Anti-pattern 4: Not monitoring during reshard
# No visibility into progress or issues

# Anti-pattern 5: Removing node before emptying
redis-cli --cluster del-node node1:6379 <node-id>
# Will fail or lose data if node still has slots
```

**Correct (safe resharding practices):**

```bash
# Correct 1: Pre-resharding checklist
# 1. Backup all nodes (RDB)
# 2. Check cluster health
# 3. Plan during low-traffic window
# 4. Notify stakeholders
# 5. Have rollback plan

# Check cluster health first
redis-cli --cluster check node1:6379

# Verify cluster state
redis-cli -c -h node1 -p 6379 CLUSTER INFO

# Correct 2: Add new node before resharding
# Add empty node to cluster
redis-cli --cluster add-node new-node:6379 existing-node:6379

# Verify node added
redis-cli --cluster check node1:6379

# Correct 3: Reshard in small batches
# Move 1000 slots at a time, not all at once
redis-cli --cluster reshard node1:6379 \
    --cluster-from <source-node-id> \
    --cluster-to <target-node-id> \
    --cluster-slots 1000 \
    --cluster-yes

# Correct 4: Use redis-cli --cluster rebalance for even distribution
redis-cli --cluster rebalance node1:6379 \
    --cluster-weight <node-id>=1 \
    --cluster-use-empty-masters
```

```python
from redis.cluster import RedisCluster
import time

rc = RedisCluster(host='node1', port=6379)

# Correct 5: Monitor during resharding
def monitor_resharding():
    """Monitor cluster during resharding operations"""
    while True:
        health = check_cluster_during_reshard()
        print(f"Cluster state: {health['state']}")
        print(f"Migrating slots: {health['migrating_slots']}")
        print(f"Importing slots: {health['importing_slots']}")

        if health['migrating_slots'] == 0 and health['importing_slots'] == 0:
            print("Resharding complete!")
            break

        time.sleep(5)

def check_cluster_during_reshard():
    """Check cluster status during resharding"""
    cluster_info = rc.cluster_info()
    nodes_info = rc.cluster_nodes()

    migrating = 0
    importing = 0

    # Count migrating/importing slots
    for node_line in nodes_info.split('\n'):
        migrating += node_line.count('[')
        if 'importing' in node_line.lower():
            importing += 1

    return {
        'state': cluster_info.get('cluster_state'),
        'migrating_slots': migrating,
        'importing_slots': importing,
        'cluster_size': cluster_info.get('cluster_size'),
        'known_nodes': cluster_info.get('cluster_known_nodes'),
    }

# Correct 6: Verify data integrity after resharding
def verify_cluster_after_reshard(sample_keys):
    """Verify data accessible after resharding"""
    issues = []

    for key in sample_keys:
        try:
            value = rc.get(key)
            if value is None:
                issues.append(f"Key {key} not found")
        except Exception as e:
            issues.append(f"Key {key} error: {e}")

    # Check slot coverage
    cluster_info = rc.cluster_info()
    if cluster_info.get('cluster_slots_ok') != 16384:
        issues.append(f"Not all slots covered: {cluster_info.get('cluster_slots_ok')}/16384")

    return {'valid': len(issues) == 0, 'issues': issues}
```

```python
# Correct 7: Safe node removal procedure
def safe_remove_node(rc, node_id):
    """Safely remove a node from cluster"""

    # Step 1: Check if node has slots
    nodes = rc.cluster_nodes()
    node_line = [l for l in nodes.split('\n') if node_id in l]

    if not node_line:
        print(f"Node {node_id} not found")
        return False

    # Check for slots
    if 'master' in node_line[0] and any(c.isdigit() for c in node_line[0].split('connected')[-1]):
        print(f"Node {node_id} still has slots - must reshard first!")
        return False

    # Step 2: Verify node has no slots
    slot_count = 0  # Parse slot ranges from node info
    if slot_count > 0:
        print(f"Node has {slot_count} slots - reshard first")
        return False

    # Step 3: Remove node
    print(f"Removing node {node_id}...")
    # redis-cli --cluster del-node <any-node>:6379 <node-id>

    return True

# Correct 8: Rolling upgrade procedure
def rolling_upgrade_plan(nodes):
    """Plan for rolling cluster upgrade"""
    plan = []

    for i, node in enumerate(nodes):
        step = {
            'order': i + 1,
            'node': node,
            'actions': [
                f"1. Verify cluster health",
                f"2. Take backup of {node}",
                f"3. If master, failover to replica first",
                f"4. Upgrade {node}",
                f"5. Restart {node}",
                f"6. Wait for node to rejoin cluster",
                f"7. Verify cluster health",
                f"8. Wait for replication to catch up (if replica)",
            ]
        }
        plan.append(step)

    return plan
```

```bash
# Correct 9: Complete resharding procedure

# Pre-flight checks
echo "=== Pre-flight Checks ==="
redis-cli --cluster check node1:6379
redis-cli -c -h node1 CLUSTER INFO | grep cluster_state

# Backup
echo "=== Creating Backups ==="
for node in node1 node2 node3; do
    redis-cli -h $node BGSAVE
done
sleep 10

# Add new node
echo "=== Adding New Node ==="
redis-cli --cluster add-node new-node:6379 node1:6379

# Reshard in batches
echo "=== Resharding (batch 1/4) ==="
redis-cli --cluster reshard node1:6379 \
    --cluster-from all \
    --cluster-to <new-node-id> \
    --cluster-slots 1000 \
    --cluster-yes

# Check between batches
redis-cli --cluster check node1:6379

# Continue with more batches...

# Final verification
echo "=== Final Verification ==="
redis-cli --cluster check node1:6379
redis-cli -c -h node1 CLUSTER INFO
```

Reference: [Redis Cluster Administration](https://redis.io/docs/management/scaling/)

### 7.3 Understand Redis Cluster Hash Slots

**Impact: HIGH** (essential for multi-key operations and scaling)

## Understand Redis Cluster Hash Slots

Understand how Redis Cluster distributes data across nodes using hash slots. Keys are mapped to one of 16,384 slots, and each node owns a subset. This affects which operations are possible and how to design your key strategy.

**How It Works:**
- 16,384 hash slots total
- Key's slot = CRC16(key) mod 16384
- Each master owns a range of slots
- Data moves by reassigning slots between nodes

**Key Design Impact:**
- Multi-key operations require keys on same node
- Use hash tags `{tag}` to force keys to same slot
- Cross-slot operations fail with CROSSSLOT error

**Incorrect (not understanding slot distribution):**

```python
import redis
from redis.cluster import RedisCluster

rc = RedisCluster(host='node1', port=6379)

# Anti-pattern 1: Multi-key operation without hash tags
rc.mget(['user:1', 'user:2', 'user:3'])  # CROSSSLOT error likely!
# Keys hash to different slots

# Anti-pattern 2: Transaction across slots
pipe = rc.pipeline()
pipe.set('order:123', 'data')
pipe.set('inventory:456', 'data')
pipe.execute()  # CROSSSLOT error if different slots!

# Anti-pattern 3: Lua script with keys on different slots
rc.eval("return redis.call('GET', KEYS[1]) + redis.call('GET', KEYS[2])",
        2, 'counter:a', 'counter:b')  # CROSSSLOT error!

# Anti-pattern 4: SCAN expecting all keys
# SCAN only returns keys on connected node
for key in rc.scan_iter(match='user:*'):
    # Only sees subset of keys!
    pass
```

**Correct (proper cluster-aware design):**

```python
from redis.cluster import RedisCluster

rc = RedisCluster(
    host='node1',
    port=6379,
    decode_responses=True
)

# Correct 1: Use hash tags for related keys
# All keys with same {tag} go to same slot
rc.set('{user:123}:profile', 'profile_data')
rc.set('{user:123}:settings', 'settings_data')
rc.set('{user:123}:session', 'session_data')

# Now multi-key operations work!
rc.mget(['{user:123}:profile', '{user:123}:settings'])

# Correct 2: Transactions with hash tags
pipe = rc.pipeline()
pipe.hset('{order:abc}:details', mapping={'item': 'widget'})
pipe.sadd('{order:abc}:items', 'item1', 'item2')
pipe.execute()  # Works - same hash tag

# Correct 3: Design key patterns for cluster
# Pattern: {entity_type:id}:attribute
def user_keys(user_id):
    """Generate related keys with same hash tag"""
    base = f"{{user:{user_id}}}"
    return {
        'profile': f"{base}:profile",
        'settings': f"{base}:settings",
        'cart': f"{base}:cart",
        'sessions': f"{base}:sessions"
    }

keys = user_keys('123')
# {user:123}:profile, {user:123}:settings - all same slot!

# Correct 4: Check which slot a key uses
def get_key_slot(key):
    """Get the hash slot for a key"""
    # Redis Cluster command
    return rc.cluster_keyslot(key)

# Same hash tag = same slot
assert get_key_slot('{user:123}:a') == get_key_slot('{user:123}:b')

# Correct 5: SCAN across entire cluster
def scan_all_cluster(pattern):
    """Scan all nodes in cluster for keys matching pattern"""
    all_keys = set()

    # Get all master nodes
    nodes = rc.get_nodes()

    for node in nodes:
        if node.server_type == 'primary':  # Only masters have data
            node_client = rc.get_redis_connection(node)
            for key in node_client.scan_iter(match=pattern, count=100):
                all_keys.add(key)

    return all_keys

# Correct 6: Handle CROSSSLOT errors gracefully
def safe_multi_get(keys):
    """Get multiple keys, handling cross-slot case"""
    try:
        return rc.mget(keys)
    except redis.exceptions.ResponseError as e:
        if 'CROSSSLOT' in str(e):
            # Fallback: get keys individually
            return [rc.get(k) for k in keys]
        raise
```

```python
# Correct 7: Atomic operations across related keys
def transfer_inventory(from_warehouse, to_warehouse, item, quantity):
    """
    Transfer inventory between warehouses atomically.
    Uses hash tags to ensure same slot.
    """
    # Keys with same hash tag for atomicity
    from_key = f"{{inventory:{item}}}:{from_warehouse}"
    to_key = f"{{inventory:{item}}}:{to_warehouse}"

    # Lua script works because keys are on same slot
    script = """
    local from_qty = tonumber(redis.call('GET', KEYS[1]) or '0')
    local transfer = tonumber(ARGV[1])

    if from_qty >= transfer then
        redis.call('DECRBY', KEYS[1], transfer)
        redis.call('INCRBY', KEYS[2], transfer)
        return 1
    end
    return 0
    """

    return rc.eval(script, 2, from_key, to_key, quantity)

# Correct 8: Understand slot distribution for capacity planning
def get_cluster_slot_distribution():
    """Get slot distribution across nodes"""
    slots_info = rc.cluster_slots()
    distribution = []

    for slot_range in slots_info:
        start_slot, end_slot = slot_range[0], slot_range[1]
        master = slot_range[2]  # [host, port, node_id]

        distribution.append({
            'start': start_slot,
            'end': end_slot,
            'slots': end_slot - start_slot + 1,
            'master': f"{master[0]}:{master[1]}"
        })

    return distribution
```

```javascript
// Node.js - ioredis Cluster
const Redis = require('ioredis');

const cluster = new Redis.Cluster([
    { host: 'node1', port: 6379 },
    { host: 'node2', port: 6379 },
    { host: 'node3', port: 6379 },
]);

// Use hash tags for related keys
await cluster.set('{user:123}:profile', 'data');
await cluster.set('{user:123}:settings', 'data');

// Multi-key with hash tags
const values = await cluster.mget(
    '{user:123}:profile',
    '{user:123}:settings'
);

// Pipeline with hash tags
const results = await cluster.pipeline()
    .set('{order:abc}:status', 'pending')
    .set('{order:abc}:total', '99.99')
    .exec();
```

Reference: [Redis Cluster Specification](https://redis.io/docs/reference/cluster-spec/)

### 7.4 Offload Reads to Replicas

**Impact: MEDIUM** (reduces master load, improves read throughput)

## Offload Reads to Replicas

Configure reads from replicas to reduce load on masters and improve read throughput. By default, clients read from masters only. Enable replica reads for read-heavy workloads, understanding the eventual consistency trade-off.

**When to Use Replica Reads:**
- Read-heavy workloads (>80% reads)
- Acceptable eventual consistency (milliseconds lag)
- Need to scale read throughput
- Want to reduce master load

**Trade-offs:**
- Eventual consistency: Replicas may be slightly behind
- Stale reads possible during replication lag
- Failover can cause brief unavailability

**Incorrect (all reads from master):**

```python
from redis.cluster import RedisCluster

# Default: all reads go to master
rc = RedisCluster(host='node1', port=6379)

# High read load overwhelms masters
for i in range(100000):
    rc.get(f'key:{i}')  # All hitting masters!
```

```python
# Anti-pattern: Manual replica selection without proper handling
r = redis.Redis(host='replica-host', port=6379)
r.get('key')  # May fail during failover, no automatic discovery
```

**Correct (replica reads with proper configuration):**

```python
from redis.cluster import RedisCluster

# Correct 1: Enable replica reads in cluster
rc = RedisCluster(
    host='node1',
    port=6379,
    decode_responses=True,
    read_from_replicas=True,  # Enable replica reads
)

# Reads automatically distributed to replicas
value = rc.get('key')  # May hit replica

# Correct 2: With Sentinel - separate master/replica clients
from redis.sentinel import Sentinel

sentinel = Sentinel([
    ('sentinel1', 26379),
    ('sentinel2', 26379),
    ('sentinel3', 26379),
])

# Master for writes
master = sentinel.master_for('mymaster', socket_timeout=0.5)

# Replica for reads
replica = sentinel.slave_for('mymaster', socket_timeout=0.5)

def get(key, allow_stale=True):
    """Read with option to use replica"""
    if allow_stale:
        return replica.get(key)
    return master.get(key)

def set(key, value, **kwargs):
    """Writes always go to master"""
    return master.set(key, value, **kwargs)

# Correct 3: Read-your-writes pattern
class ConsistentRedisClient:
    """
    Client that ensures read-your-writes consistency.
    After a write, reads from master briefly.
    """
    def __init__(self, sentinel, master_name):
        self.master = sentinel.master_for(master_name)
        self.replica = sentinel.slave_for(master_name)
        self._recent_writes = {}  # key -> timestamp
        self._consistency_window = 0.1  # 100ms

    def set(self, key, value, **kwargs):
        result = self.master.set(key, value, **kwargs)
        self._recent_writes[key] = time.time()
        return result

    def get(self, key):
        # Check if we recently wrote this key
        write_time = self._recent_writes.get(key, 0)
        if time.time() - write_time < self._consistency_window:
            # Read from master to ensure we see our write
            return self.master.get(key)
        # Safe to read from replica
        return self.replica.get(key)
```

```python
# Correct 4: Monitor replication lag before enabling replica reads
def check_replication_lag(rc):
    """Check replication lag across cluster"""
    nodes = rc.get_nodes()
    lag_info = []

    for node in nodes:
        if node.server_type == 'primary':
            try:
                conn = rc.get_redis_connection(node)
                info = conn.info('replication')

                # Check each replica's lag
                for i in range(info.get('connected_slaves', 0)):
                    replica_info = info.get(f'slave{i}', '')
                    # Parse: ip=x.x.x.x,port=6379,state=online,offset=123,lag=0
                    if 'lag=' in replica_info:
                        lag = int(replica_info.split('lag=')[1].split(',')[0])
                        lag_info.append({
                            'master': f"{node.host}:{node.port}",
                            'replica': i,
                            'lag_seconds': lag
                        })
            except Exception as e:
                pass

    return lag_info

def is_replica_read_safe(max_lag_seconds=1):
    """Check if replica reads are safe (low lag)"""
    lags = check_replication_lag(rc)
    if not lags:
        return False  # No replicas

    max_lag = max(l['lag_seconds'] for l in lags)
    return max_lag <= max_lag_seconds
```

```javascript
// Node.js - ioredis replica reads
const Redis = require('ioredis');

// Cluster with replica reads
const cluster = new Redis.Cluster([
    { host: 'node1', port: 6379 }
], {
    scaleReads: 'slave',  // Read from replicas
    // Or: 'all' to read from both masters and replicas
});

// Reads distributed to replicas
const value = await cluster.get('key');

// Force read from master when needed
const freshValue = await cluster.get('key', (err, result, key, node) => {
    // This callback is called but doesn't help force master
});

// For guaranteed fresh reads, use a separate master-only client
const masterCluster = new Redis.Cluster([
    { host: 'node1', port: 6379 }
], {
    scaleReads: 'master',  // Only read from masters
});

// Sentinel with replica reads
const sentinelRedis = new Redis({
    sentinels: [
        { host: 'sentinel1', port: 26379 }
    ],
    name: 'mymaster',
    role: 'slave',  // Connect to replica
    preferredSlaves: [
        // Prefer specific replicas
        { ip: 'replica1', port: 6379, prio: 1 },
    ]
});
```

```python
# Correct 5: Replica reads with health checking
class HealthAwareReplicaClient:
    """
    Read from replicas only when they're healthy and caught up.
    """
    def __init__(self, sentinel, master_name, max_lag_seconds=1):
        self.sentinel = sentinel
        self.master_name = master_name
        self.max_lag = max_lag_seconds
        self._master = None
        self._replica = None
        self._replica_healthy = True
        self._last_health_check = 0

    @property
    def master(self):
        if not self._master:
            self._master = self.sentinel.master_for(self.master_name)
        return self._master

    @property
    def replica(self):
        if not self._replica:
            self._replica = self.sentinel.slave_for(self.master_name)
        return self._replica

    def _check_replica_health(self):
        """Check if replica is healthy (low lag)"""
        if time.time() - self._last_health_check < 5:  # Cache for 5s
            return self._replica_healthy

        try:
            info = self.master.info('replication')
            for i in range(info.get('connected_slaves', 0)):
                slave_info = info.get(f'slave{i}', '')
                if 'lag=' in slave_info:
                    lag = int(slave_info.split('lag=')[1].split(',')[0])
                    self._replica_healthy = lag <= self.max_lag
                    break
        except:
            self._replica_healthy = False

        self._last_health_check = time.time()
        return self._replica_healthy

    def get(self, key):
        """Read from replica if healthy, else master"""
        if self._check_replica_health():
            try:
                return self.replica.get(key)
            except redis.ConnectionError:
                self._replica_healthy = False
                return self.master.get(key)
        return self.master.get(key)
```

Reference: [Redis Replication](https://redis.io/docs/management/replication/)

### 7.5 Use Sentinel for High Availability

**Impact: HIGH** (automatic failover, prevents single point of failure)

## Use Sentinel for High Availability

Use Redis Sentinel for high availability when you don't need data sharding. Sentinel monitors Redis instances, performs automatic failover, and provides service discovery. It's simpler than Redis Cluster when all data fits on one machine.

**Sentinel vs Cluster:**
- **Sentinel**: HA without sharding, simpler, data fits on one node
- **Cluster**: HA with sharding, more complex, data exceeds one node

**Sentinel Provides:**
- Monitoring: Checks if master and replicas are working
- Notification: Alerts on failures
- Automatic failover: Promotes replica to master
- Service discovery: Clients query Sentinel for current master

**Incorrect (no HA or misconfigured):**

```bash
# Anti-pattern 1: Single Redis instance in production
# No Sentinel, no replicas
# If Redis crashes, complete outage

# Anti-pattern 2: Single Sentinel
sentinel monitor mymaster 127.0.0.1 6379 1
# Single Sentinel can't form quorum if it fails
# Need at least 3 Sentinels

# Anti-pattern 3: Sentinel quorum too low
sentinel monitor mymaster 127.0.0.1 6379 1  # quorum of 1
# Single Sentinel can trigger failover
# Risk of split-brain scenarios
```

```python
# Anti-pattern: Connecting directly to master without Sentinel
import redis
r = redis.Redis(host='redis-master', port=6379)  # Hardcoded master
# If master fails and Sentinel promotes replica, client still points to dead node
```

**Correct (proper Sentinel setup):**

```bash
# Correct 1: Minimum 3 Sentinel nodes for quorum
# sentinel1.conf
sentinel monitor mymaster 192.168.1.10 6379 2  # quorum of 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 60000
sentinel parallel-syncs mymaster 1

# Sentinel authentication (Redis 6.0+)
sentinel auth-pass mymaster your-redis-password
requirepass your-sentinel-password

# sentinel2.conf and sentinel3.conf - same configuration
```

```bash
# Redis master configuration
# redis-master.conf
port 6379
requirepass your-redis-password
masterauth your-redis-password  # For replica promotion

# Redis replica configuration
# redis-replica.conf
port 6379
replicaof 192.168.1.10 6379
masterauth your-redis-password
requirepass your-redis-password
replica-read-only yes
```

```python
import redis
from redis.sentinel import Sentinel

# Correct 2: Connect through Sentinel for automatic failover
sentinel = Sentinel(
    [
        ('sentinel1.example.com', 26379),
        ('sentinel2.example.com', 26379),
        ('sentinel3.example.com', 26379),
    ],
    socket_timeout=0.5,
    sentinel_kwargs={'password': 'sentinel-password'}  # If Sentinel has auth
)

# Get master connection (auto-discovers current master)
master = sentinel.master_for(
    'mymaster',
    socket_timeout=0.5,
    password='redis-password',
    retry_on_timeout=True
)

# Get replica for read operations
replica = sentinel.slave_for(
    'mymaster',
    socket_timeout=0.5,
    password='redis-password'
)

# Write to master
master.set('key', 'value')

# Read from replica (eventual consistency)
value = replica.get('key')

# Correct 3: Handle failover transparently
def get_with_failover(key):
    """Get value, automatically handling failover"""
    try:
        return master.get(key)
    except redis.ConnectionError:
        # Sentinel will automatically reconnect to new master
        # on next request
        raise

# Correct 4: Check Sentinel status
def check_sentinel_status():
    """Check Sentinel cluster health"""
    for sentinel_host, sentinel_port in sentinel.sentinels:
        try:
            s = redis.Redis(host=sentinel_host, port=sentinel_port)
            info = s.sentinel_master('mymaster')
            print(f"Sentinel {sentinel_host}: Master is {info['ip']}:{info['port']}")
        except Exception as e:
            print(f"Sentinel {sentinel_host} error: {e}")
```

```python
# Correct 5: Full application setup with Sentinel
class RedisSentinelClient:
    def __init__(self, sentinel_hosts, master_name, password=None, sentinel_password=None):
        self.sentinel = Sentinel(
            sentinel_hosts,
            socket_timeout=0.5,
            sentinel_kwargs={'password': sentinel_password} if sentinel_password else {}
        )
        self.master_name = master_name
        self.password = password

    @property
    def master(self):
        """Get master connection for writes"""
        return self.sentinel.master_for(
            self.master_name,
            socket_timeout=0.5,
            password=self.password,
            retry_on_timeout=True,
            max_connections=50
        )

    @property
    def replica(self):
        """Get replica connection for reads"""
        return self.sentinel.slave_for(
            self.master_name,
            socket_timeout=0.5,
            password=self.password,
            max_connections=50
        )

    def get(self, key, use_replica=True):
        """Read operation (from replica by default)"""
        client = self.replica if use_replica else self.master
        return client.get(key)

    def set(self, key, value, **kwargs):
        """Write operation (always to master)"""
        return self.master.set(key, value, **kwargs)

    def get_master_info(self):
        """Get current master info"""
        return self.sentinel.discover_master(self.master_name)

    def get_replica_info(self):
        """Get replica info"""
        return self.sentinel.discover_slaves(self.master_name)

# Usage
client = RedisSentinelClient(
    sentinel_hosts=[
        ('sentinel1', 26379),
        ('sentinel2', 26379),
        ('sentinel3', 26379),
    ],
    master_name='mymaster',
    password='redis-password',
    sentinel_password='sentinel-password'
)

client.set('user:123', 'data')
value = client.get('user:123')
```

```javascript
// Node.js with ioredis Sentinel support
const Redis = require('ioredis');

const redis = new Redis({
    sentinels: [
        { host: 'sentinel1', port: 26379 },
        { host: 'sentinel2', port: 26379 },
        { host: 'sentinel3', port: 26379 },
    ],
    name: 'mymaster',  // Master name
    password: 'redis-password',
    sentinelPassword: 'sentinel-password',
    enableReadyCheck: true,
    maxRetriesPerRequest: 3,
});

redis.on('ready', () => console.log('Connected to master'));
redis.on('+switch-master', () => console.log('Master switched'));
redis.on('error', (err) => console.error('Redis error:', err));

// Use normally - ioredis handles failover
await redis.set('key', 'value');
const value = await redis.get('key');
```

Reference: [Redis Sentinel](https://redis.io/docs/management/sentinel/)

---

## 8. Performance & Monitoring

**Impact: LOW-MEDIUM**

### 8.1 Use redis-benchmark Correctly

**Impact: MEDIUM** (enables proper performance testing and capacity planning)

## Use redis-benchmark Correctly

Use redis-benchmark properly for performance testing and capacity planning. Incorrect benchmarking leads to wrong conclusions. Understand what the tool measures and how to interpret results.

**What redis-benchmark Measures:**
- Raw Redis throughput (ops/sec)
- Latency distribution
- Best-case performance (pipelining, small payloads)

**What It Doesn't Measure:**
- Real application patterns
- Network across data centers
- Complex queries or Lua scripts
- Mixed workload patterns

**Incorrect (misleading benchmarks):**

```bash
# Anti-pattern 1: Default benchmark without understanding
redis-benchmark
# Uses pipelining, small payloads - not realistic

# Anti-pattern 2: Comparing different configurations unfairly
# Benchmark A: pipelining enabled, single key
# Benchmark B: no pipelining, random keys
# Results are not comparable!

# Anti-pattern 3: Not considering payload size
redis-benchmark -t set,get
# Uses tiny default payloads - not representative if your data is larger

# Anti-pattern 4: Testing on same machine as Redis
redis-benchmark -h localhost
# No network latency - unrealistic for production
```

**Correct (meaningful benchmarks):**

```bash
# Correct 1: Baseline benchmark with common options
redis-benchmark \
    -h redis.example.com \
    -p 6379 \
    -a password \
    -c 50 \         # 50 concurrent connections
    -n 100000 \     # 100K requests
    -d 256 \        # 256 byte payload
    --threads 4 \   # Multi-threaded (Redis 6.0+)
    -q              # Quiet mode (summary only)

# Correct 2: Realistic no-pipelining test
redis-benchmark \
    -h redis.example.com \
    -c 50 \
    -n 100000 \
    -P 1 \          # No pipelining (1 command at a time)
    -d 256 \
    -t set,get,lpush,lpop,hset

# Correct 3: Test specific commands
redis-benchmark -t set -n 100000 -d 1024  # SET with 1KB payload
redis-benchmark -t get -n 100000          # GET
redis-benchmark -t lpush,lpop -n 100000   # List operations
redis-benchmark -t hset -n 100000         # Hash operations
redis-benchmark -t sadd,spop -n 100000    # Set operations
redis-benchmark -t zadd,zrange -n 100000  # Sorted Set operations

# Correct 4: Test with realistic key patterns
redis-benchmark \
    -c 50 \
    -n 100000 \
    -r 100000 \     # Random keys from 100K key space
    -d 512 \
    -t set,get

# Correct 5: Compare with and without pipelining
echo "=== Without pipelining ==="
redis-benchmark -c 50 -n 100000 -P 1 -t set -q

echo "=== With pipelining (10 commands) ==="
redis-benchmark -c 50 -n 100000 -P 10 -t set -q

echo "=== With pipelining (50 commands) ==="
redis-benchmark -c 50 -n 100000 -P 50 -t set -q

# Correct 6: Latency focused test
redis-benchmark \
    -c 1 \          # Single connection
    -n 10000 \
    -P 1 \
    -d 256 \
    --csv           # CSV output for analysis
```

```python
# Correct 7: Application-specific benchmarks
import redis
import time
import statistics
import concurrent.futures

r = redis.Redis(host='redis.example.com', port=6379)

def benchmark_operation(name, func, iterations=10000):
    """Benchmark a specific operation"""
    latencies = []

    start_total = time.perf_counter()
    for i in range(iterations):
        start = time.perf_counter()
        func(i)
        latencies.append((time.perf_counter() - start) * 1000)
    total_time = time.perf_counter() - start_total

    latencies.sort()
    return {
        'name': name,
        'iterations': iterations,
        'total_time_sec': total_time,
        'ops_per_sec': iterations / total_time,
        'avg_ms': statistics.mean(latencies),
        'min_ms': min(latencies),
        'max_ms': max(latencies),
        'p50_ms': latencies[len(latencies) // 2],
        'p95_ms': latencies[int(len(latencies) * 0.95)],
        'p99_ms': latencies[int(len(latencies) * 0.99)],
    }

# Benchmark your actual access patterns
def run_application_benchmark():
    results = []

    # String cache pattern
    results.append(benchmark_operation(
        'cache_set',
        lambda i: r.setex(f'cache:{i}', 3600, 'x' * 256)
    ))

    results.append(benchmark_operation(
        'cache_get',
        lambda i: r.get(f'cache:{i % 1000}')  # Hot keys
    ))

    # Session pattern
    results.append(benchmark_operation(
        'session_hset',
        lambda i: r.hset(f'session:{i}', mapping={'user': 'john', 'token': 'xyz'})
    ))

    results.append(benchmark_operation(
        'session_hgetall',
        lambda i: r.hgetall(f'session:{i % 1000}')
    ))

    # Rate limiter pattern
    results.append(benchmark_operation(
        'rate_limit',
        lambda i: (r.incr(f'ratelimit:{i % 100}'),
                   r.expire(f'ratelimit:{i % 100}', 60))
    ))

    # Pipeline pattern
    def pipeline_ops(i):
        pipe = r.pipeline()
        for j in range(10):
            pipe.get(f'key:{i * 10 + j}')
        pipe.execute()

    results.append(benchmark_operation(
        'pipeline_10_gets',
        pipeline_ops,
        iterations=1000
    ))

    return results

# Correct 8: Concurrent benchmark
def concurrent_benchmark(operations, num_workers=10, per_worker=1000):
    """Run benchmark with concurrent workers"""
    def worker(worker_id):
        results = []
        for i in range(per_worker):
            start = time.perf_counter()
            operations(worker_id * per_worker + i)
            results.append(time.perf_counter() - start)
        return results

    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(worker, i) for i in range(num_workers)]
        all_latencies = []
        for f in concurrent.futures.as_completed(futures):
            all_latencies.extend(f.result())
    total_time = time.perf_counter() - start

    all_latencies = [l * 1000 for l in all_latencies]  # to ms
    all_latencies.sort()

    return {
        'total_ops': len(all_latencies),
        'total_time_sec': total_time,
        'ops_per_sec': len(all_latencies) / total_time,
        'avg_ms': statistics.mean(all_latencies),
        'p99_ms': all_latencies[int(len(all_latencies) * 0.99)],
    }

# Usage
result = concurrent_benchmark(
    lambda i: r.get(f'key:{i % 10000}'),
    num_workers=20,
    per_worker=5000
)
print(f"Concurrent throughput: {result['ops_per_sec']:.0f} ops/sec")
```

```bash
# Correct 9: Interpret benchmark results

# Sample output:
# SET: 125000.00 requests per second, p50=0.199 msec
#
# Interpretation:
# - 125K ops/sec is raw throughput
# - Real application will be lower due to:
#   - Application logic overhead
#   - No pipelining
#   - Larger payloads
#   - Network latency
#   - Connection pool overhead

# Good benchmark checklist:
# [ ] Test from a client machine, not Redis server
# [ ] Use realistic payload sizes
# [ ] Test with expected concurrency
# [ ] Compare with and without pipelining
# [ ] Test your actual command patterns
# [ ] Run multiple times for consistency
# [ ] Consider warm-up period
```

Reference: [redis-benchmark](https://redis.io/docs/management/optimization/benchmarks/)

### 8.2 Track and Diagnose Latency Issues

**Impact: HIGH** (identifies latency sources, enables optimization)

## Track and Diagnose Latency Issues

Monitor and diagnose Redis latency to ensure responsive applications. Latency can come from network, slow commands, persistence operations, or memory issues. Use Redis's built-in latency monitoring tools.

**Common Latency Sources:**
- Network round-trip time
- Slow commands (see SLOWLOG)
- Persistence (BGSAVE, AOF rewrites)
- Memory operations (swapping, fragmentation)
- Cluster redirections
- Client connection issues

**Latency Metrics:**
- P50, P99, P99.9 latencies
- Operations per second
- Command execution time
- Network latency

**Incorrect (ignoring latency issues):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: No latency monitoring
def get_data(key):
    return r.get(key)  # No visibility into latency
# Latency issues go undetected until users complain

# Anti-pattern 2: Only checking average latency
def check_latency_bad():
    latencies = [measure_one() for _ in range(10)]
    print(f"Average: {sum(latencies)/len(latencies)}ms")
# Misses P99 spikes that affect user experience

# Anti-pattern 3: Not using Redis latency tools
# Manually timing without SLOWLOG or LATENCY commands
```

**Correct (comprehensive latency monitoring):**

```python
import redis
import time
import statistics

r = redis.Redis()

# Correct 1: Measure round-trip latency
def measure_latency(samples=100):
    """Measure ping latency to Redis"""
    latencies = []

    for _ in range(samples):
        start = time.perf_counter()
        r.ping()
        elapsed = (time.perf_counter() - start) * 1000  # ms
        latencies.append(elapsed)

    latencies.sort()

    return {
        'samples': samples,
        'min_ms': min(latencies),
        'max_ms': max(latencies),
        'avg_ms': statistics.mean(latencies),
        'median_ms': statistics.median(latencies),
        'p95_ms': latencies[int(samples * 0.95)],
        'p99_ms': latencies[int(samples * 0.99)],
        'stddev_ms': statistics.stdev(latencies) if samples > 1 else 0
    }

# Correct 2: Use Redis latency monitoring
def enable_latency_monitor(threshold_ms=100):
    """Enable Redis latency monitor for events exceeding threshold"""
    # Set threshold in milliseconds
    r.config_set('latency-monitor-threshold', threshold_ms)

def get_latency_history():
    """Get latency history for all event types"""
    try:
        # LATENCY HISTORY returns [timestamp, latency_ms] pairs
        events = ['command', 'fast-command', 'fork', 'aof-fsync-always',
                  'aof-write', 'aof-write-pending-fsync', 'rdb-unlink-temp-file']

        history = {}
        for event in events:
            try:
                data = r.execute_command('LATENCY', 'HISTORY', event)
                if data:
                    history[event] = [
                        {'timestamp': ts, 'latency_ms': lat}
                        for ts, lat in data
                    ]
            except:
                pass

        return history
    except:
        return {}

def get_latency_latest():
    """Get latest latency spike for each event type"""
    try:
        data = r.execute_command('LATENCY', 'LATEST')
        results = []
        for entry in data:
            if len(entry) >= 4:
                results.append({
                    'event': entry[0].decode() if isinstance(entry[0], bytes) else entry[0],
                    'timestamp': entry[1],
                    'latest_latency_ms': entry[2],
                    'max_latency_ms': entry[3]
                })
        return results
    except:
        return []

def get_latency_doctor():
    """Get latency doctor analysis"""
    try:
        report = r.execute_command('LATENCY', 'DOCTOR')
        return report.decode() if isinstance(report, bytes) else report
    except:
        return "Latency doctor not available"

# Correct 3: Continuous latency monitoring
class LatencyMonitor:
    def __init__(self, redis_client, window_size=1000):
        self.r = redis_client
        self.latencies = []
        self.window_size = window_size
        self.alerts = []

    def record_operation(self, operation_func):
        """Measure and record operation latency"""
        start = time.perf_counter()
        result = operation_func()
        latency = (time.perf_counter() - start) * 1000

        self.latencies.append({
            'timestamp': time.time(),
            'latency_ms': latency
        })

        # Keep bounded window
        if len(self.latencies) > self.window_size:
            self.latencies = self.latencies[-self.window_size:]

        # Alert on high latency
        if latency > 100:  # 100ms threshold
            self.alerts.append({
                'timestamp': time.time(),
                'latency_ms': latency
            })

        return result

    def get_stats(self):
        """Get latency statistics"""
        if not self.latencies:
            return None

        lats = [l['latency_ms'] for l in self.latencies]
        lats.sort()

        return {
            'count': len(lats),
            'min': min(lats),
            'max': max(lats),
            'avg': statistics.mean(lats),
            'p50': lats[len(lats) // 2],
            'p95': lats[int(len(lats) * 0.95)],
            'p99': lats[int(len(lats) * 0.99)],
        }

# Correct 4: Diagnose latency sources
def diagnose_latency():
    """Comprehensive latency diagnosis"""
    diagnosis = {
        'issues': [],
        'recommendations': []
    }

    # Check SLOWLOG
    slow_commands = r.slowlog_get(10)
    if slow_commands:
        avg_slow = sum(c['duration'] for c in slow_commands) / len(slow_commands) / 1000
        diagnosis['slow_commands'] = {
            'count': len(slow_commands),
            'avg_duration_ms': avg_slow
        }
        if avg_slow > 100:
            diagnosis['issues'].append(f"Slow commands averaging {avg_slow:.1f}ms")
            diagnosis['recommendations'].append("Review SLOWLOG and optimize slow commands")

    # Check memory
    mem_info = r.info("memory")
    frag = mem_info.get('mem_fragmentation_ratio', 1)
    if frag < 1:
        diagnosis['issues'].append("Memory fragmentation < 1: Using swap!")
        diagnosis['recommendations'].append("Add more memory or reduce dataset")
    elif frag > 1.5:
        diagnosis['issues'].append(f"Memory fragmentation: {frag:.2f}")
        diagnosis['recommendations'].append("Enable active defragmentation")

    # Check persistence
    persistence = r.info("persistence")
    if persistence.get('aof_rewrite_in_progress'):
        diagnosis['issues'].append("AOF rewrite in progress")
    if persistence.get('rdb_bgsave_in_progress'):
        diagnosis['issues'].append("RDB save in progress")

    # Check clients
    clients = r.info("clients")
    blocked = clients.get('blocked_clients', 0)
    if blocked > 10:
        diagnosis['issues'].append(f"{blocked} blocked clients")
        diagnosis['recommendations'].append("Check for blocking operations")

    # Network latency
    latency = measure_latency(10)
    diagnosis['network_latency'] = latency
    if latency['p99_ms'] > 10:
        diagnosis['issues'].append(f"Network P99 latency: {latency['p99_ms']:.1f}ms")

    return diagnosis
```

```bash
# CLI commands for latency monitoring

# Enable latency monitoring (threshold in ms)
redis-cli CONFIG SET latency-monitor-threshold 100

# Get latest latency events
redis-cli LATENCY LATEST

# Get latency history for specific event
redis-cli LATENCY HISTORY command

# Get doctor's analysis
redis-cli LATENCY DOCTOR

# Reset latency data
redis-cli LATENCY RESET

# Intrinsic latency test (run on Redis server)
redis-cli --intrinsic-latency 60  # Test for 60 seconds

# Continuous latency monitor
redis-cli --latency

# Latency distribution
redis-cli --latency-dist

# Latency history
redis-cli --latency-history
```

```python
# Correct 5: Track latency by command type
def benchmark_commands():
    """Measure latency for different command types"""
    results = {}

    # String operations
    results['SET'] = measure_operation(lambda: r.set('bench:key', 'value'))
    results['GET'] = measure_operation(lambda: r.get('bench:key'))

    # Hash operations
    r.hset('bench:hash', mapping={'a': '1', 'b': '2'})
    results['HGET'] = measure_operation(lambda: r.hget('bench:hash', 'a'))
    results['HGETALL'] = measure_operation(lambda: r.hgetall('bench:hash'))

    # List operations
    r.rpush('bench:list', *range(100))
    results['LRANGE'] = measure_operation(lambda: r.lrange('bench:list', 0, -1))

    # Cleanup
    r.delete('bench:key', 'bench:hash', 'bench:list')

    return results

def measure_operation(func, iterations=100):
    """Measure operation latency"""
    latencies = []
    for _ in range(iterations):
        start = time.perf_counter()
        func()
        latencies.append((time.perf_counter() - start) * 1000)

    latencies.sort()
    return {
        'avg_ms': statistics.mean(latencies),
        'p50_ms': latencies[len(latencies) // 2],
        'p99_ms': latencies[int(len(latencies) * 0.99)]
    }
```

Reference: [Redis Latency Monitoring](https://redis.io/docs/management/optimization/latency-monitor/)

### 8.3 Track Memory Usage and Trends

**Impact: HIGH** (prevents OOM, enables capacity planning)

## Track Memory Usage and Trends

Monitor Redis memory usage continuously to prevent OOM situations and plan capacity. Track not just current usage but trends over time to predict when you'll need more capacity.

**Key Metrics to Monitor:**
- `used_memory`: Memory allocated by Redis
- `used_memory_rss`: OS-reported memory (actual memory usage)
- `used_memory_peak`: Historical peak usage
- `maxmemory`: Configured limit
- `mem_fragmentation_ratio`: RSS / used_memory
- `evicted_keys`: Keys removed due to maxmemory

**Incorrect (no memory monitoring):**

```python
# Anti-pattern 1: No memory monitoring
# Only notice memory issues when OOM kills Redis

# Anti-pattern 2: Checking memory only occasionally
def weekly_health_check():
    info = r.info("memory")
    print(f"Memory: {info['used_memory_human']}")
# Too infrequent, can't track trends

# Anti-pattern 3: Only checking used_memory
# Ignoring RSS, fragmentation, and trends
```

**Correct (comprehensive memory monitoring):**

```python
import redis
import time
from datetime import datetime

r = redis.Redis()

# Correct 1: Get comprehensive memory stats
def get_memory_stats():
    """Get all relevant memory statistics"""
    info = r.info("memory")

    stats = {
        # Current usage
        'used_memory': info['used_memory'],
        'used_memory_human': info['used_memory_human'],
        'used_memory_rss': info['used_memory_rss'],
        'used_memory_rss_human': info['used_memory_rss_human'],

        # Peak usage
        'used_memory_peak': info['used_memory_peak'],
        'used_memory_peak_human': info['used_memory_peak_human'],

        # Configuration
        'maxmemory': info.get('maxmemory', 0),
        'maxmemory_human': info.get('maxmemory_human', '0'),
        'maxmemory_policy': info.get('maxmemory_policy', 'noeviction'),

        # Fragmentation
        'mem_fragmentation_ratio': info.get('mem_fragmentation_ratio', 0),
        'mem_fragmentation_bytes': info.get('mem_fragmentation_bytes', 0),

        # Dataset
        'used_memory_dataset': info.get('used_memory_dataset', 0),
        'used_memory_overhead': info.get('used_memory_overhead', 0),

        # Lua
        'used_memory_lua': info.get('used_memory_lua', 0),
        'used_memory_scripts': info.get('used_memory_scripts', 0),
    }

    # Calculate utilization percentage
    if stats['maxmemory'] > 0:
        stats['utilization_pct'] = (stats['used_memory'] / stats['maxmemory']) * 100
    else:
        stats['utilization_pct'] = None

    return stats

# Correct 2: Memory health check with alerts
def check_memory_health():
    """Check memory health and return alerts"""
    stats = get_memory_stats()
    alerts = []

    # Check utilization
    if stats['utilization_pct']:
        if stats['utilization_pct'] > 90:
            alerts.append({
                'severity': 'critical',
                'message': f"Memory at {stats['utilization_pct']:.1f}% - near limit"
            })
        elif stats['utilization_pct'] > 75:
            alerts.append({
                'severity': 'warning',
                'message': f"Memory at {stats['utilization_pct']:.1f}%"
            })
    else:
        alerts.append({
            'severity': 'warning',
            'message': "maxmemory not configured"
        })

    # Check fragmentation
    frag = stats['mem_fragmentation_ratio']
    if frag < 1:
        alerts.append({
            'severity': 'critical',
            'message': f"Fragmentation {frag:.2f} - using swap!"
        })
    elif frag > 1.5:
        alerts.append({
            'severity': 'warning',
            'message': f"High fragmentation: {frag:.2f}"
        })

    return {
        'healthy': len([a for a in alerts if a['severity'] == 'critical']) == 0,
        'alerts': alerts,
        'stats': stats
    }

# Correct 3: Track memory trends over time
class MemoryTrendTracker:
    def __init__(self, redis_client, history_size=1440):
        self.r = redis_client
        self.history = []
        self.history_size = history_size  # 24 hours at 1-minute intervals

    def record(self):
        """Record current memory stats"""
        stats = get_memory_stats()
        self.history.append({
            'timestamp': time.time(),
            'used_memory': stats['used_memory'],
            'used_memory_rss': stats['used_memory_rss'],
            'fragmentation': stats['mem_fragmentation_ratio']
        })

        # Keep bounded history
        if len(self.history) > self.history_size:
            self.history = self.history[-self.history_size:]

    def get_trend(self, minutes=60):
        """Calculate memory growth trend over period"""
        cutoff = time.time() - (minutes * 60)
        recent = [h for h in self.history if h['timestamp'] > cutoff]

        if len(recent) < 2:
            return None

        first = recent[0]['used_memory']
        last = recent[-1]['used_memory']
        duration_hours = (recent[-1]['timestamp'] - recent[0]['timestamp']) / 3600

        growth_rate = (last - first) / duration_hours if duration_hours > 0 else 0

        return {
            'start_memory': first,
            'end_memory': last,
            'growth_bytes': last - first,
            'growth_rate_per_hour': growth_rate,
            'growth_rate_human': f"{growth_rate / 1024 / 1024:.2f} MB/hour"
        }

    def predict_time_to_full(self):
        """Predict when memory will reach maxmemory"""
        stats = get_memory_stats()
        trend = self.get_trend(60)

        if not trend or trend['growth_rate_per_hour'] <= 0:
            return None

        if not stats['maxmemory']:
            return None

        remaining = stats['maxmemory'] - stats['used_memory']
        hours_to_full = remaining / trend['growth_rate_per_hour']

        return {
            'hours_to_full': hours_to_full,
            'estimated_full_time': datetime.fromtimestamp(
                time.time() + hours_to_full * 3600
            ),
            'current_utilization_pct': stats['utilization_pct']
        }
```

```python
# Correct 4: Analyze memory by data type
def analyze_memory_by_type():
    """Sample keys to understand memory distribution by type"""
    type_stats = {}
    sample_size = 1000
    count = 0

    for key in r.scan_iter(count=100):
        if count >= sample_size:
            break

        key_type = r.type(key).decode()
        memory = r.memory_usage(key) or 0

        if key_type not in type_stats:
            type_stats[key_type] = {'count': 0, 'memory': 0, 'samples': []}

        type_stats[key_type]['count'] += 1
        type_stats[key_type]['memory'] += memory
        if len(type_stats[key_type]['samples']) < 5:
            type_stats[key_type]['samples'].append({
                'key': key.decode(),
                'memory': memory
            })

        count += 1

    # Calculate percentages
    total_memory = sum(t['memory'] for t in type_stats.values())
    for t in type_stats.values():
        t['percentage'] = (t['memory'] / total_memory * 100) if total_memory > 0 else 0
        t['avg_memory'] = t['memory'] / t['count'] if t['count'] > 0 else 0

    return type_stats

# Correct 5: Find top memory consumers
def find_large_keys(top_n=20, sample_size=10000):
    """Find largest keys by memory usage"""
    large_keys = []
    count = 0

    for key in r.scan_iter(count=100):
        if count >= sample_size:
            break

        memory = r.memory_usage(key)
        if memory:
            large_keys.append({
                'key': key.decode(),
                'memory': memory,
                'type': r.type(key).decode()
            })

        count += 1

    # Sort by memory and return top N
    large_keys.sort(key=lambda x: x['memory'], reverse=True)
    return large_keys[:top_n]
```

```bash
# CLI commands for memory monitoring

# Get memory info
redis-cli INFO memory

# Memory doctor (recommendations)
redis-cli MEMORY DOCTOR

# Memory stats
redis-cli MEMORY STATS

# Memory usage for specific key
redis-cli MEMORY USAGE mykey

# Get key count
redis-cli DBSIZE

# Debug memory for a key (detailed)
redis-cli DEBUG OBJECT mykey
```

```javascript
// Node.js - Memory monitoring
const Redis = require('ioredis');
const redis = new Redis();

async function getMemoryStats() {
    const info = await redis.info('memory');
    const lines = info.split('\r\n');
    const stats = {};

    lines.forEach(line => {
        const [key, value] = line.split(':');
        if (key && value) {
            stats[key] = value;
        }
    });

    return {
        usedMemory: parseInt(stats.used_memory),
        usedMemoryHuman: stats.used_memory_human,
        maxmemory: parseInt(stats.maxmemory || 0),
        fragmentationRatio: parseFloat(stats.mem_fragmentation_ratio),
    };
}
```

Reference: [Redis MEMORY Commands](https://redis.io/commands/memory-usage/)

### 8.4 Use INFO Command for Comprehensive Stats

**Impact: MEDIUM** (single source for all Redis metrics)

## Use INFO Command for Comprehensive Stats

Use the INFO command to gather comprehensive statistics about Redis server state. INFO provides data on memory, clients, replication, CPU, keyspace, and more - essential for monitoring and debugging.

**INFO Sections:**
- `server`: General server info (version, uptime, etc.)
- `clients`: Connected clients info
- `memory`: Memory usage and stats
- `persistence`: RDB/AOF status
- `stats`: General statistics (ops/sec, etc.)
- `replication`: Master/replica info
- `cpu`: CPU consumption
- `cluster`: Cluster state
- `keyspace`: Database statistics

**Incorrect (not using INFO effectively):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: No monitoring at all
# Running Redis with no visibility into metrics

# Anti-pattern 2: Only checking PING
def health_check_bad():
    return r.ping()  # Tells you nothing about memory, clients, etc.

# Anti-pattern 3: Manual queries for stats
def get_stats_bad():
    # Querying multiple sources instead of INFO
    key_count = r.dbsize()
    # Missing memory, ops/sec, replication status, etc.
    return {"keys": key_count}
```

**Correct (using INFO effectively):**

```python
import redis
r = redis.Redis()

# Correct 1: Get all INFO sections
def get_all_info():
    """Get complete INFO output"""
    return r.info()

# Correct 2: Get specific section
def get_memory_info():
    return r.info("memory")

def get_stats_info():
    return r.info("stats")

def get_replication_info():
    return r.info("replication")

# Correct 3: Build a comprehensive dashboard
def get_redis_dashboard():
    """Get key metrics for monitoring dashboard"""
    server = r.info("server")
    clients = r.info("clients")
    memory = r.info("memory")
    stats = r.info("stats")
    replication = r.info("replication")
    persistence = r.info("persistence")

    return {
        # Server
        'version': server.get('redis_version'),
        'uptime_days': server.get('uptime_in_days'),
        'uptime_seconds': server.get('uptime_in_seconds'),

        # Clients
        'connected_clients': clients.get('connected_clients'),
        'blocked_clients': clients.get('blocked_clients'),
        'max_clients': clients.get('maxclients'),

        # Memory
        'used_memory_human': memory.get('used_memory_human'),
        'used_memory_peak_human': memory.get('used_memory_peak_human'),
        'maxmemory_human': memory.get('maxmemory_human'),
        'mem_fragmentation_ratio': memory.get('mem_fragmentation_ratio'),

        # Operations
        'total_commands_processed': stats.get('total_commands_processed'),
        'instantaneous_ops_per_sec': stats.get('instantaneous_ops_per_sec'),
        'total_connections_received': stats.get('total_connections_received'),

        # Cache performance
        'keyspace_hits': stats.get('keyspace_hits'),
        'keyspace_misses': stats.get('keyspace_misses'),
        'hit_rate': calculate_hit_rate(stats),

        # Replication
        'role': replication.get('role'),
        'connected_slaves': replication.get('connected_slaves'),
        'master_link_status': replication.get('master_link_status'),

        # Persistence
        'rdb_last_save_time': persistence.get('rdb_last_save_time'),
        'rdb_last_bgsave_status': persistence.get('rdb_last_bgsave_status'),
        'aof_enabled': persistence.get('aof_enabled'),
        'aof_last_write_status': persistence.get('aof_last_write_status'),

        # Eviction
        'evicted_keys': stats.get('evicted_keys'),
        'expired_keys': stats.get('expired_keys'),
    }

def calculate_hit_rate(stats):
    """Calculate cache hit rate"""
    hits = stats.get('keyspace_hits', 0)
    misses = stats.get('keyspace_misses', 0)
    total = hits + misses
    return (hits / total * 100) if total > 0 else 0

# Correct 4: Monitor ops/sec over time
class OpsMonitor:
    def __init__(self, redis_client):
        self.r = redis_client
        self.last_total = None
        self.last_time = None

    def get_ops_per_sec(self):
        """Calculate actual ops/sec between calls"""
        stats = self.r.info("stats")
        current_total = stats.get('total_commands_processed', 0)
        current_time = time.time()

        if self.last_total is None:
            self.last_total = current_total
            self.last_time = current_time
            return stats.get('instantaneous_ops_per_sec', 0)

        elapsed = current_time - self.last_time
        ops = current_total - self.last_total

        self.last_total = current_total
        self.last_time = current_time

        return ops / elapsed if elapsed > 0 else 0

# Correct 5: Check replication health
def check_replication_health():
    """Check replication status and lag"""
    info = r.info("replication")
    role = info.get('role')

    if role == 'master':
        slaves = info.get('connected_slaves', 0)
        slave_info = []
        for i in range(slaves):
            slave_data = info.get(f'slave{i}', '')
            # Parse: ip=x.x.x.x,port=6379,state=online,offset=123,lag=0
            if slave_data:
                parts = dict(p.split('=') for p in slave_data.split(','))
                slave_info.append(parts)

        return {
            'role': 'master',
            'connected_slaves': slaves,
            'slaves': slave_info
        }
    else:
        return {
            'role': 'replica',
            'master_host': info.get('master_host'),
            'master_port': info.get('master_port'),
            'master_link_status': info.get('master_link_status'),
            'master_last_io_seconds_ago': info.get('master_last_io_seconds_ago'),
            'slave_read_repl_offset': info.get('slave_read_repl_offset'),
        }

# Correct 6: Get keyspace statistics
def get_keyspace_stats():
    """Get per-database key counts and expiry info"""
    info = r.info("keyspace")
    databases = {}

    for db, data in info.items():
        # data is like: {'keys': 1234, 'expires': 100, 'avg_ttl': 3600000}
        databases[db] = {
            'keys': data.get('keys', 0),
            'expires': data.get('expires', 0),
            'avg_ttl_ms': data.get('avg_ttl', 0),
            'pct_with_expiry': (data.get('expires', 0) / data.get('keys', 1)) * 100
        }

    return databases
```

```bash
# CLI commands for INFO

# Full info
redis-cli INFO

# Specific section
redis-cli INFO memory
redis-cli INFO stats
redis-cli INFO replication
redis-cli INFO clients

# One-liner metrics
redis-cli INFO stats | grep instantaneous_ops
redis-cli INFO memory | grep used_memory_human
redis-cli INFO clients | grep connected_clients

# Watch ops/sec in real-time
watch -n 1 'redis-cli INFO stats | grep instantaneous_ops'
```

```python
# Correct 7: Export metrics to monitoring system
def export_prometheus_metrics():
    """Format metrics for Prometheus scraping"""
    dashboard = get_redis_dashboard()

    metrics = [
        f'redis_connected_clients {dashboard["connected_clients"]}',
        f'redis_blocked_clients {dashboard["blocked_clients"]}',
        f'redis_used_memory_bytes {r.info("memory")["used_memory"]}',
        f'redis_ops_per_sec {dashboard["instantaneous_ops_per_sec"]}',
        f'redis_keyspace_hits_total {dashboard["keyspace_hits"]}',
        f'redis_keyspace_misses_total {dashboard["keyspace_misses"]}',
        f'redis_evicted_keys_total {dashboard["evicted_keys"]}',
        f'redis_expired_keys_total {dashboard["expired_keys"]}',
        f'redis_mem_fragmentation_ratio {dashboard["mem_fragmentation_ratio"]}',
    ]

    return '\n'.join(metrics)
```

Reference: [Redis INFO Command](https://redis.io/commands/info/)

### 8.5 Monitor Slow Commands with SLOWLOG

**Impact: HIGH** (identifies performance bottlenecks and problematic commands)

## Monitor Slow Commands with SLOWLOG

Use Redis SLOWLOG to identify slow commands that impact performance. SLOWLOG captures commands exceeding a configurable threshold, helping identify anti-patterns, missing indexes, or unexpected load.

**What SLOWLOG Captures:**
- Commands taking longer than threshold (default 10ms)
- Timestamp, duration, command, and arguments
- Last N slow commands (configurable)

**Common Slow Command Causes:**
- KEYS with many matches
- Operations on large collections
- Blocking commands timing out
- Complex Lua scripts
- Cross-slot operations in cluster

**Incorrect (not monitoring slow commands):**

```python
import redis
r = redis.Redis()

# Anti-pattern 1: No slow log monitoring
# Problems go undetected until outage

# Anti-pattern 2: SLOWLOG threshold too high
# redis.conf: slowlog-log-slower-than 1000000 (1 second)
# Missing commands that take 100-999ms

# Anti-pattern 3: SLOWLOG buffer too small
# redis.conf: slowlog-max-len 32
# Slow commands get evicted before review
```

**Correct (proper SLOWLOG configuration and monitoring):**

```bash
# Correct 1: Configure SLOWLOG appropriately
# redis.conf

# Log commands slower than 10ms (10000 microseconds)
slowlog-log-slower-than 10000

# Keep last 1000 slow commands
slowlog-max-len 1000

# For production debugging, consider lower threshold
# slowlog-log-slower-than 5000  # 5ms
```

```python
import redis
from datetime import datetime

r = redis.Redis()

# Correct 2: Get and analyze slow log
def get_slow_log(count=100):
    """Retrieve slow log entries"""
    entries = r.slowlog_get(count)
    parsed = []

    for entry in entries:
        parsed.append({
            'id': entry['id'],
            'timestamp': datetime.fromtimestamp(entry['start_time']),
            'duration_ms': entry['duration'] / 1000,
            'command': entry['command'].decode() if isinstance(entry['command'], bytes) else entry['command'],
            'client_addr': entry.get('client_address', b'').decode() if entry.get('client_address') else None,
            'client_name': entry.get('client_name', b'').decode() if entry.get('client_name') else None,
        })

    return parsed

def print_slow_log():
    """Print slow log in readable format"""
    entries = get_slow_log()
    print(f"{'ID':<8} {'Duration':<12} {'Command':<50} {'Time'}")
    print("-" * 100)
    for e in entries:
        cmd = e['command'][:47] + '...' if len(e['command']) > 50 else e['command']
        print(f"{e['id']:<8} {e['duration_ms']:>8.2f}ms   {cmd:<50} {e['timestamp']}")

# Correct 3: Alert on slow commands
def check_slow_log_alerts(duration_threshold_ms=100):
    """Alert if there are very slow commands"""
    entries = get_slow_log(50)
    alerts = [e for e in entries if e['duration_ms'] > duration_threshold_ms]

    if alerts:
        return {
            'alert': True,
            'count': len(alerts),
            'slowest': max(alerts, key=lambda x: x['duration_ms']),
            'commands': [e['command'] for e in alerts]
        }
    return {'alert': False}

# Correct 4: Analyze slow log patterns
def analyze_slow_commands():
    """Identify patterns in slow commands"""
    entries = get_slow_log(500)
    analysis = {
        'total_entries': len(entries),
        'by_command': {},
        'by_duration': {
            '10-50ms': 0,
            '50-100ms': 0,
            '100-500ms': 0,
            '500ms+': 0
        }
    }

    for entry in entries:
        # Extract command type (first word)
        cmd_type = entry['command'].split()[0].upper()
        if cmd_type not in analysis['by_command']:
            analysis['by_command'][cmd_type] = {
                'count': 0,
                'total_ms': 0,
                'max_ms': 0
            }

        analysis['by_command'][cmd_type]['count'] += 1
        analysis['by_command'][cmd_type]['total_ms'] += entry['duration_ms']
        analysis['by_command'][cmd_type]['max_ms'] = max(
            analysis['by_command'][cmd_type]['max_ms'],
            entry['duration_ms']
        )

        # Duration buckets
        if entry['duration_ms'] < 50:
            analysis['by_duration']['10-50ms'] += 1
        elif entry['duration_ms'] < 100:
            analysis['by_duration']['50-100ms'] += 1
        elif entry['duration_ms'] < 500:
            analysis['by_duration']['100-500ms'] += 1
        else:
            analysis['by_duration']['500ms+'] += 1

    # Calculate averages
    for cmd, data in analysis['by_command'].items():
        data['avg_ms'] = data['total_ms'] / data['count'] if data['count'] > 0 else 0

    return analysis
```

```python
# Correct 5: Reset and monitor continuously
def reset_slow_log():
    """Reset slow log for fresh measurement period"""
    r.slowlog_reset()
    print("Slow log reset")

def monitor_slow_log_continuous(interval_seconds=60):
    """Continuously monitor and report slow log"""
    import time

    last_id = 0
    while True:
        entries = get_slow_log(100)
        new_entries = [e for e in entries if e['id'] > last_id]

        if new_entries:
            print(f"\n--- {len(new_entries)} new slow commands ---")
            for e in new_entries:
                print(f"  [{e['duration_ms']:.1f}ms] {e['command'][:80]}")

            last_id = max(e['id'] for e in new_entries)

        time.sleep(interval_seconds)

# Correct 6: Configure SLOWLOG at runtime
def configure_slowlog(threshold_microseconds=10000, max_len=1000):
    """Configure SLOWLOG settings"""
    r.config_set('slowlog-log-slower-than', threshold_microseconds)
    r.config_set('slowlog-max-len', max_len)

    current = {
        'threshold_us': r.config_get('slowlog-log-slower-than'),
        'max_len': r.config_get('slowlog-max-len')
    }
    return current
```

```bash
# CLI commands for SLOWLOG

# Get slow log entries
redis-cli SLOWLOG GET 20

# Get slow log length
redis-cli SLOWLOG LEN

# Reset slow log
redis-cli SLOWLOG RESET

# Get current settings
redis-cli CONFIG GET slowlog-*

# Set threshold to 5ms
redis-cli CONFIG SET slowlog-log-slower-than 5000

# Example output:
# 1) 1) (integer) 14               # ID
#    2) (integer) 1309448221       # Timestamp
#    3) (integer) 15               # Duration in microseconds
#    4) 1) "ping"                  # Command
#    5) "127.0.0.1:58217"         # Client address
#    6) ""                         # Client name
```

```javascript
// Node.js - SLOWLOG monitoring
const Redis = require('ioredis');
const redis = new Redis();

async function getSlowLog(count = 100) {
    const entries = await redis.slowlog('GET', count);
    return entries.map(entry => ({
        id: entry[0],
        timestamp: new Date(entry[1] * 1000),
        durationMs: entry[2] / 1000,
        command: entry[3].join(' '),
        clientAddr: entry[4],
        clientName: entry[5]
    }));
}

async function analyzeSlowLog() {
    const entries = await getSlowLog(500);
    const byCommand = {};

    entries.forEach(entry => {
        const cmdType = entry.command.split(' ')[0].toUpperCase();
        if (!byCommand[cmdType]) {
            byCommand[cmdType] = { count: 0, totalMs: 0 };
        }
        byCommand[cmdType].count++;
        byCommand[cmdType].totalMs += entry.durationMs;
    });

    return { totalEntries: entries.length, byCommand };
}
```

Reference: [Redis SLOWLOG](https://redis.io/commands/slowlog/)

---

## References

- [Redis Documentation](https://redis.io/docs/)
- [Redis Best Practices](https://redis.io/docs/management/optimization/)
- [Redis Patterns](https://redis.io/docs/manual/patterns/)
- [Redis Data Types](https://redis.io/docs/data-types/)
- [Redis Commands](https://redis.io/commands/)
