# Usage Examples

Complete examples of design-review skill usage in different scenarios.

## Example 1: Basic Module Review

**User request:**

> Review the design docs for effect-type-registry

**Execution:**

1. Load config: `.claude/design/design.config.json`
2. Find module: `effect-type-registry`
3. Locate design docs: `.claude/design/effect-type-registry/`
4. Find files: 2 docs (cache-optimization.md, observability.md)
5. Analyze each document
6. Calculate health scores
7. Generate report

**Report Summary:**

```markdown
# Design Documentation Health Report

**Target:** effect-type-registry
**Files Analyzed:** 2
**Overall Health:** 🟢 85/100

## Executive Summary

**Health Score:** 85/100
**Status:** Healthy

**Quick Stats:**
- Total docs: 2
- Docs needing attention: 1
- Critical issues: 0
- Recommended actions: 3

**Component Scores:**
- Completeness: 45/100 (1 stub, 1 current)
- Recency: 100/100 (both recently updated)
- Quality: 90/100 (observability.md is excellent)
- References: 100/100 (no broken refs)

## Issues by Priority

### 🟡 Warning (Action Recommended)

1. **cache-optimization.md**: Stub document, no content beyond template
   - **Impact:** Placeholder doc provides no value
   - **Recommendation:** Complete or archive within 30 days
   - **Effort:** MEDIUM (4-6 hours to complete)
```

## Example 2: Review All Modules

**User request:**

> Review all design documentation

**Execution:**

1. Find all modules with design docs:
   - effect-type-registry (2 docs)
   - rspress-plugin-api-extractor (13 docs)
   - design-doc-system (5 docs)
2. Analyze 20 total documents
3. Calculate per-module and overall health
4. Identify cross-module patterns
5. Generate comprehensive report

**Cross-Module Insights:**

```markdown
## Cross-Module Insights

### Missing Relationships

Suggested cross-references:

- `effect-type-registry/observability.md` ↔
  `rspress-plugin-api-extractor/error-observability.md`
  - **Reason:** Both document event-based observability systems

- `rspress-plugin-api-extractor/type-loading-vfs.md` ↔
  `effect-type-registry/observability.md`
  - **Reason:** Type-loading uses effect-type-registry services

### Common Patterns

- 35% of docs have `last-synced: never`
- 15% of docs missing cross-references
- 0 docs with status/completeness mismatches

### Health Trends

- Average completeness: 68%
- Average age: 45 days
- Most common status: current (65%)
- Abandonment rate: 5% (1 stub >90 days)
```

## Example 3: Verbose Analysis

**User request:**

> Do a detailed review of rspress-plugin-api-extractor docs

**Execution:**

1. Load module docs (13 files)
2. Run comprehensive analysis on each
3. Generate detailed findings per document
4. Include verbose content quality assessments

**Verbose Output Example:**

```markdown
### error-observability.md - observability

**Status:** current | **Completeness:** 85% | **Age:** 2 days

**Health Indicators:**
- ✅ Frontmatter complete and valid
- ✅ Status matches completeness (current at 85%)
- ✅ Recently updated (2 days ago)
- ⚠️ Not synced with codebase (last-synced: 2026-01-17)
- ✅ Cross-references valid

**Content Quality:**
- Overview: 🟢 Excellent (420 words, clear problem statement)
- Current State: 🟢 Excellent (specific implementations, code refs)
- Rationale: 🟢 Excellent (alternatives, trade-offs documented)
- Implementation: 🟢 Excellent (detailed code examples, patterns)
- Future: 🟡 Good (3 phases defined, could add estimates)

**Structure:**
- ✅ All required sections present
- ✅ Table of contents accurate
- ✅ Proper heading hierarchy
- ✅ Code blocks have language specifiers

**Cross-References:**
- Related: 0 docs
- Dependencies: 0 docs
- ⚠️ Consider linking to performance-observability.md (related system)

**Recommendations:**
1. 🟡 Add cross-reference to performance-observability.md
2. 🟢 Add effort estimates to Future Enhancements
3. 🟢 Link from rspress-plugin-api-extractor/CLAUDE.md

**Next Action:** Add cross-references (15 min)
```

## Example 4: Focus on Completeness

**User request:**

> Review design docs focusing on completeness issues

**Execution:**

1. Load all design docs
2. Filter analysis to completeness-related checks:
   - Status/completeness mismatches
   - Placeholder counts
   - Stub abandonment
   - Completeness staleness
3. Generate focused report

**Focused Report:**

```markdown
# Completeness-Focused Review

## Status/Completeness Alignment

### ✅ Aligned (17 docs)
All docs have appropriate status for their completeness level.

### ⚠️ Misaligned (0 docs)
No status/completeness mismatches found.

## Placeholder Analysis

### High Placeholder Count (1 doc)

**cache-optimization.md** - 95% placeholders
- Status: stub (0% complete)
- Created: 2026-01-17 (same as updated)
- **Action:** Complete or archive

### Some Placeholders (0 docs)

### No Placeholders (19 docs)

## Abandonment Risk

### 🔴 Abandoned Stubs (0 docs)
No stubs >90 days without updates.

### 🟡 At Risk (1 doc)

**cache-optimization.md**
- Age: 0 days (just created)
- Status: stub
- **Action:** Track progress over next 30 days

## Completeness Recommendations

1. **Immediate:** Monitor cache-optimization.md for progress
2. **This Month:** None - completeness tracking is healthy
3. **Ongoing:** Continue tracking status/completeness alignment
```

## Example 5: Focus on Quality

**User request:**

> Review quality of current documentation in rspress-plugin-api-extractor

**Execution:**

1. Load module docs
2. Filter to status="current" (11 docs)
3. Analyze content quality:
   - Overview depth
   - Current state detail
   - Rationale completeness
   - Implementation examples
4. Generate quality-focused report

**Quality Report:**

```markdown
# Quality-Focused Review: rspress-plugin-api-extractor

## Current Docs Quality (11 docs)

### Excellent Quality (9 docs)
- error-observability.md (95/100)
- performance-observability.md (95/100)
- build-architecture.md (90/100)
- component-development.md (90/100)
- source-mapping-system.md (85/100)
- type-loading-vfs.md (85/100)
- snapshot-tracking-system.md (85/100)
- import-generation-system.md (85/100)
- cross-linking-architecture.md (85/100)

### Good Quality (2 docs)
- ssg-compatible-components.md (75/100)
- page-generation-system.md (70/100)

### Quality Breakdown

**Strengths:**
- All docs have clear problem statements
- Implementation details with specific code locations
- Most include code examples and patterns
- Trade-offs documented where applicable

**Areas for Improvement:**
- 2 docs could expand Rationale sections
- 3 docs missing "when to reference" guidance
- Future Enhancements could use more detail (phases, estimates)

## Recommendations by Impact

### High Impact, Low Effort
1. Add "when to reference" guidance to 3 docs (30 min total)
2. Expand Future Enhancements with phases (1 hour total)

### Medium Impact, Medium Effort
3. Add more code examples to 2 docs (2 hours total)
4. Expand Rationale sections with alternatives (3 hours total)
```

## Example 6: Focus on References

**User request:**

> Check cross-reference health across all design docs

**Execution:**

1. Load all design docs
2. Map all cross-references:
   - Extract `related` arrays
   - Extract `dependencies` arrays
   - Find internal links
3. Validate all references
4. Check for bidirectionality
5. Suggest missing relationships

**Reference Report:**

```markdown
# Cross-Reference Health Report

## Reference Coverage

**Stats:**
- Total docs: 20
- Docs with related refs: 6 (30%)
- Docs with dependencies: 5 (25%)
- Orphaned docs: 14 (70%)

## Broken References

### 🔴 Critical (0 broken refs)
All references point to existing files.

## One-Way References

### 🟡 Warning (3 one-way refs)

1. **implementation-status.md** → **architecture-proposal.md**
   - Missing reciprocal link
   - **Fix:** Add implementation-status.md to architecture-proposal.md
     related array

2. **build-architecture.md** → **component-development.md**
   - Reciprocal exists ✅

3. **build-architecture.md** → **ssg-compatible-components.md**
   - Missing reciprocal link
   - **Fix:** Add build-architecture.md to
     ssg-compatible-components.md related array

## Missing Relationships (Suggested)

Based on category and content analysis:

1. **effect-type-registry/observability.md** ↔
   **rspress-plugin-api-extractor/error-observability.md**
   - Both: observability category
   - Reason: Related observability patterns

2. **rspress-plugin-api-extractor/type-loading-vfs.md** ↔
   **effect-type-registry/observability.md**
   - Reason: Type-loading uses effect-type-registry

3. **rspress-plugin-api-extractor/performance-observability.md** ↔
   **rspress-plugin-api-extractor/error-observability.md**
   - Both: observability systems in same module
   - Reason: Complementary observability approaches

## Recommendations

1. **Immediate:** Fix 2 one-way references (10 min)
2. **This Week:** Add 3 suggested cross-module relationships (30 min)
3. **This Month:** Review 14 orphaned docs for relationships (2 hours)

**Target:** 60% reference coverage (12/20 docs with refs)
```

## Example 7: Focus on Maintenance

**User request:**

> Check maintenance health - what docs are stale or abandoned?

**Execution:**

1. Load all design docs
2. Check update dates
3. Analyze git activity
4. Identify abandonment patterns
5. Generate maintenance report

**Maintenance Report:**

```markdown
# Maintenance Health Report

## Update Recency

### Recently Updated (<30 days) - 20 docs
All docs updated within last 30 days.

### Moderately Stale (31-90 days) - 0 docs

### Stale (91-180 days) - 0 docs

### Very Stale (181-365 days) - 0 docs

### Ancient (>365 days) - 0 docs

## Abandonment Analysis

### 🟢 Active Development (19 docs)
Regular updates, good progress.

### 🟡 At Risk (1 doc)

**cache-optimization.md**
- Status: stub
- Age: 0 days
- Created = Updated: Yes
- **Action:** Monitor for progress over 30 days
- **Risk:** May become abandoned if no updates

### 🔴 Abandoned (0 docs)

## Sync Status

### Never Synced - 7 docs (35%)

Current/complete docs that have never synced:
1. observability.md (completeness: 90%, age: 2 days)
2. build-architecture.md (completeness: 90%, age: 2 days)
3. component-development.md (completeness: 85%, age: 2 days)
4. error-observability.md (completeness: 85%, age: 2 days)
5. source-mapping-system.md (completeness: 85%, age: 2 days)
6. implementation-status.md (completeness: 90%, age: 2 days)
7. architecture-proposal.md (completeness: 95%, age: 2 days)

**Recommendation:** Run `/design-sync all` to verify accuracy

### Recently Synced - 13 docs (65%)

## Maintenance Recommendations

1. **This Week:** Sync 7 never-synced docs
2. **This Month:** Monitor cache-optimization.md for progress
3. **Ongoing:** Maintain <30 day update cycle for active docs
```

## Example 8: Success Report Format

After analyzing healthy documentation:

```markdown
# Design Documentation Health Report

**Target:** effect-type-registry
**Files Analyzed:** 2
**Generated:** 2026-01-17
**Overall Health:** 🟢 85/100

---

## Executive Summary

**Health Score:** 85/100
**Status:** Healthy ✅

**Quick Stats:**
- Total docs: 2
- Docs needing attention: 1 (stub)
- Critical issues: 0
- Recommended actions: 1

**Component Scores:**
- Completeness: 45/100 ⚠️
- Recency: 100/100 ✅
- Quality: 90/100 ✅
- References: 100/100 ✅

**Key Takeaway:** Documentation is healthy overall. One stub document
needs completion or archival.

---

## Next Steps

### Immediate Actions (This Week)
1. Complete cache-optimization.md stub or archive if not needed

**Estimated Effort:** 4-6 hours
**Expected Impact:** Raise completeness score to 90+

### Short-term Actions (This Month)
No additional actions needed - docs are healthy.

### Long-term Actions (This Quarter)
1. Add cross-references between related systems
2. Establish monthly review cycle

---

**Next Review Recommended:** 2026-02-17 (30 days)
```
