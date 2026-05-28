---
name: Caching Strategies
description: This skill should be used when the user asks to "caching strategy, Redis, Memcached, cache invalidation, CDN cache, cache patterns, distributed cache, cache-aside, write-through, cache warming", or needs help with Redis, Memcached, CDN caching, and cache invalidation strategies.
version: 1.0.0
---

# Caching Strategies

Comprehensive guidance for implementing caching at multiple layers including application caching with Redis/Memcached, CDN caching, browser caching, and cache invalidation patterns.

## Caching Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Client Browser                            │
│                    [Browser Cache / Local Storage]               │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                           CDN                                    │
│              [Edge Cache - CloudFront/Cloudflare]               │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      API Gateway                                 │
│                    [Response Cache]                              │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                     Application Layer                            │
│              [Redis/Memcached - Distributed Cache]              │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                        Database                                  │
│                   [Query Cache / Buffer Pool]                    │
└─────────────────────────────────────────────────────────────────┘
```

## Redis Caching

### Redis Setup

```yaml
# docker-compose.yml - Redis cluster
version: '3.8'

services:
  redis-master:
    image: redis:7-alpine
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis-replica:
    image: redis:7-alpine
    command: redis-server --replicaof redis-master 6379 --appendonly yes
    depends_on:
      - redis-master

  redis-sentinel:
    image: redis:7-alpine
    command: redis-sentinel /etc/redis/sentinel.conf
    volumes:
      - ./sentinel.conf:/etc/redis/sentinel.conf
    depends_on:
      - redis-master
      - redis-replica

volumes:
  redis_data:
```

### Redis Client Configuration

```javascript
// redis.js - Node.js Redis client with connection pooling
const Redis = require('ioredis');

const redis = new Redis({
    host: process.env.REDIS_HOST || 'localhost',
    port: process.env.REDIS_PORT || 6379,
    password: process.env.REDIS_PASSWORD,
    db: 0,

    // Connection options
    retryDelayOnFailover: 100,
    maxRetriesPerRequest: 3,
    enableReadyCheck: true,

    // Connection pooling
    lazyConnect: true,

    // Sentinel configuration (for HA)
    sentinels: process.env.REDIS_SENTINELS ? [
        { host: 'sentinel-1', port: 26379 },
        { host: 'sentinel-2', port: 26379 },
        { host: 'sentinel-3', port: 26379 },
    ] : undefined,
    name: 'mymaster',
});

redis.on('error', (err) => {
    console.error('Redis connection error:', err);
});

redis.on('connect', () => {
    console.log('Connected to Redis');
});

module.exports = redis;
```

### Python Redis Client

```python
# cache.py - Python Redis caching with type hints
import json
import pickle
from typing import Any, Optional, TypeVar, Callable
from functools import wraps
import redis
from redis.sentinel import Sentinel

T = TypeVar('T')

class RedisCache:
    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0,
                 password: Optional[str] = None, prefix: str = ''):
        self.redis = redis.Redis(
            host=host,
            port=port,
            db=db,
            password=password,
            decode_responses=False,
            socket_connect_timeout=5,
            socket_timeout=5,
        )
        self.prefix = prefix

    def _key(self, key: str) -> str:
        return f"{self.prefix}{key}" if self.prefix else key

    def get(self, key: str, default: T = None) -> Optional[T]:
        """Get value from cache."""
        try:
            value = self.redis.get(self._key(key))
            if value is None:
                return default
            return pickle.loads(value)
        except (redis.RedisError, pickle.PickleError) as e:
            print(f"Cache get error: {e}")
            return default

    def set(self, key: str, value: Any, ttl: int = 3600) -> bool:
        """Set value in cache with TTL."""
        try:
            serialized = pickle.dumps(value)
            return self.redis.setex(self._key(key), ttl, serialized)
        except (redis.RedisError, pickle.PickleError) as e:
            print(f"Cache set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        try:
            return bool(self.redis.delete(self._key(key)))
        except redis.RedisError as e:
            print(f"Cache delete error: {e}")
            return False

    def delete_pattern(self, pattern: str) -> int:
        """Delete all keys matching pattern."""
        try:
            keys = self.redis.keys(self._key(pattern))
            if keys:
                return self.redis.delete(*keys)
            return 0
        except redis.RedisError as e:
            print(f"Cache delete pattern error: {e}")
            return 0

    def get_or_set(self, key: str, factory: Callable[[], T], ttl: int = 3600) -> T:
        """Get from cache or compute and store."""
        value = self.get(key)
        if value is not None:
            return value

        value = factory()
        self.set(key, value, ttl)
        return value


def cached(cache: RedisCache, key_template: str, ttl: int = 3600):
    """Decorator for caching function results."""
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            # Build cache key from template and arguments
            cache_key = key_template.format(*args, **kwargs)

            # Try to get from cache
            cached_value = cache.get(cache_key)
            if cached_value is not None:
                return cached_value

            # Compute and cache
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result

        # Add cache control methods
        wrapper.invalidate = lambda *args, **kwargs: cache.delete(
            key_template.format(*args, **kwargs)
        )

        return wrapper
    return decorator


# Usage example
cache = RedisCache(prefix='myapp:')

@cached(cache, 'user:{0}', ttl=300)
def get_user(user_id: int) -> dict:
    """Fetch user from database (cached for 5 minutes)."""
    # Database query here
    return {'id': user_id, 'name': 'John'}

# Invalidate specific user cache
get_user.invalidate(123)
```

## Caching Patterns

### Cache-Aside (Lazy Loading)

```javascript
// cache-aside.js
class CacheAsideService {
    constructor(cache, db) {
        this.cache = cache;
        this.db = db;
    }

    async get(key) {
        // 1. Check cache first
        let data = await this.cache.get(key);

        if (data) {
            console.log('Cache hit:', key);
            return JSON.parse(data);
        }

        console.log('Cache miss:', key);

        // 2. Load from database
        data = await this.db.findOne({ id: key });

        if (data) {
            // 3. Store in cache for next time
            await this.cache.setex(key, 3600, JSON.stringify(data));
        }

        return data;
    }

    async update(key, data) {
        // 1. Update database first
        await this.db.update({ id: key }, data);

        // 2. Invalidate cache (next read will refresh)
        await this.cache.del(key);
    }
}
```

### Write-Through Cache

```javascript
// write-through.js
class WriteThroughService {
    constructor(cache, db) {
        this.cache = cache;
        this.db = db;
    }

    async get(key) {
        // Read from cache (always populated)
        const data = await this.cache.get(key);
        return data ? JSON.parse(data) : null;
    }

    async set(key, data) {
        // 1. Write to database
        await this.db.upsert({ id: key }, data);

        // 2. Write to cache (synchronously)
        await this.cache.setex(key, 3600, JSON.stringify(data));

        return data;
    }
}
```

### Write-Behind (Write-Back) Cache

```javascript
// write-behind.js
class WriteBehindService {
    constructor(cache, db, writeQueue) {
        this.cache = cache;
        this.db = db;
        this.writeQueue = writeQueue;
    }

    async set(key, data) {
        // 1. Write to cache immediately
        await this.cache.setex(key, 3600, JSON.stringify(data));

        // 2. Queue async write to database
        await this.writeQueue.add('db-write', {
            key,
            data,
            timestamp: Date.now(),
        });

        return data;
    }
}

// Queue processor (Bull/BullMQ)
const Queue = require('bullmq');

const dbWriteProcessor = async (job) => {
    const { key, data } = job.data;
    await db.upsert({ id: key }, data);
};
```

### Read-Through Cache

```javascript
// read-through.js - Automatic cache population
class ReadThroughCache {
    constructor(redis, loaders) {
        this.redis = redis;
        this.loaders = loaders; // Map of key patterns to loader functions
    }

    async get(key) {
        // Check cache
        let data = await this.redis.get(key);

        if (data) {
            return JSON.parse(data);
        }

        // Find matching loader
        const loader = this.findLoader(key);
        if (!loader) {
            throw new Error(`No loader for key: ${key}`);
        }

        // Load data
        data = await loader.load(key);

        // Store in cache
        await this.redis.setex(key, loader.ttl, JSON.stringify(data));

        return data;
    }

    findLoader(key) {
        for (const [pattern, loader] of this.loaders) {
            if (key.match(pattern)) {
                return loader;
            }
        }
        return null;
    }
}

// Usage
const cache = new ReadThroughCache(redis, new Map([
    [/^user:\d+$/, {
        ttl: 300,
        load: (key) => db.users.findById(key.split(':')[1])
    }],
    [/^product:\d+$/, {
        ttl: 600,
        load: (key) => db.products.findById(key.split(':')[1])
    }],
]));
```

## Cache Invalidation

### Time-Based (TTL)

```javascript
// Simple TTL-based expiration
await redis.setex('user:123', 300, JSON.stringify(user)); // 5 minutes

// Sliding expiration (refresh on read)
async function getWithSlidingExpiry(key, ttl) {
    const data = await redis.get(key);
    if (data) {
        // Refresh TTL on access
        await redis.expire(key, ttl);
    }
    return data;
}
```

### Event-Based Invalidation

```javascript
// event-invalidation.js
const EventEmitter = require('events');

class CacheInvalidator extends EventEmitter {
    constructor(redis, pubsub) {
        super();
        this.redis = redis;
        this.pubsub = pubsub;

        // Subscribe to invalidation events
        this.pubsub.subscribe('cache:invalidate', (message) => {
            this.handleInvalidation(JSON.parse(message));
        });
    }

    async invalidate(pattern, reason = 'manual') {
        // Publish to all instances
        await this.pubsub.publish('cache:invalidate', JSON.stringify({
            pattern,
            reason,
            timestamp: Date.now(),
        }));
    }

    async handleInvalidation({ pattern, reason }) {
        console.log(`Invalidating cache: ${pattern} (${reason})`);

        const keys = await this.redis.keys(pattern);
        if (keys.length > 0) {
            await this.redis.del(...keys);
        }

        this.emit('invalidated', { pattern, count: keys.length });
    }
}

// Usage with database events
db.on('user:updated', async (user) => {
    await cacheInvalidator.invalidate(`user:${user.id}*`, 'user_updated');
});

db.on('user:deleted', async (userId) => {
    await cacheInvalidator.invalidate(`user:${userId}*`, 'user_deleted');
});
```

### Tag-Based Invalidation

```javascript
// tag-invalidation.js
class TaggedCache {
    constructor(redis) {
        this.redis = redis;
    }

    async set(key, value, ttl, tags = []) {
        const pipeline = this.redis.pipeline();

        // Store the value
        pipeline.setex(key, ttl, JSON.stringify(value));

        // Add key to each tag set
        for (const tag of tags) {
            pipeline.sadd(`tag:${tag}`, key);
            pipeline.expire(`tag:${tag}`, ttl);
        }

        await pipeline.exec();
    }

    async invalidateByTag(tag) {
        const keys = await this.redis.smembers(`tag:${tag}`);

        if (keys.length > 0) {
            const pipeline = this.redis.pipeline();
            pipeline.del(...keys);
            pipeline.del(`tag:${tag}`);
            await pipeline.exec();
        }

        return keys.length;
    }
}

// Usage
const cache = new TaggedCache(redis);

// Cache user with tags
await cache.set('user:123', userData, 3600, ['users', 'team:engineering']);

// Cache product with tags
await cache.set('product:456', productData, 3600, ['products', 'category:electronics']);

// Invalidate all user caches
await cache.invalidateByTag('users');

// Invalidate everything for a team
await cache.invalidateByTag('team:engineering');
```

## CDN Caching

### CloudFront Configuration

```yaml
# CloudFront distribution (AWS CDK)
const distribution = new cloudfront.Distribution(this, 'Distribution', {
  defaultBehavior: {
    origin: new origins.S3Origin(bucket),
    viewerProtocolPolicy: cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
    cachePolicy: new cloudfront.CachePolicy(this, 'CachePolicy', {
      defaultTtl: Duration.days(1),
      maxTtl: Duration.days(365),
      minTtl: Duration.seconds(0),
      enableAcceptEncodingGzip: true,
      enableAcceptEncodingBrotli: true,
      headerBehavior: cloudfront.CacheHeaderBehavior.allowList(
        'Authorization',
        'Accept-Language'
      ),
      queryStringBehavior: cloudfront.CacheQueryStringBehavior.allowList(
        'version',
        'lang'
      ),
      cookieBehavior: cloudfront.CacheCookieBehavior.none(),
    }),
    responseHeadersPolicy: new cloudfront.ResponseHeadersPolicy(this, 'SecurityHeaders', {
      securityHeadersBehavior: {
        strictTransportSecurity: {
          accessControlMaxAge: Duration.days(365),
          includeSubdomains: true,
          preload: true,
        },
        contentTypeOptions: { override: true },
        frameOptions: {
          frameOption: cloudfront.HeadersFrameOption.DENY,
          override: true
        },
      },
    }),
  },
  additionalBehaviors: {
    '/api/*': {
      origin: new origins.HttpOrigin('api.example.com'),
      cachePolicy: cloudfront.CachePolicy.CACHING_DISABLED,
      originRequestPolicy: cloudfront.OriginRequestPolicy.ALL_VIEWER,
    },
    '/static/*': {
      origin: new origins.S3Origin(staticBucket),
      cachePolicy: cloudfront.CachePolicy.CACHING_OPTIMIZED,
    },
  },
});
```

### Cache-Control Headers

```javascript
// Express middleware for cache headers
function cacheControl(options = {}) {
    const {
        maxAge = 0,
        sMaxAge = null,
        staleWhileRevalidate = null,
        staleIfError = null,
        private: isPrivate = false,
        noStore = false,
        noCache = false,
        mustRevalidate = false,
    } = options;

    return (req, res, next) => {
        const directives = [];

        if (noStore) {
            directives.push('no-store');
        } else {
            if (noCache) {
                directives.push('no-cache');
            }

            directives.push(isPrivate ? 'private' : 'public');
            directives.push(`max-age=${maxAge}`);

            if (sMaxAge !== null) {
                directives.push(`s-maxage=${sMaxAge}`);
            }

            if (staleWhileRevalidate !== null) {
                directives.push(`stale-while-revalidate=${staleWhileRevalidate}`);
            }

            if (staleIfError !== null) {
                directives.push(`stale-if-error=${staleIfError}`);
            }

            if (mustRevalidate) {
                directives.push('must-revalidate');
            }
        }

        res.set('Cache-Control', directives.join(', '));
        next();
    };
}

// Usage
app.use('/static', cacheControl({
    maxAge: 31536000,  // 1 year
    sMaxAge: 31536000,
}));

app.use('/api', cacheControl({
    maxAge: 0,
    sMaxAge: 60,  // CDN caches for 1 minute
    staleWhileRevalidate: 86400,
}));

app.use('/user', cacheControl({
    private: true,
    maxAge: 300,
    mustRevalidate: true,
}));
```

### ETag Implementation

```javascript
// etag.js - Entity tag for conditional requests
const crypto = require('crypto');

function generateETag(content) {
    const hash = crypto.createHash('md5').update(content).digest('hex');
    return `"${hash}"`;
}

function etagMiddleware(req, res, next) {
    const originalSend = res.send.bind(res);

    res.send = function(body) {
        if (req.method === 'GET' && res.statusCode === 200) {
            const etag = generateETag(typeof body === 'string' ? body : JSON.stringify(body));
            res.set('ETag', etag);

            const ifNoneMatch = req.headers['if-none-match'];
            if (ifNoneMatch === etag) {
                return res.status(304).end();
            }
        }

        return originalSend(body);
    };

    next();
}
```

## Cache Warming

```javascript
// cache-warmer.js
class CacheWarmer {
    constructor(cache, db) {
        this.cache = cache;
        this.db = db;
    }

    async warmPopularItems(limit = 100) {
        console.log(`Warming cache with top ${limit} items...`);

        // Get most accessed items
        const popularItems = await this.db.items
            .find()
            .sort({ accessCount: -1 })
            .limit(limit);

        const pipeline = this.cache.pipeline();

        for (const item of popularItems) {
            pipeline.setex(
                `item:${item.id}`,
                3600,
                JSON.stringify(item)
            );
        }

        await pipeline.exec();
        console.log(`Warmed ${popularItems.length} items`);
    }

    async warmUserSessions(userIds) {
        console.log(`Warming sessions for ${userIds.length} users...`);

        const users = await this.db.users.find({
            _id: { $in: userIds }
        });

        const pipeline = this.cache.pipeline();

        for (const user of users) {
            pipeline.setex(
                `user:${user.id}`,
                1800,
                JSON.stringify(user)
            );
        }

        await pipeline.exec();
    }

    // Schedule warming
    scheduleWarming() {
        // Warm at startup
        this.warmPopularItems();

        // Refresh every hour
        setInterval(() => {
            this.warmPopularItems();
        }, 60 * 60 * 1000);
    }
}
```

## Monitoring

### Cache Metrics

```javascript
// cache-metrics.js
const promClient = require('prom-client');

const cacheHits = new promClient.Counter({
    name: 'cache_hits_total',
    help: 'Total cache hits',
    labelNames: ['cache_name', 'key_pattern'],
});

const cacheMisses = new promClient.Counter({
    name: 'cache_misses_total',
    help: 'Total cache misses',
    labelNames: ['cache_name', 'key_pattern'],
});

const cacheLatency = new promClient.Histogram({
    name: 'cache_operation_duration_seconds',
    help: 'Cache operation latency',
    labelNames: ['cache_name', 'operation'],
    buckets: [0.001, 0.005, 0.01, 0.05, 0.1],
});

class InstrumentedCache {
    constructor(cache, name = 'default') {
        this.cache = cache;
        this.name = name;
    }

    async get(key) {
        const timer = cacheLatency.startTimer({
            cache_name: this.name,
            operation: 'get'
        });

        try {
            const value = await this.cache.get(key);
            const pattern = this.getKeyPattern(key);

            if (value) {
                cacheHits.inc({ cache_name: this.name, key_pattern: pattern });
            } else {
                cacheMisses.inc({ cache_name: this.name, key_pattern: pattern });
            }

            return value;
        } finally {
            timer();
        }
    }

    getKeyPattern(key) {
        // Extract pattern like 'user:*' from 'user:123'
        return key.replace(/:\d+/g, ':*').replace(/:[a-f0-9-]{36}/g, ':*');
    }
}
```

## Best Practices Summary

| Strategy | Use Case | Consistency | Performance |
|----------|----------|-------------|-------------|
| Cache-Aside | Read-heavy, tolerates stale | Eventually consistent | Good reads |
| Write-Through | Write consistency needed | Strong | Slower writes |
| Write-Behind | High write volume | Eventually consistent | Fast writes |
| Read-Through | Automatic cache population | Eventually consistent | Simplified code |

### Cache Key Design

```
# Good key patterns
user:{user_id}                    # user:123
user:{user_id}:profile            # user:123:profile
product:{product_id}:details      # product:456:details
search:{hash(query)}              # search:a1b2c3d4
session:{session_id}              # session:abc-def-123

# Include version for cache busting
config:v2:{config_name}           # config:v2:feature_flags
```

### TTL Guidelines

| Data Type | Recommended TTL | Reason |
|-----------|-----------------|--------|
| User session | 30 min - 24 hours | Security |
| User profile | 5-15 minutes | Moderate change frequency |
| Product catalog | 1-6 hours | Infrequent updates |
| Static content | 24 hours - 1 year | Rarely changes |
| API responses | 1-5 minutes | Freshness required |
| Search results | 5-15 minutes | Balance freshness/load |
