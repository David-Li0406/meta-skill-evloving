---
name: api-cache-redis
description: Generate Redis cache service with tenant-prefixed keys to prevent cross-tenant leakage, TTL management, and cache invalidation patterns. Use when caching data or reducing database load.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Redis Cache Service

## Purpose

Generate Redis cache service with tenant-prefixed keys to prevent cross-tenant data leakage, TTL management for memory efficiency, and cache invalidation patterns.

## When to Use

- Caching frequently accessed data
- Session storage
- Rate limiting
- Reducing database load
- Tenant-isolated caching

## What It Generates

### Directory Structure

```
apps/api/src/modules/{feature}/services/
├── {feature}-cache.service.ts
├── {feature}-cache.service.spec.ts
└── index.ts
```

## Patterns Enforced

### Tenant-Prefixed Keys

Cache keys use format: `tenant:{tenantId}:{key}`

- Prevents cross-tenant cache pollution
- Enables tenant-wide cache clearing
- Isolates rate limit counters

### TTL Management

- All cache keys have TTL
- Default TTL: 5 minutes (300 seconds)
- Session TTL: 24 hours (86400 seconds)
- No infinite TTL (prevents memory leaks)

### Cache Invalidation

- Pattern-based deletion: `delPattern('tenant:{tenantId}:*')`
- Tag-based invalidation
- Automatic invalidation on updates

## Usage Example

```bash
/skill cache-redis --name=User --methods='cacheUser,cachePermissions,clearUserCache'
```

## Related Files

- [Data Repository](../../core/data-repository/SKILL.md) - Repository using cache
- [BullMQ Queues](../queue-bullmq/SKILL.md) - Queue jobs with caching
