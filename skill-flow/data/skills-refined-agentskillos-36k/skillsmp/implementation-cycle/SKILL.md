---
name: implementation-cycle
description: HAIOS Implementation Cycle for structured work item implementation. Use
  when starting implementation of a plan. Guides PLAN->DO->CHECK->DONE workflow with
  phase-specific tooling.
recipes:
- node
generated: 2025-12-22
last_updated: '2026-01-16T21:51:18'
---
# Implementation Cycle

This skill defines the PLAN-DO-CHECK-DONE cycle for structured implementation of work items. It composes existing primitives (Skills, Commands, Subagents, Justfile) into a coherent workflow.

## When to Use

**SHOULD** invoke this skill when:
- Starting implementation of a backlog item
- Resuming work on an in-progress item
- Unsure of next step in implementation workflow

**Invocation:** `Skill(skill="implementation-cycle")`

---

## The Cycle

```
PLAN --> DO --> CHECK --> DONE --> CHAIN
  ^       ^       |                  |
  |       +-------+ (if tests fail)  [route next]
  +-- (if no plan)                   |
                              /-------------\
                             INV-*    has plan?   else
                               |         |          |
                          investigation  implement  work-creation
                             -cycle      -cycle     -cycle
```

### 1. PLAN Phase

**On Entry:**
```bash
just set-cycle implementation-cycle PLAN {work_id}
```

**Goal:** Verify plan exists and is ready for implementation.

**Actions:**
1. Read the plan file: `docs/work/active/{backlog_id}/plans/PLAN.md` (or legacy `docs/plans/PLAN-{backlog_id}-*.md`)
2. Verify plan has filled-in sections (not template placeholders)
3. Check `status: draft` -> if so, fill in design first
4. **MUST:** Read referenced specifications (see MUST Gate below)
5. Optional: Run preflight checker (E2-093 when available)

**MUST Gate: Read Source Specifications (E2-254 Learning)**
Even if plan was authored in a prior session, the implementer **MUST** read source specs:
1. Parse plan's `## References` section
2. **MUST** read each referenced specification document
3. Verify plan's Detailed Design matches spec interface
4. If mismatch detected, **BLOCK** and return to plan-authoring-cycle

> **Anti-pattern prevented:** "Inherit without verify" - accepting a plan from a prior session without reading the specs it references leads to implementing the wrong design.

**FORESIGHT Prep (Optional - E2-106):**
Before leaving PLAN phase, capture predictions to frontmatter:
```yaml
foresight_prep:
  predicted_outcome: "What I expect to happen when this is complete"
  predicted_confidence: 0.75  # How confident am I? (0-1)
  knowledge_gaps: ["What do I need to learn?"]
  skill_gaps: ["What abilities am I missing?"]
  competence_domain: "category_tag"  # e.g., "hook_development", "subagent_creation"
```
> This prepares data for Epoch 3 FORESIGHT layer. Captures ANTICIPATE operation output.

**Exit Criteria:**
- [ ] Plan file exists with complete design
- [ ] **MUST:** Referenced specifications read and verified against plan
- [ ] Tests defined in "Tests First" section
- [ ] Current/Desired state documented
- [ ] (Optional) foresight_prep captured with prediction
- [ ] **MUST:** Invoke `Skill(skill="plan-validation-cycle")` before proceeding to DO
- [ ] **MUST:** Invoke `Task(subagent_type='preflight-checker')` to validate readiness

**Exit Gate (MUST):**
Before transitioning to DO phase, **MUST** invoke plan-validation-cycle:
```
Skill(skill="plan-validation-cycle")
```

**THEN MUST** invoke preflight-checker agent to validate plan readiness:
```
Task(subagent_type='preflight-checker', prompt='Check plan for {backlog_id}')
```
This validates plan completeness and file scope. DO phase is blocked until preflight passes.

**Tools:** Read, Glob, Task(preflight-checker), Skill(plan-validation-cycle)

---

### 2. DO Phase

**On Entry:**
```bash
just set-cycle implementation-cycle DO {work_id}
```

**Goal:** Implement the design from the plan.

**Guardrails (SHOULD follow):**
1. **List affected files BEFORE writing** - Create manifest of files to modify
2. **One logical change at a time** - Atomic commits, easier rollback
3. **If >3 files, pause for confirmation** - Large scope = higher risk

**File Manifest Format:**
```markdown
## Files to Modify
- [ ] path/to/file1.py - Add function X
- [ ] path/to/file2.py - Update import
- [ ] tests/test_file.py - Add test for X
```

> If manifest has >3 files, SHOULD confirm scope with operator before proceeding.
> Preflight Checker (E2-093) will enforce this when available.

**Actions:**
1. Create file manifest (list all files to modify)
2. **MUST** write failing tests first (from plan's Tests section) - no code before tests
3. Implement ONE change at a time (RED -> GREEN -> REFACTOR)
4. Follow plan's Implementation Steps
5. Use memory-agent skill for prior learnings

**TDD Enforcement (Session 90):**
- Tests **MUST** exist before implementation code
- For non-pytest code (PowerShell, configs), define manual verification steps in plan
- If no tests possible, document why in plan and get operator approval

**Exit Criteria:**
- [ ] Tests written BEFORE implementation code
- [ ] File manifest complete and followed
- [ ] All planned code changes made
- [ ] Implementation matches Detailed Design
- [ ] Each change tested before next
- [ ] **MUST:** Invoke `Skill(skill="design-review-validation")` before proceeding to CHECK

**Exit Gate (MUST):**
Before transitioning to CHECK phase, **MUST** invoke design-review-validation:
```
Skill(skill="design-review-validation")
```
This verifies implementation aligns with Detailed Design. CHECK phase is blocked until validation passes.

**Tools:** Write, Edit, Bash(pytest), Skill(memory-agent), Skill(design-review-validation), Task(preflight-checker)

---

### 3. CHECK Phase

**On Entry:**
```bash
just set-cycle implementation-cycle CHECK {work_id}
```

**Goal:** Verify implementation meets quality bar.

**Actions:**
1. Run test suite: `pytest tests/ -v`
2. Verify all tests pass (no regressions)
3. **DEMO the feature** - Exercise the new code path to surface bugs (Session 90)
4. Run plan's Ground Truth Verification
5. Check DoD criteria (ADR-033)
6. **MUST: Verify WORK.md Deliverables** (Session 192 - E2-290 Learning)
7. **If creating discoverable artifact:** Verify runtime discovery (see below)
8. **(Optional) Invoke validation-agent** for unbiased review: `Task(subagent_type='validation-agent')`

**MUST Gate: Deliverables Verification (Session 192)**
Before declaring CHECK complete:
1. **MUST** read `docs/work/active/{backlog_id}/WORK.md`
2. **MUST** find the `## Deliverables` section
3. **MUST** verify EACH deliverable checkbox can be checked:
   - For each `- [ ]` item, confirm the work is actually done
   - If ANY deliverable is incomplete, **BLOCK** - return to DO phase
4. **MUST** also check plan's Implementation Steps are all complete

> **Anti-pattern prevented:** "Tests pass = Done" (E2-290 Session 192). Agent declared victory after tests passed but skipped 2 of 7 deliverables. Tests verify code works, deliverables verify scope is complete. Both are required.

**Demo Step (Session 90 - TDD Gap Discovery):**
- Demo **MUST** exercise the happy path at minimum
- For hooks/commands: Run them and verify output
- For new functions: Call them with real data
- Document any bugs found during demo
- If bugs found: Fix and re-run CHECK phase

**For non-code tasks** (docs, ADRs, configs):
- Skip pytest if no code changes
- Focus on Ground Truth Verification (files exist, content correct)
- Use `/validate` command for template compliance
- Manual review replaces automated tests

**For discoverable artifacts** (skills, agents, commands):
- Run `just update-status-slim`
- Verify artifact appears in haios-status-slim.json
- File existence is NOT sufficient - must verify runtime discovery
- See INV-012 for anti-pattern details

**FORESIGHT Calibration (Optional - E2-106):**
Compare prediction to actual outcome, update foresight_prep in frontmatter:
```yaml
foresight_prep:
  # ... PLAN phase fields preserved ...
  actual_outcome: "What actually happened"
  prediction_error: 0.2  # How wrong was I? (0-1 scale)
  competence_estimate: 0.7  # How good am I at this domain now? (0-1)
  failure_modes_discovered: ["What I didn't anticipate"]
```
> This prepares data for Epoch 3 FORESIGHT layer. Enables UPDATE operation calibration.

**Exit Criteria:**
- [ ] All tests pass (or N/A for non-code)
- [ ] Ground Truth Verification complete
- [ ] No regressions in full test suite (or N/A)
- [ ] **MUST:** All WORK.md deliverables verified complete
- [ ] **MUST:** All plan Implementation Steps checked off
- [ ] Discoverable artifacts appear in runtime status (or N/A)
- [ ] (Optional) foresight_prep calibration fields updated

**Tools:** Bash(pytest), Read, Task(test-runner), Task(validation-agent), /validate, just update-status

---

### 4. DONE Phase

**On Entry:**
```bash
just set-cycle implementation-cycle DONE {work_id}
```

**Goal:** Complete implementation and prepare for closure.

**Actions:**
1. Capture WHY: Store learnings to memory
2. Update plan status: `status: complete`
3. Update documentation if behavior changed

**Exit Criteria:**
- [ ] WHY captured (memory_refs in checkpoint)
- [ ] Plan marked complete
- [ ] Docs updated (CLAUDE.md, READMEs)

**Tools:** ingester_ingest, Edit, Write

---

### 5. CHAIN Phase (Post-DONE)

**On Entry:**
```bash
just set-cycle implementation-cycle CHAIN {work_id}
```

**Goal:** Close work item and route to next work item.

**Actions:**
1. Close work item: `/close {backlog_id}`
2. Query next work: `just ready`
3. If items returned, read first work file to check `documents.plans`
4. **Apply routing decision table** (see `routing-gate` skill):
   - If `next_work_id` is None → `await_operator`
   - If ID starts with `INV-` → `invoke_investigation`
   - If `has_plan` is True → `invoke_implementation`
   - Else → `invoke_work_creation`
5. Execute the action:
   - `invoke_investigation` -> `Skill(skill="investigation-cycle")`
   - `invoke_implementation` -> `Skill(skill="implementation-cycle")`
   - `invoke_work_creation` -> `Skill(skill="work-creation-cycle")`
   - `await_operator` -> Report "No unblocked work. Awaiting operator direction."

**MUST:** Do not pause for acknowledgment - execute routing immediately.

**Exit Criteria:**
- [ ] Work item closed via /close
- [ ] Next work item identified (or none available)
- [ ] Appropriate cycle skill invoked (or awaiting operator)

**On Complete:**
```bash
just clear-cycle
```

**Tools:** /close, Bash(just ready), Read, Skill(routing-gate)

---

## Composition Map

| Phase | Primary Tool | Optional Subagent | Command |
|-------|--------------|-------------------|---------|
| PLAN  | Read, Glob   | preflight-checker | /new-plan |
| DO    | Write, Edit  | -                 | - |
| CHECK | Bash(pytest) | test-runner       | /validate |
| DONE  | Edit, Write  | why-capturer      | - |
| CHAIN | Bash, Skill  | -                 | /close |

---

## Quick Reference

| Phase | Question to Ask | If NO |
|-------|-----------------|-------|
| PLAN  | Is the plan ready? | Fill in design |
| DO    | Is file manifest created? | List files first |
| DO    | Is implementation done? | One change at a time |
| CHECK | Is verification complete? | Fix issues, retest |
| CHECK | **Are ALL WORK.md deliverables done?** | **BLOCK - return to DO** |
| CHECK | **Are ALL plan steps checked off?** | **BLOCK - return to DO** |
| CHECK | Is artifact discoverable? | Run update-status, verify in slim JSON |
| DONE  | Is WHY captured? | Store learnings |
| CHAIN | Is work item closed? | Run /close {backlog_id} |
| CHAIN | Is next work identified? | Run `just ready` |

**DO phase guardrails:**
- List files BEFORE writing (manifest)
- One logical change at a time
- >3 files? Pause and confirm scope

**CHECK varies by task type:**
- Code: `pytest tests/ -v` + Ground Truth
- Docs/ADRs: `/validate` + Ground Truth
- Config: Manual review + Ground Truth
- Skills/Agents/Commands: `just update-status` + verify in haios-status-slim.json

---

## TDD Cycle Within DO Phase

```
Write Test (FAIL) --> Run --> Write Code --> Run (PASS) --> Refactor --> Loop
     RED                         GREEN                      REFACTOR
```

1. Write a failing test first
2. Run test - see it FAIL (RED)
3. Write minimal code to pass
4. Run test - see it PASS (GREEN)
5. Refactor if needed
6. Repeat for next test

---

## Governance Event Logging (E2-108)

**SHOULD** log phase transitions and validation outcomes for observability.

### Phase Transition Logging

Phase transitions are logged automatically via governance hooks. View with:
```bash
just governance-metrics
```

### Validation Outcome Logging

Validation outcomes are logged automatically. Check audit trail via:
```bash
just events
```

### Benefits

- **Metrics:** `just governance-metrics` shows pass rates and common failures
- **Warnings:** Repeated failures (3+) trigger immediate warning
- **Audit:** Events are checked at close time to surface governance bypasses

---

## Related

- **ADR-033:** Work Item Lifecycle (DoD criteria)
- **ADR-038:** M2-Governance Symphony Architecture
- **E2-108:** Gate Observability (governance event logging)
- **/implement command:** E2-092 will invoke this skill
- **Preflight Checker:** E2-093 will enforce DO phase guardrails
- **Test Runner:** E2-094 for isolated test execution
- **WHY Capturer:** E2-095 for automated learning capture
- **FORESIGHT Prep:** E2-106 adds optional prediction/calibration fields (Epoch 3 bridge)
- **Epoch 3 Spec:** `epoch3/foresight-spec.md` - SIMULATE, INTROSPECT, ANTICIPATE, UPDATE operations
