# Status Report Examples

Complete usage examples for design-report skill in different scenarios.

## Example 1: Full Report for All Modules

**User request:**

> Generate a design doc status report

**Execution:**

1. Load all modules from config (3 modules)
2. Find all design docs (12 found)
3. Parse frontmatter metadata
4. Calculate progress metrics
5. Assess health scores
6. Identify issues
7. Generate markdown report

**Output:**

```markdown
# Design Documentation Status Report

**Generated:** 2026-01-17
**Modules:** 3
**Total Documents:** 12
**Overall Health:** 72/100 ⚠️

---

## Executive Summary

### Progress

- **Total Coverage:** 62% (744 / 1200 points)
- **Average Completeness:** 62%
- **Documents Complete:** 5/12 (42%)

### Health

- **Overall Score:** 72/100
- **Excellent:** 3 docs (25%)
- **Good:** 5 docs (42%)
- **Fair:** 2 docs (17%)
- **Poor:** 2 docs (17%)

### Status Distribution

- Current: 7 (58%)
- Draft: 3 (25%)
- Stub: 2 (17%)
- Needs Review: 0 (0%)
- Archived: 0 (0%)

---

## Module Reports

### effect-type-registry

**Documents:** 4
**Health Score:** 78/100 ✅
**Average Completeness:** 68%

**Status Breakdown:**

- Current: 3 (75%)
- Draft: 1 (25%)

**Documents:**

1. **observability.md** (current, 85%, health: 88)
   - Last updated: 5 days ago
   - Synced: 5 days ago
   - Relationships: 3
   - **Status:** ✅ Excellent

2. **architecture.md** (current, 90%, health: 92)
   - Last updated: 10 days ago
   - Synced: 10 days ago
   - Relationships: 4
   - **Status:** ✅ Excellent

3. **cache-optimization.md** (draft, 45%, health: 58)
   - Last updated: 15 days ago
   - Synced: never
   - Relationships: 2
   - **Status:** ⚠️  Fair
   - **Issues:**
     - Never synced with codebase
     - Below 60% completeness for draft

4. **type-system.md** (stub, 5%, health: 12)
   - Last updated: 7 days ago
   - Synced: never
   - Relationships: 0
   - **Status:** ❌ Poor
   - **Issues:**
     - Orphaned (no relationships)
     - Very low completeness
     - Never synced

**Module Issues:**

- 1 orphaned document
- 2 documents never synced
- 1 document below expected completeness

---

### rspress-plugin-api-extractor

**Documents:** 5
**Health Score:** 82/100 ✅
**Average Completeness:** 74%

**Status Breakdown:**

- Current: 4 (80%)
- Draft: 1 (20%)

**Documents:**

1. **build-architecture.md** (current, 85%, health: 90)
2. **type-loading-vfs.md** (current, 80%, health: 85)
3. **snapshot-tracking-system.md** (current, 75%, health: 80)
4. **performance-observability.md** (current, 75%, health: 78)
5. **error-observability.md** (draft, 55%, health: 62)

**Module Issues:**

- 1 draft document needs completion

---

### design-doc-system

**Documents:** 3
**Health Score:** 58/100 ⚠️
**Average Completeness:** 48%

**Status Breakdown:**

- Current: 2 (67%)
- Draft: 1 (33%)

**Documents:**

1. **architecture-proposal.md** (current, 70%, health: 75)
2. **user-documentation.md** (current, 65%, health: 68)
   - **Issues:**
     - Low completeness for current status
3. **implementation-status.md** (draft, 10%, health: 28)
   - **Issues:**
     - Never synced
     - Very low completeness

**Module Issues:**

- 1 document with low completeness for status
- 1 document never synced

---

## Category Coverage

### Architecture

**Documents:** 5
**Modules:** 3
**Average Completeness:** 76%
**Health Score:** 81/100

**Coverage:**

- effect-type-registry: architecture.md (90%)
- rspress-plugin-api-extractor: build-architecture.md (85%)
- rspress-plugin-api-extractor: type-loading-vfs.md (80%)
- design-doc-system: architecture-proposal.md (70%)
- effect-type-registry: type-system.md (5%) ❌

### Performance

**Documents:** 2
**Modules:** 2
**Average Completeness:** 60%
**Health Score:** 68/100

**Coverage:**

- effect-type-registry: cache-optimization.md (45%)
- rspress-plugin-api-extractor: performance-observability.md (75%)

### Observability

**Documents:** 3
**Modules:** 2
**Average Completeness:** 73%
**Health Score:** 78/100

**Coverage:**

- effect-type-registry: observability.md (85%)
- rspress-plugin-api-extractor: performance-observability.md (75%)
- rspress-plugin-api-extractor: error-observability.md (55%)

### Missing Categories

- **Testing:** No documents (expected in rspress-plugin-api-extractor)
- **Integration:** No documents across all modules

---

## Issues and Recommendations

### Critical Issues (2)

1. **Orphaned Documents**
   - effect-type-registry/type-system.md
   - **Fix:** Add cross-references or archive

2. **Stale Documents**
   - rspress-plugin-api-extractor/legacy-api.md (120 days old)
   - **Fix:** Review for archival

### Warnings (5)

1. **Never Synced (3 docs)**
   - effect-type-registry/cache-optimization.md
   - effect-type-registry/type-system.md
   - design-doc-system/implementation-status.md
   - **Fix:** Run /design-sync to verify accuracy

2. **Low Completeness for Current Status (1 doc)**
   - design-doc-system/user-documentation.md (current, 65%)
   - **Fix:** Complete or change status to draft

3. **Missing Categories (2)**
   - Testing
   - Integration
   - **Fix:** Create docs or remove from config

### Recommendations

**Priority 1 (This Week):**

1. Resolve 2 orphaned documents
2. Sync 3 never-synced documents
3. Review 1 stale document for archival

**Priority 2 (This Month):**

1. Complete 3 draft documents
2. Fill missing category gaps (testing, integration)
3. Update completeness for 1 current doc

**Priority 3 (This Quarter):**

1. Establish regular sync schedule
2. Add more cross-references
3. Improve relationship density

---

## Progress Trends

**Since Last Report:**

- Documents added: +2
- Average completeness: 58% → 62% (+4%)
- Health score: 68/100 → 72/100 (+4)
- Current status docs: 5 → 7 (+2)

**Velocity:**

- Docs completed per month: ~1.5
- Estimated time to 80% coverage: 3 months

---

## Health Score Breakdown

| Range | Rating | Count | Percentage |
| :---- | :----- | :---- | :--------- |
| 90-100 | Excellent | 3 | 25% |
| 70-89 | Good | 5 | 42% |
| 50-69 | Fair | 2 | 17% |
| 0-49 | Poor | 2 | 17% |

**Target Distribution:**

- Excellent: 50% (currently 25%, need +3 docs)
- Good: 40% (currently 42%, on target)
- Fair: 10% (currently 17%, need -1 doc)
- Poor: 0% (currently 17%, need -2 docs)

---

## Next Steps

1. **Immediate Actions:**
   - Archive or complete effect-type-registry/type-system.md
   - Sync 3 documents with codebase
   - Review rspress-plugin-api-extractor/legacy-api.md

2. **This Week:**
   - Complete cache-optimization.md (draft → current)
   - Add testing category docs
   - Update stale documents

3. **This Month:**
   - Improve overall health to 80/100
   - Reach 70% average completeness
   - Eliminate poor-rated documents

---

**Report Generated:** 2026-01-17 10:30:00 UTC
**Next Report:** 2026-02-01 (2 weeks)
```

## Example 2: Progress Focus for Single Module

**User request:**

> Show me progress report for effect-type-registry

**Execution:**

1. Load module: effect-type-registry
2. Find design docs (4 found)
3. Calculate progress metrics only
4. Generate focused report

**Output:**

```markdown
# Design Documentation Progress Report

**Module:** effect-type-registry
**Documents:** 4
**Generated:** 2026-01-17

## Progress Metrics

### Overall

- **Total Coverage:** 68% (272 / 400 points)
- **Average Completeness:** 68%
- **Documents Complete (>90%):** 2/4 (50%)

### By Status

- Current: 3 (75%)
- Draft: 1 (25%)
- Stub: 0 (0%)

### By Completeness Range

| Range | Count | Percentage |
| :---- | :---- | :--------- |
| 90-100% | 2 | 50% |
| 70-89% | 1 | 25% |
| 50-69% | 0 | 0% |
| 30-49% | 1 | 25% |
| 0-29% | 0 | 0% |

### Documents

1. **architecture.md** (current, 90%) ✅
2. **observability.md** (current, 85%) ✅
3. **cache-optimization.md** (draft, 45%) ⚠️
4. **type-system.md** (stub, 5%) ❌

### Next to Complete

**cache-optimization.md** (draft, 45%)

- Current: 45%
- Target: 80% (for current status)
- Remaining: 35 percentage points
- Estimated sections to complete:
  - Implementation Details
  - Benchmarks
  - Future Enhancements

### Velocity

- Docs completed last 30 days: 1
- Average time to complete: ~2 weeks per doc
- Estimated time to 80% coverage: 1 month

### Recommendations

1. Complete cache-optimization.md to reach 70% coverage
2. Review type-system.md (5% completeness, consider archiving)
3. Maintain current docs with regular syncs
```

## Example 3: Health Focus in JSON Format

**User request:**

> Generate health report in JSON format

**Execution:**

1. Load all modules
2. Find all design docs
3. Calculate health scores
4. Generate JSON output with health focus

**Output:**

```json
{
  "metadata": {
    "generated": "2026-01-17T10:30:00Z",
    "generator": "design-report",
    "version": "1.0",
    "modules": 3,
    "total_documents": 12,
    "focus": "health"
  },
  "summary": {
    "health": {
      "overall_score": 72,
      "rating": "good",
      "distribution": {
        "excellent": 3,
        "good": 5,
        "fair": 2,
        "poor": 2
      }
    }
  },
  "modules": [
    {
      "name": "effect-type-registry",
      "health_score": 78,
      "rating": "good",
      "documents": [
        {
          "name": "observability.md",
          "health_score": 88,
          "rating": "excellent",
          "health_components": {
            "completeness": 0.85,
            "status": 1.0,
            "freshness": 1.0,
            "relationships": 1.0
          }
        },
        {
          "name": "architecture.md",
          "health_score": 92,
          "rating": "excellent",
          "health_components": {
            "completeness": 0.90,
            "status": 1.0,
            "freshness": 1.0,
            "relationships": 1.0
          }
        },
        {
          "name": "cache-optimization.md",
          "health_score": 58,
          "rating": "fair",
          "health_components": {
            "completeness": 0.45,
            "status": 0.6,
            "freshness": 1.0,
            "relationships": 0.7
          },
          "issues": [
            {
              "type": "never_synced",
              "severity": "warning"
            }
          ]
        },
        {
          "name": "type-system.md",
          "health_score": 12,
          "rating": "poor",
          "health_components": {
            "completeness": 0.05,
            "status": 0.2,
            "freshness": 1.0,
            "relationships": 0.0
          },
          "issues": [
            {
              "type": "orphaned",
              "severity": "critical"
            },
            {
              "type": "never_synced",
              "severity": "warning"
            }
          ]
        }
      ]
    }
  ],
  "health_breakdown": {
    "excellent": {
      "count": 3,
      "percentage": 25,
      "target": 50,
      "gap": -3
    },
    "good": {
      "count": 5,
      "percentage": 42,
      "target": 40,
      "gap": 0
    },
    "fair": {
      "count": 2,
      "percentage": 17,
      "target": 10,
      "gap": 1
    },
    "poor": {
      "count": 2,
      "percentage": 17,
      "target": 0,
      "gap": 2
    }
  },
  "recommendations": {
    "priority_1": [
      {
        "action": "Improve poor-rated documents",
        "target": ["effect-type-registry/type-system.md"],
        "expected_impact": "health +10"
      }
    ]
  }
}
```

## Example 4: Gaps Focus

**User request:**

> Show me documentation gaps

**Execution:**

1. Load all modules and their category requirements
2. Find all design docs
3. Identify missing categories
4. Identify under-documented areas
5. Generate focused report

**Output:**

```markdown
# Design Documentation Gaps Report

**Generated:** 2026-01-17
**Modules:** 3

## Missing Categories

### Testing

**Expected in:** rspress-plugin-api-extractor
**Current coverage:** 0 documents
**Recommendation:** Create testing strategy doc

**Suggested topics:**

- Unit testing approach
- Integration test patterns
- Test coverage goals
- Mocking strategies

### Integration

**Expected in:** All modules
**Current coverage:** 0 documents
**Recommendation:** Document integration patterns

**Suggested topics:**

- Inter-module dependencies
- API contracts
- Event-driven integration
- Error handling across boundaries

## Under-Documented Categories

### Performance

**Current documents:** 2
**Average completeness:** 60%
**Below target:** Yes (target: 75%)

**Documents:**

- effect-type-registry/cache-optimization.md (45%) ❌
- rspress-plugin-api-extractor/performance-observability.md (75%) ✅

**Recommendation:** Complete cache-optimization.md

## Under-Documented Modules

### design-doc-system

**Documents:** 3
**Average completeness:** 48%
**Health score:** 58/100

**Issues:**

- Below 60% average completeness
- 1 document with <20% completeness
- Missing testing and integration categories

**Recommendations:**

1. Complete implementation-status.md (currently 10%)
2. Improve user-documentation.md to 80%+
3. Add testing and integration docs

## Coverage Matrix

| Module | Architecture | Performance | Observability | Testing |
Integration |
| :-------------------------- | :----------- | :---------- | :------------ |
:------- | :---------- |
| effect-type-registry | 90% ✅ | 45% ⚠️  | 85% ✅ | — | — |
| rspress-plugin-api-extractor | 85% ✅ | 75% ✅ | 75% ✅ | — | — |
| design-doc-system | 70% ✅ | — | — | — | — |

**Legend:**

- ✅ >= 75% completeness
- ⚠️  < 75% completeness
- — No coverage

## Priority Actions

**High Priority:**

1. Create testing category docs for rspress-plugin-api-extractor
2. Complete cache-optimization.md (45% → 80%)
3. Complete implementation-status.md (10% → 70%)

**Medium Priority:**

1. Add integration docs for all modules
2. Improve user-documentation.md (65% → 80%)

**Low Priority:**

1. Review if all expected categories are still needed
2. Consider merging similar docs to improve focus
```

## Example 5: Module Comparison

**User request:**

> Compare documentation quality across modules

**Execution:**

1. Load all modules
2. Calculate metrics per module
3. Generate comparison report

**Output:**

```markdown
# Module Documentation Comparison

**Generated:** 2026-01-17

## Module Rankings

| Rank | Module | Docs | Health | Completeness | Status |
| :--- | :-------------------------- | :--- | :----- |
:------------ | :----- |
| 1 | rspress-plugin-api-extractor | 5 | 82/100 | 74% | ✅ Good |
| 2 | effect-type-registry | 4 | 78/100 | 68% | ✅ Good |
| 3 | design-doc-system | 3 | 58/100 | 48% | ⚠️  Fair |

## Detailed Comparison

### Document Count

- rspress-plugin-api-extractor: 5 (42%)
- effect-type-registry: 4 (33%)
- design-doc-system: 3 (25%)

### Health Scores

- rspress-plugin-api-extractor: 82/100 ✅
- effect-type-registry: 78/100 ✅
- design-doc-system: 58/100 ⚠️

**Analysis:** All modules above 50/100 baseline. design-doc-system needs
improvement.

### Average Completeness

- rspress-plugin-api-extractor: 74% ✅
- effect-type-registry: 68% ✅
- design-doc-system: 48% ❌

**Analysis:** design-doc-system significantly below target (75%).

### Status Distribution

**rspress-plugin-api-extractor:**

- Current: 4 (80%)
- Draft: 1 (20%)
- Stub: 0 (0%)

**effect-type-registry:**

- Current: 3 (75%)
- Draft: 1 (25%)
- Stub: 0 (0%)

**design-doc-system:**

- Current: 2 (67%)
- Draft: 1 (33%)
- Stub: 0 (0%)

**Analysis:** Similar distribution across modules. Good progression from
draft to current.

### Category Coverage

**rspress-plugin-api-extractor:**

- Architecture: 2 docs (85% avg)
- Performance: 1 doc (75%)
- Observability: 2 docs (65% avg)

**effect-type-registry:**

- Architecture: 2 docs (48% avg) ⚠️
- Performance: 1 doc (45%) ⚠️
- Observability: 1 doc (85%)

**design-doc-system:**

- Architecture: 1 doc (70%)

**Analysis:** rspress-plugin-api-extractor has best category coverage.
effect-type-registry needs architecture improvements.

## Recommendations by Module

### rspress-plugin-api-extractor

**Strengths:**

- Highest health score (82/100)
- Best completeness (74%)
- Good category coverage

**Areas for improvement:**

- Add testing category docs
- Complete error-observability.md (draft)

**Priority:** Low (maintain current quality)

### effect-type-registry

**Strengths:**

- Good health score (78/100)
- Excellent observability doc (85%)

**Areas for improvement:**

- Complete cache-optimization.md (45%)
- Resolve type-system.md orphan (5%)
- Improve architecture completeness

**Priority:** Medium (complete drafts, resolve orphan)

### design-doc-system

**Strengths:**

- Core architecture documented (70%)

**Areas for improvement:**

- Increase health from 58 to 70+
- Complete implementation-status.md (10%)
- Improve user-documentation.md (65% → 80%)
- Add missing categories

**Priority:** High (below quality baseline)
```

## Example 6: Including Archived Documents

**User request:**

> Generate report including archived documents

**Execution:**

1. Load all modules
2. Find all design docs including archived
3. Calculate metrics
4. Generate report with archived section

**Output:**

```markdown
# Design Documentation Status Report (Including Archived)

**Generated:** 2026-01-17
**Total Documents:** 14 (12 active, 2 archived)

## Active Documents

[... standard report sections ...]

---

## Archived Documents

### rspress-plugin-api-extractor/legacy-api.md

**Archived:** 2026-01-05 (12 days ago)
**Status:** archived
**Completeness:** 90%
**Archived reason:** Superseded by current-api.md

**Metadata:**

- Created: 2025-10-01
- Last updated: 2025-12-20
- Active period: 3 months

**Replacement:** current-api.md (created 2025-12-15)

**Action:** None required - properly archived

### effect-type-registry/legacy-observability.md

**Archived:** 2025-11-01 (78 days ago)
**Status:** archived
**Completeness:** 75%
**Archived reason:** Merged into observability.md

**Metadata:**

- Created: 2025-08-15
- Last updated: 2025-10-28
- Active period: 2.5 months

**Replacement:** observability.md (updated 2025-11-01)

**Action:** Consider deleting after 90 days

---

## Archive Statistics

- Total archived: 2
- Average time before archival: 2.75 months
- Archival reasons:
  - Superseded: 1
  - Merged: 1

## Archive Health

Both archived documents properly handled:

- Clear archival dates
- Documented replacement/successor
- High completeness before archival (avg 83%)
```

## Example 7: No Documents Found

**User request:**

> Generate report for new-module

**Execution:**

1. Load config
2. Check for new-module design docs
3. No docs found

**Output:**

```text
INFO: No design documents found

**Module:** new-module
**Path:** .claude/design/new-module/

This is normal for new modules.

**Next steps:**

1. Run /design-init new-module {topic} to create your first design doc
2. Document key architectural decisions
3. Run /design-report to track progress

**Suggested first docs:**

- architecture.md - System architecture and component design
- observability.md - Logging, metrics, error tracking
```

## Example 8: Invalid Frontmatter Warning

**User request:**

> Generate status report

**Execution:**

1. Load all modules
2. Find design docs (12 found)
3. Parse frontmatter - 1 invalid
4. Generate report with warning

**Output:**

```markdown
# Design Documentation Status Report

**Generated:** 2026-01-17
**Modules:** 3
**Total Documents:** 11 (1 excluded due to errors)

⚠️  **Warning:** 1 document excluded from report due to invalid frontmatter

---

## Excluded Documents

### effect-type-registry/broken-doc.md

**Issue:** Invalid YAML frontmatter
**Error:** Missing required field: status
**Impact:** Document not included in metrics

**Fix:**

1. Run /design-validate effect-type-registry
2. Add missing frontmatter fields
3. Re-run /design-report

---

[... rest of report for valid documents ...]
```
