---
name: close-work-cycle
description: HAIOS Close Work Cycle for structured work item closure. Use when closing
  work items. Guides VALIDATE->ARCHIVE->MEMORY workflow with DoD enforcement.
recipes:
- close-work
- update-status
generated: 2025-12-25
last_updated: '2026-01-19T17:31:34'
---
# Close Work Cycle

This skill defines the VALIDATE-ARCHIVE-MEMORY cycle for closing work items with Definition of Done (DoD) enforcement per ADR-033.

## When to Use

**Invoked automatically** by `/close` command after observation-capture-cycle.
**Manual invocation:** `Skill(skill="close-work-cycle")` when closing an existing work item.

---

## The Cycle

```
[observation-capture-cycle] --> [dod-validation-cycle] --> VALIDATE --> ARCHIVE --> MEMORY --> CHAIN
         │                                                                                       |
         │                                                                                [route next]
   reflection first                                                                              |
   (RECALL->NOTICE->COMMIT)                                                             /-------------\
                                                                                       INV-*    has plan?   else
                                                                                         |         |          |
                                                                                    investigation  implement  work-creation
                                                                                       -cycle      -cycle     -cycle
```

**Entry Gates (MUST):**

1. **Observation Capture (E2-278):** Before starting this cycle, **MUST** invoke observation-capture-cycle:
   ```
   Skill(skill="observation-capture-cycle")
   ```
   This forces genuine reflection in dedicated cognitive context before entering "closing mode."

2. **DoD Validation:** Before VALIDATE phase, **MUST** invoke dod-validation-cycle:
   ```
   Skill(skill="dod-validation-cycle")
   ```
   This validates DoD criteria in an isolated bridge skill.

---

### 1. VALIDATE Phase

**On Entry:**
```bash
just set-cycle close-work-cycle VALIDATE {work_id}
```

**Goal:** Verify work item meets Definition of Done criteria.

**Guardrails (MUST follow):**
1. **Tests MUST pass** - Prompt user to confirm
2. **WHY MUST be captured** - Check for memory_refs in associated docs
3. **Docs MUST be current** - CLAUDE.md, READMEs updated
4. **Traced files MUST be complete** - Associated plans have status: complete

**Actions:**
1. Read work file: `docs/work/active/{id}/WORK.md` (or `docs/work/active/WORK-{id}-*.md` for legacy)
2. Check work directory for plans: `docs/work/active/{id}/plans/`
3. Check plan statuses - all must be `complete`
4. For INV-* items: Apply investigation-specific DoD
5. Prompt user for DoD confirmation

**Exit Criteria:**
- [ ] Work file exists and has status: active
- [ ] All associated plans have status: complete
- [ ] User confirms: tests pass, WHY captured, docs current

**Tools:** Read, Glob, Grep

---

### 2. ARCHIVE Phase

**On Entry:**
```bash
just set-cycle close-work-cycle ARCHIVE {work_id}
```

**Goal:** Update work item status to complete.

**Note:** Per ADR-041 "status over location" - work items stay in `docs/work/active/` until epoch cleanup. The `status: complete` field determines state, not directory path.

**Actions:**
1. Run atomic close-work recipe:
   ```bash
   just close-work {id}
   ```
   This atomically performs:
   - Update `status: active` to `status: complete`
   - Update `closed: null` to `closed: {YYYY-MM-DD}`
   - Run cascade and update-status

2. Update any associated plans to `status: complete` (if not already)

**Exit Criteria:**
- [ ] `just close-work` succeeded
- [ ] Work file has `status: complete` and `closed: {date}`
- [ ] Associated plans marked complete

**Tools:** Bash(just close-work)

---

### 3. MEMORY Phase

**On Entry:**
```bash
just set-cycle close-work-cycle MEMORY {work_id}
```

**Goal:** Store closure summary to memory and verify governance events.

**Actions:**

#### 3a. Governance Event Check (E2-108)

1. **Check for cycle events** (soft gate - warns but does not block):
   ```bash
   just events | grep "{id}"
   ```
   - If no events found for the work ID, warn that governance may have been bypassed
   - Work item can still close, but warning surfaces potential governance bypass

#### 3b. Memory Capture

2. Store closure summary via `ingester_ingest`:
   - Title, backlog_id, DoD status, associated documents
   - Include observation summary if any captured in observation-capture-cycle
   - Use source_path: `closure:{backlog_id}`

#### 3c. Report Closure

3. Report closure to user with memory concept ID

**Exit Criteria:**
- [ ] Governance event check completed (warning if no events)
- [ ] Closure summary stored to memory
- [ ] User informed of successful closure with memory concept ID

**Tools:** governance_events.check_work_item_events, ingester_ingest

**Note:** Status refresh is handled by `just close-work` in ARCHIVE phase (includes cascade and update-status).

---

### 4. CHAIN Phase (Post-MEMORY)

**On Entry:**
```bash
just set-cycle close-work-cycle CHAIN {work_id}
```

**Goal:** Checkpoint context then route to next work item.

#### 4a. Checkpoint (MUST - E2-287)

**MUST** invoke checkpoint-cycle before routing to next work:

```
Skill(skill="checkpoint-cycle")
```

**Rationale:** Work complexity within hardened gating system makes context limits per work item likely. Checkpointing after closure ensures context from completed work is preserved before starting new work. Next session picks up with full context of decisions made.

#### 4b. Route to Next Work

**Actions:**
1. (Closure already completed in MEMORY phase)
2. (Checkpoint completed in 4a)
3. Query next work: `just ready`
4. If items returned, read first work file to check `documents.plans`
5. **Apply routing decision table** (see `routing-gate` skill):
   - If `next_work_id` is None → `await_operator`
   - If ID starts with `INV-` → `invoke_investigation`
   - If `has_plan` is True → `invoke_implementation`
   - Else → `invoke_work_creation`
6. Execute the action:
   - `invoke_investigation` -> `Skill(skill="investigation-cycle")`
   - `invoke_implementation` -> `Skill(skill="implementation-cycle")`
   - `invoke_work_creation` -> `Skill(skill="work-creation-cycle")`
   - `await_operator` -> Report "No unblocked work. Awaiting operator direction."

**MUST:** Do not pause for acknowledgment - checkpoint then execute routing immediately.

**Exit Criteria:**
- [ ] **MUST:** checkpoint-cycle invoked (E2-287)
- [ ] Next work item identified (or none available)
- [ ] Appropriate cycle skill invoked (or awaiting operator)

**On Complete:**
```bash
just clear-cycle
```

**Tools:** Bash(just ready), Read, Skill(checkpoint-cycle, routing-gate)

---

## Composition Map

| Phase | Primary Tool | Memory Integration |
|-------|--------------|-------------------|
| (Entry) observation-capture-cycle | Skill | Observation capture via RECALL->NOTICE->COMMIT |
| VALIDATE | Read, Glob, Grep | Query for prior work (optional) |
| ARCHIVE | Bash(just close-work) | - |
| MEMORY | ingester_ingest | Closure summary |
| CHAIN | Skill (checkpoint-cycle, routing) | Context preservation (E2-287) |

---

## Quick Reference

| Phase | Question to Ask | If NO |
|-------|-----------------|-------|
| (Entry) | Observations captured? | Invoke observation-capture-cycle first |
| VALIDATE | Does work file exist? | STOP - not found |
| VALIDATE | Are all plans complete? | STOP or warn user |
| VALIDATE | Does user confirm DoD? | STOP - DoD not met |
| ARCHIVE | Is work file archived? | Run `just close-work` |
| MEMORY | Is closure stored? | Store via ingester |
| CHAIN | Is next work identified? | Run `just ready` |

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Three phases | VALIDATE -> ARCHIVE -> MEMORY | E2-278: OBSERVE extracted to observation-capture-cycle |
| observation-capture-cycle as entry gate | Dedicated cognitive context | INV-059: Embedding causes completion mode bias |
| Keep command lookup | Skill assumes work item found | Command handles "not found" case before skill |
| Skill documents steps | Command + Skill redundancy | Command is authoritative; skill provides structure |
| MEMORY phase after archive | After archive | Memory should reflect completed state |

---

## Related

- **observation-capture-cycle skill:** Entry gate for genuine reflection (E2-278)
- **observation-triage-cycle skill:** Processes captured observations
- **work-creation-cycle skill:** Parallel workflow for creation
- **implementation-cycle skill:** Parallel workflow for implementation
- **investigation-cycle skill:** Parallel workflow for research
- **ADR-033:** Work Item Lifecycle Governance
- **/close command:** Invokes observation-capture-cycle then this skill
