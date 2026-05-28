---
title: Use Sorted Sets for Rankings and Time-Series
impact: HIGH
impactDescription: O(log n) ranked operations, efficient range queries
tags: data-structures, sorted-set, leaderboard, ranking, time-series
---

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
