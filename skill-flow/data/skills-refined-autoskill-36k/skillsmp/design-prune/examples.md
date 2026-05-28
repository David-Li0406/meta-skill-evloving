# Pruning Examples

Complete usage examples for design-prune skill in different scenarios.

## Example 1: Normal Mode Pruning

**User request:**

> Prune observability.md

**Execution:**

1. Read observability.md (1,245 lines)
2. Analyze content for staleness
3. Identify prunable sections
4. Generate pruning plan
5. Apply removals
6. Create archive file

**Output:**

```markdown
# Pruning Complete - observability.md

**Module:** effect-type-registry
**Document:** observability.md
**Date:** 2026-01-17
**Mode:** Normal

## Results

- **Original size:** 1,245 lines
- **After pruning:** 892 lines
- **Removed:** 353 lines (28% reduction)
- **Archived:** Yes → observability-history.md

## Content Removed

### 1. Implementation History (78 lines)

**Lines:** 234-312
**Staleness:** 85/100

Detailed timeline of implementation phases from June-August 2024.

**Reason:** Historical timeline, not current state

### 2. Migration from v1 (67 lines)

**Lines:** 456-523
**Staleness:** 92/100

Step-by-step migration guide from v1 to v2.

**Reason:** v1 migration completed 8 months ago

### 3. Deprecated Event Types (30 lines)

**Lines:** 678-708
**Staleness:** 78/100

List of deprecated event types with old → new mapping.

**Reason:** Deprecated > 6 months ago, well communicated

### 4. Old Benchmarks (24 lines)

**Lines:** 823-847
**Staleness:** 88/100

Benchmark results from June 2024.

**Reason:** 8 months old, likely outdated

### 5. Redundant Overview (22 lines)

**Lines:** 12-34
**Staleness:** 45/100

Overview section duplicating Introduction.

**Reason:** Duplicate content

### 6. API Documentation Duplication (144 lines)

**Lines:** 912-1056
**Staleness:** 35/100

Full API reference duplicating auto-generated docs.

**Reason:** Better in auto-generated API docs

**Replacement:** Link to `/api/observability`

### 7. Old Decision Rationale (24 lines)

**Lines:** 1089-1113
**Staleness:** 70/100

"Why Not Redis" section explaining why Redis wasn't chosen.

**Reason:** Still valuable context (kept in normal mode)
**Action:** Kept (not removed)

## Benefits

- 28% smaller, more focused
- Easier to maintain
- Current information only
- Faster to read for new contributors

## Archive

Historical content preserved in:

`.claude/design/effect-type-registry/_archive/observability-history.md`

## Validation

- ✅ Structure valid
- ✅ No broken cross-references
- ✅ Markdown linting passed
- ✅ Completeness: 85% → 82%

## Next Steps

1. Review pruned document for flow
2. Update links from other docs if needed
3. Consider pruning other docs in module
```

## Example 2: Aggressive Mode Pruning

**User request:**

> Aggressively prune observability.md to focus only on current state

**Execution:**

1. Read observability.md
2. Apply aggressive mode rules
3. Remove all historical content
4. Remove all design rationales

**Output:**

```markdown
# Pruning Complete - observability.md

**Module:** effect-type-registry
**Document:** observability.md
**Date:** 2026-01-17
**Mode:** Aggressive

## Results

- **Original size:** 1,245 lines
- **After pruning:** 748 lines
- **Removed:** 497 lines (40% reduction)
- **Archived:** Yes → observability-history.md

## Content Removed (Additional from Normal Mode)

All removals from normal mode (353 lines) plus:

### 8. Old Decision Rationale (24 lines)

"Why Not Redis" section explaining past decisions.

**Reason:** Aggressive mode removes all historical context

### 9. Implementation Notes (45 lines)

Notes on implementation approach and trade-offs.

**Reason:** Focused on how, not why

### 10. Evolution Section (38 lines)

How the observability system evolved over time.

**Reason:** Historical, not current

### 11. Lessons Learned (37 lines)

Lessons from implementing the observability system.

**Reason:** Historical insights, not current state

## Comparison with Normal Mode

**Normal:** 353 lines removed (28%)
**Aggressive:** 497 lines removed (40%)
**Difference:** 144 lines of valuable context removed

## Trade-offs

**Gained:**

- Maximum brevity
- Pure current state
- No historical baggage

**Lost:**

- Design decision context
- Implementation rationale
- Lessons learned

## Recommendation

Consider if context loss is acceptable. For new contributors, historical
context can be valuable for understanding why things are the way they are.
```

## Example 3: Preview Mode

**User request:**

> Show what would be pruned from all effect-type-registry docs

**Execution:**

1. Scan all docs in module
2. Analyze each without modifying
3. Generate preview report

**Output:**

```markdown
# Pruning Preview - effect-type-registry

**Total documents:** 4
**Total prunable content:** 687 lines (24% of 2,863 lines)
**Mode:** Normal (preview only, no changes made)

## Per-Document Analysis

### observability.md

**Current:** 1,245 lines
**After pruning:** 892 lines
**Reduction:** 353 lines (28%)

**Sections to remove:**

1. Implementation History (78 lines) - Staleness: 85/100
2. Migration from v1 (67 lines) - Staleness: 92/100
3. Deprecated Events (30 lines) - Staleness: 78/100
4. Old Benchmarks (24 lines) - Staleness: 88/100
5. Redundant sections (154 lines) - Staleness: 40-50/100

**Priority:** High (significant cruft)

### architecture.md

**Current:** 892 lines
**After pruning:** 756 lines
**Reduction:** 136 lines (15%)

**Sections to remove:**

1. Historical Architecture (45 lines) - Staleness: 82/100
2. Old Component Diagram (32 lines) - Staleness: 75/100
3. Version History (28 lines) - Staleness: 90/100
4. Duplicate Overview (31 lines) - Staleness: 55/100

**Priority:** Medium (moderate cruft)

### cache-optimization.md

**Current:** 623 lines
**After pruning:** 512 lines
**Reduction:** 111 lines (18%)

**Sections to remove:**

1. Original Design (42 lines) - Staleness: 88/100
2. Failed Experiments (35 lines) - Staleness: 80/100
3. Old Metrics (24 lines) - Staleness: 86/100
4. Excessive API docs (10 lines) - Staleness: 40/100

**Priority:** Medium (some cruft)

### type-system.md

**Current:** 234 lines
**After pruning:** 147 lines
**Reduction:** 87 lines (37%)

**Sections to remove:**

1. Stub sections (45 lines) - Empty TODOs
2. Placeholder content (32 lines) - "{To be filled}"
3. Incomplete examples (10 lines) - Not finished

**Priority:** Critical (doc is 37% stubs/placeholders)

**Recommendation:** Consider completing type-system.md rather than pruning.
A 37% reduction suggests the doc is incomplete, not just cruft-filled.

## Summary Recommendations

1. **Prune immediately:** observability.md (28% cruft)
2. **Prune soon:** architecture.md (15% cruft)
3. **Prune eventually:** cache-optimization.md (18% cruft)
4. **Complete instead:** type-system.md (37% incomplete)

## Estimated Impact

**Before:** 2,863 lines total
**After:** 2,176 lines total
**Reduction:** 687 lines (24%)

**Benefits:**

- More focused documentation
- Easier maintenance
- Current information only

**Next Steps:**

1. Run actual pruning (remove `--preview` flag)
2. Review type-system.md completion status
3. Set up quarterly pruning schedule
```

## Example 4: Conservative Mode

**User request:**

> Conservatively prune cache-optimization.md

**Execution:**

1. Read cache-optimization.md
2. Apply conservative rules (only obvious cruft)
3. Keep valuable history

**Output:**

```markdown
# Pruning Complete - cache-optimization.md

**Module:** effect-type-registry
**Document:** cache-optimization.md
**Date:** 2026-01-17
**Mode:** Conservative

## Results

- **Original size:** 623 lines
- **After pruning:** 589 lines
- **Removed:** 34 lines (5% reduction)
- **Archived:** No (minimal content, kept inline)

## Content Removed

### 1. Very Old Benchmarks (18 lines)

Benchmark results from 2023 (>18 months old).

**Reason:** Clearly outdated, multiple architecture changes since

### 2. Completed Migration Note (16 lines)

Migration from v0.9 to v1.0 (completed 2 years ago).

**Reason:** Migration window long closed

## Content Kept (Conservative Mode)

### Failed Experiments (35 lines)

Kept: Explains why current approach was chosen

### Design Rationale (45 lines)

Kept: Valuable context for understanding trade-offs

### Implementation History (28 lines)

Kept: Helps understand evolution

## Conservative Mode Philosophy

Only removed content that was:

- Demonstrably obsolete (> 18 months old)
- Clearly completed (v0.9 migration)
- No longer relevant

Kept anything that might provide valuable context.

## Next Steps

- Review in 6 months
- Consider normal mode if more cruft accumulates
```

## Example 5: Single Section Removal

**User request:**

> Remove the implementation history from observability.md

**Execution:**

1. Read observability.md
2. Find "Implementation History" section
3. Remove section
4. Update structure

**Output:**

```markdown
# Section Removed - observability.md

**Section:** Implementation History
**Lines removed:** 78 (lines 234-312)
**Archive:** No (user didn't request)

## Before

```markdown
## Current State

...

## Implementation History

### Phase 1 (June 2024)
Initially implemented basic console logging...

### Phase 2 (July 2024)
Added structured logging...

### Phase 3 (August 2024)
Metrics collection...

## Architecture

...
```

## After

```markdown
## Current State

...

## Architecture

...
```

## Impact

- Document: 1,245 → 1,167 lines
- Removed historical timeline
- Improved focus on current state

## Warning

Content permanently removed (no archive created).
Consider archiving if history might be needed later.

## Example 6: Stub Document Pruning

**User request:**

> Prune type-system.md

**Execution:**

1. Read type-system.md
2. Detect high percentage of stubs
3. Recommend completion over pruning

**Output:**

```markdown
# Pruning Analysis - type-system.md

**Module:** effect-type-registry
**Document:** type-system.md
**Date:** 2026-01-17

## Analysis Results

- **Current size:** 234 lines
- **Prunable content:** 87 lines (37%)
- **Status:** Stub/incomplete document

## Prunable Content Found

### 1. Empty TODO Sections (45 lines)

```markdown
## Advanced Type Resolution

TODO: Document advanced resolution strategies

## Performance Optimization

TODO: Add benchmarks and optimization techniques
```

### 2. Placeholder Text (32 lines)

```markdown
{Details to be filled in once implementation is complete}

{This section will describe the type system architecture}
```

### 3. Incomplete Examples (10 lines)

Started examples that trail off without completion.

## Recommendation

⚠️ **Do not prune this document.**

**Reason:** 37% prunable content indicates document is incomplete, not
cruft-filled.

**Better actions:**

1. **Complete the document:** Fill in TODO sections
2. **Update status:** Mark as `status: stub` in frontmatter
3. **Or archive entirely:** If type system docs aren't priority

**Pruning would:**

- Remove placeholders (good)
- But leave incomplete document (bad)
- Not address root issue (incompleteness)

## Suggested Next Steps

1. Decide if type system documentation is priority
2. If yes: Complete TODO sections, remove placeholders
3. If no: Archive document with `reason: incomplete`
4. Then consider pruning for any remaining cruft

## If You Still Want to Prune

Removing placeholders would yield:

- Before: 234 lines
- After: 147 lines
- Reduction: 87 lines (37%)

But document would still be incomplete.

## Example 7: Multi-Document Batch Pruning

**User request:**

> Prune all design docs in effect-type-registry

**Execution:**

1. Load all docs in module (4 docs)
2. Prune each according to normal mode
3. Generate combined report

**Output:**

```markdown
# Batch Pruning Complete - effect-type-registry

**Documents:** 4
**Mode:** Normal
**Date:** 2026-01-17

## Overall Results

- **Total before:** 2,863 lines
- **Total after:** 2,176 lines
- **Total removed:** 687 lines (24% reduction)
- **Archives created:** 3

## Per-Document Results

### observability.md ✅

- Removed: 353 lines (28%)
- Archive: observability-history.md
- Status: Pruned successfully

### architecture.md ✅

- Removed: 136 lines (15%)
- Archive: architecture-history.md
- Status: Pruned successfully

### cache-optimization.md ✅

- Removed: 111 lines (18%)
- Archive: cache-optimization-history.md
- Status: Pruned successfully

### type-system.md ⚠️

- Removed: 0 lines (0%)
- Archive: None
- Status: Skipped (recommend completion, not pruning)
- Note: 37% stub content detected

## Archives Created

All removed content saved to:

```text
.claude/design/effect-type-registry/_archive/
├── observability-history.md
├── architecture-history.md
└── cache-optimization-history.md
```

## Benefits

- 24% reduction in total documentation size
- More focused on current state
- Historical content preserved in archives
- Easier maintenance going forward

## Recommendations

1. Review type-system.md for completion
2. Set up quarterly pruning schedule
3. Monitor for future cruft accumulation

## Validation

- ✅ All pruned docs valid markdown
- ✅ No broken cross-references
- ✅ All links functional
- ✅ Frontmatter correct

## Example 8: Archive Creation

**User request:**

> Prune observability.md and archive removed content

**Archive file created:**

```markdown
# Observability System - Historical Content

**Archived from:** observability.md
**Archive date:** 2026-01-17
**Reason:** Pruned during documentation maintenance
**Original completeness:** 85%

This file contains historical content removed from observability.md to
keep the main document focused on current state.

---

## Implementation History

### Phase 1 (June 2024)

Initially, we implemented basic console logging using simple console.log
statements throughout the codebase. This provided minimal visibility but
was sufficient for early development.

### Phase 2 (July 2024)

Added structured logging with pino. This provided JSON-structured logs
with context propagation and log levels. Migration from console.log to
structured logging took approximately 2 weeks.

### Phase 3 (August 2024)

Implemented metrics collection using custom MetricsCollector. This
allowed tracking cache hits/misses, fetch latency, and error rates.

---

## Migration from v1 to v2

If you're upgrading from version 1.x of the observability system:

### Breaking Changes

1. Event names changed from dot notation to colon notation
   - Old: `cache.hit`, `cache.miss`
   - New: `cache:hit`, `cache:miss`

2. Logger API simplified
   - Old: `Logger.getInstance().log(level, message)`
   - New: `logger.log(message)` (level in context)

### Migration Steps

1. Update all event listeners to use new event names
2. Replace Logger.getInstance() calls with new logger API
3. Update metric collection to use MetricsCollector
4. Run migration verification: `npm run verify-observability`

### Timeline

- v2.0 released: 2024-08-15
- v1.x support until: 2025-02-15
- Migration deadline: 2025-03-01

---

## Old Benchmarks

Benchmark results from June 2024 (macOS, M1 Pro, 32GB RAM):

**Event Emission:**

- Empty event: 0.02ms
- Event with payload: 0.05ms
- 1000 events: 45ms total

**Logger Performance:**

- Console write: 0.08ms
- Structured log: 0.12ms
- 1000 logs: 115ms total

**Metrics Collection:**

- Counter increment: 0.01ms
- Gauge update: 0.01ms
- Histogram record: 0.03ms

**Note:** These benchmarks were run before optimization work in August 2024.
Current performance is likely better but not re-benchmarked.

---

## Deprecated Event Types

⚠️ The following event types are deprecated as of v2.0:

**Cache events:**

- `cache.hit` → use `cache:hit`
- `cache.miss` → use `cache:miss`
- `cache.evict` → use `cache:evict`

**Fetch events:**

- `fetch.start` → use `fetch:start`
- `fetch.complete` → use `fetch:complete`
- `fetch.error` → use `fetch:error`

**Type events:**

- `type.resolve` → use `type:resolve`
- `type.error` → use `type:error`

Deprecated events will be removed in v3.0 (estimated Q2 2025).

---

## Reference

For current observability documentation, see:
[observability.md](../observability.md)
```

## Example 9: No Prunable Content

**User request:**

> Prune newly-created-doc.md

**Output:**

```markdown
# No Pruning Needed - newly-created-doc.md

**Module:** effect-type-registry
**Document:** newly-created-doc.md
**Date:** 2026-01-17

## Analysis Results

- **Document age:** 2 weeks
- **Staleness score:** 12/100 (very fresh)
- **Prunable content:** 0 lines
- **Status:** Current and focused

## Content Analysis

✅ No historical content
✅ No deprecated features
✅ No redundancy
✅ No old benchmarks
✅ Current architecture only

## Recommendation

No pruning needed. Document is current, focused, and well-maintained.

**Next review:** 2026-04-17 (3 months)
```

## Example 10: Error - Document Too Small

**User request:**

> Prune short-doc.md

**Output:**

```markdown
# Pruning Not Recommended - short-doc.md

**Module:** effect-type-registry
**Document:** short-doc.md
**Size:** 89 lines

## Warning

Document is very small (< 100 lines).

Pruning might remove valuable content and leave document too sparse.

## Recommendation

**Instead of pruning:**

1. Consider if document should exist at all
2. If yes: Expand with more details
3. If no: Archive entire document

**If you still want to prune:**

Add `--force` flag to override this warning.

## Prunable Content Found

- 12 lines of old migration notes
- Would reduce to 77 lines

At 77 lines, document would be very minimal.
```
