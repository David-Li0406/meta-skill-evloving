# Spec Delta: [INVARIANT-XX] [Brief Title]

**Date**: YYYY-MM-DD
**Author**: [Name]
**Status**: Draft | Under Review | Approved | Rejected
**Severity**: Critical | High | Medium | Low

---

## Failure Description

### What Happened
<!-- Describe the incident in concrete terms. What broke? When? What was the user-visible impact? -->

### Timeline
| Time | Event |
|------|-------|
| T+0  | Initial symptom observed |
| T+X  | ... |
| T+Y  | Incident resolved |

### Impact
- **Duration**: X hours/days
- **Users Affected**: X
- **Revenue Impact**: $X (if applicable)
- **Data Loss**: Yes/No (describe if yes)
- **Reputation**: Internal only / Customer-visible / Public incident

---

## Root Cause Analysis

### Technical Root Cause
<!-- What was the actual technical failure? Be specific. -->

### Contributing Factors
<!-- What made this worse or allowed it to happen? -->
1.
2.
3.

### Why Existing Invariants Didn't Catch This
<!-- Which invariants should have caught this? Why didn't they? Or why was there no applicable invariant? -->

---

## Proposed Invariant

### Invariant ID
`INVARIANT-XX`

### Rule Statement
<!-- Clear, testable statement of what must always be true -->
```
[COMPONENT] MUST [REQUIREMENT] WHEN [CONDITION]
```

### Rationale
<!-- Why this invariant prevents the failure class, not just this specific incident -->

### Category
<!-- Which invariant category does this belong to? -->
- [ ] Critical Data Protection
- [ ] Observability Requirements
- [ ] Deployment Safety
- [ ] Security Boundaries
- [ ] Performance Guarantees
- [ ] API Contracts
- [ ] Other: ____________

### Enforcement Level
- [ ] **Hard Block**: Deployment fails if violated
- [ ] **Soft Warning**: Warning issued, requires override justification
- [ ] **Audit Only**: Logged for review, no blocking

---

## Validation

### Retrospective Test
<!-- Would this invariant have caught the original incident? Prove it. -->

**Scenario**: [Describe the exact state that existed before the incident]

**Expected Invariant Check Result**: FAIL

**Why It Would Have Blocked**:
<!-- Specific explanation of how the check would have prevented deployment/execution -->

### False Positive Analysis
<!-- Could this invariant block legitimate changes? -->

**Potential False Positives**:
1.
2.

**Mitigation for False Positives**:
<!-- How to handle legitimate exceptions -->

### Implementation Complexity
- [ ] Simple regex/pattern match
- [ ] AST analysis required
- [ ] Runtime check needed
- [ ] Cross-file analysis
- [ ] External system integration

**Estimated Implementation Effort**: X hours/days

---

## Review Checklist

- [ ] Failure is documented with sufficient detail for someone unfamiliar to understand
- [ ] Root cause identifies systemic issue, not just symptoms
- [ ] Proposed invariant is specific and testable
- [ ] Validation proves invariant would have caught this incident
- [ ] False positive analysis is complete
- [ ] At least one other team member has reviewed

---

## Approval

| Role | Name | Date | Decision |
|------|------|------|----------|
| Author | | | Proposed |
| Tech Lead | | | |
| Platform Owner | | | |

---

## Post-Approval

### Implementation PR
<!-- Link to PR that implements this invariant -->

### Verification
<!-- How was it verified that the invariant is now active and working? -->

### Monitoring
<!-- How will we track this invariant's effectiveness? -->
