# Rate Limiting - Sharp Edges

## Memory Rate Limit

### **Id**
memory-rate-limit
### **Summary**
In-memory rate limiting doesn't work in production
### **Severity**
critical
### **Situation**
  You implement rate limiting with a Map or in-memory store. Works in dev.
  In production, you have 5 servers. Each server has its own counter.
  User can make 5x the limit by hitting different servers.
  
### **Why**
  In-memory storage is per-process:
  - Each server instance has separate counters
  - Load balancer distributes requests across servers
  - User gets N * limit where N = server count
  - Restart resets all counters
  
### **Solution**
  Always use distributed storage in production:
  
  import { RateLimiterRedis } from 'rate-limiter-flexible';
  import Redis from 'ioredis';
  
  const redis = new Redis(process.env.REDIS_URL);
  
  const limiter = new RateLimiterRedis({
    storeClient: redis,
    keyPrefix: 'ratelimit',
    points: 100,
    duration: 60,
  });
  
  // Fallback to memory only for single-server or dev
  const fallbackLimiter = new RateLimiterMemory({
    points: 100,
    duration: 60,
  });
  
  async function rateLimit(key: string) {
    try {
      return await limiter.consume(key);
    } catch (error) {
      if (error instanceof Error) {
        // Redis down - use fallback
        console.error('Redis rate limit failed, using memory');
        return await fallbackLimiter.consume(key);
      }
      throw error;  // Rate limited
    }
  }
  
### **Symptoms**
  - Rate limits higher than configured
  - Limits reset after deploy
  - Different behavior on different servers
  - Why can they make 500 requests with 100 limit?
### **Detection Pattern**
new Map.*rate|rateLimit.*Map|limits.*=.*\\{\\}

## Fixed Window Boundary

### **Id**
fixed-window-boundary
### **Summary**
Fixed window allows 2x limit at window boundaries
### **Severity**
high
### **Situation**
  Your limit is 100 requests per minute. User makes 100 requests at 11:59:59.
  Clock ticks to 12:00:00, counter resets. User makes 100 more requests.
  200 requests in 2 seconds, system overwhelmed.
  
### **Why**
  Fixed window resets counter at exact intervals:
  - 11:59:59 → counter at 100 (limit)
  - 12:00:00 → counter resets to 0
  - 12:00:00 → 100 more requests allowed immediately
  
  This is a 2x burst at every window boundary.
  
### **Solution**
  Use sliding window for accurate limiting:
  
  // Sliding window counter (efficient approximation)
  async function slidingWindow(key: string, limit: number, windowMs: number) {
    const now = Date.now();
    const currentWindow = Math.floor(now / windowMs);
    const previousWindow = currentWindow - 1;
    const windowProgress = (now % windowMs) / windowMs;
  
    const currentKey = `${key}:${currentWindow}`;
    const previousKey = `${key}:${previousWindow}`;
  
    const [current, previous] = await redis.mget(currentKey, previousKey);
  
    const currentCount = parseInt(current || '0');
    const previousCount = parseInt(previous || '0');
  
    // Weighted average based on time into current window
    const count = previousCount * (1 - windowProgress) + currentCount;
  
    if (count >= limit) {
      return { allowed: false, count };
    }
  
    await redis.multi()
      .incr(currentKey)
      .expire(currentKey, Math.ceil(windowMs / 1000 * 2))
      .exec();
  
    return { allowed: true, count: count + 1 };
  }
  
  // Or use token bucket for smooth rate limiting
  // Tokens refill continuously, not in steps
  
### **Symptoms**
  - Traffic spikes at minute/hour boundaries
  - System overload at predictable times
  - Monitoring shows 2x expected traffic briefly
### **Detection Pattern**
Math\\.floor.*Date\\.now.*60000(?![\\s\\S]{0,500}sliding|weighted)

## Ip Only Limiting

### **Id**
ip-only-limiting
### **Summary**
IP-only limiting fails for shared IPs
### **Severity**
high
### **Situation**
  You rate limit by IP address. A large company (thousands of employees)
  shares one public IP via NAT. One employee hits the limit, everyone
  is blocked. You get angry support tickets.
  
### **Why**
  Many users share IPs:
  - Corporate NAT (all office users = 1 IP)
  - University networks
  - Mobile carriers (CGNAT)
  - VPN users
  - Coffee shops
  
  Limiting by IP punishes innocent users.
  
### **Solution**
  Prefer user identification, fall back to IP:
  
  function getRateLimitKey(req: Request): string {
    // Prefer authenticated user ID
    if (req.user?.id) {
      return `user:${req.user.id}`;
    }
  
    // For unauthenticated, combine signals
    const ip = req.ip;
    const userAgent = req.headers['user-agent'] || 'unknown';
    const fingerprint = crypto
      .createHash('sha256')
      .update(`${ip}:${userAgent}`)
      .digest('hex')
      .slice(0, 16);
  
    return `anon:${fingerprint}`;
  }
  
  // Layered limiting
  async function checkRateLimit(req: Request) {
    // Layer 1: Per-user (generous)
    if (req.user) {
      await userLimiter.consume(req.user.id);
    }
  
    // Layer 2: Per-IP (stricter, catches abuse)
    await ipLimiter.consume(req.ip);
  
    // Layer 3: Global (emergency brake)
    await globalLimiter.consume('global');
  }
  
### **Symptoms**
  - All our employees are rate limited
  - Support tickets from offices/universities
  - One user affecting others
  - False positives from VPN users
### **Detection Pattern**
rateLimit.*req\\.ip(?![\\s\\S]{0,200}user|userId)

## No Retry After

### **Id**
no-retry-after
### **Summary**
Missing Retry-After header causes client storms
### **Severity**
high
### **Situation**
  Your API returns 429 without Retry-After header. Well-behaved clients
  don't know when to retry. They implement their own backoff, or worse,
  immediately retry, making the overload worse.
  
### **Why**
  Without Retry-After:
  - Clients guess when to retry
  - Aggressive clients retry immediately
  - Conservative clients wait too long
  - All clients retry at same time (thundering herd)
  
### **Solution**
  Always include Retry-After header:
  
  async function rateLimitMiddleware(req, res, next) {
    try {
      const result = await limiter.consume(req.user.id);
  
      // Success - add remaining info
      res.set('X-RateLimit-Limit', LIMIT.toString());
      res.set('X-RateLimit-Remaining', result.remainingPoints.toString());
      res.set('X-RateLimit-Reset', new Date(Date.now() + result.msBeforeNext).toISOString());
  
      next();
    } catch (rateLimiterRes) {
      // Rate limited - tell client when to retry
      const retryAfter = Math.ceil(rateLimiterRes.msBeforeNext / 1000);
  
      res.set('Retry-After', retryAfter.toString());
      res.set('X-RateLimit-Limit', LIMIT.toString());
      res.set('X-RateLimit-Remaining', '0');
      res.set('X-RateLimit-Reset', new Date(Date.now() + rateLimiterRes.msBeforeNext).toISOString());
  
      res.status(429).json({
        error: 'Too Many Requests',
        message: `Rate limit exceeded. Retry after ${retryAfter} seconds.`,
        retryAfter,
      });
    }
  }
  
  // Add jitter suggestion for clients
  res.json({
    error: 'Too Many Requests',
    retryAfter,
    retryAfterWithJitter: retryAfter + Math.random() * 5,  // Suggest jitter
  });
  
### **Symptoms**
  - Client retry storms after rate limit
  - Clients all retry at same time
  - API unstable after rate limiting starts
  - 429s are making things worse
### **Detection Pattern**
status\\(429\\)(?![\\s\\S]{0,200}Retry-After)

## Rate Limiting Health Checks

### **Id**
rate-limiting-health-checks
### **Summary**
Rate limiting health check endpoints breaks orchestration
### **Severity**
medium
### **Situation**
  You apply rate limiting to all routes. Health check endpoint gets
  rate limited during traffic spikes. Kubernetes thinks pod is unhealthy.
  Pod gets killed. Remaining pods get more traffic. Cascade failure.
  
### **Why**
  Orchestration systems (K8s, ELB, etc.) constantly poll health endpoints:
  - Liveness probes: "Is the process running?"
  - Readiness probes: "Can it handle traffic?"
  
  If these are rate limited, orchestration makes wrong decisions.
  
### **Solution**
  Exclude internal and health endpoints:
  
  const limiter = rateLimit({
    windowMs: 60000,
    max: 100,
    skip: (req) => {
      // Skip health endpoints
      if (req.path === '/health' || req.path === '/ready') {
        return true;
      }
  
      // Skip internal endpoints with key
      if (req.path.startsWith('/internal/')) {
        return req.headers['x-internal-key'] === process.env.INTERNAL_KEY;
      }
  
      // Skip metrics endpoints
      if (req.path === '/metrics') {
        return true;
      }
  
      return false;
    },
  });
  
  // Or use separate routers
  app.get('/health', (req, res) => res.json({ status: 'ok' }));
  app.use('/api', rateLimiter, apiRouter);  // Only API is limited
  
### **Symptoms**
  - Pods marked unhealthy during load
  - Cascade failures during traffic spikes
  - Healthy service being killed
  - K8s restarts during high traffic
### **Detection Pattern**
app\\.use.*rateLimit(?![\\s\\S]{0,500}skip.*health)

## Blocking Without Warning

### **Id**
blocking-without-warning
### **Summary**
Blocking users without warning escalates
### **Severity**
medium
### **Situation**
  User hits rate limit. You immediately block for an hour. User gets
  frustrated, opens support ticket, writes angry tweet. You lose a
  customer over something that could have been a gentle warning.
  
### **Why**
  Aggressive blocking:
  - Frustrates legitimate users
  - Doesn't distinguish accident from abuse
  - No opportunity to correct behavior
  - Creates adversarial relationship
  
### **Solution**
  Implement progressive enforcement:
  
  const PROGRESSIVE_LIMITS = {
    warning: { points: 100, blockDuration: 0 },     // Soft limit - headers only
    soft: { points: 150, blockDuration: 60 },       // 1 min block
    hard: { points: 200, blockDuration: 300 },      // 5 min block
    severe: { points: 300, blockDuration: 3600 },   // 1 hour block
  };
  
  async function progressiveRateLimit(req, res, next) {
    const userId = req.user.id;
    const key = `progressive:${userId}`;
  
    // Track violations
    const violations = await redis.get(`violations:${userId}`) || '0';
    const level = violations < 3 ? 'warning'
                : violations < 5 ? 'soft'
                : violations < 10 ? 'hard'
                : 'severe';
  
    const limit = PROGRESSIVE_LIMITS[level];
  
    try {
      await limiter.consume(userId);
      next();
    } catch (error) {
      // Increment violations
      await redis.incr(`violations:${userId}`);
      await redis.expire(`violations:${userId}`, 86400);
  
      // Warn before blocking
      if (level === 'warning') {
        res.set('X-RateLimit-Warning', 'Approaching rate limit');
        next();  // Allow through with warning
        return;
      }
  
      res.status(429).json({
        error: 'Rate limited',
        level,
        blockedFor: limit.blockDuration,
        violationCount: parseInt(violations) + 1,
      });
    }
  }
  
### **Symptoms**
  - Angry support tickets about rate limiting
  - Legitimate users blocked for mistakes
  - I only went over once!
  - Users gaming the system instead
### **Detection Pattern**
blockDuration.*3600|block.*hour(?![\\s\\S]{0,300}progressive|warning)

## Race Condition Redis

### **Id**
race-condition-redis
### **Summary**
Race condition in Redis rate limiting
### **Severity**
medium
### **Situation**
  Your rate limit code does: GET count, check limit, INCR count.
  Between GET and INCR, another request sneaks in. Both pass the check.
  Limit of 100 allows 105 requests.
  
### **Why**
  Non-atomic operations have race windows:
  - Request A: GET count = 99
  - Request B: GET count = 99
  - Request A: 99 < 100, proceed
  - Request B: 99 < 100, proceed
  - Request A: INCR count = 100
  - Request B: INCR count = 101  // Over limit!
  
### **Solution**
  Use atomic operations:
  
  // INCR returns new value atomically
  async function atomicRateLimit(key: string, limit: number, windowSeconds: number) {
    const count = await redis.incr(key);
  
    if (count === 1) {
      await redis.expire(key, windowSeconds);
    }
  
    return count <= limit;
  }
  
  // Or use Lua for complex logic
  const RATE_LIMIT_SCRIPT = `
    local key = KEYS[1]
    local limit = tonumber(ARGV[1])
    local window = tonumber(ARGV[2])
  
    local count = redis.call('INCR', key)
  
    if count == 1 then
      redis.call('EXPIRE', key, window)
    end
  
    if count > limit then
      return {0, count}
    end
  
    return {1, count}
  `;
  
  async function luaRateLimit(key: string, limit: number, window: number) {
    const [allowed, count] = await redis.eval(
      RATE_LIMIT_SCRIPT, 1, key, limit, window
    );
    return { allowed: allowed === 1, count };
  }
  
### **Symptoms**
  - Limit occasionally exceeded by small amount
  - Race conditions under high load
  - Inconsistent limit enforcement
  - Sometimes 102 requests go through
### **Detection Pattern**
redis\\.get.*limit.*redis\\.incr|get.*then.*incr

## No Bypass For Testing

### **Id**
no-bypass-for-testing
### **Summary**
Can't test API because rate limits block tests
### **Severity**
medium
### **Situation**
  Your test suite runs 1000 API calls. Rate limit is 100/minute.
  Tests fail with 429 errors. You disable rate limiting in test.
  Now you can't test the rate limiting itself.
  
### **Why**
  Tests need:
  - High volume to test functionality
  - Low limits to test rate limiting behavior
  - Both in same suite
  
  One size doesn't fit all.
  
### **Solution**
  Separate test concerns:
  
  // 1. Allow bypass for integration tests
  const limiter = rateLimit({
    skip: (req) => {
      if (process.env.NODE_ENV === 'test') {
        // Skip for normal tests unless explicitly testing rate limits
        return req.headers['x-test-rate-limit'] !== 'true';
      }
      return false;
    },
  });
  
  // 2. Different limits for test environment
  const LIMITS = {
    production: { points: 100, duration: 60 },
    development: { points: 1000, duration: 60 },
    test: { points: 10000, duration: 60 },
  };
  
  const config = LIMITS[process.env.NODE_ENV] || LIMITS.production;
  
  // 3. Dedicated rate limit tests with mock time
  describe('Rate Limiting', () => {
    beforeEach(() => {
      redis.flushdb();  // Reset limits
    });
  
    it('blocks after limit exceeded', async () => {
      for (let i = 0; i < 100; i++) {
        await request(app)
          .get('/api/test')
          .set('X-Test-Rate-Limit', 'true')
          .expect(200);
      }
  
      // Next request should be blocked
      await request(app)
        .get('/api/test')
        .set('X-Test-Rate-Limit', 'true')
        .expect(429);
    });
  });
  
### **Symptoms**
  - Tests fail with 429 errors
  - Rate limiting disabled in tests entirely
  - Rate limiting bugs found in production only
  - Flaky tests due to rate limits
### **Detection Pattern**
test.*skip.*rateLimit|NODE_ENV.*test.*rateLimit