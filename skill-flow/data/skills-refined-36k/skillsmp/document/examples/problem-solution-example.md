# Race Condition in Distributed Cache

## Metadata

- **Timestamp**: 2026-01-15 16:45:12
- **Project**: user-service
- **Category**: Problem-Solution
- **Tags**: concurrency, cache, redis, race-condition, critical
- **Related Commit**: f8b2c41
- **Severity**: High

## Problem Statement

Multiple concurrent requests to update user profiles were causing inconsistent cache state. Users would see stale data after updating their profile, and some updates were lost entirely.

- **Failure**: Cache contained outdated user data despite successful database updates
- **Observable symptom**: Users reporting profile changes not appearing, or reverting to old values
- **Impact**: ~5% of profile updates affected, poor user experience, loss of trust

## Context

The issue occurred during high-traffic periods, particularly:
- When users rapidly changed profile settings
- During automated batch updates
- Peak usage hours (11 AM - 2 PM UTC)

Components involved:
- User profile API endpoints
- Redis cache layer
- PostgreSQL user database
- Multiple application server instances

## Investigation Process

1. **Log analysis**: Noticed cache SET operations completing after database UPDATE
   - Discovered timing window of 50-200ms where race could occur
2. **Trace analysis**: Multiple concurrent requests for same user showed interleaved execution
   - Request A: read DB → update DB → set cache
   - Request B: read DB → update DB → set cache (overwrites A's changes)
3. **Reproduced locally**: Created test that spawned 10 concurrent updates to same user
   - Confirmed race condition reproducible with concurrent updates

### Root Cause

Cache-aside pattern implemented without pessimistic locking or versioning. The sequence was:

1. Request A reads user from DB (version 1)
2. Request B reads user from DB (version 1)
3. Request A updates DB (version 2)
4. Request B updates DB (version 3, overwrites A)
5. Request A writes to cache (version 2, stale)
6. Request B writes to cache (version 3, correct but A's write happened after)

The cache would contain whichever request's SET operation completed last, regardless of which update was newer.

## Solution

### Approach

Implemented optimistic locking using version numbers in both database and cache, with atomic compare-and-set operations in Redis.

**Alternatives considered:**
- Pessimistic locking: Rejected due to potential deadlocks and poor performance
- Cache-through pattern: Rejected due to complexity and single point of failure concerns
- Queue-based updates: Rejected due to added latency for synchronous operations

### Implementation

```go
type User struct {
    ID       string
    Email    string
    Name     string
    Version  int64  // Added version field
}

func (s *UserService) UpdateProfile(ctx context.Context, userID string, updates map[string]interface{}) error {
    const maxRetries = 3

    for attempt := 0; attempt < maxRetries; attempt++ {
        // Read current version
        user, err := s.repo.GetUser(ctx, userID)
        if err != nil {
            return err
        }

        // Update database with version check
        updated, err := s.repo.UpdateUserWithVersion(ctx, userID, user.Version, updates)
        if err != nil {
            if errors.Is(err, repo.ErrVersionMismatch) {
                continue // Retry on version mismatch
            }
            return err
        }

        // Update cache with compare-and-set
        cacheKey := fmt.Sprintf("user:%s:v%d", userID, updated.Version)
        err = s.cache.SetNX(ctx, cacheKey, updated, 1*time.Hour)
        if err != nil {
            log.Warn("cache update failed", "error", err)
            // Don't fail request if cache update fails
        }

        // Invalidate old cache entry
        oldCacheKey := fmt.Sprintf("user:%s:v%d", userID, user.Version)
        s.cache.Del(ctx, oldCacheKey)

        return nil
    }

    return errors.New("max retries exceeded due to concurrent modifications")
}
```

### Files Modified

- `internal/user/model.go` - Added Version field to User struct
- `internal/user/repository.go` - Implemented UpdateUserWithVersion with optimistic locking
- `internal/user/service.go` - Updated cache strategy with versioned keys
- `migrations/000015_add_user_version.sql` - Database migration for version column

## Verification

**Tests added:**
- `TestConcurrentProfileUpdates` - 50 goroutines updating same user
- `TestCacheConsistencyAfterUpdate` - Verifies cache reflects latest DB state
- `TestVersionMismatchRetry` - Validates retry logic on conflicts

**Manual validation:**
- Load tested with 100 concurrent requests per user
- Monitored cache hit/miss rates and version conflicts in staging
- Verified no stale data in cache after 1 hour of high-traffic simulation

**Metrics monitored:**
- Version conflict rate: < 0.1% of updates (acceptable)
- Cache consistency: 100% accurate after updates
- P99 latency: Increased by 5ms (acceptable trade-off)

## Prevention

**Changes implemented:**
1. Added integration test suite for concurrent scenarios
2. Updated code review checklist to include concurrency review for cache operations
3. Documented cache update patterns in team wiki
4. Set up alerting for high version conflict rates

**Future improvements:**
- Consider implementing distributed lock for critical operations
- Evaluate cache-through pattern for high-contention resources
- Add circuit breaker for cache operations

## Lessons Learned

- Cache-aside pattern requires careful concurrency handling in distributed systems
- Optimistic locking is effective but requires retry logic at application level
- Version conflicts are a good metric for detecting high contention
- Always test cache operations under concurrent load
- Don't fail user requests due to cache failures (cache should be transparent)
