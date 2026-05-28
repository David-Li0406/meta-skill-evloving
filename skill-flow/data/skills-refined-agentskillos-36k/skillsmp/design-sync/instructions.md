# Design Sync Detailed Instructions

Complete step-by-step workflow for synchronizing design documentation with
codebase state.

## Detailed Workflow

### 1. Parse Parameters

Extract module and document from user request.

**Parameter parsing examples:**

- `/design-sync effect-type-registry` → module: `effect-type-registry`,
  doc: `all`
- `/design-sync module observability.md` → module: `module`, doc:
  `observability.md`
- `/design-sync module --auto-update` → enable automatic safe updates

### 2. Load Configuration

Read `.claude/design.config.json` to get:

- Module configuration
- Module path in monorepo
- Design docs path

**Configuration structure:**

```json
{
  "modules": {
    "module-name": {
      "path": ".claude/design/module-name",
      "packagePath": "pkgs/module-name"
    }
  }
}
```

### 3. Read Design Document

Load document content and extract:

**File references:**

```markdown
The main implementation is in `src/index.ts`.
See `src/TypeRegistry.ts` for the core logic.
```

**Documented exports:**

```markdown
Exports:
- TypeRegistry class
- fetchTypes function
```

**Implementation claims:**

```markdown
The cache implementation uses disk-based storage with ~500 lines of code.
```

**Architecture descriptions:**

```markdown
The system consists of three main components:
1. PackageFetcher - Downloads packages
2. TypeRegistry - Manages type definitions
3. CacheManager - Handles caching
```

**Metrics/benchmarks:**

```markdown
Performance: <100ms for cached lookups, <2s for fresh fetches.
```

**Dependencies:**

```markdown
Dependencies: @effect/platform, node:fs, node:path
```

### 4. Analyze Source Code

For each claim, verify against actual code.

See [analysis-strategies.md](analysis-strategies.md) for detailed verification
methods.

**File existence check:**

```bash
test -f "pkgs/module-name/src/index.ts"
```

**Exports verification:**

```bash
grep "export.*TypeRegistry" pkgs/module-name/src/index.ts
```

**Line count verification:**

```bash
wc -l pkgs/module-name/src/CacheManager.ts
# Compare with documented count
```

**Dependencies verification:**

```bash
grep "\"@effect/platform\"" pkgs/module-name/package.json
```

**Architecture structure:**

```bash
# Check files exist for each component
test -f pkgs/module-name/src/PackageFetcher.ts
test -f pkgs/module-name/src/TypeRegistry.ts
test -f pkgs/module-name/src/CacheManager.ts
```

### 5. Generate Sync Report

Create detailed report with findings.

**Report structure:**

```markdown
# Sync Report - {module}

**Document:** {doc-name}
**Date:** {timestamp}
**Mode:** {check-only|auto-update}

## Summary

- Files checked: {count}
- Issues found: {count}
- Updates suggested: {count}
- Updates applied: {count}

## Critical Issues

### Deleted File Reference

**Doc claims:** "Implementation in `src/OldFile.ts`"
**Reality:** File does not exist
**Severity:** High
**Suggestion:** Remove reference or update to new file path

## Warnings

### Outdated Line Count

**Doc claims:** "~500 lines of code"
**Reality:** 650 lines
**Severity:** Medium
**Suggestion:** Update to "~650 lines"

## Safe Updates

✅ Updated last-synced timestamp: 2026-01-17

## Manual Review Required

### Export Signature Changed

**Doc claims:** `fetchTypes(pkg: string): Promise<string>`
**Reality:** `fetchTypes(pkg: string, version?: string): Promise<string>`
**Action:** Review and update documentation
```

### 6. Apply Updates

See [update-operations.md](update-operations.md) for detailed update strategies.

**Safe updates (auto-applied if --auto-update):**

- Update last-synced timestamp
- Fix simple typos in file paths
- Update line counts
- Update dependency versions

**Unsafe updates (require manual review):**

- Function signature changes
- Architecture changes
- Removed features
- New major functionality

**Update algorithm:**

```javascript
for (update of suggestedUpdates) {
  if (update.safe && autoUpdate) {
    applyUpdate(update)
    reportApplied(update)
  } else {
    reportManualReview(update)
  }
}
```

### 7. Update Frontmatter

Update document frontmatter with sync results:

```yaml
---
last-synced: 2026-01-17
sync-status: clean  # or: warnings, issues
sync-issues: 0
---
```

### 8. Report Results

Generate final summary:

```markdown
# Sync Complete - {module}

## Results

✅ {count} documents synced
⚠️  {count} documents with warnings
❌ {count} documents with issues

## Actions Taken

- Updated {count} last-synced timestamps
- Applied {count} safe updates
- Flagged {count} items for manual review

## Next Steps

1. Review flagged items in sync report
2. Update documentation for breaking changes
3. Re-run sync after fixes
```

## Verification Methods

### File Existence

```bash
# Check if file exists
test -f "{path}" && echo "EXISTS" || echo "MISSING"
```

### Export Verification

```bash
# Check for specific export
grep -q "export.*{name}" "{file}" && echo "FOUND" || echo "MISSING"
```

### Line Count

```bash
# Get line count
wc -l "{file}" | awk '{print $1}'
```

### Dependency Check

```bash
# Check package.json for dependency
grep -q "\"${package}\"" package.json && echo "FOUND" || echo "MISSING"
```

### Function Signature

```bash
# Extract function signature
grep -A 3 "function ${name}" "{file}"
# or for exported functions
grep -A 3 "export.*function ${name}" "{file}"
```

### Performance Metrics

For performance claims, suggest running actual benchmarks:

```markdown
⚠️  Performance metric claimed but not recently verified.
Suggestion: Run benchmark suite to confirm <100ms claim.
```

## Edge Cases

### Document References Non-Existent Code

**Scenario:** Design doc describes planned features not yet implemented.

**Solution:**

1. Check doc status field
2. If status is "draft" or "stub", allow future references
3. If status is "current", flag as issue

### Code Exists But Not Documented

**Scenario:** New code files exist but aren't mentioned in design doc.

**Solution:**

1. Report as potential gap in documentation
2. Suggest updating doc to include new files
3. Don't auto-update (requires human judgment)

### Multiple Versions Referenced

**Scenario:** Doc references "v1.0.0" but code is now "v2.0.0".

**Solution:**

1. Check if doc has version scope
2. If versioned doc, it's accurate for that version
3. If unversioned, suggest updating to current version

### Monorepo Package Moves

**Scenario:** Package moved from `packages/` to `pkgs/`.

**Solution:**

1. Check module config for current `packagePath`
2. Update file references to use current path
3. Mark as safe update (path correction)
