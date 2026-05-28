# Scoring and Report Formats

Health score calculation formulas, rubrics, and report templates for design
documentation review.

## Health Score Formula

Overall Health = (Completeness + Recency + Quality + References) / 4

Each component scored 0-100, overall is average of four components.

## Component Scoring

### Completeness Score (0-100)

Measures how complete documentation is relative to expectations.

**Calculation:**

```text
Base Score = Average completeness across all docs (weighted by importance)

Adjustments:
- Status/completeness mismatch: -10 per doc
- Abandoned stubs (>90 days): -15 per doc
- Stalled drafts (>180 days): -10 per doc
- High placeholder count: -5 per doc

Final Score = max(0, Base Score + Adjustments)
```

**Weighting by Importance:**

- Architecture docs: 2x weight
- Current status docs: 1.5x weight
- Draft/stub docs: 1x weight
- Archived docs: 0.5x weight

**Rubric:**

- 90-100: Excellent - Nearly all docs well-developed
- 75-89: Good - Most docs complete, some gaps
- 60-74: Fair - Many docs incomplete
- 40-59: Poor - Significant incompleteness
- 0-39: Critical - Mostly stubs or abandoned

### Recency Score (0-100)

Measures how up-to-date documentation is.

**Calculation:**

```text
For each doc:
  Age in days = current_date - updated_date
  Age penalty:
    0-30 days: 0 points
    31-90 days: -5 points
    91-180 days: -15 points
    181-365 days: -30 points
    >365 days: -50 points

  Never synced penalty: -20 points for current/complete docs

  Doc score = 100 + age_penalty + sync_penalty

Average all doc scores = Recency Score
```

**Rubric:**

- 90-100: Excellent - All docs recently updated
- 75-89: Good - Most docs current
- 60-74: Fair - Some stale docs
- 40-59: Poor - Many outdated docs
- 0-39: Critical - Severely outdated

### Quality Score (0-100)

Measures content depth and usefulness.

**Calculation:**

```text
For each doc, assess:
  Overview quality: 0-25 points
    - Clear problem statement: 10
    - When to use guidance: 10
    - Appropriate length: 5

  Current State quality: 0-25 points
    - Specific code locations: 10
    - Metrics/measurements: 10
    - Integration points: 5

  Rationale quality: 0-25 points
    - Alternatives considered: 10
    - Trade-offs documented: 10
    - Decision criteria: 5

  Implementation quality: 0-25 points
    - Code examples: 10
    - Patterns documented: 10
    - Sufficient detail: 5

  Doc score = sum of section scores

Average all doc scores = Quality Score
```

**Rubric:**

- 90-100: Excellent - Thorough, detailed documentation
- 75-89: Good - Adequate detail, some gaps
- 60-74: Fair - Basic info, lacking depth
- 40-59: Poor - Mostly placeholders
- 0-39: Critical - Template boilerplate only

### References Score (0-100)

Measures cross-reference coverage and health.

**Calculation:**

```text
Base metrics:
  - Docs with related refs: X%
  - Docs with dependencies: Y%
  - Bidirectional refs: Z%
  - Broken refs: -10 per broken link

Reference coverage:
  Expected refs = count_obvious_relationships()
  Actual refs = count_valid_references()
  Coverage = (Actual / Expected) * 100

Penalties:
  - Broken references: -10 each
  - One-way refs: -5 each
  - Missing CLAUDE.md integration: -10 each

Score = min(100, Coverage + Penalties)
```

**Rubric:**

- 90-100: Excellent - Comprehensive cross-referencing
- 75-89: Good - Most relationships documented
- 60-74: Fair - Basic references, gaps exist
- 40-59: Poor - Many missing connections
- 0-39: Critical - Isolated docs, no navigation

## Health Levels

Based on overall score:

- **🟢 Healthy (80-100)**
  - Well-maintained documentation
  - Comprehensive coverage
  - Regular updates
  - Strong cross-referencing

- **🟡 Needs Attention (60-79)**
  - Some issues present
  - Improvement recommended
  - Not critical but should address
  - May have stale or incomplete docs

- **🔴 Critical (<60)**
  - Significant issues
  - Immediate action required
  - Blocks effective documentation use
  - Many abandoned or broken docs

## Issue Priority Classification

### 🔴 Critical Issues (Immediate Action)

**Criteria:**

- Blocks documentation usage
- Causes confusion or errors
- Been unresolved >30 days

**Examples:**

- Abandoned stubs (>90 days, no updates)
- Broken references (missing files)
- Status "needs-review" >14 days
- All docs in module have completeness <20%

**Impact:** HIGH - Prevents effective documentation use

**Effort to Fix:** Varies

### 🟡 Warning Issues (Action Recommended)

**Criteria:**

- Reduces documentation quality
- Should be addressed soon
- Not immediately blocking

**Examples:**

- Stale content (>180 days old)
- Status/completeness mismatches
- Missing cross-references
- Brief or generic content
- Never synced with codebase

**Impact:** MEDIUM - Degrades documentation value

**Effort to Fix:** Usually LOW to MEDIUM

### 🟢 Info Issues (Optional Improvements)

**Criteria:**

- Minor quality improvements
- Nice to have, not essential
- Can be addressed over time

**Examples:**

- Empty related docs arrays
- Brief overviews (<150 words)
- Missing optional sections
- TOC formatting issues
- Could expand Future Enhancements

**Impact:** LOW - Minor quality improvements

**Effort to Fix:** LOW

## Report Format Template

```markdown
# Design Documentation Health Report

**Target:** {module|all}
**Files Analyzed:** {count}
**Generated:** {YYYY-MM-DD}
**Overall Health:** 🟢/🟡/🔴 {score}/100

---

## Executive Summary

**Health Score:** {score}/100
**Status:** {Healthy|Needs Attention|Critical}

**Quick Stats:**
- Total docs: {count}
- Docs needing attention: {count}
- Critical issues: {count}
- Recommended actions: {count}

**Component Scores:**
- Completeness: {score}/100
- Recency: {score}/100
- Quality: {score}/100
- References: {score}/100

---

## Health Breakdown

### By Status

| Status | Count | % Stale |
|--------|-------|---------|
| Stub | {X} | {Y}% |
| Draft | {X} | {Y}% |
| Current | {X} | {Y}% |
| Needs Review | {X} | {Y}% |
| Archived | {X} | - |

### By Completeness

| Range | Count | Avg Age |
|-------|-------|---------|
| 0-20% | {X} | {Y} days |
| 21-40% | {X} | {Y} days |
| 41-60% | {X} | {Y} days |
| 61-80% | {X} | {Y} days |
| 81-100% | {X} | {Y} days |

### By Category

| Category | Count | Avg Health |
|----------|-------|------------|
| Architecture | {X} | {score}/100 |
| Performance | {X} | {score}/100 |
| Observability | {X} | {score}/100 |
| Other | {X} | {score}/100 |

---

## Issues by Priority

### 🔴 Critical (Immediate Action Required)

1. **{doc-name}**: {issue-summary}
   - **Impact:** {impact-description}
   - **Recommendation:** {specific-action}
   - **Effort:** {LOW|MEDIUM|HIGH}

2. **{doc-name}**: {issue-summary}
   - **Impact:** {impact-description}
   - **Recommendation:** {specific-action}
   - **Effort:** {LOW|MEDIUM|HIGH}

### 🟡 Warning (Action Recommended)

1. **{doc-name}**: {issue-summary}
   - **Impact:** {impact-description}
   - **Recommendation:** {specific-action}
   - **Effort:** {LOW|MEDIUM|HIGH}

### 🟢 Info (Optional Improvements)

1. **{doc-name}**: {issue-summary}
   - **Impact:** {impact-description}
   - **Recommendation:** {specific-action}
   - **Effort:** {LOW|MEDIUM|HIGH}

---

## Detailed Findings

### {module-name} ({X} docs)

#### {doc-name}.md - {category}

**Status:** {status} | **Completeness:** {X}% | **Age:** {Y} days

**Health Indicators:**
- ✅ Frontmatter complete
- ⚠️ Status/completeness mismatch
- ❌ Missing required section: {section}
- ✅ Cross-references valid
- ⚠️ Not synced (last-synced: never)

**Content Quality:**
- Overview: 🟢/🟡/🔴 {assessment}
- Current State: 🟢/🟡/🔴 {assessment}
- Rationale: 🟢/🟡/🔴 {assessment}
- Implementation: 🟢/🟡/🔴 {assessment}
- Future: 🟢/🟡/🔴 {assessment}

**Recommendations:**
1. {Specific action with priority}
2. {Specific action with priority}

**Next Action:** {Highest priority action}

---

## Cross-Module Insights

### Missing Relationships

Suggested cross-references between docs:

- `{module}/{doc-a}.md` ↔ `{module}/{doc-b}.md`
  - **Reason:** {why these should be linked}

### Common Patterns

Issues affecting multiple docs:

- {X}% of docs have `last-synced: never`
- {X}% of docs missing cross-references
- {X} docs have status/completeness mismatches

### Health Trends

- Average completeness: {X}%
- Average age: {Y} days
- Most common status: {status} ({X}%)
- Abandonment rate: {X}%

---

## Recommendations

### Immediate Actions (This Week)

1. Fix {X} broken cross-references
2. Complete or archive {X} abandoned stubs
3. Update {X} status/completeness mismatches
4. Add missing sections to {X} docs

**Estimated Effort:** {X} hours
**Expected Impact:** Resolve all critical issues

### Short-term Actions (This Month)

1. Sync {X} docs with codebase
2. Fill placeholders in {X} draft docs
3. Add cross-references between related docs
4. Review {X} stale documents

**Estimated Effort:** {X} hours
**Expected Impact:** Improve quality score by {X} points

### Long-term Actions (This Quarter)

1. Establish documentation sync workflow
2. Set up automated staleness monitoring
3. Create missing architecture documentation
4. Improve cross-reference coverage to 80%

**Estimated Effort:** {X} hours
**Expected Impact:** Achieve healthy score (80+)

---

**Next Review Recommended:** {date + 30 days}
```

## Recommendation Framework

### By Impact and Effort

**High Impact, Low Effort (Do First):**

- Fix broken references
- Update status/completeness mismatches
- Add missing required sections
- Update last-synced dates

**High Impact, High Effort (Plan Carefully):**

- Complete abandoned stub documents
- Add comprehensive Rationale sections
- Sync stale docs with codebase
- Split overly broad documents

**Low Impact, Low Effort (Quick Wins):**

- Add cross-references
- Expand brief overviews
- Update examples
- Fill simple placeholders

**Low Impact, High Effort (Defer):**

- Create architecture diagrams
- Comprehensive doc rewrites
- Optional enhancement sections
- Visual documentation

### Action Templates

**For Abandoned Stubs:**

```text
Recommendation: Complete or Archive

Options:
1. Complete the document (if still needed)
   - Allocate {X} hours
   - Use template as guide
   - Target: Move to draft status (>20% complete)

2. Archive the document (if obsolete)
   - Update status to 'archived'
   - Add archival note explaining why
   - Remove from active documentation

Decision Criteria:
- Still needed? → Complete
- Superseded? → Archive with pointer to replacement
- Never started? → Archive
```

**For Stale Documentation:**

```text
Recommendation: Review and Sync

Process:
1. Review current codebase state
2. Identify what changed since last update
3. Update documentation to match
4. Update last-synced date
5. Adjust completeness if needed

Estimated Effort: {X} hours per doc
Priority: HIGH if doc is frequently referenced
```

**For Missing Cross-References:**

```text
Recommendation: Add Bidirectional Links

Steps:
1. Identify related documents
2. Add to 'related' array in frontmatter
3. Add reciprocal reference in target doc
4. Add inline links in relevant sections
5. Validate links work

Estimated Effort: 15 min per relationship
Priority: MEDIUM
```
