# Design Audit Detailed Instructions

Complete step-by-step workflow for comprehensive design documentation audits.

## Detailed Workflow

### 1. Parse Parameters

**Optional:**

- `module`: Limit to specific module (default: all)
- `strict`: Enable strict mode (default: true)
- `include-archived`: Include archived docs (default: false)
- `output`: Output file path for report

### 2. Load Configuration

Read `.claude/design/design.config.json` for:

- Quality standards (min completeness, max staleness, etc.)
- Module structure
- Validation rules

### 3. Discover All Design Documents

Find all design docs across modules:

```bash
for module in ${modules[@]}; do
  glob "*.md" --path=".claude/design/${module}"
done
```

Count by module, category, and status.

### 4. Run Validation Checks

See [checks.md](checks.md) for full check list.

**Categories:**

- Frontmatter validation (required fields, types, dates)
- Structure validation (required sections, heading levels)
- Content quality (completeness, clarity, examples)
- Cross-reference integrity (broken links, circular dependencies)
- Sync status (code alignment, staleness)
- Technical debt (TODOs, incomplete sections)

### 5. Analyze Content Quality

**Metrics:**

- Completeness vs. status alignment
- Section depth and detail
- Code examples present
- Rationale documented
- Future work documented

**Scoring algorithm:**

```javascript
contentScore = (
  completenessAccuracy * 0.3 +
  sectionDepth * 0.25 +
  codeExamples * 0.20 +
  rationalePresent * 0.15 +
  futureWorkPresent * 0.10
) * 100
```

### 6. Check Cross-Reference Integrity

**Checks:**

- All frontmatter references exist
- All content links valid
- No circular dependencies
- Bidirectional references balanced

**Broken reference resolution:**

1. Find reference in frontmatter or content
2. Resolve relative path to absolute
3. Check file exists
4. If not, report broken reference with suggestion

### 7. Verify Sync Status

**For each doc:**

- Check `last-synced` date
- Compare to `updated` date
- Flag if never synced or >60 days stale
- Validate referenced code still exists

### 8. Calculate Health Scores

See [checks.md](checks.md) for scoring formulas.

**Per document:**

```javascript
docHealth = (
  frontmatterScore * 0.25 +
  structureScore * 0.20 +
  contentScore * 0.30 +
  referencesScore * 0.15 +
  syncScore * 0.10
) * 100
```

**Module aggregate:**

Average of all docs in module.

**Overall:**

Weighted average across all modules.

### 9. Identify Issues

**Issue severity:**

- Critical: Missing required fields, broken structure
- High: Stale current docs, significant quality gaps
- Medium: Incomplete content, sync lag
- Low: Minor quality improvements, optimization opportunities

### 10. Generate Audit Report

**Report sections:**

1. Executive Summary (overall health, key findings)
2. Module Health Scores (per-module breakdown)
3. Validation Results (pass/fail counts)
4. Content Quality Analysis (completeness, depth)
5. Cross-Reference Integrity (broken links, cycles)
6. Sync Status (stale docs, never synced)
7. Issues by Severity (critical, high, medium, low)
8. Recommendations (prioritized action items)
9. Trends (if historical data available)

**Output formats:**

- Markdown (human-readable)
- JSON (machine-readable)
- HTML (styled with charts)

### 11. Provide Recommendations

Prioritize by:

1. Fix critical issues (broken structure, missing fields)
2. Resolve high-priority items (stale docs, quality gaps)
3. Address medium items (sync lag, content depth)
4. Optimize low-priority items (minor improvements)

**Recommendation format:**

```markdown
### Fix {issue-type} in {doc}

**Severity:** {Critical|High|Medium|Low}
**Impact:** {description}
**Fix:** {specific action}
**Effort:** {Low|Medium|High}
```

## Advanced Features

### Historical Trend Analysis

Compare current audit with previous audits to identify:

- Health score trends
- Issue count changes
- Module improvements/regressions
- Quality velocity

### Automated Fixes

For low-risk issues:

- Auto-update date formats
- Auto-fix heading levels
- Auto-sync completeness percentages
- Auto-resolve simple broken links

### Custom Check Plugins

Extend audit with custom checks:

```javascript
function customCheck(doc) {
  // Custom validation logic
  return {
    passed: boolean,
    severity: 'critical'|'high'|'medium'|'low',
    message: string
  }
}
```
