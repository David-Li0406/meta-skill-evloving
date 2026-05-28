---
name: plan-validation-cycle
description: HAIOS Plan Validation Bridge for validating plan readiness. Use before
  entering DO phase. Guides CHECK->VALIDATE->APPROVE workflow.
generated: 2025-12-25
last_updated: '2026-01-19T17:31:24'
---
# Plan Validation Cycle (Bridge Skill)

This is a **Validation Skill** (bridge) that validates implementation plans are complete before entering the DO phase. It acts as a quality gate between plan-authoring-cycle and implementation-cycle.

## When to Use

**Manual invocation:** `Skill(skill="plan-validation-cycle")` before starting implementation.
**Called from:** implementation-cycle PLAN phase exit (optional quality gate).

---

## The Cycle

```
CHECK --> SPEC_ALIGN --> VALIDATE --> L4_ALIGN --> APPROVE
```

### 1. CHECK Phase

**Goal:** Verify all required plan sections exist.

**Required Sections:**
- Goal (one sentence, >20 chars)
- Effort Estimation (metrics filled)
- Current State (code or description)
- Desired State (code or description)
- Tests First (at least one test or skip rationale)
- Detailed Design (implementation details)
  - Key Design Decisions table (with rationale, not placeholders)
- Implementation Steps (checklist items)
- Risks & Mitigations table (at least one risk identified)
- Verification (criteria defined)

**Actions:**
1. Read plan file
2. Check each required section exists
3. Detect placeholder text: `[...]`, `[N]`, `[X]`
4. Report missing or incomplete sections

**Exit Criteria:**
- [ ] All required sections present
- [ ] No placeholder text detected

**Tools:** Read

---

### 2. SPEC_ALIGN Phase (E2-254 Learning)

**Goal:** Verify plan's Detailed Design matches referenced specifications.

**MUST Gate:** This phase prevents "Assume over verify" anti-pattern where plans are designed from assumptions rather than actual specifications.

**Actions:**
1. Parse plan's `## References` section for specification documents
2. **MUST** read each referenced specification (INV-*, TRD-*, ADR-*, etc.)
3. Extract interface definitions from spec:
   - INPUT/OUTPUT signatures
   - Required functions/methods
   - Data structures/types
   - Dependencies
4. Compare plan's `## Detailed Design` against spec interface
5. Flag mismatches:
   - Functions in spec but missing from plan
   - Different signatures (params, return types)
   - Missing data structures
   - Wrong dependencies

**Exit Criteria:**
- [ ] **MUST:** All referenced specs read
- [ ] **MUST:** Plan's interface matches spec's interface
- [ ] **MUST:** No undocumented deviations from spec

**On Mismatch:** BLOCK with message listing specific deviations. Return to plan-authoring-cycle.
**On No References:** WARN "Plan has no referenced specifications - design may be based on assumptions"

**Tools:** Read, Grep

---

### 3. VALIDATE Phase

**Goal:** Check section content quality.

**Quality Checks:**
- Goal: Single sentence, measurable outcome
- Effort: Real numbers from file analysis
- Tests: Concrete assertions, not placeholders
- Design: File paths, code snippets present
- Key Design Decisions: Rationale column filled (not "[WHY...]" placeholders)
- Steps: Actionable checklist items
- Risks: At least one risk with mitigation (not just placeholders)
- **Open Decisions: No [BLOCKED] entries in Chosen column** (Gate 4 - E2-275)

> **INV-058 Gate 4:** This is the final gate of the Ambiguity Gating defense-in-depth strategy.
> - Gate 1 (E2-272): `operator_decisions` field in work_item.md template
> - Gate 2 (E2-273): "Open Decisions" section in implementation_plan.md template
> - Gate 3 (E2-274): AMBIGUITY phase in plan-authoring-cycle
> - **Gate 4 (E2-275): Open Decisions check in plan-validation-cycle (this check)**

**Actions:**
1. For each section, verify content quality
2. **Check Key Design Decisions has real rationale** - not placeholders
3. **Check Risks & Mitigations has real risks** - at least one identified
4. Flag sections with insufficient detail
5. **Check Open Decisions section (Gate 4):**
   - Scan "## Open Decisions" section for table
   - Check Chosen column for `[BLOCKED]` pattern
   - If ANY `[BLOCKED]` found: **BLOCK** with message listing unresolved decisions
   - If section missing or empty: Pass (no blocking decisions)
6. Report validation status

**Exit Criteria:**
- [ ] Goal is measurable
- [ ] Effort based on real analysis
- [ ] Tests have concrete assertions
- [ ] Design has implementation details
- [ ] **MUST:** Key Design Decisions has rationale (not placeholders)
- [ ] **MUST:** Risks & Mitigations has at least one real risk
- [ ] **MUST:** Open Decisions table has no `[BLOCKED]` entries (Gate 4)

**Tools:** Read

---

### 4. L4_ALIGN Phase

**Goal:** Verify plan deliverables align with L4 functional requirements.

**Prerequisite:** Get work_id from plan frontmatter `backlog_id` field.

**Actions:**
1. Read `.claude/haios/manifesto/L4-implementation.md`
2. Search for work_id in L4 (pattern: `### ModuleName (work_id)`)
3. If found, extract function requirements from table under that section
4. Parse plan "Implementation Steps" for deliverables mentioned
5. Match: For each L4 function, check if plan mentions it
6. Report gaps (L4 requires X but plan doesn't cover X)

**Exit Criteria:**
- [ ] L4 section found for work_id (or skip with note if not found)
- [ ] All L4 functions mentioned in plan steps (or gaps accepted by operator)

**On Gap Found:** Report gap, ask operator: "Accept gaps or revise plan?"
**On No L4 Entry:** Skip with note: "No L4 requirements found for {work_id}"

**Tools:** Read

---

### 5. APPROVE Phase

**Goal:** Mark plan as validated and ready, checkpoint context.

**Actions:**
1. If all checks pass, plan is approved
2. Report validation summary
3. **MUST** invoke checkpoint-cycle (E2-287)
4. Return to calling cycle

#### 5a. Checkpoint (MUST - E2-287)

**MUST** invoke checkpoint-cycle after validation passes:

```
Skill(skill="checkpoint-cycle")
```

**Rationale:** Work complexity within hardened gating system makes context limits per work item likely. Checkpointing after plan validation ensures continuity if context exhausts during implementation.

**On PASS:** Checkpoint then return to implementation-cycle - it will invoke preflight-checker next.
**On FAIL:** Return to plan-authoring-cycle or report blockers (no checkpoint needed for failures).

**MUST:** Do not pause for acknowledgment - checkpoint then return to calling cycle immediately.

**Exit Criteria:**
- [ ] All CHECK criteria passed
- [ ] **MUST:** SPEC_ALIGN passed (plan matches spec interface)
- [ ] All VALIDATE criteria passed
- [ ] L4_ALIGN passed or gaps accepted
- [ ] Plan ready for implementation
- [ ] **MUST:** checkpoint-cycle invoked (E2-287)
- [ ] Returned to calling cycle (no pause)

**Tools:** Skill (checkpoint-cycle)

---

## Composition Map

| Phase | Primary Tool | Output |
|-------|--------------|--------|
| CHECK | Read | List of missing sections |
| SPEC_ALIGN | Read, Grep | Spec vs plan comparison (MUST gate) |
| VALIDATE | Read | Quality assessment |
| L4_ALIGN | Read | Gap report (L4 vs plan) |
| APPROVE | Skill (checkpoint-cycle) | Validation summary + context preserved (E2-287) |

---

## Quick Reference

| Phase | Question to Ask | If NO |
|-------|-----------------|-------|
| CHECK | Are all sections present? | Report missing sections |
| CHECK | Any placeholders? | Report placeholder locations |
| SPEC_ALIGN | Are referenced specs read? | **BLOCK** - read specs first |
| SPEC_ALIGN | Does plan interface match spec? | **BLOCK** - revise plan |
| VALIDATE | Is Goal measurable? | Flag for revision |
| VALIDATE | Are Tests concrete? | Flag for revision |
| **VALIDATE** | Any `[BLOCKED]` in Open Decisions? | **BLOCK** - resolve decisions first (Gate 4) |
| L4_ALIGN | Does L4 have entry for work_id? | Skip with note |
| L4_ALIGN | All L4 functions in plan? | Report gaps, ask to accept |
| APPROVE | All checks passed? | Return to authoring |

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Five phases | CHECK -> SPEC_ALIGN -> VALIDATE -> L4_ALIGN -> APPROVE | SPEC_ALIGN added after E2-254 learning |
| SPEC_ALIGN = MUST gate | BLOCK if mismatch | Prevents "Assume over verify" anti-pattern |
| Validation not authoring | Separate from plan-authoring-cycle | Different concerns |
| Read-only | No modifications | Bridge skills validate, don't modify |
| Optional gate | Not required | Some plans may be pre-validated |
| L4_ALIGN gaps = warning | Operator can accept | Iterative implementation may defer functions |

---

## Related

- **plan-authoring-cycle skill:** Populates plan sections
- **implementation-cycle skill:** Uses validated plans
- **close-work-cycle skill:** Parallel validation pattern
- **Implementation plan template:** `.claude/templates/implementation_plan.md`
