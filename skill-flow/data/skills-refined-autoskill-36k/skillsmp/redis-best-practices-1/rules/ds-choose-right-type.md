---
title: Choose the Right Data Structure
impact: CRITICAL
impactDescription: wrong type can cause 10-100x performance degradation
tags: data-structures, design, performance
---

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
