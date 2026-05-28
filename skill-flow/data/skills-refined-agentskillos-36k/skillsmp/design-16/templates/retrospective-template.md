# Retrospective Template

> Post-implementation learning capture with mandatory system analysis.

---

## Meta

```yaml
retrospective_id: RETRO-{{DATE}}-{{PROJECT_NAME}}
project: {{PROJECT_NAME}}
spec_path: {{SPEC_PATH}}
prp_path: {{PRP_PATH}}
completion_date: {{COMPLETION_DATE}}
author: {{AUTHOR}}
```

---

## 1. Project Summary

### What We Built

{{BRIEF_DESCRIPTION}}

### Timeline

| Phase | Planned | Actual | Delta |
|-------|---------|--------|-------|
| {{PHASE_1}} | {{PLANNED_1}} | {{ACTUAL_1}} | {{DELTA_1}} |
| {{PHASE_2}} | {{PLANNED_2}} | {{ACTUAL_2}} | {{DELTA_2}} |
| {{PHASE_3}} | {{PLANNED_3}} | {{ACTUAL_3}} | {{DELTA_3}} |
| **Total** | {{TOTAL_PLANNED}} | {{TOTAL_ACTUAL}} | {{TOTAL_DELTA}} |

### Final Metrics

| Metric | Target | Actual | Met? |
|--------|--------|--------|------|
| {{METRIC_1}} | {{TARGET_1}} | {{ACTUAL_1}} | {{MET_1}} |
| {{METRIC_2}} | {{TARGET_2}} | {{ACTUAL_2}} | {{MET_2}} |
| {{METRIC_3}} | {{TARGET_3}} | {{ACTUAL_3}} | {{MET_3}} |

---

## 2. What Went Well

### Wins

1. {{WIN_1}}
2. {{WIN_2}}
3. {{WIN_3}}

### Patterns to Repeat

| Pattern | Why It Worked | Apply To |
|---------|---------------|----------|
| {{PATTERN_1}} | {{WHY_1}} | {{APPLY_1}} |
| {{PATTERN_2}} | {{WHY_2}} | {{APPLY_2}} |

---

## 3. What Didn't Go Well

### Issues Encountered

| Issue | Impact | Root Cause | Resolution |
|-------|--------|------------|------------|
| {{ISSUE_1}} | {{IMPACT_1}} | {{CAUSE_1}} | {{RESOLUTION_1}} |
| {{ISSUE_2}} | {{IMPACT_2}} | {{CAUSE_2}} | {{RESOLUTION_2}} |
| {{ISSUE_3}} | {{IMPACT_3}} | {{CAUSE_3}} | {{RESOLUTION_3}} |

### Surprises

1. {{SURPRISE_1}}
2. {{SURPRISE_2}}

---

## 4. Validation Gate Analysis

### Gate Results

| Gate | Passed First Try? | Iterations Needed | Blocking Issues |
|------|-------------------|-------------------|-----------------|
| {{GATE_1}} | {{FIRST_1}} | {{ITERATIONS_1}} | {{BLOCKERS_1}} |
| {{GATE_2}} | {{FIRST_2}} | {{ITERATIONS_2}} | {{BLOCKERS_2}} |
| {{GATE_3}} | {{FIRST_3}} | {{ITERATIONS_3}} | {{BLOCKERS_3}} |

### Gate Effectiveness

- **Most Valuable Gate**: {{MOST_VALUABLE_GATE}} - Caught: {{WHAT_IT_CAUGHT}}
- **Least Valuable Gate**: {{LEAST_VALUABLE_GATE}} - Consider: {{IMPROVEMENT}}
- **Missing Gate**: {{MISSING_GATE}} - Would have caught: {{MISSED_ISSUE}}

---

## 5. System Improvements (MANDATORY)

> This section must be completed before the retrospective is considered done.
> These questions drive continuous improvement of the Design Ops system itself.

### 5.1 Process/Template Improvements

**What process, template, or checklist could have prevented the issues encountered?**

{{PROCESS_IMPROVEMENT}}

**Specific template changes to make:**

- [ ] Template: {{TEMPLATE_NAME}} - Change: {{CHANGE_DESCRIPTION}}
- [ ] Template: {{TEMPLATE_NAME_2}} - Change: {{CHANGE_DESCRIPTION_2}}

### 5.2 Missing Invariants

**What invariant was missing that would have caught issues earlier?**

{{MISSING_INVARIANT_DESCRIPTION}}

**Proposed new invariant:**

```
Invariant #{{NUMBER}}: {{INVARIANT_NAME}}

CONDITION: {{WHAT_TO_CHECK}}
VIOLATION: {{WHAT_TRIGGERS_VIOLATION}}
FIX: {{HOW_TO_FIX}}

Applies to: {{DOMAIN_OR_UNIVERSAL}}
```

### 5.3 CONVENTIONS.md Updates

**What should be added to CONVENTIONS.md based on this learning?**

{{CONVENTIONS_UPDATE}}

**Specific additions:**

```markdown
## {{SECTION_NAME}}

{{CONVENTION_TEXT}}
```

### 5.4 Domain Module Updates

**Should this create a new domain module or update an existing one?**

- [ ] No domain changes needed
- [ ] Update existing domain: {{DOMAIN_NAME}}
- [ ] Create new domain module: {{NEW_DOMAIN_NAME}}

**If updating/creating domain, what invariants to add?**

{{DOMAIN_INVARIANT_ADDITIONS}}

### 5.5 Validation Command Improvements

**What validation command should be added to catch this issue in the future?**

```bash
{{NEW_VALIDATION_COMMAND}}
```

**Add to which template/library?**

- [ ] validation-commands-library.md
- [ ] prp-base.md
- [ ] Project-specific validation

---

## 6. Confidence Score Accuracy

### Predicted vs Actual

| Factor | Predicted Score | Actual Difficulty | Accurate? |
|--------|-----------------|-------------------|-----------|
| Requirement Clarity | {{PRED_CLARITY}} | {{ACTUAL_CLARITY}} | {{ACC_CLARITY}} |
| Pattern Availability | {{PRED_PATTERNS}} | {{ACTUAL_PATTERNS}} | {{ACC_PATTERNS}} |
| Test Coverage | {{PRED_TESTS}} | {{ACTUAL_TESTS}} | {{ACC_TESTS}} |
| Edge Cases | {{PRED_EDGES}} | {{ACTUAL_EDGES}} | {{ACC_EDGES}} |
| Tech Familiarity | {{PRED_TECH}} | {{ACTUAL_TECH}} | {{ACC_TECH}} |

**Overall Confidence Score**: Predicted {{PRED_TOTAL}} / Actual {{ACTUAL_TOTAL}}

### Calibration Notes

{{CALIBRATION_NOTES}}

---

## 7. Knowledge Transfer

### Documentation Created

| Document | Location | Purpose |
|----------|----------|---------|
| {{DOC_1}} | {{LOC_1}} | {{PURPOSE_1}} |
| {{DOC_2}} | {{LOC_2}} | {{PURPOSE_2}} |

### Patterns to Codify

| Pattern | Description | Add to examples/? |
|---------|-------------|-------------------|
| {{PATTERN_1}} | {{DESC_1}} | {{ADD_1}} |
| {{PATTERN_2}} | {{DESC_2}} | {{ADD_2}} |

### Training/Handoff Needed

- [ ] {{TRAINING_ITEM_1}}
- [ ] {{TRAINING_ITEM_2}}

---

## 8. Spec-Delta Candidates

> Issues significant enough to warrant a formal spec-delta entry.

### Candidate 1

**Issue**: {{DELTA_ISSUE_1}}
**Category**: {{CATEGORY_1}} (process | invariant | template | tooling)
**Severity**: {{SEVERITY_1}} (critical | high | medium | low)
**Recommendation**: {{RECOMMENDATION_1}}

### Candidate 2

**Issue**: {{DELTA_ISSUE_2}}
**Category**: {{CATEGORY_2}}
**Severity**: {{SEVERITY_2}}
**Recommendation**: {{RECOMMENDATION_2}}

---

## 9. Action Items

| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| {{ACTION_1}} | {{OWNER_1}} | {{DUE_1}} | {{STATUS_1}} |
| {{ACTION_2}} | {{OWNER_2}} | {{DUE_2}} | {{STATUS_2}} |
| {{ACTION_3}} | {{OWNER_3}} | {{DUE_3}} | {{STATUS_3}} |

---

## 10. Final Assessment

### Project Success Rating

- [ ] Exceeded expectations
- [ ] Met expectations
- [ ] Partially met expectations
- [ ] Did not meet expectations

### Would You Do It Again the Same Way?

{{SAME_WAY_ASSESSMENT}}

### Key Takeaway

> {{ONE_SENTENCE_TAKEAWAY}}

---

## Completion Checklist

Before marking this retrospective complete:

- [ ] All sections filled in
- [ ] Section 5 (System Improvements) fully completed with specific recommendations
- [ ] At least one template/process improvement identified
- [ ] Confidence score calibration reviewed
- [ ] Spec-delta candidates evaluated
- [ ] Action items assigned with owners and due dates

---

*Retrospective completed: {{COMPLETION_DATE}}*
*Author: {{AUTHOR}}*
