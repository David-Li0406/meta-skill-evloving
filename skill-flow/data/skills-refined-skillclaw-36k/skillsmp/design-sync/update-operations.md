# Update Operations

Guidelines for applying updates during design doc synchronization, including
safe vs unsafe updates and auto-update rules.

## Overview

When syncing design docs with code, updates can be:

1. **Safe** - Factual, low-risk, can be auto-applied
2. **Unsafe** - Require judgment, need manual review

This document defines criteria for each category and provides update
procedures.

## Update Categories

### Safe Updates (Auto-Apply)

Updates that are factual and low-risk, suitable for automatic application.

#### Safe Update 1: Add New Exports

**When:** New exports detected in source code

**Example:**

```text
UPDATE: Add new export to documentation

**Section:** Implementation Details
**Auto-apply:** Safe ✅

**Current text:**
> Main exports: `TypeRegistry`, `PackageFetcher`

**Suggested update:**
> Main exports: `TypeRegistry`, `PackageFetcher`, `CacheStrategy`

**Reason:** `CacheStrategy` is now exported from `src/index.ts:15`
```

**Why safe:** Exports are verifiable facts from source code.

#### Safe Update 2: Update File Paths

**When:** Files renamed or moved

**Example:**

```text
UPDATE: Update file location

**Section:** Current State
**Line:** 67
**Auto-apply:** Safe ✅

**Current text:**
> Event handlers are in `src/observability/events.ts`

**Suggested update:**
> Event handlers are in `src/observability/EventEmitter.ts`

**Reason:** File renamed from `events.ts` to `EventEmitter.ts`
```

**Why safe:** File paths are verifiable, clear rename detected.

#### Safe Update 3: Update Line Counts

**When:** Code size estimates are outdated

**Example:**

```text
UPDATE: Update line count

**Section:** Implementation Details
**Auto-apply:** Safe ✅

**Current text:**
> The observability system is ~500 lines of code

**Suggested update:**
> The observability system is ~687 lines of code

**Reason:** Current file sizes:
- EventEmitter.ts: 234 lines
- Logger.ts: 189 lines
- Metrics.ts: 264 lines
```

**Why safe:** Line counts are objective measurements.

#### Safe Update 4: Mark Completed Phases

**When:** Planned features are now implemented

**Example:**

```text
UPDATE: Mark Phase 2 as complete

**Section:** Future Enhancements
**Auto-apply:** Safe ✅

**Current text:**
> **Phase 2:** Implement structured logging

**Suggested update:**
Move to "Completed" section:
> **Phase 2 (Completed):** Structured logging via Logger.ts

**Reason:** `src/observability/Logger.ts` exists and exports StructuredLogger
```

**Why safe:** File existence proves implementation.

#### Safe Update 5: Add Dependencies

**When:** New dependencies in package.json

**Example:**

```text
UPDATE: Add new dependency

**Section:** Dependencies
**Auto-apply:** Safe ✅

**Current text:**
> Dependencies: none (pure Effect-TS)

**Suggested update:**
> Dependencies:
> - Effect-TS (runtime)
> - pino (logging, optional peer dependency)

**Reason:** `package.json` shows `pino` as peerDependency
```

**Why safe:** package.json is source of truth for dependencies.

### Unsafe Updates (Manual Review)

Updates requiring judgment or affecting critical content.

#### Unsafe Update 1: Remove Content (Deleted Files)

**When:** Referenced files no longer exist

**Example:**

```text
CRITICAL: Referenced file deleted

**Section:** Current State
**Line:** 45
**Manual review required** ⚠️

**Documented:**
> The cache implementation is in `src/cache/DiskCache.ts`

**Reality:**
- File `src/cache/DiskCache.ts` does not exist
- May have been deleted or moved

**Fix options:**
1. Check git history: `git log --all --full-history -- "*/DiskCache.ts"`
2. If moved, update path
3. If deleted, update docs to reflect current caching approach
```

**Why unsafe:** Deletion could mean:

- Feature removed (update required)
- File moved (path update)
- Refactored into other files (architectural change)

#### Unsafe Update 2: Change Metrics/Benchmarks

**When:** Documented metrics can't be verified

**Example:**

```text
WARNING: Metric mismatch

**Section:** Performance
**Manual review required** ⚠️

**Documented:**
> Cache hit rate: 85%

**Reality:**
- No instrumentation found in code
- Metric cannot be verified

**Fix options:**
1. Verify metric source (logs, monitoring)
2. Remove claim if unverifiable
3. Add instrumentation then update
```

**Why unsafe:** Performance claims need verification beyond code analysis.

#### Unsafe Update 3: Update Architecture Descriptions

**When:** Component structure changed

**Example:**

```text
WARNING: Architecture change detected

**Section:** Architecture
**Manual review required** ⚠️

**Documented:**
> Cache uses in-memory LRU with disk fallback

**Reality:**
- DiskCache.ts deleted
- MemoryCache.ts exists
- No disk fallback found

**Fix options:**
1. Verify architecture change was intentional
2. Update design rationale if approach changed
3. Document migration from old to new approach
```

**Why unsafe:** Architecture changes may involve design decisions that need
documentation.

#### Unsafe Update 4: Modify Design Decisions

**When:** Implementation differs from documented design

**Example:**

```text
WARNING: Implementation differs from design

**Section:** Design Rationale
**Manual review required** ⚠️

**Documented:**
> We chose Strategy Pattern for cache eviction

**Reality:**
- No Strategy interface found
- Direct implementation in Cache.ts

**Fix options:**
1. Verify if design decision changed
2. Document why simpler approach was chosen
3. Update design rationale section
```

**Why unsafe:** Design decisions have context that code analysis can't
capture.

## Auto-Update Rules

### Rule 1: File Path Updates

**When to auto-apply:**

- Git history shows clear rename (same content, different path)
- File moved to subdirectory with same name
- Single file reference update

**When to skip:**

- File deleted (not just moved)
- Multiple possible replacements
- Path in architectural description

### Rule 2: Export Updates

**When to auto-apply:**

- New export added to existing list
- Export is a top-level class/function/type
- Export name is self-documenting

**When to skip:**

- Export removed (could be breaking change)
- Export is internal/private looking (_prefix, internal/)
- Requires architectural explanation

### Rule 3: Dependency Updates

**When to auto-apply:**

- New dependency or peerDependency in package.json
- Version update of existing dependency
- Optional peer dependency

**When to skip:**

- Dependency removed (could indicate refactor)
- Major version change (could indicate breaking changes)
- Requires explanation of why added

### Rule 4: Implementation Status

**When to auto-apply:**

- File exists matching planned feature
- Clear 1:1 mapping between plan and implementation
- Feature name matches file name

**When to skip:**

- Partial implementation (file exists but incomplete)
- Different approach than documented
- Requires architectural explanation

### Rule 5: Line Count Updates

**When to auto-apply:**

- Always safe (objective measurement)
- Update estimates like "~500 lines"
- Update component sizes

**When to skip:**

- Never skip (always safe)

## Update Application Process

### Step 1: Categorize Update

For each detected discrepancy:

1. Determine if safe or unsafe
2. If safe, add to auto-apply queue
3. If unsafe, add to manual review list

### Step 2: Apply Safe Updates

For each safe update:

1. Read the document section
2. Use Edit tool to apply change
3. Log the update
4. Increment counter

### Step 3: Report Unsafe Updates

For each unsafe update:

1. Document the issue clearly
2. Provide context (git history, code analysis)
3. Suggest fix options
4. Mark for manual review

### Step 4: Update Frontmatter

After all updates applied:

```yaml
last-synced: {current-date}
updated: {current-date}
```

If significant content added, consider updating `completeness`.

## Sync Modes

### Mode 1: Check-Only

**Behavior:**

- Analyze and report discrepancies
- No updates applied
- Generate full report

**Use case:** CI/CD validation, pre-commit checks

**Command example:**

```text
/design-sync effect-type-registry --check-only
```

### Mode 2: Auto-Safe

**Behavior:**

- Apply safe updates automatically
- Report unsafe updates for manual review
- Update last-synced timestamp

**Use case:** Regular syncs, trusted changes

**Command example:**

```text
/design-sync effect-type-registry --auto-update
```

### Mode 3: Interactive

**Behavior:**

- Prompt for each suggested update
- Allow skip, apply, or apply-all
- User confirms each change

**Use case:** First sync, major changes

**Command example:**

```text
/design-sync effect-type-registry --interactive
```

### Mode 4: Full-Auto (Risky)

**Behavior:**

- Apply all updates including unsafe
- Use with caution
- Good for initial sync of new docs

**Use case:** New docs, experimental

**Command example:**

```text
/design-sync effect-type-registry --full-auto
```

## Update Templates

### Template 1: Safe Update Format

```text
UPDATE: {What changed}

**Section:** {Section name}
**Line:** {Line number if specific}
**Auto-apply:** Safe ✅

**Current text:**
> {Current content}

**Suggested update:**
> {New content}

**Reason:** {Why this update is needed}
```

### Template 2: Unsafe Update Format

```text
WARNING: {Issue description}

**Section:** {Section name}
**Line:** {Line number if specific}
**Manual review required** ⚠️

**Documented:**
> {What docs say}

**Reality:**
- {What code shows}
- {Additional context}

**Fix options:**
1. {Option 1}
2. {Option 2}
3. {Option 3}
```

### Template 3: Critical Issue Format

```text
CRITICAL: {Critical issue}

**Section:** {Section name}
**Line:** {Line number}
**Immediate action required** ❌

**Documented:**
> {What docs say}

**Reality:**
- {Critical problem}
- {Impact}

**Fix:**
1. {Required action}
2. {Verification step}
3. {Update needed}
```

## Special Cases

### Case 1: Newly Implemented Features

**Scenario:** Feature documented in Future Enhancements now exists in code

**Safe approach:**

1. Verify file exists and exports match plan
2. If 1:1 match, auto-move to Current State
3. If different approach, flag for review

**Example:**

```text
UPDATE: Feature implemented

**Auto-apply:** Safe ✅

Move from "Future Enhancements" to "Current State":

**Current location:** Future Enhancements
> **Phase 2:** Implement structured logging

**New location:** Current State
> **Structured Logging:** Implemented in src/observability/Logger.ts
> Provides JSON-structured logs with context and correlation IDs.

**Reason:** Logger.ts exists, exports StructuredLogger
```

### Case 2: Refactored Code (Same Functionality)

**Scenario:** Code reorganized but same functionality

**Safe approach:**

1. Update file paths
2. Note refactoring in changelog
3. Keep design rationale intact

**Example:**

```text
UPDATE: File paths after refactor

**Auto-apply:** Safe ✅

**Current:**
> Implementation in src/cache/DiskCache.ts and src/cache/MemoryCache.ts

**Updated:**
> Implementation in src/cache/Cache.ts (unified implementation)

**Note:** Files consolidated during refactor (commit abc123)
```

### Case 3: Deprecated Features

**Scenario:** Feature documented but removed from code

**Unsafe approach:**

```text
CRITICAL: Feature removed from code

**Manual review required** ⚠️

**Documented:**
> Disk-based caching with TTL support

**Reality:**
- DiskCache.ts deleted (commit abc123)
- No replacement found

**Options:**
1. Archive this design doc if feature fully removed
2. Update to document current approach
3. Add deprecation note if transitional
```

### Case 4: Configuration Changes

**Scenario:** package.json, tsconfig, or build config changed

**Safe approach:**

1. Update dependency lists (safe)
2. Update build commands (safe)
3. Flag architectural config changes (unsafe)

**Example safe:**

```text
UPDATE: Add build dependency

**Auto-apply:** Safe ✅

**Current:**
> Build tools: TypeScript, Rollup

**Updated:**
> Build tools: TypeScript, Rollup, API Extractor

**Reason:** @microsoft/api-extractor added to devDependencies
```

## Verification After Updates

### Verify 1: Markdown Validity

Run markdownlint to ensure document structure intact:

```bash
markdownlint-cli2 .claude/design/{module}/{doc}
```

### Verify 2: Frontmatter Validity

Check YAML frontmatter is valid:

```bash
# Use design-validate to check structure
/design-validate {module} {doc}
```

### Verify 3: Cross-References

Ensure updated paths don't break cross-references:

```bash
# Check if referenced docs exist
grep -o '\./[^)]*\.md' {doc} | while read ref; do
  [ -f "$(dirname {doc})/${ref}" ] || echo "Broken: ${ref}"
done
```

### Verify 4: Content Coherence

Manual checks:

- Updates fit context of section
- Tone and style match rest of doc
- No orphaned references
- Sections flow logically

## Success Criteria

A successful update application:

- ✅ All safe updates applied correctly
- ✅ Unsafe updates clearly documented
- ✅ last-synced timestamp updated
- ✅ Document remains valid markdown
- ✅ Frontmatter structure intact
- ✅ Cross-references unbroken
- ✅ Clear report generated
- ✅ Manual review items actionable
