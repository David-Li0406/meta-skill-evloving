# Caching Patterns - Sharp Edges

## Cache Stampede Outage

### **Id**
cache-stampede-outage
### **Summary**
Cache expiration causes thundering herd that overwhelms database
### **Severity**
critical
### **Situation**
High-traffic cache key expires, all requests hit database simultaneously
### **Why**
  Popular endpoint cached for 1 hour. 10,000 requests/minute. Cache expires.
  1000 concurrent requests miss cache. All 1000 hit database at once.
  Database connection pool exhausted. Queries timeout. Application hangs.
  Cache can't repopulate because database is overwhelmed. Full outage.
  
### **Solution**
  // WRONG: Simple cache-aside without protection
  async function getPopularData() {
    const cached = await redis.get('popular:data');
    if (cached) return JSON.parse(cached);
  
    const data = await db.query('SELECT ...');  // 1000 concurrent hits!
    await redis.setex('popular:data', 3600, JSON.stringify(data));
    return data;
  }
  
  // RIGHT: Lock-based single-flight
  import Redlock from 'redlock';
  
  const redlock = new Redlock([redis]);
  
  async function getPopularData() {
    const cached = await redis.get('popular:data');
    if (cached) return JSON.parse(cached);
  
    // Only one request fetches, others wait
    const lock = await redlock.acquire(['lock:popular:data'], 5000);
    try {
      // Double-check after acquiring lock
      const cached2 = await redis.get('popular:data');
      if (cached2) return JSON.parse(cached2);
  
      const data = await db.query('SELECT ...');
      await redis.setex('popular:data', 3600, JSON.stringify(data));
      return data;
    } finally {
      await lock.release();
    }
  }
  
  // RIGHT: Probabilistic early expiration
  async function getWithXFetch(key, fetchFn, ttl) {
    const result = await redis.get(key);
    if (result) {
      const { data, delta, expireAt } = JSON.parse(result);
      const now = Date.now() / 1000;
  
      // Random early recomputation prevents synchronized expiry
      if (now - delta * Math.log(Math.random()) < expireAt) {
        return data;
      }
    }
    // Recompute...
  }
  
  // RIGHT: Stale-while-revalidate pattern
  async function getWithStale(key, fetchFn, ttl) {
    const cached = await redis.get(key);
    const stale = await redis.get(`${key}:stale`);
  
    if (cached) return JSON.parse(cached);
  
    if (stale) {
      // Return stale immediately, refresh in background
      refreshInBackground(key, fetchFn, ttl);
      return JSON.parse(stale);
    }
  
    // Neither available, fetch synchronously
    return await fetchAndCache(key, fetchFn, ttl);
  }
  
### **Symptoms**
  - Database CPU spikes on cache expiry
  - Timeout errors after cache expiry
  - Application hangs periodically
  - Connection pool exhaustion
### **Detection Pattern**
redis\\.get.*return.*db\\.|cache.*miss.*query

## Stale Data Forever

### **Id**
stale-data-forever
### **Summary**
Cache never invalidated, users see data hours/days out of date
### **Severity**
high
### **Situation**
Data updated in database but cache still serves old version
### **Why**
  Update user profile in database. Forget to invalidate cache.
  User refreshes page - still sees old data. "But I just updated it!"
  Support ticket. Developer checks database - data is correct.
  Hours of debugging. Cache had stale data. No TTL set. Stale forever.
  
### **Solution**
  // WRONG: Update without invalidation
  async function updateUser(userId, data) {
    await db.user.update({ where: { id: userId }, data });
    return { success: true };
    // Cache still has old data!
  }
  
  // WRONG: No TTL
  await redis.set(`user:${userId}`, JSON.stringify(user));
  // No expiration = stale forever if invalidation misses
  
  // RIGHT: Invalidate on every write
  async function updateUser(userId, data) {
    await db.user.update({ where: { id: userId }, data });
    await redis.del(`user:${userId}`);
    // Also invalidate derived caches
    await redis.del(`user:${userId}:permissions`);
    await redis.del(`team:${user.teamId}:members`);
    return { success: true };
  }
  
  // RIGHT: Always use TTL as safety net
  await redis.setex(`user:${userId}`, 3600, JSON.stringify(user));
  // Even if invalidation fails, data refreshes in 1 hour max
  
  // RIGHT: Use write-through cache
  async function updateUser(userId, data) {
    const user = await db.user.update({ where: { id: userId }, data });
    await redis.setex(`user:${userId}`, 3600, JSON.stringify(user));
    return user;
    // Cache always has fresh data after write
  }
  
  // RIGHT: Event-driven invalidation
  // Emit event on every data change
  eventBus.emit('user:updated', { userId, data });
  
  // Cache service listens and invalidates
  eventBus.on('user:updated', async ({ userId }) => {
    await redis.del(`user:${userId}`);
    await invalidateRelatedCaches(userId);
  });
  
### **Symptoms**
  - User reports stale data after updates
  - Data correct in database but wrong in UI
  - Clearing cache fixes the issue
  - No TTL on cache keys
### **Detection Pattern**
redis\\.set\\([^)]*\\)(?!.*ex|setex)|update.*return(?!.*del|redis)

## Cache Before Database

### **Id**
cache-before-database
### **Summary**
Cache updated before database, data inconsistency on failure
### **Severity**
high
### **Situation**
Cache write succeeds but database write fails
### **Why**
  Save to cache first (fast feedback!). Then save to database.
  Database write fails (constraint violation, timeout, whatever).
  Cache has data that doesn't exist in database. User sees phantom record.
  Or: User updates profile, cache updated, database fails, rollback.
  Cache still has "new" data. User refreshes - sees successful update.
  Database has old data. Next cache expiry - old data appears. Confusion.
  
### **Solution**
  // WRONG: Cache first, database second
  async function createOrder(orderData) {
    const order = { id: generateId(), ...orderData };
    await redis.setex(`order:${order.id}`, 3600, JSON.stringify(order));
    await db.order.create({ data: order });  // This might fail!
    return order;
  }
  // If db.order.create fails, cache has phantom order
  
  // RIGHT: Database first, cache second
  async function createOrder(orderData) {
    const order = await db.order.create({ data: orderData });
    // Database succeeded, safe to cache
    await redis.setex(`order:${order.id}`, 3600, JSON.stringify(order));
    return order;
  }
  
  // RIGHT: Transaction with compensating action
  async function createOrder(orderData) {
    const order = await db.order.create({ data: orderData });
    try {
      await redis.setex(`order:${order.id}`, 3600, JSON.stringify(order));
    } catch (cacheError) {
      // Cache failed, but that's okay - data is in database
      // Next read will populate cache
      logger.warn({ error: cacheError }, 'Cache write failed');
    }
    return order;
  }
  
  // RIGHT: Use database as source of truth for writes
  // Cache is only for reads, invalidated on writes
  async function updateOrder(orderId, data) {
    const order = await db.order.update({
      where: { id: orderId },
      data,
    });
    await redis.del(`order:${orderId}`);  // Invalidate, don't set
    return order;
    // Next read will fetch fresh data from database
  }
  
### **Symptoms**
  - Data in cache but not in database
  - Phantom records appearing
  - Data disappears after cache expiry
  - Inconsistent data after failures
### **Detection Pattern**
redis\\.set.*\\n.*db\\.|cache.*create.*before.*save

## Cached Errors

### **Id**
cached-errors
### **Summary**
Error responses cached, system serves errors even when recovered
### **Severity**
high
### **Situation**
Database was down, null/error cached, now serving stale errors
### **Why**
  Database briefly unavailable. Query returns null or throws.
  You cache null: "User 123 not found". Database recovers.
  Cache serves "user not found" for 1 hour. User definitely exists.
  Or: External API returns 500. You cache the error. API recovers.
  All requests get cached 500 error. You're down even though API is up.
  
### **Solution**
  // WRONG: Caching null/error results
  async function getUser(userId) {
    const cached = await redis.get(`user:${userId}`);
    if (cached) return JSON.parse(cached);
  
    const user = await db.user.findUnique({ where: { id: userId } });
    // Caching null means "not found" is permanent until TTL
    await redis.setex(`user:${userId}`, 3600, JSON.stringify(user));
    return user;
  }
  
  // WRONG: Caching errors
  async function fetchExternalData() {
    try {
      const data = await externalApi.getData();
      await redis.setex('external:data', 3600, JSON.stringify(data));
      return data;
    } catch (error) {
      await redis.setex('external:data', 3600, JSON.stringify({ error: true }));
      // Now error is cached for 1 hour!
      throw error;
    }
  }
  
  // RIGHT: Only cache successful results
  async function getUser(userId) {
    const cached = await redis.get(`user:${userId}`);
    if (cached) return JSON.parse(cached);
  
    const user = await db.user.findUnique({ where: { id: userId } });
  
    if (user) {
      await redis.setex(`user:${userId}`, 3600, JSON.stringify(user));
    }
    // Don't cache null - next request will retry database
  
    return user;
  }
  
  // RIGHT: Short TTL for negative cache (if needed)
  async function getUser(userId) {
    const cached = await redis.get(`user:${userId}`);
    if (cached === 'NOT_FOUND') return null;  // Known negative
    if (cached) return JSON.parse(cached);
  
    const user = await db.user.findUnique({ where: { id: userId } });
  
    if (user) {
      await redis.setex(`user:${userId}`, 3600, JSON.stringify(user));
    } else {
      // Very short TTL for negative cache
      await redis.setex(`user:${userId}`, 60, 'NOT_FOUND');
    }
  
    return user;
  }
  
  // RIGHT: Circuit breaker for external services
  // Don't cache during open circuit, return fallback
  
### **Symptoms**
  - Null results cached long-term
  - System serves errors after recovery
  - "Not found" for existing records
  - Errors continue after fix deployed
### **Detection Pattern**
setex.*null|setex.*error|cache.*catch.*set

## Redis Keys Command

### **Id**
redis-keys-command
### **Summary**
Using KEYS command blocks Redis, causes full service outage
### **Severity**
critical
### **Situation**
Using KEYS * or pattern matching on production Redis
### **Why**
  Developer needs to find all user cache keys. Uses KEYS user:*.
  Redis is single-threaded. KEYS scans entire keyspace.
  10 million keys. KEYS blocks for 30 seconds.
  All other Redis operations queue behind it. All apps waiting on Redis.
  Connection timeouts cascade. Full outage from one KEYS command.
  
### **Solution**
  // WRONG: KEYS in production
  const keys = await redis.keys('user:*');  // Blocks entire Redis!
  for (const key of keys) {
    await redis.del(key);
  }
  
  // RIGHT: Use SCAN for iteration
  async function deletePattern(pattern) {
    let cursor = '0';
    do {
      const [nextCursor, keys] = await redis.scan(
        cursor,
        'MATCH', pattern,
        'COUNT', 100,  // Process in batches
      );
      cursor = nextCursor;
  
      if (keys.length > 0) {
        await redis.del(...keys);
      }
    } while (cursor !== '0');
  }
  
  await deletePattern('user:*');
  
  // RIGHT: Use sets for grouped keys
  // When creating user cache:
  await redis.sadd('cache:user-keys', `user:${userId}`);
  await redis.setex(`user:${userId}`, 3600, JSON.stringify(user));
  
  // When invalidating all users:
  const keys = await redis.smembers('cache:user-keys');
  if (keys.length) {
    await redis.del(...keys);
    await redis.del('cache:user-keys');
  }
  
  // RIGHT: Use key expiration instead of manual deletion
  // Let Redis clean up automatically
  
  // RIGHT: Design keys for known lookup patterns
  // If you need to invalidate by user, include user in key
  // user:123:profile, user:123:orders
  // Don't need pattern matching
  
### **Symptoms**
  - Redis slowlog shows KEYS commands
  - Periodic Redis freezes
  - Connection timeouts during admin operations
  - High latency on all Redis operations
### **Detection Pattern**
redis\\.keys\\(|KEYS \\*|keys.*\\*

## Multi Layer Invalidation Miss

### **Id**
multi-layer-invalidation-miss
### **Summary**
CDN/edge cache not invalidated, users see stale content
### **Severity**
medium
### **Situation**
Updated database and Redis but CDN still serving old version
### **Why**
  Three cache layers: CDN, Redis, local. Update product price in database.
  Invalidate Redis cache. Local cache expires in 60 seconds.
  CDN still has old price cached for 24 hours. Most users hit CDN.
  Wrong price displayed. Or worse: checkout price differs from displayed.
  Angry customers. Revenue loss.
  
### **Solution**
  // Multi-layer invalidation
  async function updateProduct(productId, data) {
    // 1. Update database
    const product = await db.product.update({
      where: { id: productId },
      data,
    });
  
    // 2. Invalidate local cache
    localCache.del(`product:${productId}`);
  
    // 3. Invalidate Redis
    await redis.del(`product:${productId}`);
  
    // 4. Publish for other instances
    await redis.publish('cache:invalidate', JSON.stringify({
      type: 'product',
      id: productId,
    }));
  
    // 5. Purge CDN
    await purgeCdn([
      `/products/${productId}`,
      `/api/products/${productId}`,
      `/collections/*`,  // Product appears in collections
    ]);
  
    return product;
  }
  
  // CDN purge examples
  async function purgeCdn(paths) {
    // CloudFlare
    await fetch('https://api.cloudflare.com/client/v4/zones/{zone}/purge_cache', {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${CF_TOKEN}` },
      body: JSON.stringify({ files: paths.map(p => `${BASE_URL}${p}`) }),
    });
  
    // Fastly (using surrogate keys)
    await fetch(`https://api.fastly.com/service/{service}/purge/${surrogateKey}`, {
      method: 'POST',
      headers: { 'Fastly-Key': FASTLY_TOKEN },
    });
  }
  
  // Use surrogate keys for efficient CDN invalidation
  app.get('/api/products/:id', (req, res) => {
    res.set('Surrogate-Key', `product-${req.params.id} products all-products`);
    // Can purge by any of these keys
  });
  
  // Cache version in URL for aggressive caching
  // /products/123?v=abc123
  // Change version on update = immediate cache bust
  
### **Symptoms**
  - CDN serving old content after update
  - Different data on cache vs no-cache requests
  - Regional differences in content
  - Updates take hours to propagate
### **Detection Pattern**
update.*redis\\.del(?!.*cdn|purge|cloudflare|fastly)

## Hot Key Problem

### **Id**
hot-key-problem
### **Summary**
Single cache key receives too much traffic, becomes bottleneck
### **Severity**
medium
### **Situation**
Viral content or popular resource overloads single cache entry
### **Why**
  News story goes viral. Millions of requests for same article.
  Single Redis key. Single shard. All traffic to one server.
  Network bandwidth saturated. Key becomes bottleneck.
  Or: Local cache helps, but every 60 seconds, stampede to Redis.
  
### **Solution**
  // Problem: One key gets all traffic
  await redis.get('article:viral');  // Millions of hits
  
  // Solution 1: Local caching layer
  import NodeCache from 'node-cache';
  const localCache = new NodeCache({ stdTTL: 10 });  // 10 second local cache
  
  async function getArticle(articleId) {
    const localKey = `article:${articleId}`;
  
    // Check local first (per-instance)
    const local = localCache.get(localKey);
    if (local) return local;
  
    // Then Redis
    const remote = await redis.get(localKey);
    if (remote) {
      const article = JSON.parse(remote);
      localCache.set(localKey, article);
      return article;
    }
  
    // Database...
  }
  
  // Solution 2: Shard hot keys
  function getShardedKey(baseKey, shardCount = 10) {
    const shard = Math.floor(Math.random() * shardCount);
    return `${baseKey}:shard:${shard}`;
  }
  
  // Write to all shards
  async function setHotKey(baseKey, value, ttl) {
    const pipeline = redis.pipeline();
    for (let i = 0; i < 10; i++) {
      pipeline.setex(`${baseKey}:shard:${i}`, ttl, JSON.stringify(value));
    }
    await pipeline.exec();
  }
  
  // Read from random shard
  async function getHotKey(baseKey) {
    const shard = Math.floor(Math.random() * 10);
    return redis.get(`${baseKey}:shard:${shard}`);
  }
  
  // Solution 3: Read replicas
  // Use Redis cluster with read replicas for hot keys
  const readReplica = new Redis(process.env.REDIS_REPLICA_URL);
  const hot = await readReplica.get('article:viral');  // Spread load
  
### **Symptoms**
  - Single Redis key with high traffic
  - One shard overloaded
  - Latency on specific keys
  - Viral content causing issues
### **Detection Pattern**
get.*viral|popular.*single.*key

## Serialization Deserialization Cost

### **Id**
serialization-deserialization-cost
### **Summary**
JSON parsing overhead negates caching benefit for large objects
### **Severity**
low
### **Situation**
Caching large objects where serialization cost exceeds database cost
### **Why**
  Cache 10MB JSON document. Every access: parse 10MB JSON.
  JSON.parse on 10MB = 100ms CPU time. Database query = 50ms.
  Cache is slower than database! Plus memory pressure from large objects.
  "But it's cached!" - caching isn't always faster.
  
### **Solution**
  // WRONG: Cache everything regardless of size
  const hugeReport = await generateReport();  // 50MB object
  await redis.setex('report', 3600, JSON.stringify(hugeReport));  // Slow
  const cached = JSON.parse(await redis.get('report'));  // Slow again
  
  // RIGHT: Cache smaller, frequently accessed parts
  const reportMetadata = await getReportMetadata();  // 1KB
  await redis.setex('report:meta', 3600, JSON.stringify(reportMetadata));
  
  // Fetch full report from database when needed
  const fullReport = await db.report.findUnique({ where: { id } });
  
  // RIGHT: Use compression for large values
  import { gzip, gunzip } from 'zlib';
  import { promisify } from 'util';
  
  const gzipAsync = promisify(gzip);
  const gunzipAsync = promisify(gunzip);
  
  async function setCompressed(key, data, ttl) {
    const compressed = await gzipAsync(JSON.stringify(data));
    await redis.setex(key, ttl, compressed);
  }
  
  async function getCompressed(key) {
    const compressed = await redis.getBuffer(key);
    if (!compressed) return null;
    const decompressed = await gunzipAsync(compressed);
    return JSON.parse(decompressed.toString());
  }
  
  // RIGHT: Use MessagePack for faster serialization
  import msgpack from 'msgpack-lite';
  
  await redis.set(key, msgpack.encode(data));
  const data = msgpack.decode(await redis.getBuffer(key));
  
  // RIGHT: Measure before caching
  // If serialization + deserialization > query time, don't cache
  
### **Symptoms**
  - Cache slower than expected
  - High CPU on cache operations
  - Large objects in cache
  - Serialization in profiler output
### **Detection Pattern**
stringify.*MB|large.*cache|JSON\\.parse.*big