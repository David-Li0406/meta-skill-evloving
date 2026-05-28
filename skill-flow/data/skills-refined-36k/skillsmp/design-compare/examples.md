# Design Compare Examples

Usage examples for comparing design document versions.

## Example 1: Compare with Main Branch

**User request:**

> Compare observability.md with main branch

**Execution:**

```bash
/design-compare effect-type-registry observability.md --ref=main
```

**Output:**

```markdown
# Comparison Report

**Document:** effect-type-registry/observability.md
**From:** main (a1b2c3d)
**To:** HEAD (e4f5g6h)

## Summary

- Lines added: 45 (+12%)
- Lines removed: 8 (-2%)
- Net change: +37 lines
- Percentage change: 10%

## Frontmatter Changes

| Field | Before | After |
|-------|--------|-------|
| completeness | 75% | 85% |
| updated | 2026-01-10 | 2026-01-17 |

## Structural Changes

### Sections Added
- Performance Metrics

[... full diff ...]
```

## Example 2: Compare Two Commits

**User request:**

> Compare cache-optimization.md between v1.0 and v2.0

**Execution:**

```bash
/design-compare module cache-optimization.md --from=v1.0.0 --to=v2.0.0
```

**Output:**

Detailed comparison between two specific versions.

## Example 3: Semantic Comparison

**User request:**

> Show high-level changes to architecture.md

**Execution:**

```bash
/design-compare module architecture.md --ref=main --format=semantic
```

**Output:**

```markdown
# Semantic Changes

**Status:** draft → current
**Completeness:** +25% (60% → 85%)

**Sections Added:**
- Future Enhancements
- Migration Path

**Sections Modified:**
- Current State (major changes)

**Key Changes:**
- Documented new caching strategy
- Added performance benchmarks
```

## Example 4: No Changes

**User request:**

> Compare doc.md with previous commit

**Output:**

```text
INFO: No changes detected

Document: module/doc.md
Reference: HEAD~1

The document is identical to the reference version.
```

## Example 5: Document Doesn't Exist in Reference

**User request:**

> Compare new-feature.md with main

**Output:**

```text
INFO: Document did not exist in main branch

Document: module/new-feature.md

This is a new document created after main.
All content is new (125 lines added).
```
