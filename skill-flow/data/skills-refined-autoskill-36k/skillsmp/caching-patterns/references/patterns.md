# Caching Patterns

## Patterns


---
  #### **Name**
Cache-Aside Pattern
  #### **Description**
Application manages cache reads and writes explicitly
  #### **When**
Need fine-grained control over caching logic
  #### **Example**
    import Redis from 'ioredis';
    
    const redis = new Redis(process.env.REDIS_URL);
    const CACHE_TTL = 3600; // 1 hour
    
    // Cache-aside: Application manages both cache and database
    async function getUser(userId: string): Promise<User | null> {
      const cacheKey = `user:${userId}`;
    
      // 1. Try cache first
      const cached = await redis.get(cacheKey);
      if (cached) {
        return JSON.parse(cached);
      }
    
      // 2. Cache miss - fetch from database
      const user = await db.user.findUnique({ where: { id: userId } });
    
      if (user) {
        // 3. Populate cache for next time
        await redis.setex(cacheKey, CACHE_TTL, JSON.stringify(user));
      }
    
      return user;
    }
    
    // On update, invalidate cache
    async function updateUser(userId: string, data: Partial<User>): Promise<User> {
      // Update database first
      const user = await db.user.update({
        where: { id: userId },
        data,
      });
    
      // Then invalidate cache
      await redis.del(`user:${userId}`);
    
      return user;
    }
    
    // Alternative: Update cache instead of invalidate
    async function updateUserWithCacheRefresh(userId: string, data: Partial<User>): Promise<User> {
      const user = await db.user.update({
        where: { id: userId },
        data,
      });
    
      // Refresh cache with new data
      await redis.setex(`user:${userId}`, CACHE_TTL, JSON.stringify(user));
    
      return user;
    }
    

---
  #### **Name**
Cache Stampede Prevention
  #### **Description**
Prevent thundering herd when cache expires
  #### **When**
High-traffic endpoints with expensive computations
  #### **Example**
    import Redis from 'ioredis';
    
    const redis = new Redis(process.env.REDIS_URL);
    
    // Method 1: Lock-based prevention
    async function getWithLock<T>(
      key: string,
      fetchFn: () => Promise<T>,
      ttl: number,
    ): Promise<T> {
      // Try to get from cache
      const cached = await redis.get(key);
      if (cached) {
        return JSON.parse(cached);
      }
    
      const lockKey = `lock:${key}`;
      const lockTtl = 10; // Lock expires in 10 seconds
    
      // Try to acquire lock
      const acquired = await redis.set(lockKey, '1', 'EX', lockTtl, 'NX');
    
      if (acquired) {
        try {
          // We got the lock - fetch data
          const data = await fetchFn();
          await redis.setex(key, ttl, JSON.stringify(data));
          return data;
        } finally {
          await redis.del(lockKey);
        }
      } else {
        // Wait and retry (someone else is fetching)
        await new Promise(resolve => setTimeout(resolve, 100));
        return getWithLock(key, fetchFn, ttl);
      }
    }
    
    // Method 2: Probabilistic early expiration (XFetch)
    async function getWithEarlyExpire<T>(
      key: string,
      fetchFn: () => Promise<T>,
      ttl: number,
      beta: number = 1,
    ): Promise<T> {
      const result = await redis.get(key);
    
      if (result) {
        const { data, delta, expireAt } = JSON.parse(result);
        const now = Date.now() / 1000;
    
        // Probabilistic early recomputation
        // Higher beta = more eager recomputation
        const shouldRecompute = now - delta * beta * Math.log(Math.random()) >= expireAt;
    
        if (!shouldRecompute) {
          return data;
        }
      }
    
      // Fetch and cache with metadata
      const start = Date.now();
      const data = await fetchFn();
      const delta = (Date.now() - start) / 1000;
    
      const cacheValue = {
        data,
        delta,
        expireAt: Date.now() / 1000 + ttl,
      };
    
      await redis.setex(key, ttl + 60, JSON.stringify(cacheValue)); // Extra TTL for metadata
      return data;
    }
    
    // Method 3: Stale-while-revalidate
    async function getWithStaleRevalidate<T>(
      key: string,
      fetchFn: () => Promise<T>,
      ttl: number,
      staleTtl: number,
    ): Promise<T> {
      const [data, staleData] = await Promise.all([
        redis.get(key),
        redis.get(`${key}:stale`),
      ]);
    
      if (data) {
        return JSON.parse(data);
      }
    
      if (staleData) {
        // Return stale data immediately, refresh in background
        setImmediate(async () => {
          const fresh = await fetchFn();
          await redis.setex(key, ttl, JSON.stringify(fresh));
          await redis.setex(`${key}:stale`, staleTtl, JSON.stringify(fresh));
        });
        return JSON.parse(staleData);
      }
    
      // Neither fresh nor stale - fetch synchronously
      const fresh = await fetchFn();
      await redis.setex(key, ttl, JSON.stringify(fresh));
      await redis.setex(`${key}:stale`, staleTtl, JSON.stringify(fresh));
      return fresh;
    }
    

---
  #### **Name**
HTTP Caching Headers
  #### **Description**
Leverage browser and CDN caching with proper headers
  #### **When**
Serving static or semi-static content via HTTP
  #### **Example**
    // Express middleware for cache control
    
    // Static assets - cache forever (versioned filenames)
    app.use('/assets', express.static('public', {
      maxAge: '1y',
      immutable: true,
    }));
    // Produces: Cache-Control: public, max-age=31536000, immutable
    
    // API responses - short cache with revalidation
    app.get('/api/products', async (req, res) => {
      const products = await getProducts();
      const etag = generateETag(products);
    
      // Check if client has valid cached version
      if (req.headers['if-none-match'] === etag) {
        return res.status(304).end();
      }
    
      res.set({
        'Cache-Control': 'public, max-age=60, stale-while-revalidate=300',
        'ETag': etag,
      });
    
      res.json(products);
    });
    
    // Private user data - no caching
    app.get('/api/user/profile', authenticate, async (req, res) => {
      const profile = await getUserProfile(req.user.id);
    
      res.set({
        'Cache-Control': 'private, no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
      });
    
      res.json(profile);
    });
    
    // CDN-friendly caching with Vary
    app.get('/api/content', async (req, res) => {
      const content = await getContent(req.headers['accept-language']);
    
      res.set({
        'Cache-Control': 'public, max-age=3600',
        'Vary': 'Accept-Language', // Cache separately per language
      });
    
      res.json(content);
    });
    
    // Surrogate-Key for CDN invalidation (Fastly, CloudFlare)
    app.get('/api/products/:id', async (req, res) => {
      const product = await getProduct(req.params.id);
    
      res.set({
        'Cache-Control': 'public, max-age=86400',
        'Surrogate-Key': `product-${req.params.id} products`,
        // Invalidate with: PURGE /products or specific product
      });
    
      res.json(product);
    });
    

---
  #### **Name**
Multi-Layer Cache Architecture
  #### **Description**
Combine in-memory, Redis, and CDN caching
  #### **When**
Need maximum performance with distributed system
  #### **Example**
    import NodeCache from 'node-cache';
    import Redis from 'ioredis';
    
    // Layer 1: In-memory cache (per-instance, fastest)
    const localCache = new NodeCache({
      stdTTL: 60,  // 1 minute local cache
      checkperiod: 30,
    });
    
    // Layer 2: Distributed cache (shared across instances)
    const redis = new Redis(process.env.REDIS_URL);
    const REDIS_TTL = 3600; // 1 hour
    
    // Multi-layer get
    async function getProduct(productId: string): Promise<Product | null> {
      const cacheKey = `product:${productId}`;
    
      // Layer 1: Check local cache
      const local = localCache.get<Product>(cacheKey);
      if (local) {
        return local;
      }
    
      // Layer 2: Check Redis
      const remote = await redis.get(cacheKey);
      if (remote) {
        const product = JSON.parse(remote);
        // Populate local cache
        localCache.set(cacheKey, product);
        return product;
      }
    
      // Layer 3: Database
      const product = await db.product.findUnique({
        where: { id: productId },
      });
    
      if (product) {
        // Populate both caches
        localCache.set(cacheKey, product);
        await redis.setex(cacheKey, REDIS_TTL, JSON.stringify(product));
      }
    
      return product;
    }
    
    // Multi-layer invalidation
    async function invalidateProduct(productId: string): Promise<void> {
      const cacheKey = `product:${productId}`;
    
      // Invalidate local cache
      localCache.del(cacheKey);
    
      // Invalidate Redis
      await redis.del(cacheKey);
    
      // Publish invalidation for other instances
      await redis.publish('cache:invalidate', JSON.stringify({
        type: 'product',
        id: productId,
      }));
    
      // Purge CDN (if applicable)
      await purgeCdn(`/api/products/${productId}`);
    }
    
    // Subscribe to invalidation events
    const subscriber = redis.duplicate();
    subscriber.subscribe('cache:invalidate');
    subscriber.on('message', (channel, message) => {
      const { type, id } = JSON.parse(message);
      localCache.del(`${type}:${id}`);
    });
    

---
  #### **Name**
Cache Key Design
  #### **Description**
Design cache keys for efficient lookup and invalidation
  #### **When**
Setting up any caching system
  #### **Example**
    // Cache key principles:
    // 1. Include all query parameters that affect the result
    // 2. Use consistent, predictable format
    // 3. Support partial invalidation with prefixes
    
    // Basic key structure: type:id
    const userKey = `user:${userId}`;
    
    // With version for schema changes
    const userKeyV2 = `v2:user:${userId}`;
    
    // Query-specific keys
    function productListKey(filters: ProductFilters): string {
      const parts = ['products'];
    
      if (filters.category) parts.push(`cat:${filters.category}`);
      if (filters.priceMax) parts.push(`max:${filters.priceMax}`);
      if (filters.sort) parts.push(`sort:${filters.sort}`);
    
      parts.push(`page:${filters.page || 1}`);
    
      return parts.join(':');
    }
    // Result: products:cat:electronics:max:100:sort:price:page:1
    
    // User-specific keys (for private data)
    const userOrdersKey = `user:${userId}:orders:page:${page}`;
    
    // Compound keys for relationships
    const userCartKey = `user:${userId}:cart`;
    const cartItemKey = `cart:${cartId}:item:${itemId}`;
    
    // Invalidation patterns
    async function invalidateUserCache(userId: string) {
      // Delete specific key
      await redis.del(`user:${userId}`);
    
      // Delete pattern (use SCAN, not KEYS in production)
      const pattern = `user:${userId}:*`;
      let cursor = '0';
      do {
        const [nextCursor, keys] = await redis.scan(cursor, 'MATCH', pattern, 'COUNT', 100);
        cursor = nextCursor;
        if (keys.length) {
          await redis.del(...keys);
        }
      } while (cursor !== '0');
    }
    
    // Use Redis hash for structured data
    await redis.hset(`user:${userId}`, {
      profile: JSON.stringify(profile),
      preferences: JSON.stringify(preferences),
      lastLogin: Date.now(),
    });
    
    // Get specific field without deserializing everything
    const profile = await redis.hget(`user:${userId}`, 'profile');
    

---
  #### **Name**
TTL Strategy
  #### **Description**
Choose appropriate cache expiration times
  #### **When**
Deciding how long to cache different data types
  #### **Example**
    // TTL guidelines by data characteristics
    
    const TTL_STRATEGIES = {
      // Immutable data - cache forever
      // Static assets, historical records, archived content
      IMMUTABLE: 60 * 60 * 24 * 365, // 1 year
    
      // Rarely changing - long cache
      // System config, feature flags, category lists
      RARE_CHANGE: 60 * 60 * 24, // 24 hours
    
      // Regular updates - medium cache
      // Product catalog, user profiles, blog posts
      REGULAR: 60 * 60, // 1 hour
    
      // Frequent updates - short cache
      // Stock prices, inventory counts, leaderboards
      FREQUENT: 60 * 5, // 5 minutes
    
      // Real-time data - very short or no cache
      // Cart contents, notifications, live data
      REALTIME: 60, // 1 minute or use pub/sub
    
      // Session data - based on session length
      SESSION: 60 * 60 * 24, // 24 hours
    };
    
    // Adaptive TTL based on update frequency
    async function setWithAdaptiveTTL<T>(
      key: string,
      data: T,
      updateHistory: Date[],
    ): Promise<void> {
      // Calculate average time between updates
      if (updateHistory.length < 2) {
        await redis.setex(key, TTL_STRATEGIES.REGULAR, JSON.stringify(data));
        return;
      }
    
      const intervals = [];
      for (let i = 1; i < updateHistory.length; i++) {
        intervals.push(updateHistory[i].getTime() - updateHistory[i-1].getTime());
      }
      const avgInterval = intervals.reduce((a, b) => a + b, 0) / intervals.length;
    
      // TTL = half the average update interval (safety margin)
      const ttl = Math.min(
        Math.max(avgInterval / 2000, 60), // At least 1 minute
        TTL_STRATEGIES.RARE_CHANGE, // At most 24 hours
      );
    
      await redis.setex(key, ttl, JSON.stringify(data));
    }
    
    // Jitter to prevent synchronized expiration
    function ttlWithJitter(baseTtl: number, jitterPercent: number = 10): number {
      const jitter = baseTtl * (jitterPercent / 100);
      return baseTtl + Math.random() * jitter - jitter / 2;
    }
    
    // Usage
    await redis.setex(key, ttlWithJitter(3600), data);
    

## Anti-Patterns


---
  #### **Name**
Cache Everything
  #### **Description**
Caching all database queries regardless of access pattern
  #### **Why**
Cache isn't free. Memory costs money. Invalidation complexity grows. You cache user-specific data that's accessed once. You cache rapidly changing data that's stale immediately. Cache hit rate matters more than cache size.
  #### **Instead**
Cache expensive computations and frequently accessed data. Measure hit rates. If < 90%, re-evaluate what you're caching.

---
  #### **Name**
No TTL (Infinite Cache)
  #### **Description**
Caching without expiration, relying only on manual invalidation
  #### **Why**
Invalidation logic has bugs. You forget edge cases. Data becomes stale forever. User sees 6-month-old profile picture because invalidation missed one path. TTL is your safety net.
  #### **Instead**
Always set TTL. Even for "permanent" data, use long TTL (24h+). TTL catches what invalidation misses.

---
  #### **Name**
Cache Then Database Write
  #### **Description**
Updating cache before confirming database write succeeds
  #### **Why**
Cache update succeeds. Database write fails. Now cache has data that doesn't exist in database. User sees phantom record. Or sees update that was rolled back.
  #### **Instead**
Database write first, then cache update. If cache update fails, data is just not cached (slower, but correct).

---
  #### **Name**
Ignoring Cache Stampede
  #### **Description**
No protection against thundering herd on cache miss
  #### **Why**
Cache expires. 1000 concurrent requests. All miss cache. All hit database. Database overwhelmed. Application timeout. Full outage from one cache expiration.
  #### **Instead**
Use locks, probabilistic early expiration, or stale-while-revalidate. One request fetches, others wait or get stale data.

---
  #### **Name**
Caching Errors
  #### **Description**
Caching error responses or null results
  #### **Why**
Database temporarily down. Cache null result. Database recovers. Users still get null from cache. "User not found" for existing user. Support tickets incoming.
  #### **Instead**
Only cache successful results. For null, either don't cache or use short TTL. Log and alert on repeated cache-miss patterns.

---
  #### **Name**
KEYS Command in Production
  #### **Description**
Using Redis KEYS command for pattern matching
  #### **Why**
KEYS blocks Redis. Single-threaded. 10 million keys. KEYS * scans them all. Redis frozen. All other operations blocked. Everything depending on Redis times out.
  #### **Instead**
Use SCAN for iteration. Use sorted sets or sets for grouping. Design keys for known lookup patterns.