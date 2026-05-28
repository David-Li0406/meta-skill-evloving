# Design Audit Examples

Usage examples for comprehensive design documentation audits.

## Example 1: Full Audit of All Modules

**User request:**

> Audit all design docs

**Execution:**

1. Load all modules from config
2. Discover 12 design docs total
3. Run all validation checks
4. Analyze content quality
5. Check cross-references
6. Verify sync status
7. Calculate health scores
8. Generate comprehensive report

**Output:**

```markdown
# Design Documentation Audit Report

**Generated:** 2026-01-17 15:30:00 UTC
**Scope:** All modules (3 modules, 12 documents)

## Executive Summary

**Overall Health:** 78/100 (Good)

**Key Findings:**
- 3 documents with broken cross-references
- 2 documents never synced with codebase
- 5 documents with completeness accuracy issues
- 1 circular dependency detected

**Recommendations:**
1. Fix broken references in 3 documents [HIGH]
2. Sync 2 current documents with codebase [HIGH]
3. Adjust completeness percentages [MEDIUM]
4. Resolve circular dependency [HIGH]

## Module Health Scores

- effect-type-registry: 82/100 (Good)
- rspress-plugin-api-extractor: 75/100 (Fair)
- design-doc-system: 77/100 (Fair)

[Detailed findings follow...]
```

## Example 2: Module-Specific Audit

**User request:**

> Audit effect-type-registry design docs in strict mode

**Parameters:**

- module: `effect-type-registry`
- strict: `true`

**Output:**

Focused audit report for single module with strict validation.

## Example 3: Quick Audit Without Archived

**User request:**

> Quick audit excluding archived docs

**Parameters:**

- strict: `false`
- include-archived: `false`

**Output:**

Faster audit focusing on active documentation only.

## Example 4: Audit with JSON Output

**User request:**

> Generate audit report in JSON format

**Parameters:**

- output: `audit-report.json`

**Output:**

Machine-readable JSON with all findings and scores.

## Audit Findings Examples

### Critical Issues

```markdown
### CRITICAL: Missing Required Frontmatter Field

**Document:** rspress-plugin-api-extractor/type-loading-vfs.md
**Issue:** Missing 'status' field in frontmatter
**Impact:** Cannot determine document maturity
**Fix:** Add `status: current` to frontmatter
```

### Broken Cross-References

```markdown
### HIGH: Broken Cross-Reference

**Document:** effect-type-registry/observability.md
**Reference:** ./non-existent-doc.md
**Location:** Frontmatter 'related' field
**Fix:** Remove reference or create missing document
```

### Sync Issues

```markdown
### HIGH: Document Never Synced

**Document:** effect-type-registry/observability.md
**Status:** current
**Last Synced:** Never
**Age:** 45 days
**Fix:** Run /design-sync to align with codebase
```

### Content Quality Issues

```markdown
### MEDIUM: Completeness Accuracy

**Document:** rspress-plugin/snapshot-tracking.md
**Declared:** 85% complete
**Actual:** ~60% complete (missing Future Enhancements section)
**Fix:** Either complete missing sections or adjust completeness to 60%
```

## Report Formats

### Markdown (Human-Readable)

Full report with sections, findings, and recommendations.

### JSON (Machine-Readable)

```json
{
  "generated": "2026-01-17T15:30:00Z",
  "scope": {
    "modules": ["all"],
    "documentCount": 12
  },
  "overallHealth": {
    "score": 78,
    "rating": "Good"
  },
  "moduleHealth": {
    "effect-type-registry": {
      "score": 82,
      "documentCount": 4,
      "issues": []
    }
  },
  "issues": {
    "critical": [],
    "high": [],
    "medium": [],
    "low": []
  },
  "recommendations": []
}
```

### HTML (Styled with Charts)

Interactive report with health score visualizations and filterable findings.
