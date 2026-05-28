# Rate Limiting & Throttling

## Patterns

### **Token Bucket**
  #### **Name**
Token Bucket Algorithm
  #### **Description**
Classic rate limiting with burst allowance
  #### **When**
Need to allow short bursts while maintaining average rate
  #### **Pattern**
    // Token bucket: Tokens accumulate, requests consume them
    // Allows bursts up to bucket size
    
    class TokenBucket {
      private tokens: number;
      private lastRefill: number;
    
      constructor(
        private capacity: number,     // Max tokens (burst limit)
        private refillRate: number,   // Tokens per second
      ) {
        this.tokens = capacity;
        this.lastRefill = Date.now();
      }
    
      tryConsume(tokens: number = 1): boolean {
        this.refill();
    
        if (this.tokens >= tokens) {
          this.tokens -= tokens;
          return true;
        }
        return false;
      }
    
      private refill() {
        const now = Date.now();
        const elapsed = (now - this.lastRefill) / 1000;
        this.tokens = Math.min(
          this.capacity,
          this.tokens + elapsed * this.refillRate
        );
        this.lastRefill = now;
      }
    
      getWaitTime(): number {
        if (this.tokens >= 1) return 0;
        const tokensNeeded = 1 - this.tokens;
        return Math.ceil(tokensNeeded / this.refillRate * 1000);
      }
    }
    
    // Usage
    const bucket = new TokenBucket(10, 1);  // 10 burst, 1/sec sustained
    
    if (bucket.tryConsume()) {
      // Process request
    } else {
      const waitMs = bucket.getWaitTime();
      res.set('Retry-After', Math.ceil(waitMs / 1000));
      res.status(429).json({ error: 'Rate limited', retryAfter: waitMs });
    }
    
  #### **Why**
Token bucket allows natural burst patterns while enforcing sustained rates
### **Sliding Window**
  #### **Name**
Sliding Window Rate Limiter
  #### **Description**
Accurate rate limiting without burst allowance
  #### **When**
Need strict per-minute/hour limits without bursts
  #### **Pattern**
    import Redis from 'ioredis';
    
    const redis = new Redis();
    
    // Sliding window log: Track exact timestamps
    async function slidingWindowLog(
      key: string,
      limit: number,
      windowMs: number
    ): Promise<{ allowed: boolean; remaining: number }> {
      const now = Date.now();
      const windowStart = now - windowMs;
    
      const multi = redis.multi();
    
      // Remove old entries
      multi.zremrangebyscore(key, 0, windowStart);
    
      // Count current entries
      multi.zcard(key);
    
      // Add current request (tentatively)
      multi.zadd(key, now, `${now}-${Math.random()}`);
    
      // Set expiry
      multi.expire(key, Math.ceil(windowMs / 1000));
    
      const results = await multi.exec();
      const count = results[1][1] as number;
    
      if (count >= limit) {
        // Over limit - remove the entry we just added
        await redis.zremrangebyscore(key, now, now);
        return { allowed: false, remaining: 0 };
      }
    
      return { allowed: true, remaining: limit - count - 1 };
    }
    
    // Sliding window counter: Memory-efficient approximation
    async function slidingWindowCounter(
      key: string,
      limit: number,
      windowMs: number
    ): Promise<{ allowed: boolean; remaining: number }> {
      const now = Date.now();
      const currentWindow = Math.floor(now / windowMs);
      const previousWindow = currentWindow - 1;
      const windowProgress = (now % windowMs) / windowMs;
    
      const currentKey = `${key}:${currentWindow}`;
      const previousKey = `${key}:${previousWindow}`;
    
      // Get counts from both windows
      const [current, previous] = await redis.mget(currentKey, previousKey);
    
      const currentCount = parseInt(current || '0');
      const previousCount = parseInt(previous || '0');
    
      // Weighted count based on window progress
      const count = previousCount * (1 - windowProgress) + currentCount;
    
      if (count >= limit) {
        return { allowed: false, remaining: 0 };
      }
    
      // Increment current window
      await redis.multi()
        .incr(currentKey)
        .expire(currentKey, Math.ceil(windowMs / 1000 * 2))
        .exec();
    
      return { allowed: true, remaining: Math.floor(limit - count - 1) };
    }
    
  #### **Why**
Sliding window provides accurate limiting without burst spikes at window boundaries
### **Fixed Window**
  #### **Name**
Fixed Window Rate Limiter
  #### **Description**
Simple but has edge case at window boundaries
  #### **When**
Simple rate limiting, boundary spike is acceptable
  #### **Pattern**
    import Redis from 'ioredis';
    
    const redis = new Redis();
    
    async function fixedWindow(
      key: string,
      limit: number,
      windowSeconds: number
    ): Promise<{ allowed: boolean; remaining: number; reset: number }> {
      const window = Math.floor(Date.now() / 1000 / windowSeconds);
      const windowKey = `${key}:${window}`;
    
      const count = await redis.incr(windowKey);
    
      if (count === 1) {
        await redis.expire(windowKey, windowSeconds);
      }
    
      const reset = (window + 1) * windowSeconds;
    
      if (count > limit) {
        return {
          allowed: false,
          remaining: 0,
          reset,
        };
      }
    
      return {
        allowed: true,
        remaining: limit - count,
        reset,
      };
    }
    
    // Usage
    const result = await fixedWindow(`user:${userId}`, 100, 60);  // 100/min
    
    if (!result.allowed) {
      res.set('X-RateLimit-Limit', '100');
      res.set('X-RateLimit-Remaining', '0');
      res.set('X-RateLimit-Reset', result.reset.toString());
      res.status(429).json({ error: 'Rate limited' });
    }
    
  #### **Why**
Fixed window is simple to implement but can allow 2x limit at window boundaries
### **Express Middleware**
  #### **Name**
Express Rate Limiting Middleware
  #### **Description**
Production-ready rate limiting for Express
  #### **When**
Building Express API with rate limiting
  #### **Pattern**
    import rateLimit from 'express-rate-limit';
    import RedisStore from 'rate-limit-redis';
    import Redis from 'ioredis';
    
    const redis = new Redis(process.env.REDIS_URL);
    
    // Basic rate limiter
    const limiter = rateLimit({
      windowMs: 60 * 1000,  // 1 minute
      max: 100,             // 100 requests per window
      standardHeaders: true, // Return rate limit info in headers
      legacyHeaders: false,
      store: new RedisStore({
        sendCommand: (...args: string[]) => redis.call(...args),
      }),
      message: { error: 'Too many requests, please try again later' },
      keyGenerator: (req) => {
        // Use authenticated user ID if available, else IP
        return req.user?.id || req.ip;
      },
    });
    
    // Different limits for different endpoints
    const authLimiter = rateLimit({
      windowMs: 15 * 60 * 1000,  // 15 minutes
      max: 5,                    // 5 attempts
      skipSuccessfulRequests: true,  // Only count failures
      message: { error: 'Too many login attempts' },
    });
    
    const apiLimiter = rateLimit({
      windowMs: 60 * 1000,
      max: 1000,  // Higher limit for authenticated API
      skip: (req) => !req.user,  // Only limit authenticated users
    });
    
    // Apply to routes
    app.use('/api/', limiter);
    app.use('/auth/login', authLimiter);
    app.use('/api/v1/', apiLimiter);
    
    // Custom limiter with tiered limits
    const tieredLimiter = rateLimit({
      windowMs: 60 * 1000,
      max: (req) => {
        // Different limits based on plan
        const plan = req.user?.plan || 'free';
        const limits = {
          free: 60,
          pro: 600,
          enterprise: 6000,
        };
        return limits[plan] || 60;
      },
      keyGenerator: (req) => req.user?.id || req.ip,
    });
    
  #### **Why**
express-rate-limit provides battle-tested rate limiting with Redis support
### **Rate Limiter Flexible**
  #### **Name**
Flexible Rate Limiting Library
  #### **Description**
Advanced rate limiting with multiple strategies
  #### **When**
Need complex rate limiting logic
  #### **Pattern**
    import {
      RateLimiterRedis,
      RateLimiterMemory,
      RateLimiterUnion,
    } from 'rate-limiter-flexible';
    import Redis from 'ioredis';
    
    const redis = new Redis();
    
    // Per-user rate limiter
    const userLimiter = new RateLimiterRedis({
      storeClient: redis,
      keyPrefix: 'rl:user',
      points: 100,      // 100 requests
      duration: 60,     // Per minute
      blockDuration: 60, // Block for 1 min if exceeded
    });
    
    // Per-IP rate limiter (stricter)
    const ipLimiter = new RateLimiterRedis({
      storeClient: redis,
      keyPrefix: 'rl:ip',
      points: 30,
      duration: 60,
    });
    
    // Combined limiter (both must pass)
    const combinedLimiter = new RateLimiterUnion(userLimiter, ipLimiter);
    
    // Middleware
    async function rateLimitMiddleware(req, res, next) {
      const userId = req.user?.id || 'anonymous';
      const ip = req.ip;
    
      try {
        // Consume from both limiters
        await Promise.all([
          userLimiter.consume(userId),
          ipLimiter.consume(ip),
        ]);
        next();
      } catch (error) {
        if (error instanceof Error) {
          return next(error);
        }
        // RateLimiterRes object
        const retryAfter = Math.ceil(error.msBeforeNext / 1000);
        res.set('Retry-After', retryAfter);
        res.status(429).json({
          error: 'Rate limited',
          retryAfter,
        });
      }
    }
    
    // Endpoint-specific limiter
    const endpointLimiters = {
      '/api/search': new RateLimiterRedis({
        storeClient: redis,
        keyPrefix: 'rl:search',
        points: 10,
        duration: 60,
      }),
      '/api/export': new RateLimiterRedis({
        storeClient: redis,
        keyPrefix: 'rl:export',
        points: 5,
        duration: 3600,  // Per hour
      }),
    };
    
    // Weighted consumption (expensive operations cost more)
    async function consumeWeighted(key: string, weight: number) {
      await userLimiter.consume(key, weight);
    }
    
    // Check without consuming
    async function checkLimit(key: string) {
      const result = await userLimiter.get(key);
      return {
        remaining: result ? result.remainingPoints : 100,
        reset: result ? new Date(Date.now() + result.msBeforeNext) : null,
      };
    }
    
  #### **Why**
rate-limiter-flexible offers the most flexibility for complex scenarios
### **Redis Distributed**
  #### **Name**
Distributed Rate Limiting with Redis
  #### **Description**
Consistent rate limiting across multiple servers
  #### **When**
Running multiple API servers
  #### **Pattern**
    import Redis from 'ioredis';
    
    const redis = new Redis(process.env.REDIS_URL);
    
    // Atomic Lua script for race-free limiting
    const SLIDING_WINDOW_SCRIPT = `
      local key = KEYS[1]
      local now = tonumber(ARGV[1])
      local window = tonumber(ARGV[2])
      local limit = tonumber(ARGV[3])
    
      -- Remove old entries
      redis.call('ZREMRANGEBYSCORE', key, 0, now - window)
    
      -- Count current entries
      local count = redis.call('ZCARD', key)
    
      if count < limit then
        -- Add new entry
        redis.call('ZADD', key, now, now .. '-' .. math.random())
        redis.call('EXPIRE', key, math.ceil(window / 1000))
        return {1, limit - count - 1}
      end
    
      return {0, 0}
    `;
    
    async function checkRateLimit(
      key: string,
      limit: number,
      windowMs: number
    ): Promise<{ allowed: boolean; remaining: number }> {
      const result = await redis.eval(
        SLIDING_WINDOW_SCRIPT,
        1,
        key,
        Date.now(),
        windowMs,
        limit
      ) as [number, number];
    
      return {
        allowed: result[0] === 1,
        remaining: result[1],
      };
    }
    
    // Token bucket with Lua for atomicity
    const TOKEN_BUCKET_SCRIPT = `
      local key = KEYS[1]
      local capacity = tonumber(ARGV[1])
      local rate = tonumber(ARGV[2])
      local now = tonumber(ARGV[3])
      local requested = tonumber(ARGV[4])
    
      local bucket = redis.call('HMGET', key, 'tokens', 'last_refill')
      local tokens = tonumber(bucket[1]) or capacity
      local last_refill = tonumber(bucket[2]) or now
    
      -- Refill tokens
      local elapsed = (now - last_refill) / 1000
      tokens = math.min(capacity, tokens + elapsed * rate)
    
      if tokens >= requested then
        tokens = tokens - requested
        redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
        redis.call('EXPIRE', key, math.ceil(capacity / rate) + 1)
        return {1, tokens}
      end
    
      redis.call('HMSET', key, 'tokens', tokens, 'last_refill', now)
      return {0, tokens}
    `;
    
    async function tokenBucketConsume(
      key: string,
      capacity: number,
      rate: number,
      tokens: number = 1
    ): Promise<{ allowed: boolean; remaining: number }> {
      const result = await redis.eval(
        TOKEN_BUCKET_SCRIPT,
        1,
        key,
        capacity,
        rate,
        Date.now(),
        tokens
      ) as [number, number];
    
      return {
        allowed: result[0] === 1,
        remaining: Math.floor(result[1]),
      };
    }
    
  #### **Why**
Lua scripts ensure atomic operations across distributed systems
### **Tiered Limits**
  #### **Name**
Tiered Rate Limits by Plan
  #### **Description**
Different limits for different subscription tiers
  #### **When**
SaaS with multiple pricing tiers
  #### **Pattern**
    import { RateLimiterRedis } from 'rate-limiter-flexible';
    
    // Define limits by plan
    const PLAN_LIMITS = {
      free: {
        requests: { points: 100, duration: 3600 },      // 100/hour
        apiCalls: { points: 1000, duration: 86400 },    // 1000/day
        exports: { points: 5, duration: 86400 },        // 5/day
      },
      pro: {
        requests: { points: 1000, duration: 3600 },     // 1000/hour
        apiCalls: { points: 50000, duration: 86400 },   // 50k/day
        exports: { points: 100, duration: 86400 },      // 100/day
      },
      enterprise: {
        requests: { points: 10000, duration: 3600 },
        apiCalls: { points: 500000, duration: 86400 },
        exports: { points: 1000, duration: 86400 },
      },
    };
    
    // Create limiters dynamically
    function getLimiter(userId: string, plan: string, type: string) {
      const limits = PLAN_LIMITS[plan] || PLAN_LIMITS.free;
      const config = limits[type];
    
      return new RateLimiterRedis({
        storeClient: redis,
        keyPrefix: `rl:${type}:${plan}`,
        points: config.points,
        duration: config.duration,
      });
    }
    
    // Middleware
    async function tieredRateLimit(req, res, next) {
      const user = req.user;
      const plan = user?.plan || 'free';
      const userId = user?.id || req.ip;
    
      const limiter = getLimiter(userId, plan, 'requests');
    
      try {
        const result = await limiter.consume(userId);
    
        // Add headers
        res.set('X-RateLimit-Limit', PLAN_LIMITS[plan].requests.points);
        res.set('X-RateLimit-Remaining', result.remainingPoints);
        res.set('X-RateLimit-Reset', new Date(Date.now() + result.msBeforeNext).toISOString());
    
        next();
      } catch (rateLimiterRes) {
        res.set('X-RateLimit-Limit', PLAN_LIMITS[plan].requests.points);
        res.set('X-RateLimit-Remaining', 0);
        res.set('Retry-After', Math.ceil(rateLimiterRes.msBeforeNext / 1000));
    
        res.status(429).json({
          error: 'Rate limit exceeded',
          limit: PLAN_LIMITS[plan].requests.points,
          retryAfter: Math.ceil(rateLimiterRes.msBeforeNext / 1000),
          upgradeUrl: plan === 'free' ? '/pricing' : undefined,
        });
      }
    }
    
    // Check quota without consuming
    async function getQuotaStatus(userId: string, plan: string) {
      const status = {};
    
      for (const [type, config] of Object.entries(PLAN_LIMITS[plan])) {
        const limiter = getLimiter(userId, plan, type);
        const result = await limiter.get(userId);
    
        status[type] = {
          limit: config.points,
          remaining: result ? result.remainingPoints : config.points,
          reset: result ? new Date(Date.now() + result.msBeforeNext) : null,
        };
      }
    
      return status;
    }
    
  #### **Why**
Tiered limits monetize API access and prevent abuse
### **Rate Limit Headers**
  #### **Name**
Standard Rate Limit Headers
  #### **Description**
Communicate rate limit status to clients
  #### **When**
Any rate-limited API
  #### **Pattern**
    // Standard headers (draft-ietf-httpapi-ratelimit-headers)
    function setRateLimitHeaders(
      res: Response,
      limit: number,
      remaining: number,
      reset: Date
    ) {
      // Standard headers
      res.set('RateLimit-Limit', limit.toString());
      res.set('RateLimit-Remaining', Math.max(0, remaining).toString());
      res.set('RateLimit-Reset', Math.ceil(reset.getTime() / 1000).toString());
    
      // Legacy headers (still widely used)
      res.set('X-RateLimit-Limit', limit.toString());
      res.set('X-RateLimit-Remaining', Math.max(0, remaining).toString());
      res.set('X-RateLimit-Reset', Math.ceil(reset.getTime() / 1000).toString());
    }
    
    // 429 response with retry info
    function sendRateLimitError(
      res: Response,
      retryAfter: number,
      message?: string
    ) {
      res.set('Retry-After', retryAfter.toString());
      res.status(429).json({
        error: 'Too Many Requests',
        message: message || 'Rate limit exceeded. Please slow down.',
        retryAfter,
        documentation: 'https://api.example.com/docs/rate-limits',
      });
    }
    
    // Include in successful responses too
    app.use((req, res, next) => {
      const originalJson = res.json.bind(res);
    
      res.json = function(body) {
        // Add rate limit info to all responses
        if (req.rateLimit) {
          setRateLimitHeaders(
            res,
            req.rateLimit.limit,
            req.rateLimit.remaining,
            req.rateLimit.reset
          );
        }
        return originalJson(body);
      };
    
      next();
    });
    
  #### **Why**
Clients need rate limit info to implement proper backoff

## Anti-Patterns

### **Memory Only**
  #### **Name**
In-Memory Rate Limiting in Production
  #### **Description**
Rate limits reset on restart, don't work across servers
  #### **Problem**
    const limits = new Map();  // Lost on restart!
    
    function rateLimit(userId) {
      const count = limits.get(userId) || 0;
      if (count > 100) return false;
      limits.set(userId, count + 1);
      return true;
    }
    
  #### **Solution**
    Use Redis or similar distributed store:
    
    import { RateLimiterRedis } from 'rate-limiter-flexible';
    
    const limiter = new RateLimiterRedis({
      storeClient: redis,
      points: 100,
      duration: 60,
    });
    
  #### **Impact**
Rate limits reset on deploy, bypassed by hitting different servers
### **Fixed Window Only**
  #### **Name**
Fixed Window Without Sliding
  #### **Description**
Allows 2x limit at window boundaries
  #### **Problem**
    // User makes 100 requests at 11:59:59
    // Window resets at 12:00:00
    // User makes 100 more requests at 12:00:01
    // = 200 requests in 2 seconds
    
    const window = Math.floor(Date.now() / 60000);
    const key = `ratelimit:${userId}:${window}`;
    
  #### **Solution**
    Use sliding window:
    
    // Sliding window counter is still efficient
    const current = Math.floor(Date.now() / 60000);
    const previous = current - 1;
    const progress = (Date.now() % 60000) / 60000;
    
    const count = previousCount * (1 - progress) + currentCount;
    
  #### **Impact**
Burst of 2x limit at window boundaries
### **No Headers**
  #### **Name**
No Rate Limit Response Headers
  #### **Description**
Clients can't implement proper backoff
  #### **Problem**
    if (isRateLimited) {
      res.status(429).json({ error: 'Too many requests' });
      // No Retry-After, no remaining count
    }
    
  #### **Solution**
    Always include rate limit headers:
    
    res.set('Retry-After', retrySeconds.toString());
    res.set('X-RateLimit-Limit', limit.toString());
    res.set('X-RateLimit-Remaining', remaining.toString());
    res.set('X-RateLimit-Reset', resetTimestamp.toString());
    
  #### **Impact**
Clients hammer API blindly, can't implement backoff
### **Client Ip Only**
  #### **Name**
Rate Limiting by IP Only
  #### **Description**
Shared IPs (NAT, VPN, office) affect all users
  #### **Problem**
    const key = `ratelimit:${req.ip}`;  // All office users share limit!
    
  #### **Solution**
    Prefer user ID when available:
    
    const key = req.user?.id
      ? `ratelimit:user:${req.user.id}`
      : `ratelimit:ip:${req.ip}`;
    
    // Or combine both
    await userLimiter.consume(req.user?.id || 'anonymous');
    await ipLimiter.consume(req.ip);  // Stricter, catches abuse
    
  #### **Impact**
Legitimate users blocked due to shared IP
### **No Bypass For Health**
  #### **Name**
Rate Limiting Health Check Endpoints
  #### **Description**
Orchestration can't check health
  #### **Problem**
    app.use(rateLimit({ max: 100 }));  // Applies to ALL routes
    app.get('/health', (req, res) => res.json({ ok: true }));
    
  #### **Solution**
    Exclude health and internal endpoints:
    
    const limiter = rateLimit({
      skip: (req) => {
        return req.path === '/health' ||
               req.path.startsWith('/internal/') ||
               req.headers['x-internal-key'] === process.env.INTERNAL_KEY;
      },
    });
    
  #### **Impact**
Load balancer marks healthy service as unhealthy