---
id: api-rate-limiting
name: "Rate Limiting"
domain: API
skill: faion-software-developer
category: "api-design"
---

## Rate Limiting

### Problem

APIs can be abused by malicious actors or overwhelmed by high traffic. Need protection.

### Framework

**Rate Limit Headers (Standard):**

```http
HTTP/1.1 200 OK
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1735689600
Retry-After: 60
```

**429 Response:**

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests",
    "retryAfter": 60,
    "limit": 100,
    "window": "1h"
  }
}
```

### Algorithms

**Fixed Window:**

```python
# Simple but has burst at window edges
class FixedWindowRateLimiter:
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = window_seconds
        self.counters = {}

    def is_allowed(self, key: str) -> bool:
        now = int(time.time())
        window_start = now - (now % self.window)
        counter_key = f"{key}:{window_start}"

        count = self.counters.get(counter_key, 0)
        if count >= self.limit:
            return False

        self.counters[counter_key] = count + 1
        return True
```

**Sliding Window:**

```python
# Smoother, no edge bursts
class SlidingWindowRateLimiter:
    def __init__(self, limit: int, window_seconds: int, redis_client):
        self.limit = limit
        self.window = window_seconds
        self.redis = redis_client

    async def is_allowed(self, key: str) -> bool:
        now = time.time()
        pipe = self.redis.pipeline()
        pipe.zremrangebyscore(key, 0, now - self.window)
        pipe.zadd(key, {str(now): now})
        pipe.zcard(key)
        pipe.expire(key, self.window)
        _, _, count, _ = await pipe.execute()
        return count <= self.limit
```

**Token Bucket:**

```python
# Allows bursts up to bucket size
class TokenBucketRateLimiter:
    def __init__(self, bucket_size: int, refill_rate: float):
        self.bucket_size = bucket_size
        self.refill_rate = refill_rate  # tokens per second
        self.buckets = {}

    def is_allowed(self, key: str, tokens: int = 1) -> bool:
        now = time.time()
        bucket = self.buckets.get(key, {
            "tokens": self.bucket_size,
            "last_refill": now
        })

        # Refill tokens
        elapsed = now - bucket["last_refill"]
        bucket["tokens"] = min(
            self.bucket_size,
            bucket["tokens"] + elapsed * self.refill_rate
        )
        bucket["last_refill"] = now

        # Check if allowed
        if bucket["tokens"] >= tokens:
            bucket["tokens"] -= tokens
            self.buckets[key] = bucket
            return True
        return False
```

### Implementation Strategies

**Per-User Limits:**

```python
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    user_id = get_user_from_request(request)
    key = f"rate_limit:{user_id}"

    if not await rate_limiter.is_allowed(key):
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded"},
            headers={"Retry-After": "60"}
        )

    return await call_next(request)
```

**Tiered Limits:**

| Tier | Requests/hour | Burst |
|------|---------------|-------|
| Free | 100 | 10 |
| Plus | 1,000 | 50 |
| Pro | 10,000 | 200 |
| Enterprise | Unlimited | N/A |

**Endpoint-Specific:**

```python
RATE_LIMITS = {
    "/api/search": {"limit": 10, "window": 60},
    "/api/export": {"limit": 5, "window": 3600},
    "/api/users": {"limit": 100, "window": 60}
}
```

### Best Practices

- Use sliding window for fairness
- Implement tiered limits by plan
- Return clear error messages
- Include Retry-After header
- Log rate limit events
- Use Redis for distributed rate limiting
- Whitelist internal services

### Agent

faion-api-agent
