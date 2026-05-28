---
name: dod-validation-cycle
description: HAIOS DoD Validation Cycle for validating Definition of Done before closure.
  Use before DONE phase. Guides CHECK->VALIDATE->APPROVE workflow.
generated: '2025-12-25'
last_updated: '2025-12-28T21:12:55'
---
# DoD Validation Cycle (Bridge Skill)

This is a **Validation Skill** (bridge) that validates Definition of Done criteria before work item closure. It acts as a quality gate at the entry to close-work-cycle.

## When to Use

**Invoked automatically** by close-work-cycle before VALIDATE phase.
**Manual invocation:** `Skill(skill="dod-validation-cycle")` before closing a work item.

---

## The Cycle

```
CHECK --> VALIDATE --> APPROVE
```

### 1. CHECK Phase

**Goal:** Verify DoD prerequisites exist.

**Prerequisites to Check:**
- Work item has associated plan(s)
- Tests were run (test results available)
- Memory refs captured (WHY documented)
- Docs reviewed (CLAUDE.md, READMEs)

**Actions:**
1. Read work file to find associated documents
2. Check plan status(es)
3. Verify memory_refs field is populated
4. Report missing prerequisites

**Exit Criteria:**
- [ ] Associated plans found
- [ ] Test results mentioned or N/A documented
- [ ] memory_refs populated or WHY captured

**Tools:** Read, Glob, Grep

---

### 2. VALIDATE Phase

**Goal:** Validate each DoD criterion per ADR-033.

**DoD Criteria (ADR-033):**
| Criterion | Check |
|-----------|-------|
| Tests pass | User confirms or test output available |
| WHY captured | memory_refs populated in work file |
| Docs current | CLAUDE.md/READMEs updated if behavior changed |
| Traced files complete | All associated plans status: complete |

**Actions:**
1. For each criterion, verify status
2. Flag any failing criteria
3. Report validation status

**Ground Truth Verification (Plan-Specific):**

If associated plans exist (from work item's documents.plans field):

1. **For each plan:**
   - Read plan file from `docs/work/active/{id}/plans/PLAN.md` (or legacy path)
   - Parse Ground Truth Verification table (looking for `## Ground Truth Verification` section)
   - Use `parse_ground_truth_table()` from `.claude/lib/validate.py`

2. **For each verification item:**
   - Classify type based on file_path pattern (via `classify_verification_type()`)
   - Execute machine-checkable items:

     | Type | Tool | Success Criteria |
     |------|------|------------------|
     | file-check | Read(path) | File exists AND expected_state pattern found |
     | grep-check | Grep(pattern) | Match count matches expectation (0 or >0) |
     | test-run | Bash(pytest) | Exit code 0 |
     | json-verify | Read + JSON parse | File exists AND expected fields present |
     | human-judgment | - | Flag for manual confirmation |

   - Flag human-judgment items for manual confirmation

3. **Report results:**
   - "X of Y machine checks passed"
   - "Z items require human confirmation" (list them)

4. **Gate decision:**
   - **BLOCK** if any machine-check FAILS (list specific failures)
   - **WARN** if unchecked items remain (items with `[ ]` checkbox)
   - **PASS** if all machine-checks pass and human-judgment items confirmed

**Exit Criteria:**
- [ ] Tests MUST pass (or N/A with rationale)
- [ ] WHY MUST be captured
- [ ] Docs MUST be current
- [ ] Associated plans MUST be complete
- [ ] Ground Truth Verification: all machine-checks MUST pass (or N/A)
- [ ] Ground Truth Verification: human-judgment items MUST be confirmed

**Tools:** Read, Grep, Bash

---

### 3. APPROVE Phase

**Goal:** Confirm work item is ready for closure.

**Actions:**
1. If all criteria pass -> APPROVED
2. If any fail -> Report blockers
3. Return to calling cycle immediately

**On PASS:** Return to close-work-cycle - it will proceed to VALIDATE phase.
**On FAIL:** Return to implementation for fixes.

**MUST:** Do not pause for acknowledgment - return to calling cycle immediately.

**Exit Criteria:**
- [ ] All DoD criteria validated
- [ ] Approval status reported
- [ ] Returned to calling cycle (no pause)

**Tools:** -

---

## Composition Map

| Phase | Primary Tool | Output |
|-------|--------------|--------|
| CHECK | Read, Glob, Grep | Prerequisites status |
| VALIDATE | Read | DoD compliance report |
| APPROVE | - | Approval/block decision |

---

## Quick Reference

| Phase | Question to Ask | If NO |
|-------|-----------------|-------|
| CHECK | Are plans found? | STOP - no work to validate |
| CHECK | Are memory_refs populated? | Flag: WHY not captured |
| VALIDATE | Do tests pass? | BLOCK - fix tests first |
| VALIDATE | Are plans complete? | BLOCK - complete plans first |
| VALIDATE | Do Ground Truth machine-checks pass? | BLOCK - fix failures first |
| VALIDATE | Are human-judgment items confirmed? | WARN - prompt for confirmation |
| APPROVE | All criteria met? | Report blockers |

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Three phases | CHECK -> VALIDATE -> APPROVE | Consistent with other validation skills |
| Read-only | No modifications | Bridge skills validate, don't modify |
| MUST gate | Required before close | Ensures quality before closure |
| ADR-033 alignment | Use official DoD criteria | Single source of truth |
| Ground Truth integration | VALIDATE phase | INV-042: Ground Truth Verification is DoD criterion |
| Machine-check failure | BLOCK | Objective failures should prevent false completions |
| Unchecked items | WARN | May be intentional (N/A) - surface but don't block |
| Parser reuse | Use validate.py functions | DRY principle, tested in E2-219 |

---

## Related

- **plan-validation-cycle skill:** Pre-DO validation (parallel pattern)
- **design-review-validation skill:** During-DO validation (parallel pattern)
- **close-work-cycle skill:** Invokes this skill as MUST gate
- **ADR-033:** Work Item Lifecycle Governance (DoD definition)
- **INV-042:** Machine-Checked DoD Gates investigation (design source)
- **E2-219:** Ground Truth Verification Parser (`parse_ground_truth_table()`, `classify_verification_type()`)
- **validate.py:** `.claude/lib/validate.py` contains parser implementation
