# Redis Specialist

## Patterns


---
  #### **Name**
Cache-Aside Pattern
  #### **Description**
Application manages cache reads and writes
  #### **When**
Caching database queries or API responses
  #### **Example**
    async function getUserWithCache(userId: string): Promise<User> {
      const cacheKey = `user:${userId}`;
    
      // Try cache first
      const cached = await redis.get(cacheKey);
      if (cached) {
        return JSON.parse(cached);
      }
    
      // Cache miss - fetch from database
      const user = await db.users.findUnique({ where: { id: userId } });
    
      if (user) {
        // Write to cache with TTL
        await redis.setex(cacheKey, 3600, JSON.stringify(user));
      }
    
      return user;
    }
    
    // Invalidation on update
    async function updateUser(userId: string, data: Partial<User>): Promise<User> {
      const user = await db.users.update({
        where: { id: userId },
        data
      });
    
      // Invalidate cache
      await redis.del(`user:${userId}`);
    
      return user;
    }
    

---
  #### **Name**
Distributed Lock with Redlock
  #### **Description**
Coordinate exclusive access across distributed systems
  #### **When**
Preventing race conditions in distributed operations
  #### **Example**
    import Redlock from 'redlock';
    
    const redlock = new Redlock([redis], {
      retryCount: 3,
      retryDelay: 200,
      retryJitter: 100
    });
    
    async function processOrderExclusively(orderId: string) {
      const lock = await redlock.acquire(
        [`lock:order:${orderId}`],
        5000  // Lock TTL in ms
      );
    
      try {
        // Critical section - only one process can be here
        const order = await db.orders.findUnique({ where: { id: orderId } });
    
        if (order.status !== 'pending') {
          return;  // Already processed
        }
    
        await processPayment(order);
        await db.orders.update({
          where: { id: orderId },
          data: { status: 'completed' }
        });
      } finally {
        // Always release the lock
        await lock.release();
      }
    }
    

---
  #### **Name**
Sliding Window Rate Limiter
  #### **Description**
Rate limiting with smooth request distribution
  #### **When**
API rate limiting that avoids burst edge cases
  #### **Example**
    async function slidingWindowRateLimit(
      key: string,
      limit: number,
      windowSec: number
    ): Promise<{ allowed: boolean; remaining: number }> {
      const now = Date.now();
      const windowMs = windowSec * 1000;
      const windowStart = now - windowMs;
    
      // Use sorted set with timestamp as score
      const multi = redis.multi();
    
      // Remove old entries
      multi.zremrangebyscore(key, 0, windowStart);
    
      // Add current request
      multi.zadd(key, now, `${now}-${Math.random()}`);
    
      // Count requests in window
      multi.zcard(key);
    
      // Set expiry on key
      multi.expire(key, windowSec);
    
      const results = await multi.exec();
      const count = results[2][1] as number;
    
      return {
        allowed: count <= limit,
        remaining: Math.max(0, limit - count)
      };
    }
    
    // Usage
    const { allowed, remaining } = await slidingWindowRateLimit(
      `ratelimit:${userId}`,
      100,  // 100 requests
      60    // per 60 seconds
    );
    
    if (!allowed) {
      throw new RateLimitError(`Rate limit exceeded. Try again later.`);
    }
    

---
  #### **Name**
Pub/Sub with Redis Streams
  #### **Description**
Reliable pub/sub with persistence and consumer groups
  #### **When**
Need message persistence or exactly-once processing
  #### **Example**
    // Producer: Add message to stream
    async function publishEvent(stream: string, event: object) {
      await redis.xadd(stream, '*', 'data', JSON.stringify(event));
    }
    
    // Consumer: Process with consumer group (exactly-once semantics)
    async function consumeEvents(
      stream: string,
      group: string,
      consumer: string
    ) {
      // Create consumer group if not exists
      try {
        await redis.xgroup('CREATE', stream, group, '0', 'MKSTREAM');
      } catch (e) {
        // Group already exists, ignore
      }
    
      while (true) {
        // Read new messages for this consumer
        const messages = await redis.xreadgroup(
          'GROUP', group, consumer,
          'COUNT', 10,
          'BLOCK', 5000,
          'STREAMS', stream, '>'
        );
    
        if (!messages) continue;
    
        for (const [, entries] of messages) {
          for (const [id, fields] of entries) {
            try {
              const event = JSON.parse(fields[1]);
              await processEvent(event);
    
              // Acknowledge successful processing
              await redis.xack(stream, group, id);
            } catch (error) {
              console.error(`Failed to process ${id}:`, error);
              // Message will be redelivered to another consumer
            }
          }
        }
      }
    }
    

---
  #### **Name**
Leaderboard with Sorted Sets
  #### **Description**
Real-time rankings with O(log n) updates
  #### **When**
Building scoreboards, rankings, or priority queues
  #### **Example**
    class Leaderboard {
      constructor(private key: string) {}
    
      async updateScore(userId: string, score: number) {
        await redis.zadd(this.key, score, userId);
      }
    
      async incrementScore(userId: string, amount: number) {
        return redis.zincrby(this.key, amount, userId);
      }
    
      async getTopN(n: number): Promise<{ userId: string; score: number }[]> {
        // Get top N with scores, highest first
        const results = await redis.zrevrange(this.key, 0, n - 1, 'WITHSCORES');
    
        const entries: { userId: string; score: number }[] = [];
        for (let i = 0; i < results.length; i += 2) {
          entries.push({
            userId: results[i],
            score: parseFloat(results[i + 1])
          });
        }
        return entries;
      }
    
      async getRank(userId: string): Promise<number | null> {
        // 0-indexed, highest score = rank 0
        const rank = await redis.zrevrank(this.key, userId);
        return rank !== null ? rank + 1 : null;  // Convert to 1-indexed
      }
    
      async getAroundUser(userId: string, range: number = 5) {
        const rank = await redis.zrevrank(this.key, userId);
        if (rank === null) return null;
    
        const start = Math.max(0, rank - range);
        const end = rank + range;
    
        return redis.zrevrange(this.key, start, end, 'WITHSCORES');
      }
    }
    

## Anti-Patterns


---
  #### **Name**
Caching Without Invalidation Strategy
  #### **Description**
Adding cache without planning how to invalidate it
  #### **Why**
    Cache with only TTL leads to stale data. Users see outdated information
    for the entire TTL duration. Writes appear to be lost. Eventually someone
    sets TTL to 1 second and you have no cache at all.
    
  #### **Instead**
Plan invalidation from the start - cache-aside with explicit delete on update

---
  #### **Name**
Hot Key Problem
  #### **Description**
Single key receiving disproportionate traffic
  #### **Why**
    One key getting 100k reads/second hits a single Redis node. That node
    becomes the bottleneck. Cluster mode does not help because data is on
    one shard.
    
  #### **Instead**
Use read replicas, local caching for hot keys, or shard the key with random suffix

---
  #### **Name**
Storing Large Values
  #### **Description**
Caching multi-megabyte objects in Redis
  #### **Why**
    Large values block the single-threaded Redis. A 10MB GET blocks all
    other operations. Network transfer is slow. Memory usage explodes.
    
  #### **Instead**
Store references/IDs, use compression, or use object storage for large blobs

---
  #### **Name**
Missing TTL on All Keys
  #### **Description**
Creating keys without expiration
  #### **Why**
    Memory fills up over time. Redis starts evicting random keys (or crashes
    with OOM). You have no idea what data is still valid. Debugging is impossible.
    
  #### **Instead**
Always set TTL. Use maxmemory-policy as safety net, not primary strategy

---
  #### **Name**
Synchronous Pub/Sub for Critical Data
  #### **Description**
Using pub/sub for data that must not be lost
  #### **Why**
    Pub/sub is fire-and-forget. If no subscribers are connected, messages
    are lost. If subscriber disconnects mid-message, it is lost. No replay,
    no persistence.
    
  #### **Instead**
Use Redis Streams with consumer groups for reliable messaging

---
  #### **Name**
Storing Relational Data
  #### **Description**
Trying to replicate database relationships in Redis
  #### **Why**
    Redis has no JOINs, no transactions across keys (mostly), no foreign
    keys. You end up with denormalized data, consistency bugs, and N+1
    query patterns in your code.
    
  #### **Instead**
Use Redis for caching and specific patterns. Keep relational data in the database