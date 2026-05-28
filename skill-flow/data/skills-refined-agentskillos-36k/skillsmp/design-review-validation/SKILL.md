---
name: design-review-validation
description: HAIOS Design Review Validation for verifying implementation alignment.
  Use during DO phase. Guides COMPARE->VERIFY->APPROVE workflow.
generated: 2025-12-25
last_updated: '2026-01-03T14:49:27'
---
# Design Review Validation (Bridge Skill)

This is a **Validation Skill** (bridge) that verifies implementation aligns with the plan's Detailed Design. Use during or after DO phase.

## When to Use

**Manual invocation:** `Skill(skill="design-review-validation")` after implementation.
**Called from:** implementation-cycle DO phase exit (optional quality gate).

---

## The Cycle

```
COMPARE --> VERIFY --> L4_ALIGN --> APPROVE
```

### 1. COMPARE Phase

**Goal:** Read implementation and compare against Detailed Design.

**Actions:**
1. Read plan's Detailed Design section
2. Read implemented files from the file manifest
3. Create comparison checklist

**Comparison Points:**
- File paths match plan
- Function signatures match plan
- Logic flow matches design diagrams
- Key design decisions followed

**Exit Criteria:**
- [ ] Plan's Detailed Design read
- [ ] Implementation files read
- [ ] Comparison checklist created

**Tools:** Read

---

### 2. VERIFY Phase

**Goal:** Check each comparison point for alignment.

**Verification Checks:**
- [ ] File manifest matches implemented files
- [ ] Function signatures match (names, params, returns)
- [ ] Logic flow matches design
- [ ] No undocumented deviations

**Actions:**
1. For each comparison point, verify alignment
2. Flag deviations as intentional or unintentional
3. Report verification status

**Exit Criteria:**
- [ ] All comparison points checked
- [ ] Deviations documented
- [ ] Verification report created

**Tools:** Read, Grep

---

### 3. L4_ALIGN Phase

**Goal:** Verify implementation covers L4 functional requirements.

**Prerequisite:** Get work_id from plan frontmatter `backlog_id` field.

**Actions:**
1. Read `.claude/haios/manifesto/L4-implementation.md`
2. Search for work_id in L4 (pattern: `### ModuleName (work_id)`)
3. If found, extract function requirements from table
4. Check implementation files for each required function
5. Report gaps (L4 requires X but implementation doesn't have X)

**Exit Criteria:**
- [ ] L4 section found for work_id (or skip with note if not found)
- [ ] All L4 functions implemented (or gaps accepted by operator)

**On Gap Found:** Report gap, ask operator: "Accept gaps or fix implementation?"
**On No L4 Entry:** Skip with note: "No L4 requirements found for {work_id}"

**Tools:** Read, Grep

---

### 4. APPROVE Phase

**Goal:** Confirm implementation is aligned or document deviations.

**Actions:**
1. If all checks pass, approve implementation
2. If deviations found:
   - Document why (intentional improvement or error)
   - Update plan if intentional change
   - Fix implementation if error
3. Report final status
4. Return to calling cycle immediately

**On PASS:** Return to implementation-cycle - it will proceed to CHECK phase.
**On FAIL:** Return to DO phase for fixes.

**MUST:** Do not pause for acknowledgment - return to calling cycle immediately.

**Exit Criteria:**
- [ ] Implementation approved, OR
- [ ] Deviations documented and addressed
- [ ] L4_ALIGN passed or gaps accepted
- [ ] Returned to calling cycle (no pause)

**Tools:** Edit (for plan updates)

---

## Composition Map

| Phase | Primary Tool | Output |
|-------|--------------|--------|
| COMPARE | Read | Comparison checklist |
| VERIFY | Read, Grep | Deviation report |
| L4_ALIGN | Read, Grep | L4 gap report |
| APPROVE | Edit (optional) | Approval status |

---

## Quick Reference

| Phase | Question to Ask | If NO |
|-------|-----------------|-------|
| COMPARE | Is Detailed Design read? | Read plan |
| COMPARE | Are implementation files read? | Read manifested files |
| VERIFY | Do signatures match? | Flag deviation |
| VERIFY | Does logic flow match? | Flag deviation |
| L4_ALIGN | Does L4 have entry for work_id? | Skip with note |
| L4_ALIGN | All L4 functions implemented? | Report gaps, ask to accept |
| APPROVE | Is implementation aligned? | Document and fix |

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Four phases | COMPARE -> VERIFY -> L4_ALIGN -> APPROVE | L4_ALIGN added for requirements traceability |
| Optional gate | Not required | Some implementations may be straightforward |
| Deviation handling | Document and decide | Not all deviations are errors |
| Read-only except APPROVE | Only modifies if updating plan | Validation doesn't change implementation |
| L4_ALIGN gaps = warning | Operator can accept | Iterative implementation may defer functions |

---

## Related

- **plan-validation-cycle skill:** Pre-DO validation (plan completeness)
- **implementation-cycle skill:** Uses this skill during DO phase
- **close-work-cycle skill:** Post-DO validation (DoD check)
- **dod-validation-cycle skill:** Parallel validation pattern
