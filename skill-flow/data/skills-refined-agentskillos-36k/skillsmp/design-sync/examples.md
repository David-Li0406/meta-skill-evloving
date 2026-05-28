# Sync Examples

Complete usage examples for design-sync skill in different scenarios.

## Example 1: Full Sync with Auto-Update

**User request:**

> Sync effect-type-registry docs and apply safe updates

**Execution:**

1. Load design.config.json for module path
2. Find all design docs in `.claude/design/effect-type-registry/`
3. For each doc:
   - Read content and extract file references
   - Analyze source code in `pkgs/effect-type-registry/src/`
   - Find discrepancies
   - Apply safe updates
   - Update last-synced timestamp
4. Generate summary report

**Output:**

```markdown
# Sync Results - effect-type-registry

**Documents Synced:** 4/4
**Issues Found:** 2
**Updates Applied:** 8
**Sync Date:** 2026-01-17

## Per-Document Results

### observability.md ✅

- Updates: 5 applied
- Issues: 1 (DiskCache deleted)
- Last synced: 2026-01-17

**Updates applied:**

1. Added CacheStrategy to exports list
2. Updated EventEmitter.ts path (was events.ts)
3. Updated line count (500 → 687 lines)
4. Marked Phase 2 as complete
5. Added pino to dependencies

**Manual review needed:**

- Line 45: DiskCache.ts referenced but file deleted
  - Check: `git log --all -- "**/DiskCache.ts"`
  - Action: Update docs to reflect current caching approach

### architecture.md ✅

- Updates: 2 applied
- Issues: 0
- Last synced: 2026-01-17

**Updates applied:**

1. Updated component diagram file path
2. Added new CacheStrategy component

### cache-optimization.md ⚠️

- Updates: 1 applied
- Issues: 1 (metrics unverified)
- Last synced: 2026-01-17

**Updates applied:**

1. Updated cache file references

**Manual review needed:**

- Line 67: Cache hit rate claim (85%) has no instrumentation
  - Action: Verify metric source or remove claim

### type-system.md ✅

- Updates: 0 (doc is accurate)
- Issues: 0
- Last synced: 2026-01-17

## Summary

- 8 total updates applied across 4 documents
- 2 issues require manual review
- All docs marked as synced

**Manual review needed:**

1. observability.md: Resolve DiskCache deletion
2. cache-optimization.md: Verify cache hit rate metric
```

## Example 2: Check-Only Mode

**User request:**

> Check if observability.md is current

**Execution:**

1. Load observability.md
2. Analyze referenced code
3. Report discrepancies
4. No updates applied

**Output:**

```markdown
# Sync Check - observability.md

**Status:** ⚠️  Out of sync
**Last synced:** 2026-01-10 (7 days ago)
**Module:** effect-type-registry
**Issues:** 3

## Discrepancies Found

### Issue 1: File reference outdated ⚠️

**Section:** Current State
**Line:** 45

**Documented:**

> The cache implementation is in `src/cache/DiskCache.ts`

**Reality:**

- File `src/cache/DiskCache.ts` does not exist
- May have been deleted or moved

**Fix:**

Check git history:

```bash
git log --all --full-history -- "**/DiskCache.ts"
```

### Issue 2: New export undocumented ⚠️

**Section:** Implementation Details

**Documented exports:**

- TypeRegistry
- PackageFetcher

**Actual exports (src/index.ts):**

- TypeRegistry (documented ✅)
- PackageFetcher (documented ✅)
- CacheStrategy (missing from docs ⚠️)
- EventEmitter (missing from docs ⚠️)

**Fix:**

Add CacheStrategy and EventEmitter to exports documentation

### Issue 3: Phase 2 complete but marked as planned ⚠️

**Section:** Future Enhancements

**Documented:**

> **Phase 2:** Implement structured logging

**Reality:**

- File exists: `src/observability/Logger.ts`
- Exports: `StructuredLogger`, `LogLevel`, `LogContext`
- Lines: 189

**Fix:**

Move to "Current State" section and mark as complete

## Verification Details

**Files checked:** 8

1. ✅ src/TypeRegistry.ts - Exists, 456 lines
2. ✅ src/PackageFetcher.ts - Exists, 234 lines
3. ❌ src/cache/DiskCache.ts - NOT FOUND
4. ✅ src/observability/EventEmitter.ts - Exists, 234 lines
5. ✅ src/observability/Logger.ts - Exists, 189 lines
6. ✅ src/observability/Metrics.ts - Exists, 264 lines
7. ✅ src/index.ts - Exists, 45 lines
8. ✅ package.json - Exists

## Recommendation

Run sync with auto-update to apply 2 safe fixes:

```bash
/design-sync effect-type-registry observability.md --auto-update
```

Then manually resolve DiskCache deletion.

**User request:**

> Sync just the cache-optimization.md file

**Execution:**

1. Load cache-optimization.md from effect-type-registry
2. Analyze referenced cache implementation files
3. Find discrepancies
4. Apply safe updates

**Output:**

```markdown
# Sync Report - cache-optimization.md

**Module:** effect-type-registry
**Document:** cache-optimization.md
**Sync Date:** 2026-01-17
**Last synced:** never → 2026-01-17

## Summary

- **Files Checked:** 5
- **Issues Found:** 1
- **Updates Applied:** 3
- **Auto-Applied:** 3 (auto-update: true)

## Updates Applied

### Update 1: File path correction ✅

**Section:** Implementation
**Line:** 34

**Before:**

> Cache implementation in `src/cache/LRUCache.ts`

**After:**

> Cache implementation in `src/cache/Cache.ts`

**Reason:** File renamed from LRUCache.ts to Cache.ts

### Update 2: Add eviction strategy ✅

**Section:** Features

**Before:**

> - TTL-based expiration
> - Size-based limits

**After:**

> - TTL-based expiration
> - Size-based limits
> - LRU eviction strategy

**Reason:** LRU eviction implemented in Cache.ts:67

### Update 3: Update dependency ✅

**Section:** Dependencies

**Before:**

> No external dependencies

**After:**

> Dependencies:
> - Effect-TS (runtime)

**Reason:** Effect-TS added to package.json dependencies

## Manual Review Needed

### Issue 1: Metric claim unverified ⚠️

**Section:** Performance
**Line:** 78

**Documented:**

> Achieves 85% cache hit rate in production

**Reality:**

- No instrumentation found for cache hit rate
- No metrics collection in Cache.ts
- Cannot verify claim

**Options:**

1. Verify metric from logs/monitoring
2. Add instrumentation to track cache hits
3. Remove claim if unverifiable

## Verification

**Files verified:**

1. ✅ src/cache/Cache.ts - Exists, 345 lines
2. ✅ src/cache/CacheStrategy.ts - Exists, 89 lines
3. ✅ src/cache/types.ts - Exists, 45 lines
4. ✅ package.json - Exists
5. ✅ src/index.ts - Exports verified

**Exports from Cache.ts:**

- Cache (documented ✅)
- CacheStrategy (documented ✅)
- LRUEviction (documented ✅)

## Next Steps

1. Verify cache hit rate metric source
2. Add instrumentation if metric is current goal
3. Re-run sync after manual fixes: `/design-sync effect-type-registry cache-optimization.md`
```

## Example 4: Newly Implemented Feature Detection

**User request:**

> Sync design docs after implementing Phase 2 features

**Execution:**

1. Scan "Future Enhancements" sections
2. Check if planned files now exist
3. Suggest moving to "Current State"
4. Apply update if safe

**Output:**

```markdown
# Sync Report - Newly Implemented Features

**Module:** effect-type-registry
**Documents:** observability.md, architecture.md

## Detected Implementations

### Feature 1: Structured Logging (observability.md) ✅

**Documented as planned:**

> **Phase 2:** Implement structured logging with context propagation

**Now implemented:**

- File: `src/observability/Logger.ts` (189 lines)
- Exports: `StructuredLogger`, `LogLevel`, `LogContext`
- Implementation matches plan

**Update applied:**

Moved from "Future Enhancements" to "Current State":

> **Structured Logging:** Implemented in src/observability/Logger.ts
>
> Provides JSON-structured logs with context propagation and correlation IDs.
> Supports multiple log levels and custom context fields.

### Feature 2: Metrics Collection (observability.md) ✅

**Documented as planned:**

> **Phase 3:** Add metrics collection for cache performance

**Now implemented:**

- File: `src/observability/Metrics.ts` (264 lines)
- Exports: `MetricsCollector`, `Counter`, `Gauge`, `Histogram`
- Implementation matches plan

**Update applied:**

Moved from "Future Enhancements" to "Current State":

> **Metrics Collection:** Implemented in src/observability/Metrics.ts
>
> Collects performance metrics including cache hits/misses, fetch latency,
> and error rates. Metrics can be exported to monitoring systems.

### Feature 3: Cache Strategy Abstraction (architecture.md) ✅

**Documented as planned:**

> Future: Abstract cache eviction strategies

**Now implemented:**

- File: `src/cache/CacheStrategy.ts` (89 lines)
- Exports: `CacheStrategy`, `LRUStrategy`, `TTLStrategy`
- Matches planned architecture

**Update applied:**

Moved to "Current Architecture" and updated diagram reference

## Summary

- ✅ 3 planned features now implemented
- ✅ All moved from Future Enhancements to Current State
- ✅ Implementation matches documented plans
- ✅ No architectural surprises

## Completeness Updates

### observability.md

- Before: 65%
- After: 85%
- Reason: Two major phases completed, added comprehensive sections

### architecture.md

- Before: 70%
- After: 75%
- Reason: Added CacheStrategy architecture details

## Next Steps

1. Review generated Current State sections for accuracy
2. Add any implementation details not in original plan
3. Update related docs that depend on these features
```

## Example 5: Refactored Code Detection

**User request:**

> Sync after major cache refactor

**Execution:**

1. Detect multiple file path changes
2. Check git history for renames vs deletions
3. Update paths safely
4. Flag architectural changes for review

**Output:**

```markdown
# Sync Report - After Cache Refactor

**Module:** effect-type-registry
**Document:** cache-optimization.md
**Sync Date:** 2026-01-17

## Refactoring Detected

**Files changed:** 6 files renamed/moved

### File Path Updates Applied (6) ✅

1. `src/cache/DiskCache.ts` → `src/cache/Cache.ts`
   - Git: Renamed in commit abc1234
   - Lines updated: 23, 45, 67

2. `src/cache/MemoryCache.ts` → (merged into `src/cache/Cache.ts`)
   - Git: Deleted, content merged
   - Lines updated: 89

3. `src/cache/LRUEviction.ts` → `src/cache/strategies/LRU.ts`
   - Git: Moved to subdirectory
   - Lines updated: 101

4. `src/cache/TTLEviction.ts` → `src/cache/strategies/TTL.ts`
   - Git: Moved to subdirectory
   - Lines updated: 103

5. `src/cache/types.ts` → `src/cache/types/index.ts`
   - Git: Restructured
   - Lines updated: 125

6. `src/cache/index.ts` → (remains same)
   - No change needed

### Architectural Changes Detected ⚠️

**Current documentation:**

> Cache uses separate DiskCache and MemoryCache implementations with
> coordinated eviction.

**Current implementation:**

> Unified Cache class with pluggable strategy pattern. Strategies in
> src/cache/strategies/ subdirectory.

**Action required:**

Update "Architecture" section to reflect:

1. Unified Cache implementation (not separate Disk/Memory)
2. Strategy pattern for eviction (LRU, TTL)
3. New directory structure

## Summary

- ✅ 6 file paths updated automatically
- ⚠️  1 architectural description needs manual update
- ✅ All references to old files corrected
- ⚠️  Design rationale may need update

## Manual Review Needed

### Architecture Section Update

**Section:** Architecture Overview

**Current:**

> The cache system uses two complementary implementations:
>
> 1. **MemoryCache**: Fast in-memory LRU cache
> 2. **DiskCache**: Persistent disk-based cache with TTL
>
> Both share a common eviction coordinator.

**Suggested:**

> The cache system uses a unified Cache implementation with pluggable
> strategies:
>
> 1. **Cache**: Main cache implementation (src/cache/Cache.ts)
> 2. **Strategies**: Pluggable eviction strategies (src/cache/strategies/)
>    - LRU: Least Recently Used eviction
>    - TTL: Time To Live expiration
>
> The strategy pattern allows runtime configuration of eviction behavior.

**Reason:** Architecture changed from dual-implementation to strategy pattern

## Next Steps

1. Review suggested architecture update
2. Update design rationale if pattern choice changed
3. Document why refactor from dual-cache to strategy pattern
4. Re-sync to verify: `/design-sync effect-type-registry cache-optimization.md --check-only`
```

## Example 6: Deleted Feature Detection

**User request:**

> Sync docs after removing experimental caching

**Execution:**

1. Detect referenced files deleted
2. Check if entire feature removed
3. Suggest archival or update

**Output:**

```markdown
# Sync Report - Deleted Feature Detected

**Module:** effect-type-registry
**Document:** experimental-caching.md
**Sync Date:** 2026-01-17

## Critical Issue: Feature Removed

### All Referenced Files Deleted ❌

**Files documented:** 4
**Files existing:** 0

1. ❌ src/cache/experimental/AdaptiveCache.ts - DELETED
2. ❌ src/cache/experimental/PredictiveEviction.ts - DELETED
3. ❌ src/cache/experimental/types.ts - DELETED
4. ❌ src/cache/experimental/index.ts - DELETED

**Git history:**

```text
commit def5678
Author: Developer
Date: 2026-01-15

Remove experimental caching - performance degradation in production
```

### Recommendation: Archive This Document ⚠️

**Reason:** Feature completely removed from codebase

**Options:**

1. **Archive document** (recommended)
   - Status: active → archived
   - Reason: completed (outcome: cancelled)
   - Notes: "Experiment showed performance degradation"
   - Keep for historical reference

2. **Delete document**
   - Only if no historical value
   - Loses context for why approach was tried

3. **Update document**
   - Document why experiment failed
   - Keep as lessons learned

## Suggested Archival Metadata

```yaml
archived:
  date: 2026-01-17
  reason: completed
  outcome: cancelled
  notes: >
    Experimental caching removed due to performance degradation.
    Benchmarks showed 15% slowdown vs standard approach.
    Returned to standard cache implementation.
```

## Next Steps

1. Run `/design-archive effect-type-registry experimental-caching.md`
   with `--reason=completed --outcome=cancelled`
2. Add lessons learned to cache-optimization.md
3. Document why approach was rejected

## Example 7: Dependency Changes Detection

**User request:**
> Sync after adding new dependencies

**Execution:**

1. Compare documented dependencies with package.json
2. Detect additions/removals
3. Apply safe updates for additions
4. Flag removals for review

**Output:**

```markdown
# Sync Report - Dependency Changes

**Module:** effect-type-registry
**Documents:** architecture.md, README updates
**Sync Date:** 2026-01-17

## Dependency Changes Detected

### New Dependencies Added (3) ✅

#### Dependency 1: pino

**Type:** peerDependency
**Version:** ^9.0.0
**Added:** Documented in architecture.md

**Update applied:**

> Dependencies:
> - Effect-TS (runtime)
> - pino (logging, optional peer dependency)

#### Dependency 2: @microsoft/api-extractor

**Type:** devDependency
**Version:** ^7.38.0
**Added:** Build tools section

**Update applied:**

> Build dependencies:
> - TypeScript
> - Rollup
> - API Extractor (type documentation)

#### Dependency 3: vitest

**Type:** devDependency
**Version:** ^2.0.0
**Added:** Testing section

**Update applied:**

> Test framework: Vitest with v8 coverage

### Dependencies Removed (1) ⚠️

#### Removed: jest

**Type:** devDependency
**Action:** Manual review needed

**Documented:**

> Tests run with Jest

**Reality:**

- jest no longer in devDependencies
- vitest now present
- Test files migrated (.test.ts → .test.ts with vitest syntax)

**Update needed:**

Replace Jest references with Vitest throughout documentation

## Summary

- ✅ 3 new dependencies documented
- ⚠️  1 dependency removal needs manual update
- ✅ All additions are safe updates

## Next Steps

1. Update testing section to reference Vitest
2. Update test command examples
3. Remove Jest-specific configuration docs
```

## Example 8: Interactive Mode

**User request:**

> Sync observability.md interactively

**Execution:**

1. Analyze doc
2. Find 5 potential updates
3. Prompt for each

**Output:**

```text
# Interactive Sync - observability.md

Analyzing document...
Found 5 potential updates.

---

Update 1 of 5:

**Type:** Safe update (file path)
**Section:** Current State (line 45)

**Current:**
> Event handlers in src/events.ts

**Suggested:**
> Event handlers in src/EventEmitter.ts

**Reason:** File renamed

Apply this update? (y/n/a=all/s=skip all safe): y

✅ Applied update 1

---

Update 2 of 5:

**Type:** Safe update (new export)
**Section:** Implementation Details

**Current:**
> Main exports: TypeRegistry, PackageFetcher

**Suggested:**
> Main exports: TypeRegistry, PackageFetcher, CacheStrategy

**Reason:** CacheStrategy exported from index.ts

Apply this update? (y/n/a/s): a

✅ Applying all remaining safe updates (3 more)

✅ Applied update 2
✅ Applied update 3 (line count)
✅ Applied update 4 (mark Phase 2 complete)

---

Update 5 of 5:

**Type:** Unsafe update (file deleted)
**Section:** Current State (line 67)

**Current:**
> Cache implementation in src/cache/DiskCache.ts

**Issue:** File DiskCache.ts deleted

Skip unsafe updates? (y/n): y

⚠️  Skipped unsafe update 5 (manual review needed)

---

# Interactive Sync Complete

**Applied:** 4 updates
**Skipped:** 1 unsafe update (manual review)
**Updated:** last-synced to 2026-01-17

## Manual Review Needed

1. Line 67: DiskCache.ts deleted
   - Check git history
   - Update to current cache approach
```

## Example 9: Multi-Module Sync

**User request:**

> Sync all design docs across all modules

**Execution:**

1. Load all modules from config
2. For each module, sync all docs
3. Generate combined report

**Output:**

```markdown
# Multi-Module Sync Report

**Modules:** 3
**Documents:** 12
**Sync Date:** 2026-01-17

## Module 1: effect-type-registry

**Documents:** 4 (observability.md, architecture.md, cache-optimization.md,
type-system.md)
**Updates:** 8 applied
**Issues:** 2 manual review

**Status:** ✅ Synced with warnings

## Module 2: rspress-plugin-api-extractor

**Documents:** 6
**Updates:** 3 applied
**Issues:** 0

**Status:** ✅ Fully synced

## Module 3: design-doc-system

**Documents:** 2
**Updates:** 0 (docs current)
**Issues:** 0

**Status:** ✅ Already current

## Summary

- **Total docs synced:** 12/12
- **Total updates:** 11
- **Issues requiring review:** 2
- **Completion:** 100%

## Issues Requiring Manual Review

### Issue 1: effect-type-registry/observability.md

- DiskCache.ts deleted but referenced (line 45)

### Issue 2: effect-type-registry/cache-optimization.md

- Cache hit rate metric unverified (line 78)

## Next Steps

1. Resolve 2 manual review items
2. Re-run sync on affected docs
3. All other docs current as of 2026-01-17
```

## Example 10: No Updates Needed

**User request:**

> Sync type-system.md

**Execution:**

1. Analyze document
2. Verify all references
3. No discrepancies found

**Output:**

```markdown
# Sync Report - type-system.md

**Module:** effect-type-registry
**Document:** type-system.md
**Sync Date:** 2026-01-17

## Result: Document is Current ✅

**Files checked:** 6
**Issues found:** 0
**Updates needed:** 0

## Verification

All documented files exist and match references:

1. ✅ src/types/TypeRegistry.ts - Exists, 245 lines
2. ✅ src/types/TypeNode.ts - Exists, 123 lines
3. ✅ src/types/Resolution.ts - Exists, 89 lines
4. ✅ src/types/index.ts - Exists, 34 lines
5. ✅ package.json - Exists
6. ✅ tsconfig.json - Exists

**Exports verified:**

- TypeNode ✅
- TypeResolution ✅
- TypeRegistry ✅

**Architecture verified:**

- Component structure matches documentation
- No new components added
- No files deleted

## Frontmatter Updated

```yaml
last-synced: 2026-01-17
updated: 2026-01-17
```

## Example 10 Recommendation

No action needed. Document accurately reflects current codebase state.
Next sync recommended: 2026-02-17 (30 days)
