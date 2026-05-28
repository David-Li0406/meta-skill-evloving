# Archival Examples

Complete usage examples for design-archive skill in different scenarios.

## Example 1: Superseded by New Doc

**User request:**

> Archive old-cache-design.md, it's been replaced by cache-optimization.md

**Execution:**

1. Validate both docs exist
2. Read old-cache-design.md frontmatter
3. Confirm archival reason: superseded
4. Update old-cache-design.md:
   - status: current → archived
   - Add archival metadata with replacement
   - Add notice pointing to new doc
5. Find references (2 docs + 1 CLAUDE.md)
6. Update references to point to cache-optimization.md
7. Report changes

**Output:**

```markdown
# Design Document Archived

**File:** .claude/design/effect-type-registry/old-cache-design.md
**Module:** effect-type-registry
**Archived:** 2026-01-17

## Archival Details

- **Reason:** superseded
- **Replacement:** cache-optimization.md
- **Moved:** no

## Updates Made

### Example 1: Document Changes

- status: current → archived
- Added archival notice with link to cache-optimization.md
- Added archival metadata to frontmatter:

```yaml
archived:
  date: 2026-01-17
  reason: superseded
  replacement: ./cache-optimization.md
  notes: "Superseded by redesigned cache system with LRU eviction"
```

### Example 1: Cross-Reference Updates

**Updated 3 files:**

1. effect-type-registry/observability.md
   - Frontmatter: replaced reference in `related` array
2. effect-type-registry/performance.md
   - Content link: updated to point to cache-optimization.md
3. CLAUDE.md
   - Removed design doc pointer

## Example 1: Validation

- ✅ cache-optimization.md exists and is current
- ✅ All references updated
- ✅ No broken links

### Example 1: Next Steps

- Review cache-optimization.md to ensure it covers all topics from old doc
- Update any external documentation that links to old-cache-design.md

## Example 2: Deprecated Feature

**User request:**

> Archive legacy-api-design.md for the v1 API that's being deprecated

**Execution:**

1. Read document
2. Prompt for deprecation details
3. User provides timeline
4. Update document with archival info
5. Keep accessible during transition (don't move to _archive)
6. Report changes

**User interaction:**

```text
Archiving legacy-api-design.md with reason: deprecated

Please provide deprecation timeline:

1. Deprecation date (default: today): [Enter for 2026-01-17]
2. End of support date: 2026-06-30
3. Planned removal date: 2026-12-31
4. Migration guide (optional): v2-api-migration.md

Confirm archival? (y/n): y
```

**Output:**

```markdown
# Design Document Archived

**File:** .claude/design/rspress-plugin-api-extractor/legacy-api-design.md
**Module:** rspress-plugin-api-extractor
**Archived:** 2026-01-17

## Archival Details

- **Reason:** deprecated
- **Deprecation Timeline:**
  - Deprecated: 2026-01-17
  - End of Support: 2026-06-30
  - Removal: 2026-12-31
- **Migration:** See v2-api-migration.md
- **Moved:** no (kept accessible during transition)

## Updates Made

### Example 2: Document Changes

- status: current → archived
- Added deprecation notice with timeline:

```markdown
> **⚠️ ARCHIVED DOCUMENTATION - DEPRECATED FEATURE**
>
> This design document was archived on 2026-01-17.
>
> **Reason:** This documents a deprecated feature/system.
>
> **Deprecation Timeline:**
>
> - **Deprecated:** 2026-01-17
> - **End of Support:** 2026-06-30
> - **Planned Removal:** 2026-12-31
>
> **Migration:** See [V2 API Migration](./v2-api-migration.md) for migration
> guide.
```

### Example 2: Cross-Reference Updates

**Updated 2 files:**

1. rspress-plugin-api-extractor/integration.md
   - Added note: "legacy-api-design.md (deprecated, see v2-api-migration.md)"
2. pkgs/rspress-plugin-api-extractor/CLAUDE.md
   - Updated pointer with deprecation note

### Example 2: Next Steps

- Review v2-api-migration.md for migration path
- Update user-facing docs with deprecation notice
- Monitor usage during transition period
- Plan removal after 2026-12-31

## Example 3: Move to Archive Directory

**User request:**

> Archive and move obsolete-patterns.md to archive folder

**Execution:**

1. Validate archival reason: obsolete
2. Update document metadata
3. Create _archive directory
4. Move file to _archive/
5. Update all references to new path
6. Create redirect stub at original location
7. Report changes

**Output:**

```markdown
# Design Document Archived

**File:** .claude/design/design-doc-system/obsolete-patterns.md
**Module:** design-doc-system
**Archived:** 2026-01-17

## Archival Details

- **Reason:** obsolete
- **Notes:** Information no longer accurate after system rewrite
- **Moved:** yes
- **New location:**
  `.claude/design/design-doc-system/_archive/obsolete-patterns.md`

## Updates Made

### Example 3: File System Changes

1. Created directory: `.claude/design/design-doc-system/_archive/`
2. Moved file: `obsolete-patterns.md` → `_archive/obsolete-patterns.md`
3. Created redirect stub at original location

**Redirect stub content:**

```markdown
---
status: archived
redirect: ./_archive/obsolete-patterns.md
---

# Obsolete Patterns

This document has been archived and moved.

See [archived version](./_archive/obsolete-patterns.md).
```

### Example 3: Cross-Reference Updates

**Updated 2 files:**

1. design-doc-system/architecture-proposal.md
   - Updated path: `./obsolete-patterns.md` →
     `./_archive/obsolete-patterns.md`
2. CLAUDE.md
   - Updated path with archive note

## Example 3: Validation

- ✅ File moved successfully
- ✅ Archive directory created
- ✅ Redirect stub created
- ✅ All references updated to new path

### Example 3: Next Steps

- Consider removing redirect stub after 90 days
- Review if archived content has historical value

## Example 4: Completed Project

**User request:**

> Archive feature-proposal.md since the feature is now implemented and
> documented

**Execution:**

1. Verify feature is complete
2. Get link to final implementation docs
3. Update document with completion info
4. Update references
5. Report changes

**User interaction:**

```text
Archiving feature-proposal.md with reason: completed

Where is this feature documented now?
1. User documentation: ../../docs/en/features/new-feature.md
2. API documentation: ../../docs/en/api/new-feature-api.md

Completion date (default: today): 2026-01-10

Confirm archival? (y/n): y
```

**Output:**

```markdown
# Design Document Archived

**File:** .claude/design/rspress-plugin-api-extractor/feature-proposal.md
**Module:** rspress-plugin-api-extractor
**Archived:** 2026-01-17

## Archival Details

- **Reason:** completed
- **Completion Date:** 2026-01-10
- **Outcome:** successfully_implemented
- **Final Docs:**
  - User docs: `../../docs/en/features/new-feature.md`
  - API docs: `../../docs/en/api/new-feature-api.md`

## Updates Made

### Example 4: Document Changes

- status: draft → archived
- Added completion notice:

```markdown
> **⚠️ ARCHIVED DOCUMENTATION - COMPLETED**
>
> This design document was archived on 2026-01-17.
>
> **Reason:** The project documented here is complete.
>
> **Completion:** Feature successfully implemented on 2026-01-10.
>
> **Final documentation:**
>
> - [User Guide](../../docs/en/features/new-feature.md)
> - [API Reference](../../docs/en/api/new-feature-api.md)
```

### Example 4: Cross-Reference Updates

**Updated 1 file:**

1. rspress-plugin-api-extractor/roadmap.md
   - Removed from "planned" section
   - Added to "completed" section with links to final docs

## Example 4: Validation

- ✅ Final documentation exists
- ✅ Feature is in production
- ✅ All references updated

### Example 4: Next Steps

- Keep proposal for historical reference
- Link from final docs back to original proposal (optional)

## Example 5: Multiple References to Update

**User request:**

> Archive old-architecture.md, replaced by architecture.md

**Execution:**

1. Validate both docs exist
2. Search for all references (found 8)
3. Update each reference
4. Report all changes

**Output:**

```markdown
# Design Document Archived

**File:** .claude/design/effect-type-registry/old-architecture.md
**Module:** effect-type-registry
**Archived:** 2026-01-17

## Archival Details

- **Reason:** superseded
- **Replacement:** architecture.md
- **References Found:** 8

## Updates Made

### Example 5: Document Changes

- status: current → archived
- Added archival notice

### Example 5: Cross-Reference Updates

**Updated 8 files:**

#### Frontmatter Updates (5 files)

1. effect-type-registry/observability.md
   - `related` array: replaced reference

2. effect-type-registry/cache-optimization.md
   - `dependencies` array: replaced reference

3. effect-type-registry/type-system.md
   - `related` array: replaced reference

4. rspress-plugin-api-extractor/type-loading-vfs.md
   - `dependencies` array: replaced reference (cross-module)

5. design-doc-system/implementation-status.md
   - `related` array: replaced reference

#### Content Link Updates (2 files)

6. effect-type-registry/performance.md
   - Line 45: Updated link text and path
   - Line 92: Updated link path

7. rspress-plugin-api-extractor/build-architecture.md
   - Line 123: Updated cross-module link

#### CLAUDE.md Updates (1 file)

8. pkgs/effect-type-registry/CLAUDE.md
   - Replaced design doc pointer

## Example 5: Validation

- ✅ All 8 references updated
- ✅ No broken links remaining
- ✅ architecture.md covers all topics

## Summary

Successfully archived old-architecture.md and updated all references to point
to the new architecture.md. All cross-module references preserved.
```

## Example 6: Already Archived

**User request:**

> Archive legacy-design.md

**Execution:**

1. Read document
2. Detect status is already "archived"
3. Report status and skip

**Output:**

```text
INFO: Document is already archived

**Document:** legacy-design.md
**Module:** effect-type-registry
**Status:** archived
**Archived Date:** 2025-12-15
**Reason:** superseded
**Replacement:** current-design.md

No action needed. Document was already archived on 2025-12-15.

To review archival details, see the document's frontmatter.
```

## Example 7: Replacement Not Found Error

**User request:**

> Archive old-doc.md, superseded by new-doc.md

**Execution:**

1. Validate old-doc.md exists ✅
2. Check new-doc.md exists ✗
3. Report error

**Output:**

```text
ERROR: Replacement document not found

**Archived Document:** old-doc.md
**Specified Replacement:** new-doc.md
**Expected Path:** .claude/design/module/new-doc.md

The replacement document does not exist. Please:

1. Create the replacement document first using /design-init
2. Or specify a different replacement
3. Or use a different archival reason if no replacement exists

Available archival reasons:
- superseded (requires replacement)
- deprecated (optional replacement)
- obsolete (no replacement needed)
- completed (final docs elsewhere)
```

## Example 8: User Cancels Archival

**User request:**

> Archive cache-design.md

**Execution:**

1. Prompt for archival reason
2. User selects "superseded"
3. Prompt for replacement
4. No suitable replacement found
5. User cancels

**User interaction:**

```text
Why is cache-design.md being archived?

1. superseded - Replaced by newer documentation
2. deprecated - Feature/system deprecated
3. obsolete - Information no longer accurate
4. completed - Project finished

Select reason (1-4): 1

Archival reason: superseded

Replacement document required. Please specify replacement:

Available candidates:
- cache-optimization.md (draft, 45% complete)
- performance.md (current, 75% complete)

Enter replacement file or 'cancel': cancel

Archival cancelled. No changes made.

Note: cache-optimization.md is still in draft status (45% complete). Consider
completing it before archiving cache-design.md.
```

## Example 9: Batch Archival with Shared Replacement

**User request:**

> Archive old-cache-v1.md and old-cache-v2.md, both replaced by
> cache-optimization.md

**Execution:**

1. Process first doc: old-cache-v1.md
2. Process second doc: old-cache-v2.md
3. Update all references to both docs
4. Report combined changes

**Output:**

```markdown
# Multiple Design Documents Archived

**Module:** effect-type-registry
**Archived:** 2026-01-17
**Count:** 2 documents

## Archived Documents

### 1. old-cache-v1.md

- **Reason:** superseded
- **Replacement:** cache-optimization.md
- **Status:** current → archived

### 2. old-cache-v2.md

- **Reason:** superseded
- **Replacement:** cache-optimization.md
- **Status:** draft → archived

## Shared Replacement

**cache-optimization.md** replaces both archived documents:

- Consolidates v1 and v2 approaches
- Covers all topics from both old docs
- Status: current (90% complete)

## Cross-Reference Updates

**Updated 6 files:**

1. observability.md - replaced old-cache-v1.md reference
2. performance.md - replaced both references
3. architecture.md - replaced old-cache-v2.md reference
4. type-system.md - replaced old-cache-v1.md reference
5. rspress-plugin-api-extractor/build.md - cross-module reference updated
6. CLAUDE.md - updated pointer

## Example 9: Validation

- ✅ Both documents archived
- ✅ All references point to cache-optimization.md
- ✅ Replacement covers consolidated content

### Example 9: Next Steps

- Review cache-optimization.md for completeness
- Verify all v1 and v2 topics are covered
```

## Example 10: Archive with Custom Notes

**User request:**

> Archive experimental-feature.md with note that experiment failed

**Execution:**

1. Archive with reason: completed (outcome: cancelled)
2. Add custom notes
3. Report

**User interaction:**

```text
Archiving experimental-feature.md with reason: completed

Project outcome:
1. successfully_implemented
2. cancelled
3. superseded

Select outcome (1-3): 2

Add notes about cancellation: Experiment showed performance degradation.
Reverted to original approach.

Confirm archival? (y/n): y
```

**Output:**

```markdown
# Design Document Archived

**File:** .claude/design/effect-type-registry/experimental-feature.md
**Module:** effect-type-registry
**Archived:** 2026-01-17

## Archival Details

- **Reason:** completed
- **Outcome:** cancelled
- **Notes:** Experiment showed performance degradation. Reverted to original
  approach.

## Updates Made

- status: draft → archived
- Added archival notice with cancellation reason
- Preserved experiment documentation for historical reference

## Cross-Reference Updates

No references to update (experimental doc was not referenced).

### Example 10: Next Steps

- Keep for historical reference
- Document lessons learned in architecture.md
- Note why approach was rejected
```
