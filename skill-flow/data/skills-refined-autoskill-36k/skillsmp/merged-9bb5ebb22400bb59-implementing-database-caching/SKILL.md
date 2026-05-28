---
name: implementing-database-caching
description: Use this skill when you need to implement multi-tier database caching solutions to improve performance, reduce database load, and enhance scalability.
---

## Overview

This skill empowers the implementation of a production-ready multi-tier caching architecture for databases. It leverages Redis for distributed caching, in-memory caching for L1 performance, and CDN for static assets, resulting in significant database load reduction and improved query latency.

## Prerequisites

Before using this skill, ensure:
- Redis server is available or you can deploy a Redis container.
- Understanding of application data access patterns and hotspots.
- Knowledge of which queries/data benefit most from caching.
- Monitoring tools to measure cache hit rates and performance.
- Development environment for testing caching implementation.
- Understanding of cache invalidation requirements for data consistency.

## Instructions

### Step 1: Analyze Caching Requirements
1. Profile database queries to identify slow or frequently executed queries.
2. Determine which data is read-heavy vs write-heavy.
3. Identify data that can tolerate eventual consistency.
4. Calculate expected cache size and Redis memory requirements.
5. Document current database load and target performance metrics.

### Step 2: Choose Caching Strategy
1. **Cache-Aside (Lazy Loading)**: Application checks cache first, loads from DB on miss.
   - Best for: Read-heavy workloads, unpredictable access patterns.
2. **Write-Through**: Application writes to cache and database simultaneously.
   - Best for: Write-heavy workloads needing consistency.
3. **Write-Behind (Write-Back)**: Application writes to cache, async writes to database.
   - Best for: High write throughput requirements.

### Step 3: Design Cache Architecture
1. Set up Redis as a distributed cache layer (L2 cache).
2. Implement in-memory LRU cache in the application (L1 cache).
3. Configure CDN for static assets (images, CSS, JS).
4. Design cache key naming convention (e.g., `user:123:profile`).
5. Define TTL (Time To Live) for different data types.

### Step 4: Implement Caching Code
1. Add Redis client library to application dependencies.
2. Create cache wrapper functions (get, set, delete, invalidate).
3. Modify database query code to check cache before DB query.
4. Implement cache population on cache miss.
5. Add error handling for cache failures (fail gracefully to database).

### Step 5: Configure Cache Invalidation
1. Implement TTL-based expiration for time-sensitive data.
2. Add explicit cache invalidation on data updates/deletes.
3. Use cache tags or patterns for bulk invalidation.
4. Implement cache warming for critical data after deployments.
5. Set up cache stampede prevention (lock/queue on miss).

### Step 6: Monitor and Optimize
1. Track cache hit rate, miss rate, and eviction rate.
2. Monitor Redis memory usage and eviction policy.
3. Analyze query performance improvements.
4. Adjust TTLs based on data update frequency.
5. Identify and cache additional hot data.

## Best Practices
- Implement proper cache invalidation strategies to ensure data consistency.
- Design effective cache keys to avoid collisions and maximize cache hit rate.
- Monitor cache performance and adjust caching strategies as needed.

## Examples

### Example 1: Implementing Redis Caching
User request: "Implement Redis caching for my PostgreSQL database to improve query performance."
- The skill will generate code to integrate Redis as a caching layer for the PostgreSQL database and configure cache-aside strategy for frequently accessed data.

### Example 2: Adding In-Memory Caching
User request: "Add an in-memory cache layer to my application to reduce latency for frequently accessed data."
- The skill will implement an in-memory cache using a suitable library and configure the application to check the in-memory cache before querying the database.

## Integration

This skill can be integrated with other database management and deployment tools to automate the entire caching implementation process. It also complements skills related to database schema design and query optimization.