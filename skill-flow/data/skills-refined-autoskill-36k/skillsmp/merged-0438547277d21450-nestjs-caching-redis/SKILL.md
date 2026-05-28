---
name: nestjs-caching-redis
description: Use this skill when implementing multi-level caching and Redis integration in high-performance NestJS applications.
---

# Caching & Redis Standards

## **Priority: P1 (OPERATIONAL)**

Caching strategies and Redis integration patterns for high-performance NestJS applications.

## Caching Strategy

- **Layering**: Use **Multi-Level Caching** for high-traffic read endpoints.
  - **L1 (Local)**: In-Memory (Node.js heap). Ultra-fast, no network. Ideal for config/static data. Use `lru-cache`.
  - **L2 (Distributed)**: Redis. Shared across pods.
- **Pattern**: Implement **Stale-While-Revalidate** where possible to avoid latency spikes during cache misses.

## NestJS Implementation

- **Library**: Use `cache-manager` with `cache-manager-redis-yet` (Recommended over `cache-manager-redis-store` for better V4 support and stability).
- **Interceptors**: Use `@UseInterceptors(CacheInterceptor)` for simple GET responses.
  - **Warning**: By default, this uses the URL as the key. Ensure consistent query param ordering or custom key generators.
- **Decorators**: Standardize custom cache keys.

  ```typescript
  @CacheKey('<custom_key>')
  @CacheTTL(<ttl_in_seconds>) // e.g., 300 for 5 minutes
  findAll() { ... }
  ```

## Redis Data Structures (Expert)

- Don't just use `GET/SET`.
- **Hash (`HSET`)**: Storing objects (User profiles). Allows partial updates (`HSET user:1 lastLogin result`) without serialization overhead.
- **Set (`SADD`)**: Unique collections (e.g., "Online User IDs"). O(1) membership checks.
- **Sorted Set (`ZADD`)**: Priority queues, Leaderboards, or Rate Limiting windows.

## Invalidation Patterns

- **Problem**: "There are only two hard things in Computer Science: cache invalidation and naming things."
- **Tagging**: Since Redis doesn't support wildcards efficiently (`KEYS` is O(N) - bans in PROD), use **Sets** to group keys.
  - _Create_: `SADD <tag>:<id> <cache_key>`
  - _Invalidate_: Fetch tags from Set, then `DEL` usage keys.
- **Event-Driven**: Listen to Domain Events (e.g., `UserUpdated`) to trigger invalidation asynchronously.

## Stampede Protection

- **Jitter**: Add random variance to TTLs (e.g., <ttl> ± <variance>) to prevent all keys expiring simultaneously.
- **Locking**: If a key is missing, **one** process computes it while others wait or return stale. (Complex, often handled by `swr` libraries).