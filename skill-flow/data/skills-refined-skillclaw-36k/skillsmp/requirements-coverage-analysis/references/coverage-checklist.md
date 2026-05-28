# Requirements Coverage Analysis Checklist

Comprehensive checklist for analyzing requirements coverage across planning and implementation artifacts.

---

## Pre-Analysis Setup

- [ ] **Identify requirements source**: Business-Requirements.md or epic requirements
- [ ] **Collect feature plans**: All feature-*.md files for scope
- [ ] **Collect wave plans** (if applicable): wave-*.md files
- [ ] **Identify phase**: Feature planning, wave design, epic review, or release planning
- [ ] **Define coverage threshold**: What percentage is acceptable for this phase?

---

## Requirement Extraction

### From Business Requirements Document

- [ ] **Extract requirement IDs**: REQ-001, REQ-002, etc.
- [ ] **Extract descriptions**: What each requirement specifies
- [ ] **Extract priorities**: Critical, High, Medium, Low
- [ ] **Extract types**: Functional, Performance, Security, etc.
- [ ] **Extract acceptance criteria**: Testable conditions for each requirement

**Validation**:
- All requirements have unique IDs
- All requirements have clear descriptions
- Priority assigned to each requirement
- Acceptance criteria are testable

---

### From Epic Plans

- [ ] **Extract epic-level requirements**: Business goals, success criteria
- [ ] **Extract constraints**: Technical or business constraints
- [ ] **Extract dependencies**: Prerequisites for epic
- [ ] **Extract success metrics**: How epic achievement measured

---

### From Feature Plans

- [ ] **Extract requirement references**: Which REQ-IDs mentioned
- [ ] **Extract user stories**: High-level stories in feature
- [ ] **Extract acceptance criteria**: Feature-level criteria
- [ ] **Extract deliverables**: What feature will produce

---

## Traceability Matrix Construction

### Forward Traceability (Requirement → Implementation)

- [ ] **Map requirements to features**: Which feature(s) address each requirement?
- [ ] **Map features to waves**: Which wave(s) implement each feature?
- [ ] **Map waves to user stories**: Which stories deliver wave scope?
- [ ] **Verify completeness**: All requirements have at least one implementation path?

**Matrix Columns**:
| Requirement ID | Description | Priority | Features | Waves | Stories | Status |
|----------------|-------------|----------|----------|-------|---------|--------|

---

### Backward Traceability (Implementation → Requirement)

- [ ] **Map user stories to waves**: Which wave contains each story?
- [ ] **Map waves to features**: Which feature does each wave belong to?
- [ ] **Map features to requirements**: Which requirements drive each feature?
- [ ] **Verify justification**: Every feature traces to a business need?

**Validation**:
- No orphaned features (feature without requirement)
- No orphaned waves (wave not part of a feature)
- No orphaned user stories (story not in a wave)

---

## Coverage Classification

### Fully Covered Requirements (✅)

**Criteria**:
- [ ] Requirement mentioned in at least one feature plan
- [ ] All acceptance criteria have corresponding deliverables
- [ ] Implementation plan complete (waves defined)
- [ ] Coverage level marked "full" in feature

**Example**:
```
REQ-001: User Authentication
├─ Feature 5.1 - Auth Service (Full coverage)
│  ├─ Wave 5.1.1 - JWT implementation
│  ├─ Wave 5.1.2 - Login/logout endpoints
│  └─ Wave 5.1.3 - Session management
└─ All acceptance criteria covered
```

---

### Partially Covered Requirements (⚠️)

**Criteria**:
- [ ] Requirement mentioned but not fully addressed
- [ ] Some acceptance criteria missing implementation
- [ ] Implementation plan incomplete
- [ ] Coverage level marked "partial" or unclear

**Example**:
```
REQ-005: Error Handling
├─ Feature 5.3 - Error Service (Partial coverage)
│  ├─ Wave 5.3.1 - Basic error handling ✅
│  └─ Missing: Retry logic, error codes, monitoring
└─ Only 2 of 5 acceptance criteria covered
```

**Action Required**:
- Document which aspects covered, which missing
- Plan additional waves or features to complete
- Or adjust requirement if partial coverage acceptable

---

### Uncovered Requirements (❌)

**Criteria**:
- [ ] Requirement exists but no feature addresses it
- [ ] No mention in any planning document
- [ ] No implementation plan
- [ ] Gap in coverage

**Example**:
```
REQ-021: Data Export
├─ No feature planned
├─ Not mentioned in any epic
└─ Completely uncovered
```

**Action Required**:
- Create new feature to address requirement
- Or mark requirement as deferred/out-of-scope with justification
- Or remove requirement if no longer needed

---

### Orphaned Features (🔵)

**Criteria**:
- [ ] Feature exists but doesn't trace to any requirement
- [ ] No business justification documented
- [ ] May indicate over-engineering or missing requirement

**Example**:
```
Feature 5.7 - Advanced Analytics
├─ No REQ-ID mentioned
├─ Not driven by business requirements
└─ Orphaned (no traceability)
```

**Action Required**:
- Create requirement to justify feature
- Or remove feature if not needed
- Or link to existing requirement if missed

---

## Coverage Metrics Calculation

### Coverage Percentage

```
Coverage = ((Fully Covered × 1.0) + (Partially Covered × 0.5)) / Total × 100
```

**Example**:
- Total: 20 requirements
- Fully Covered: 15
- Partially Covered: 3
- Uncovered: 2
- Coverage = ((15 × 1.0) + (3 × 0.5)) / 20 × 100 = 82.5%

---

### Coverage by Priority

- [ ] **Critical requirements coverage**: % of critical requirements covered
- [ ] **High priority coverage**: % of high priority requirements covered
- [ ] **Medium priority coverage**: % of medium priority requirements covered
- [ ] **Low priority coverage**: % of low priority requirements covered

**Gate**: 100% of critical requirements must be fully covered

---

### Coverage by Type

- [ ] **Functional requirements coverage**: %
- [ ] **Performance requirements coverage**: %
- [ ] **Security requirements coverage**: %
- [ ] **Usability requirements coverage**: %

**Insight**: Identify which types of requirements are most/least covered

---

## Gap Analysis

### Identify Gaps

- [ ] **Requirements with no features**: List uncovered requirements
- [ ] **Features with no waves**: List incomplete planning
- [ ] **Waves with no user stories**: List incomplete breakdown
- [ ] **Acceptance criteria with no deliverables**: List gaps in coverage

---

### Prioritize Gaps

For each gap:
- [ ] **Assess impact**: What happens if gap not filled?
- [ ] **Assess priority**: Is this requirement critical?
- [ ] **Assess effort**: How much work to fill gap?
- [ ] **Recommend action**: Create feature, defer, or descope

**Priority Matrix**:
| Priority | Impact | Action |
|----------|--------|--------|
| Critical | High | Must address before proceeding |
| High | High | Should address in current scope |
| Medium | Medium | Consider adding if capacity allows |
| Low | Low | Defer to future release |

---

## Phase-Specific Checks

### Phase 1: After Feature Planning

- [ ] All critical requirements have at least one feature
- [ ] All high priority requirements have at least one feature
- [ ] Coverage ≥ 85% overall
- [ ] Coverage = 100% for critical requirements
- [ ] No more than 3 uncovered critical requirements

**Gate**: Block if critical requirements uncovered

---

### Phase 2: Before Wave Design

- [ ] Feature fully addresses its assigned requirements
- [ ] All acceptance criteria have corresponding wave deliverables
- [ ] Feature requirements coverage = 100%
- [ ] No gaps between requirement and wave plans

**Gate**: Block if feature incomplete

---

### Phase 3: Epic Completion Review

- [ ] All epic requirements delivered
- [ ] All critical acceptance criteria met
- [ ] Epic success metrics achieved
- [ ] Coverage ≥ 95% for epic requirements

**Gate**: Document deferred requirements with justification

---

### Phase 4: Release Planning

- [ ] All release-critical requirements delivered
- [ ] Coverage ≥ 98% for critical requirements
- [ ] Coverage ≥ 90% overall
- [ ] All deferred requirements documented

**Gate**: Block release if critical requirements not met

---

## Report Generation

### Coverage Report Structure

```markdown
# Requirements Coverage Report

**Date**: YYYY-MM-DD
**Scope**: [All/Epic X/Feature Y]
**Phase**: [Feature Planning/Wave Design/Epic Review/Release]

## Executive Summary
[1-2 sentences on coverage status]

## Coverage Metrics
- Total Requirements: X
- Fully Covered: Y (YY%)
- Partially Covered: Z (ZZ%)
- Uncovered: W (WW%)
- Coverage Score: XX%

## Traceability Matrix
[Table linking requirements to features/waves]

## Uncovered Requirements
[List with recommendations]

## Partially Covered Requirements
[List with gaps and recommendations]

## Orphaned Features
[List with recommendations]

## Recommendations
[Actions to improve coverage]
```

---

### Traceability Matrix Format

| Req ID | Description | Priority | Type | Features | Waves | Status | Notes |
|--------|-------------|----------|------|----------|-------|--------|-------|
| REQ-001 | Authentication | Critical | Security | 5.1 | 5.1.1, 5.1.2 | ✅ Full | Complete |
| REQ-002 | Multi-workspace | High | Functional | 5.5 | 5.5.1, 5.5.2, 5.5.3 | ✅ Full | Complete |
| REQ-003 | Error handling | High | Functional | 5.3 | 5.3.1 | ⚠️ Partial | Missing retry |
| REQ-004 | Data export | Medium | Functional | - | - | ❌ None | Not planned |

---

## Success Criteria

- [ ] All requirements extracted and structured
- [ ] Traceability matrix complete (forward and backward)
- [ ] Coverage percentage calculated accurately
- [ ] Gaps identified and prioritized
- [ ] Recommendations provided for each gap
- [ ] Report generated in standard format
- [ ] Stakeholder sign-off obtained (if required)

---

## Common Issues and Solutions

### Issue 1: Vague Requirements
**Problem**: Requirements like "The system shall be fast"
**Solution**: Work with stakeholders to add measurable acceptance criteria

### Issue 2: Missing Requirement IDs
**Problem**: Requirements not numbered or tracked
**Solution**: Add REQ-IDs to all requirements, update documents

### Issue 3: Implicit Coverage
**Problem**: Feature addresses requirement but doesn't mention REQ-ID
**Solution**: Update feature plan to explicitly reference REQ-IDs

### Issue 4: Orphaned Features
**Problem**: Feature built without requirement
**Solution**: Retroactively create requirement or remove feature

### Issue 5: Partial Coverage Ambiguity
**Problem**: Unclear if partial coverage acceptable
**Solution**: Document what's covered/missing, get stakeholder decision

---

**Last Updated**: 2025-01-21
