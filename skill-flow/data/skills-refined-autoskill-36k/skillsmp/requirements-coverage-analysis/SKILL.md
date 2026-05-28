---
name: requirements-coverage-analysis
description: Analyze coverage of business requirements across feature plans, wave plans, and implementations to ensure completeness. Creates traceability matrices mapping requirements to features/waves/user stories, identifies uncovered or partially covered requirements, detects orphaned features, and validates acceptance criteria. Use after feature planning, before wave design, during epic reviews, for stakeholder reporting, or when validating requirement coverage.
---

# Requirements Coverage Analysis

Analyzes coverage of business requirements across planning and implementation artifacts to ensure completeness and traceability.

## Quick Start

**Check feature coverage of requirements:**
```
"Analyze requirements coverage for all feature plans against Business-Requirements.md"
```

**Verify feature completeness:**
```
"Check if feature-5.1 fully covers its assigned requirements"
```

**Generate traceability matrix:**
```
"Create traceability matrix from requirements to features to waves"
```

## Core Workflow

### Step 1: Load Requirements

Identify and extract requirements from source documents:

**Business Requirements Document**:
- Location: `Docs/architecture/_main/03-Business-Requirements.md` or `Docs/requirements/business-requirements.md`
- Extract: Requirement IDs, descriptions, priority, acceptance criteria, type (functional/non-functional)

**Epic Requirements** (if applicable):
- Location: `Docs/planning/_main/epic-{n}-{name}.md`
- Extract: Epic-specific requirements, success criteria, constraints

**Feature Specifications** (for detailed requirements):
- Location: `Docs/implementation/_main/feature-{n}.{m}-{name}.md`
- Extract: Detailed requirements, user stories, acceptance criteria

### Step 2: Load Implementation Artifacts

Collect feature plans, wave plans, and implementation summaries:

**Feature Plans**:
- Location: `Docs/implementation/_main/feature-*.md`
- Extract: Scope, requirements addressed, deliverables, user stories

**Wave Plans**:
- Location: `Docs/implementation/iterations/wave-*.md`
- Extract: User stories, deliverables, requirements traced

**Implementation Summaries** (if checking completion):
- Location: `Docs/implementation/iterations/wave-*-summary.md`
- Extract: Completed deliverables, acceptance criteria met

### Step 3: Build Traceability Matrix

Map requirements to implementation artifacts:

**Requirement → Feature Mapping**:
```
REQ-001: User Authentication
├─ Feature 5.1 - Global Services (Primary)
│  ├─ Section: Authentication Service
│  └─ Coverage: Full
└─ Feature 5.3 - Session Management (Secondary)
   ├─ Section: Session Tokens
   └─ Coverage: Partial
```

**Feature → Wave → User Story Mapping**:
```
Feature 5.1 - Global Services
├─ Wave 5.1.1 - Foundation Setup
│  ├─ US-5.1.1.1: Create authentication service class
│  ├─ US-5.1.1.2: Implement JWT token generation
│  └─ Coverage: Addresses REQ-001 (User Authentication)
└─ Wave 5.1.2 - Core Services
   ├─ US-5.1.2.1: Implement login endpoint
   └─ Coverage: Completes REQ-001 (User Authentication)
```

### Step 4: Identify Coverage Gaps

Categorize requirements by coverage status:

#### Fully Covered (✅)
- Requirement addressed by at least one feature
- All acceptance criteria have corresponding deliverables
- Implementation plan complete

#### Partially Covered (⚠️)
- Requirement addressed but missing some aspects
- Some acceptance criteria not covered
- Implementation incomplete

#### Uncovered (❌)
- Requirement exists but no feature addresses it
- No implementation plan
- Gap in planning

#### Orphaned Features (🔵)
- Feature exists but doesn't trace to any requirement
- May indicate over-engineering or missing requirement documentation

### Step 5: Generate Coverage Report

Create report in `Docs/reports/requirements/coverage-{date}.md`:

```markdown
# Requirements Coverage Report

**Date**: YYYY-MM-DD
**Scope**: [Epic/Feature/All]
**Total Requirements**: X
**Coverage**: XX%

## Executive Summary
[1-2 sentence summary of coverage status]

## Coverage Metrics
- Fully Covered: X requirements (XX%)
- Partially Covered: Y requirements (YY%)
- Uncovered: Z requirements (ZZ%)
- Orphaned Features: N features

## Traceability Matrix

| Requirement | Priority | Features | Waves | Status | Notes |
|-------------|----------|----------|-------|--------|-------|
| REQ-001 | Critical | 5.1 | 5.1.1, 5.1.2 | ✅ Full | Complete |
| REQ-002 | High | 5.3 | 5.3.1 | ⚠️ Partial | Missing retry logic |
| REQ-003 | Medium | - | - | ❌ None | Not planned |

## Uncovered Requirements (Must Address)
### REQ-003: Data Export
- **Priority**: Medium
- **Description**: Users must export data in CSV/JSON formats
- **Impact**: Cannot meet contractual obligation
- **Recommendation**: Add to Feature 5.4 or create new feature

## Partially Covered Requirements (Should Complete)
### REQ-002: Error Handling
- **Priority**: High
- **Current Coverage**: Basic error handling in Feature 5.3
- **Gaps**: Missing retry logic, missing error codes
- **Recommendation**: Add to Wave 5.3.2

## Orphaned Features (Review Justification)
### Feature 5.7: Advanced Analytics
- **Status**: Planned but no requirement traces to it
- **Recommendation**: Add requirement or remove feature
```

Use `scripts/calculate_coverage_score.py` to compute metrics.

## Key Concepts

**Requirements Coverage**: Percentage of requirements that have implementation plans

**Traceability Matrix**: Table mapping requirements to features, waves, and user stories

**Orphaned Feature**: Feature without corresponding business requirement

**Acceptance Criteria**: Testable conditions that must be met for requirement to be satisfied

**Coverage Score**: Calculated as:
```
Coverage = (Fully Covered + (Partially Covered × 0.5)) / Total Requirements × 100
```

**Forward Traceability**: Requirement → Feature → Wave → User Story

**Backward Traceability**: User Story → Wave → Feature → Requirement

## Available Resources

### Scripts
- **scripts/calculate_coverage_score.py** — Calculates coverage percentage and generates metrics
  ```bash
  python scripts/calculate_coverage_score.py --total 20 --covered 15 --partial 3
  # Output: Coverage Score: 82.5%
  ```

- **scripts/build_traceability_matrix.py** — Builds requirement-to-implementation traceability matrix
  ```bash
  python scripts/build_traceability_matrix.py \
    --requirements Docs/architecture/_main/03-Business-Requirements.md \
    --features "Docs/implementation/_main/feature-*.md" \
    --output traceability-matrix.json
  ```

- **scripts/extract_requirements.py** — Extracts structured requirements from markdown documents
  ```bash
  python scripts/extract_requirements.py \
    --doc Docs/architecture/_main/03-Business-Requirements.md \
    --format json
  ```

### References
- **references/coverage-checklist.md** — Comprehensive checklist for coverage analysis
- **references/requirement-patterns.md** — Common patterns for requirement specification
- **references/traceability-examples.md** — Example traceability matrices

## Coverage Analysis Phases

### Phase 1: Post-Feature Planning
**When**: After `/design-features` completes
**Focus**: Ensure all requirements have at least one feature
**Output**: Feature coverage report
**Gate**: All critical requirements must be covered

### Phase 2: Pre-Wave Design
**When**: Before `/design-waves` for specific feature
**Focus**: Ensure feature fully addresses its requirements
**Output**: Feature completeness report
**Gate**: All feature requirements traced to waves

### Phase 3: Epic Completion Review
**When**: After all waves in epic completed
**Focus**: Verify epic achieved all business goals
**Output**: Epic achievement report
**Gate**: All critical requirements delivered

### Phase 4: Release Planning
**When**: Before major release
**Focus**: Ensure release meets all planned requirements
**Output**: Release coverage report
**Gate**: Minimum coverage threshold met (e.g., 95% critical, 80% overall)

## Common Coverage Patterns

**Pattern 1: One-to-One Mapping**
```
REQ-001: User Authentication → Feature 5.1: Auth Service
```
Simple, direct mapping. Ideal for well-scoped requirements.

**Pattern 2: One-to-Many Mapping**
```
REQ-002: Data Management
├─ Feature 5.1: Data Storage
├─ Feature 5.2: Data Retrieval
└─ Feature 5.3: Data Export
```
Complex requirement needs multiple features. Common for broad requirements.

**Pattern 3: Many-to-One Mapping**
```
REQ-001: Authentication
REQ-002: Authorization     → Feature 5.1: Security Foundation
REQ-003: Session Management
```
Multiple related requirements addressed by single feature. Efficient for cohesive concerns.

**Pattern 4: Cross-Feature Coverage**
```
REQ-004: Audit Logging
├─ Feature 5.1: Logging Service (Primary - infrastructure)
├─ Feature 5.2: User Actions (Secondary - integration)
└─ Feature 5.3: Data Access (Secondary - integration)
```
Requirement partially addressed by multiple features. Common for cross-cutting concerns.

## Output Format

**Console Output**:
```
Requirements Coverage Analysis
==============================

Scope: All Features
Requirements Source: Docs/architecture/_main/03-Business-Requirements.md
Features Analyzed: 8 features

Coverage Score: 82.5% ✅

Fully Covered:     15 requirements (75%)
  ✅ REQ-001: User Authentication → Feature 5.1
  ✅ REQ-002: Multi-workspace → Feature 5.5
  ✅ REQ-003: Session tracking → Feature 5.3
  ... (12 more)

Partially Covered:  3 requirements (15%)
  ⚠️  REQ-015: Error handling → Feature 5.3 (missing retry logic)
  ⚠️  REQ-018: Logging → Feature 5.1 (missing structured format)
  ⚠️  REQ-020: I18n → Feature 5.6 (only English supported)

Uncovered:          2 requirements (10%)
  ❌ REQ-021: Data export functionality
  ❌ REQ-022: Scheduled reports

Orphaned Features:  1 feature
  🔵 Feature 5.7: Advanced Analytics (no requirement)

Recommendation: REVISE - Address 2 uncovered critical requirements
Report: Docs/reports/requirements/coverage-2025-01-21.md
Traceability Matrix: Docs/reports/requirements/traceability-matrix-2025-01-21.md
```

## Integration with Workflow

**`/design-features` integration**:
```markdown
## Step 6: Verify Requirements Coverage

After all features designed:
- Invoke `requirements-coverage-analysis` skill
- Review coverage report
- Address UNCOVERED critical requirements (create features)
- Document ORPHANED features (add requirements or remove)
- Aim for 100% critical requirement coverage
```

**`/design-waves` integration**:
```markdown
## Step 1.5: Verify Feature Requirement Coverage

Before designing waves for a feature:
- Verify feature fully addresses its requirements
- Check all acceptance criteria have corresponding deliverables
- Ensure no requirement gaps before wave planning
```

**`/implement-waves` integration**:
```markdown
## Step 6: Update Traceability Matrix

After wave completion:
- Update traceability matrix with completed deliverables
- Mark requirements as fully/partially satisfied
- Document any deviations from original requirements
```

**Release Planning**:
```markdown
## Release Requirements Review

Before major release:
- Generate comprehensive coverage report
- Verify all critical requirements delivered
- Document deferred requirements for next release
- Get stakeholder sign-off on coverage
```

## Success Criteria

- ✅ Coverage percentage calculated accurately
- ✅ All requirements categorized (covered/partial/uncovered)
- ✅ Traceability matrix complete and accurate
- ✅ Orphaned features identified
- ✅ Gaps clearly documented with recommendations
- ✅ Report generated in standard format
- ✅ Stakeholder-ready documentation produced

## Tips for High Coverage

1. **Track early** - Start traceability during requirements gathering
2. **Explicit mapping** - Document requirement IDs in feature plans
3. **Acceptance criteria** - Make requirements testable and specific
4. **Regular reviews** - Check coverage after each planning phase
5. **Bidirectional traceability** - Verify both forward and backward links
6. **Justify orphans** - Every feature should trace to a requirement
7. **Document deviations** - Explain why requirements not covered

## Examples

### Example 1: Post-Feature Planning Coverage

**Command**:
```
"Analyze requirements coverage for all features against Business-Requirements.md"
```

**Process**:
1. Read Docs/architecture/_main/03-Business-Requirements.md
2. Extract 20 requirements (REQ-001 through REQ-020)
3. Read all feature-*.md files in Docs/implementation/_main/
4. Build traceability matrix
5. Calculate coverage

**Report Findings**:
- Total Requirements: 20
- Fully Covered: 15 (75%)
- Partially Covered: 3 (15%)
- Uncovered: 2 (10%)
- Coverage Score: 82.5%

**Uncovered**:
- REQ-021: Data export (needs new feature)
- REQ-022: Scheduled reports (needs new feature)

**Recommendation**: Create Feature 5.8 for uncovered requirements

---

### Example 2: Feature Completeness Check

**Command**:
```
"Verify feature-5.1 fully covers its assigned requirements"
```

**Process**:
1. Read feature-5.1-global-services.md
2. Extract requirements mentioned: REQ-001, REQ-003, REQ-005
3. Check if all aspects of each requirement addressed
4. Verify acceptance criteria covered

**Report Findings**:
- REQ-001 (Authentication): ✅ Fully covered in Wave 5.1.1, 5.1.2
- REQ-003 (Service Management): ✅ Fully covered in Wave 5.1.3
- REQ-005 (Error Handling): ⚠️ Partially covered - missing retry logic

**Recommendation**: Add retry logic to Wave 5.1.4 or update requirement to mark retry as optional

---

### Example 3: Epic Achievement Verification

**Command**:
```
"Verify Epic 5 achieved all its business requirements"
```

**Process**:
1. Read epic-5-multi-workspace.md and extract requirements
2. Read all completed wave-5.*.md summaries
3. Check which requirements fully delivered
4. Verify acceptance criteria met

**Report Findings**:
- Total Epic Requirements: 12
- Delivered: 11 (92%)
- Deferred: 1 (8%) - REQ-019 workspace templates

**Acceptance Criteria**:
- ✅ All critical criteria met
- ✅ Performance goals achieved
- ⚠️ One nice-to-have deferred to next epic

**Recommendation**: ACCEPT - Epic successfully completed with 1 minor deferral

---

**Last Updated**: 2025-01-21
