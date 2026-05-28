# Design Compare Detailed Instructions

Complete step-by-step workflow for comparing design document versions across
git history.

## Detailed Workflow

### 1. Parse Parameters

Extract document and comparison reference from user request.

**Parameter parsing examples:**

- `/design-compare observability.md --ref=main` → compare current with main
  branch
- `/design-compare doc.md --ref=abc123` → compare with specific commit
- `/design-compare doc.md --ref=v1.0.0` → compare with tag
- `/design-compare doc.md --from=abc123 --to=def456` → compare two commits

### 2. Validate References

Ensure git references exist and are accessible.

```bash
# Check if commit exists
git rev-parse --verify ${ref}

# Check if branch exists
git show-ref --verify refs/heads/${ref}

# Check if tag exists
git show-ref --verify refs/tags/${ref}
```

### 3. Load Document Versions

Retrieve document content from each version.

**Current version:**

```bash
cat .claude/design/${module}/${doc}
```

**Historical version:**

```bash
git show ${ref}:.claude/design/${module}/${doc}
```

**Error handling:**

If document doesn't exist in historical version:

```text
INFO: Document did not exist in {ref}

This is a new document created after {ref}.
```

### 4. Perform Comparison

See [comparison-formats.md](comparison-formats.md) for format details.

**Line-by-line diff:**

```bash
diff -u \
  <(git show ${ref}:.claude/design/${module}/${doc}) \
  .claude/design/${module}/${doc}
```

**Unified diff format:**

```diff
--- a/.claude/design/module/doc.md
+++ b/.claude/design/module/doc.md
@@ -10,7 +10,7 @@
 ## Overview

-Old content here
+New content here

 ## Implementation
```

**Side-by-side diff:**

```bash
diff --side-by-side \
  <(git show ${ref}:.claude/design/${module}/${doc}) \
  .claude/design/${module}/${doc}
```

**Semantic diff (frontmatter changes):**

```yaml
Frontmatter Changes:
  status: draft → current
  completeness: 60 → 85
  updated: 2025-12-01 → 2026-01-17
```

### 5. Analyze Changes

Extract meaningful insights from diff.

**Change categories:**

- Frontmatter updates (status, completeness, dates)
- Section additions
- Section removals
- Content modifications
- Structural changes (heading reorganization)

**Change metrics:**

```javascript
const metrics = {
  linesAdded: countAdditions(diff),
  linesRemoved: countRemovals(diff),
  linesModified: countModifications(diff),
  sectionsAdded: countNewSections(diff),
  sectionsRemoved: countRemovedSections(diff),
  percentageChange: calculateChangePercentage(diff)
}
```

### 6. Generate Comparison Report

Create comprehensive comparison report.

**Report structure:**

```markdown
# Comparison Report

**Document:** {module}/{doc}
**From:** {ref-from} ({commit-hash})
**To:** {ref-to} ({commit-hash})
**Date:** {timestamp}

## Summary

- Lines added: {count} (+{percentage}%)
- Lines removed: {count} (-{percentage}%)
- Lines modified: {count}
- Net change: {+/-count} lines
- Percentage change: {percentage}%

## Frontmatter Changes

| Field | Before | After |
|-------|--------|-------|
| status | draft | current |
| completeness | 60% | 85% |
| updated | 2025-12-01 | 2026-01-17 |

## Structural Changes

### Sections Added
- Future Enhancements
- Performance Metrics

### Sections Removed
- Historical Implementation

### Sections Modified
- Overview (15 lines changed)
- Current State (32 lines changed)

## Content Diff

[Full diff output...]

## Analysis

Major changes:
- Promoted from draft to current status
- Increased completeness by 25%
- Added future work section
- Removed historical content
- Updated implementation details
```

### 7. Highlight Significant Changes

Identify and highlight important changes.

**Significant change patterns:**

- Status changes (draft → current, current → archived)
- Large completeness jumps (>20%)
- Major section additions/removals
- Architecture changes
- Breaking changes

**Highlighting:**

```markdown
⚠️  **Significant Change:** Status changed from draft to current

✅ **Improvement:** Completeness increased from 60% to 85%

📝 **New Section:** Added "Future Enhancements" section

🗑️  **Removed:** Deleted "Historical Implementation" section
```

### 8. Format Output

Present comparison in requested format.

**Formats:**

- `unified`: Standard unified diff (default)
- `side-by-side`: Side-by-side comparison
- `semantic`: High-level changes only
- `summary`: Just metrics and highlights

### 9. Provide Navigation

Include git commands for further exploration.

```bash
# View full commit history
git log --oneline .claude/design/${module}/${doc}

# View specific commit
git show ${commit-hash}

# View file at specific point
git show ${ref}:.claude/design/${module}/${doc}

# View all changes between refs
git diff ${ref-from}..${ref-to} .claude/design/${module}/${doc}
```

## Comparison Modes

### Single Reference Comparison

Compare current version with historical reference.

```bash
/design-compare doc.md --ref=main
```

Compares: `HEAD` vs `main`

### Two Reference Comparison

Compare two historical versions.

```bash
/design-compare doc.md --from=v1.0.0 --to=v2.0.0
```

Compares: `v1.0.0` vs `v2.0.0`

### Branch Comparison

Compare across branches.

```bash
/design-compare doc.md --ref=feature-branch
```

Compares: `HEAD` (current branch) vs `feature-branch`

### Tag Comparison

Compare with tagged versions.

```bash
/design-compare doc.md --ref=v1.0.0
```

Compares: `HEAD` vs `v1.0.0` tag

## Advanced Features

### Ignore Whitespace

```bash
diff --ignore-all-space ...
```

### Context Lines

```bash
diff -U 5 ...  # 5 lines of context
```

### Word-Level Diff

```bash
git diff --word-diff ${ref} -- .claude/design/${module}/${doc}
```

### Statistics Only

```bash
git diff --stat ${ref} -- .claude/design/${module}/${doc}
```
