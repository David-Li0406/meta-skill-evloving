---
title: Design Keys Around Access Patterns
impact: HIGH
impactDescription: enables efficient queries without secondary indexes
tags: keys, design, patterns, queries
---

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
