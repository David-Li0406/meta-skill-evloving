---
title: Use Batch Operations for Multiple Keys
impact: HIGH
impactDescription: reduces round trips by 90%+, improves throughput
tags: commands, batch, performance, mget, mset
---

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
