---
title: Avoid Large Keys and Values
impact: CRITICAL
impactDescription: large keys block Redis, cause timeouts and memory issues
tags: keys, memory, performance, size
---

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
