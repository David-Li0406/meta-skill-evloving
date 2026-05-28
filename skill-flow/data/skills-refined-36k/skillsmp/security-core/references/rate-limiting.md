# Rate Limiting

Protect APIs from abuse, brute force attacks, and DOS with rate limiting strategies.

## Strategies

| Strategy | Use Case | Implementation |
|----------|----------|----------------|
| Fixed Window | Simple counting per time window | Easy but can have burst issues |
| Sliding Window | More accurate than fixed window | Moderate complexity |
| Token Bucket | Allow bursts with sustained rate | Good for APIs |
| Leaky Bucket | Smooth rate limiting | Consistent processing |

## TypeScript Implementation

### Express + express-rate-limit

```typescript
import rateLimit from 'express-rate-limit';
import RedisStore from 'rate-limit-redis';
import { createClient } from 'redis';

const redisClient = createClient({ url: process.env.REDIS_URL });
await redisClient.connect();

// Global rate limit
const globalLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100, // 100 requests per window
  standardHeaders: true,
  legacyHeaders: false,
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:global:',
  }),
  message: 'Too many requests, please try again later',
});

app.use(globalLimiter);

// Stricter limit for auth endpoints
const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,
  max: 5, // 5 login attempts per 15 minutes
  skipSuccessfulRequests: true, // Don't count successful logins
  store: new RedisStore({
    client: redisClient,
    prefix: 'rl:auth:',
  }),
});

app.post('/login', authLimiter, loginHandler);
app.post('/register', authLimiter, registerHandler);

// API endpoint limits
const apiLimiter = rateLimit({
  windowMs: 60 * 1000, // 1 minute
  max: 60, // 60 requests per minute
  keyGenerator: (req) => {
    // Rate limit by API key instead of IP
    return req.headers['x-api-key'] as string || req.ip;
  },
});

app.use('/api', apiLimiter);
```

### Custom Sliding Window

```typescript
import { createClient } from 'redis';

class SlidingWindowRateLimiter {
  constructor(
    private redis: ReturnType<typeof createClient>,
    private windowSize: number,
    private maxRequests: number
  ) {}

  async isAllowed(key: string): Promise<boolean> {
    const now = Date.now();
    const windowStart = now - this.windowSize;

    // Remove old entries
    await this.redis.zRemRangeByScore(key, 0, windowStart);

    // Count requests in window
    const count = await this.redis.zCard(key);

    if (count < this.maxRequests) {
      // Add current request
      await this.redis.zAdd(key, [{ score: now, value: `${now}` }]);
      await this.redis.expire(key, Math.ceil(this.windowSize / 1000));
      return true;
    }

    return false;
  }

  async getRemainingRequests(key: string): Promise<number> {
    const now = Date.now();
    const windowStart = now - this.windowSize;

    await this.redis.zRemRangeByScore(key, 0, windowStart);
    const count = await this.redis.zCard(key);

    return Math.max(0, this.maxRequests - count);
  }
}

// Usage
const limiter = new SlidingWindowRateLimiter(
  redisClient,
  60000, // 1 minute window
  60 // 60 requests
);

app.use(async (req, res, next) => {
  const key = `rate:${req.ip}`;
  const allowed = await limiter.isAllowed(key);

  if (!allowed) {
    const remaining = await limiter.getRemainingRequests(key);
    res.set('X-RateLimit-Remaining', remaining.toString());
    return res.status(429).json({ error: 'Too many requests' });
  }

  next();
});
```

## Python Implementation

### FastAPI + slowapi

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import FastAPI, Request

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Global rate limit
@app.get("/")
@limiter.limit("100/15minutes")
async def index(request: Request):
    return {"message": "Hello World"}

# Strict auth limits
@app.post("/login")
@limiter.limit("5/15minutes")
async def login(request: Request, email: str, password: str):
    # Login logic
    pass

# API endpoint limits
@app.get("/api/data")
@limiter.limit("60/minute")
async def get_data(request: Request):
    return {"data": "..."}
```

### Custom Redis Implementation

```python
import redis
import time
from typing import Optional

class SlidingWindowRateLimiter:
    def __init__(
        self,
        redis_client: redis.Redis,
        window_size: int,
        max_requests: int
    ):
        self.redis = redis_client
        self.window_size = window_size
        self.max_requests = max_requests

    def is_allowed(self, key: str) -> bool:
        now = int(time.time() * 1000)
        window_start = now - self.window_size

        # Remove old entries
        self.redis.zremrangebyscore(key, 0, window_start)

        # Count requests in window
        count = self.redis.zcard(key)

        if count < self.max_requests:
            # Add current request
            self.redis.zadd(key, {str(now): now})
            self.redis.expire(key, self.window_size // 1000 + 1)
            return True

        return False

    def get_remaining_requests(self, key: str) -> int:
        now = int(time.time() * 1000)
        window_start = now - self.window_size

        self.redis.zremrangebyscore(key, 0, window_start)
        count = self.redis.zcard(key)

        return max(0, self.max_requests - count)

# Usage
redis_client = redis.Redis(host='localhost', port=6379, db=0)
limiter = SlidingWindowRateLimiter(redis_client, 60000, 60)

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    key = f"rate:{request.client.host}"

    if not limiter.is_allowed(key):
        return JSONResponse(
            status_code=429,
            content={"error": "Too many requests"}
        )

    response = await call_next(request)
    remaining = limiter.get_remaining_requests(key)
    response.headers["X-RateLimit-Remaining"] = str(remaining)

    return response
```

## Rust Implementation

### Axum + tower-governor

```rust
use axum::{Router, routing::get};
use tower_governor::{
    governor::GovernorConfigBuilder,
    GovernorLayer,
};

#[tokio::main]
async fn main() {
    // Configure rate limiter
    let governor_conf = Box::new(
        GovernorConfigBuilder::default()
            .per_second(2) // 2 requests per second
            .burst_size(10) // Allow bursts of 10
            .finish()
            .unwrap(),
    );

    let governor_limiter = governor_conf.limiter().clone();
    let governor_layer = GovernorLayer {
        config: Box::leak(governor_conf),
    };

    // Create router with rate limiting
    let app = Router::new()
        .route("/", get(handler))
        .layer(governor_layer);

    // Start server
    axum::Server::bind(&"0.0.0.0:3000".parse().unwrap())
        .serve(app.into_make_service())
        .await
        .unwrap();
}

async fn handler() -> &'static str {
    "Hello, World!"
}
```

## Rate Limiting by User

```typescript
// Rate limit authenticated users by user ID
const userLimiter = rateLimit({
  windowMs: 60 * 1000,
  max: 100,
  keyGenerator: (req) => {
    // Use user ID if authenticated, otherwise IP
    return req.user?.id || req.ip;
  },
  skip: (req) => {
    // Skip rate limiting for admins
    return req.user?.role === 'admin';
  },
});
```

## Distributed Rate Limiting

### Using Redis

```typescript
import { createClient } from 'redis';

class DistributedRateLimiter {
  private redis: ReturnType<typeof createClient>;

  constructor(redisUrl: string) {
    this.redis = createClient({ url: redisUrl });
    this.redis.connect();
  }

  async checkRateLimit(
    key: string,
    limit: number,
    windowSeconds: number
  ): Promise<{ allowed: boolean; remaining: number; resetAt: Date }> {
    const now = Math.floor(Date.now() / 1000);
    const windowKey = `${key}:${Math.floor(now / windowSeconds)}`;

    // Increment counter
    const count = await this.redis.incr(windowKey);

    // Set expiration on first request
    if (count === 1) {
      await this.redis.expire(windowKey, windowSeconds);
    }

    const allowed = count <= limit;
    const remaining = Math.max(0, limit - count);
    const resetAt = new Date((Math.floor(now / windowSeconds) + 1) * windowSeconds * 1000);

    return { allowed, remaining, resetAt };
  }
}

// Usage
const limiter = new DistributedRateLimiter(process.env.REDIS_URL!);

app.use(async (req, res, next) => {
  const key = `rate:${req.ip}`;
  const result = await limiter.checkRateLimit(key, 100, 60);

  res.set({
    'X-RateLimit-Limit': '100',
    'X-RateLimit-Remaining': result.remaining.toString(),
    'X-RateLimit-Reset': result.resetAt.toISOString(),
  });

  if (!allowed) {
    return res.status(429).json({
      error: 'Too many requests',
      retryAfter: result.resetAt,
    });
  }

  next();
});
```

## Rate Limit Response Headers

```typescript
// Standard rate limit headers
res.set({
  'X-RateLimit-Limit': limit.toString(),
  'X-RateLimit-Remaining': remaining.toString(),
  'X-RateLimit-Reset': resetTime.toString(),
  'Retry-After': secondsUntilReset.toString(),
});

// When rate limited
res.status(429).json({
  error: 'Too many requests',
  message: 'You have exceeded the rate limit',
  retryAfter: secondsUntilReset,
});
```

## Adaptive Rate Limiting

```typescript
class AdaptiveRateLimiter {
  private baseLimit = 100;
  private currentLoad = 0;

  adjustLimit(): number {
    // Reduce limit when system is under high load
    if (this.currentLoad > 0.8) {
      return Math.floor(this.baseLimit * 0.5);
    } else if (this.currentLoad > 0.6) {
      return Math.floor(this.baseLimit * 0.75);
    }

    return this.baseLimit;
  }

  updateLoad(cpuUsage: number, memoryUsage: number) {
    this.currentLoad = Math.max(cpuUsage, memoryUsage);
  }
}
```

## Best Practices

1. **Different limits for different endpoints** - Auth endpoints stricter
2. **Use distributed storage** - Redis for multiple servers
3. **Return proper headers** - X-RateLimit-* headers
4. **Graceful degradation** - Don't fail hard if Redis is down
5. **Skip on success** - Don't count successful operations (optional)
6. **By-user for authenticated requests** - More accurate than IP
7. **Whitelist trusted IPs** - Internal services, monitoring
8. **Log rate limit hits** - Detect abuse patterns
9. **Client-side respect** - Honor rate limits in clients
10. **Test limits** - Ensure they work as expected

## Testing

```typescript
import { describe, it, expect } from 'vitest';

describe('Rate Limiting', () => {
  it('should allow requests under limit', async () => {
    for (let i = 0; i < 5; i++) {
      const response = await request(app).post('/login').send({
        email: 'test@example.com',
        password: 'wrong',
      });

      expect(response.status).toBe(401); // Wrong password, but not rate limited
    }
  });

  it('should block requests over limit', async () => {
    // Make 5 requests (limit)
    for (let i = 0; i < 5; i++) {
      await request(app).post('/login').send({
        email: 'test@example.com',
        password: 'wrong',
      });
    }

    // 6th request should be blocked
    const response = await request(app).post('/login').send({
      email: 'test@example.com',
      password: 'wrong',
    });

    expect(response.status).toBe(429);
    expect(response.body.error).toContain('Too many requests');
  });

  it('should include rate limit headers', async () => {
    const response = await request(app).get('/api/data');

    expect(response.headers).toHaveProperty('x-ratelimit-limit');
    expect(response.headers).toHaveProperty('x-ratelimit-remaining');
    expect(response.headers).toHaveProperty('x-ratelimit-reset');
  });
});
```

## Checklist

- [ ] Rate limiting on all public endpoints
- [ ] Stricter limits on auth endpoints
- [ ] Distributed rate limiting for multi-server
- [ ] Proper rate limit headers returned
- [ ] Graceful handling of storage failures
- [ ] Whitelisting for trusted clients
- [ ] Logging of rate limit violations
- [ ] Tests for rate limiting
- [ ] Documentation for API consumers
- [ ] Monitoring of rate limit metrics
