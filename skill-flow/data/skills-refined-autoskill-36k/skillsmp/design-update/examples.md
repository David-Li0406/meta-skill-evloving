# Usage Examples

Complete examples of design-update skill usage in different scenarios.

## Example 1: Update Status

**User request:**

> Update cache-optimization.md status to draft in effect-type-registry

**Execution:**

1. Module: `effect-type-registry`
2. Doc: `cache-optimization.md`
3. Change: `status: stub` → `status: draft`
4. Also update: `updated: 2026-01-17`

**Validation:**

- Status "draft" requires completeness 21-60%
- Current completeness: 35% ✅
- Match confirmed, proceed

**Changes Made:**

```yaml
status: draft  # was: stub
updated: 2026-01-17  # was: 2026-01-10
```

**Output:**

```markdown
## Changes Made

**File:** .claude/design/effect-type-registry/cache-optimization.md

**Frontmatter Changes:**
- status: stub → draft
- updated: 2026-01-17

## Validation

✅ Status matches completeness (35%)
✅ All required fields present

## Next Steps

1. Continue filling in sections to reach 60%+ for current status
2. Run `/design-validate effect-type-registry` to check
```

## Example 2: Update Completeness

**User request:**

> Update observability.md completeness to 80 for effect-type-registry

**Execution:**

1. Module: `effect-type-registry`
2. Doc: `observability.md`
3. Change: `completeness: 65` → `completeness: 80`
4. Also update: `updated: 2026-01-17`

**Validation:**

- Completeness 80% suggests status "current" or "needs-review"
- Current status: "draft"
- Suggest status update

**Changes Made:**

```yaml
completeness: 80  # was: 65
updated: 2026-01-17
```

**Output:**

```markdown
## Changes Made

**File:** .claude/design/effect-type-registry/observability.md

**Frontmatter Changes:**
- completeness: 65% → 80%
- updated: 2026-01-17

## Validation

⚠️ Status/completeness mismatch
- Status: draft (suggests 21-60%)
- Completeness: 80% (suggests current)

## Recommendations

Update status to 'current' to match 80% completeness:
/design-update effect-type-registry observability.md --status=current

Or mark as ready for review:
/design-update effect-type-registry observability.md --status=needs-review
```

## Example 3: Mark as Synced

**User request:**

> Mark cache-optimization.md as synced with codebase

**Execution:**

1. Module: `effect-type-registry`
2. Doc: `cache-optimization.md`
3. Update: `last-synced: never` → `last-synced: 2026-01-17`
4. Also update: `updated: 2026-01-17`

**Changes Made:**

```yaml
last-synced: 2026-01-17  # was: never
updated: 2026-01-17
```

**Output:**

```markdown
## Changes Made

**File:** .claude/design/effect-type-registry/cache-optimization.md

**Frontmatter Changes:**
- last-synced: never → 2026-01-17
- updated: 2026-01-17

## Validation

✅ Document marked as synced with current codebase

## Next Steps

1. Consider syncing again when making code changes
2. Typical sync frequency: 30-90 days for active modules
3. Next sync recommended: 2026-04-17 (90 days)
```

## Example 4: Update Section Content

**User request:**

> Update the Overview section in type-loading-vfs.md for
> rspress-plugin-api-extractor

**Execution:**

1. Module: `rspress-plugin-api-extractor`
2. Doc: `type-loading-vfs.md`
3. Section: `Overview`
4. Read current Overview content
5. User provides new content
6. Replace section

**Changes Made:**

- Updated section: Overview
- Lines changed: ~15
- `updated: 2026-01-17`

**Output:**

```markdown
## Changes Made

**File:** .claude/design/rspress-plugin-api-extractor/type-loading-vfs.md

**Content Changes:**
- Updated section: Overview
- Lines changed: ~15

**Frontmatter Changes:**
- updated: 2026-01-17

## Validation

✅ Valid markdown syntax
✅ Section exists and updated
✅ Heading levels consistent

## Recommendations

Consider updating completeness based on content changes:
- Current: 75%
- Estimated after update: 80%
- Suggestion: Increase to 80%
```

## Example 5: Bulk Update (Status + Completeness + Sync)

**User request:**

> Update observability.md to status current, completeness 90, and mark as synced

**Execution:**

1. Module: `effect-type-registry`
2. Doc: `observability.md`
3. Multiple changes:
   - `status: draft` → `status: current`
   - `completeness: 65` → `completeness: 90`
   - `last-synced: never` → `last-synced: 2026-01-17`
   - `updated: 2026-01-17`

**Validation:**

- Status "current" with completeness 90% ✅ Match
- All fields valid

**Changes Made:**

```yaml
status: current  # was: draft
completeness: 90  # was: 65
last-synced: 2026-01-17  # was: never
updated: 2026-01-17
```

**Output:**

```markdown
## Changes Made

**File:** .claude/design/effect-type-registry/observability.md

**Frontmatter Changes:**
- status: draft → current
- completeness: 65% → 90%
- last-synced: never → 2026-01-17
- updated: 2026-01-17

## Validation

✅ Status matches completeness
✅ Document synced with codebase
✅ All validations passed

## Next Steps

1. Document is now in 'current' status at 90% complete
2. Run `/design-validate effect-type-registry` to confirm
3. Consider adding to CLAUDE.md if frequently referenced
```

## Example 6: Add Related Documentation

**User request:**

> Add cross-reference to performance.md in observability.md

**Execution:**

1. Module: `effect-type-registry`
2. Doc: `observability.md`
3. Read current `related` array: `[]`
4. Add: `effect-type-registry/performance.md`
5. Validate path exists ✅

**Changes Made:**

```yaml
related:
  - effect-type-registry/performance.md
updated: 2026-01-17
```

**Output:**

```markdown
## Changes Made

**File:** .claude/design/effect-type-registry/observability.md

**Frontmatter Changes:**
- related: [] → [effect-type-registry/performance.md]
- updated: 2026-01-17

## Validation

✅ Referenced file exists
✅ No duplicate entries

## Recommendations

Consider adding reciprocal reference:
- In performance.md, add reference back to observability.md
- Creates bidirectional navigation

Command:
/design-update effect-type-registry performance.md --add-related=observability.md
```

## Example 7: Smart Completeness Suggestion

**User request:**

> I just added Implementation Details section to cache-optimization.md

**Execution:**

1. Module: `effect-type-registry`
2. Doc: `cache-optimization.md`
3. Read current completeness: `45%`
4. Run smart estimation:
   - All major sections now filled
   - Code examples present
   - Few placeholders remaining
   - **Estimated:** 70%

**Output:**

```markdown
## Content Change Detected

You've updated cache-optimization.md by adding Implementation Details section.

## Completeness Analysis

**Current Declared:** 45%
**Estimated Based on Content:** 70%
**Difference:** +25%

### Analysis

**Completed Sections:**
- ✅ Overview (comprehensive)
- ✅ Current State (detailed)
- ✅ Rationale (complete)
- ✅ Implementation Details (just added)
- ⚠️ Future Enhancements (brief)

**Content Quality:**
- Code examples: 3 found
- Technical detail: Good
- Placeholders: 2 remaining

## Recommendation

Update completeness to 70% and status to 'current':

/design-update effect-type-registry cache-optimization.md \
  --completeness=70 \
  --status=current

Or use estimated value automatically:
/design-update effect-type-registry cache-optimization.md --auto-estimate
```

## Example 8: Archive Document

**User request:**

> Archive old-architecture.md as it's been superseded by new-architecture.md

**Execution:**

1. Module: `rspress-plugin-api-extractor`
2. Doc: `old-architecture.md`
3. Update status to `archived`
4. Add archival footer section

**Changes Made:**

```yaml
status: archived  # was: current
updated: 2026-01-17
```

**Content Changes:**

- Added footer section with archival note

**Footer Added:**

```markdown
---

## Document Status

**⚠️ This document is archived.**

**Reason:** Superseded by new architecture design

**Replacement:** See `new-architecture.md` for current architecture

**Archived:** 2026-01-17
```

**Output:**

```markdown
## Changes Made

**File:** .claude/design/rspress-plugin-api-extractor/old-architecture.md

**Frontmatter Changes:**
- status: current → archived
- updated: 2026-01-17

**Content Changes:**
- Added archival footer with reason and replacement link

## Validation

✅ Status set to archived
✅ Archival footer added
✅ Replacement document link provided

## Next Steps

1. Consider removing from CLAUDE.md active references
2. Update any links to point to new-architecture.md instead
3. Run `/design-validate rspress-plugin-api-extractor` to check
```

## Example 9: Fix Status/Completeness Mismatch

**User request:**

> Fix the status/completeness mismatch in type-loading-vfs.md

**Execution:**

1. Module: `rspress-plugin-api-extractor`
2. Doc: `type-loading-vfs.md`
3. Current state:
   - Status: `stub`
   - Completeness: `75%`
4. Mismatch detected (stub should be 0-20%)
5. Run smart estimation: Confirms 75% is accurate
6. Suggest status update

**Recommendation:**

```markdown
## Mismatch Detected

**File:** type-loading-vfs.md
**Current Status:** stub (expects 0-20%)
**Current Completeness:** 75%

## Analysis

Content analysis confirms 75% is accurate:
- All major sections complete
- Good technical detail
- Code examples present
- Few placeholders

## Recommended Fix

Update status to match completeness:

/design-update rspress-plugin-api-extractor type-loading-vfs.md \
  --status=current

This will:
- Change status: stub → current
- Keep completeness: 75%
- Update: updated date
```

**After Applying:**

```markdown
## Changes Made

**File:** .claude/design/rspress-plugin-api-extractor/type-loading-vfs.md

**Frontmatter Changes:**
- status: stub → current
- updated: 2026-01-17

## Validation

✅ Status now matches completeness (75%)
✅ Mismatch resolved

## Next Steps

1. Document is now correctly marked as 'current'
2. Consider increasing to 80%+ for near-complete status
3. Fill remaining placeholders to reach 100%
```
