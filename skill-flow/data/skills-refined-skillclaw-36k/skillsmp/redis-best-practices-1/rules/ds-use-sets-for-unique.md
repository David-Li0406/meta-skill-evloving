---
title: Use Sets for Unique Collections
impact: HIGH
impactDescription: O(1) membership checks, automatic deduplication
tags: data-structures, set, unique, membership
---

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
