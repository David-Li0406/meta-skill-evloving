---
name: investigation-cycle
description: HAIOS Investigation Cycle for structured research and discovery. Use
  when starting or resuming an investigation. Guides HYPOTHESIZE->EXPLORE->CONCLUDE
  workflow with phase-specific tooling.
recipes:
- inv
generated: 2025-12-22
last_updated: '2026-01-16T22:00:54'
---
# Investigation Cycle

This skill defines the HYPOTHESIZE-EXPLORE-CONCLUDE cycle for structured investigation of research questions. It composes existing primitives (Skills, Commands, Memory) into a coherent research workflow.

## When to Use

**SHOULD** invoke this skill when:
- Starting a new investigation
- Resuming work on an in-progress investigation
- Unsure of next step in research workflow

**Invocation:** `Skill(skill="investigation-cycle")`

---

## The Cycle

```
HYPOTHESIZE --> EXPLORE --> CONCLUDE --> CHAIN
      ^            ^           |           |
      |            +-----------+     [route next]
      +-- (if no investigation doc)        |
                                    /-------------\
                                   INV-*    has plan?   else
                                     |         |          |
                                investigation  implement  work-creation
                                   -cycle      -cycle     -cycle
```

**Parallel to Implementation Cycle:**

| Implementation | Investigation | Purpose |
|----------------|---------------|---------|
| PLAN | HYPOTHESIZE | Define what to do |
| DO | EXPLORE | Execute the work |
| CHECK + DONE | CONCLUDE | Verify, capture, close |

---

### 1. HYPOTHESIZE Phase

**On Entry:**
```bash
just set-cycle investigation-cycle HYPOTHESIZE {work_id}
```

**Goal:** Verify investigation exists and is ready for exploration.

**Actions:**
1. Read work file: `docs/work/active/{backlog_id}/WORK.md`
2. **MUST read ALL @ referenced files** at document top before proceeding
3. **MUST Glob referenced directories** to find all files (e.g., `@docs/work/active/INV-052/` → `Glob("docs/work/active/INV-052/**/*.md")`)
4. Verify work file has filled-in Context section (not template placeholders)
5. Check `status: active` - if draft, fill in context/hypotheses first
6. Query memory for prior related work

**Exit Criteria:**
- [ ] Work file exists with complete context
- [ ] **MUST:** All @ referenced files read (Session 171 learning)
- [ ] Hypotheses defined (at least H1)
- [ ] Scope defined (in/out)
- [ ] Memory queried for prior related findings

**Tools:** Read, Glob, memory_search_with_experience

---

### 2. EXPLORE Phase

**On Entry:**
```bash
just set-cycle investigation-cycle EXPLORE {work_id}
```

**Goal:** Execute investigation steps and document findings.

**Guardrails (MUST follow):**
1. **MUST invoke investigation-agent** for evidence gathering - specialized subagent handles exploration
2. **One hypothesis at a time** - Focus exploration
3. **Document findings as discovered** - Don't wait until end
4. **Query memory before assuming** - Prior work may answer questions
5. **MUST update Exploration Plan checklist** after investigation-agent returns - mark all executed steps as complete

**Actions:**
1. Execute investigation steps from document (via investigation-agent)
2. **After subagent returns:** Update Exploration Plan checklist to mark completed steps [x]
3. For each step, update Findings section
4. Use memory-agent for context before deep dives
5. If new hypotheses emerge, add them to document

**Exit Criteria:**
- [ ] All investigation steps executed
- [ ] **Exploration Plan checklist updated** (all steps marked [x])
- [ ] Findings section populated with evidence
- [ ] Hypotheses marked as confirmed/refuted/inconclusive

**Tools:** Read, Grep, Glob, Bash, memory_search_with_experience, WebSearch (if needed)

---

### 3. CONCLUDE Phase

**On Entry:**
```bash
just set-cycle investigation-cycle CONCLUDE {work_id}
```

**Goal:** Synthesize findings and spawn work items.

**Actions:**
1. Review findings against original objective
2. Identify spawned work items (ADRs, backlog items, new investigations)
3. Create spawned items using `/new-*` commands with `spawned_by: {this_investigation_id}`
4. Store findings summary to memory via `ingester_ingest`
5. Update investigation status: `status: complete`

**Exit Criteria:**
- [ ] Findings synthesized (answer to objective documented)
- [ ] Spawned work items created with `spawned_by` field linking to investigation
- [ ] Learnings stored to memory (memory_refs populated)
- [ ] Investigation marked complete

**Tools:** ingester_ingest, Edit, /new-adr, /new-plan

---

### 4. CHAIN Phase (Post-CONCLUDE)

**On Entry:**
```bash
just set-cycle investigation-cycle CHAIN {work_id}
```

**Goal:** Close investigation and route to next work item.

**Actions:**
1. Close investigation: `/close {backlog_id}`
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
- [ ] Investigation closed via /close
- [ ] Next work item identified (or none available)
- [ ] Appropriate cycle skill invoked (or awaiting operator)

**On Complete:**
```bash
just clear-cycle
```

**Tools:** /close, Bash(just ready), Read, Skill(routing-gate)

---

## Composition Map

| Phase | Primary Tool | Memory Integration | Command |
|-------|--------------|-------------------|---------|
| HYPOTHESIZE | Read, Glob | memory_search (prior work) | /new-investigation |
| EXPLORE | Grep, Read, Bash | memory_search (context) | - |
| CONCLUDE | Edit, Write | ingester_ingest (findings) | - |
| CHAIN | Bash, Skill | - | /close |

---

## Quick Reference

| Phase | Question to Ask | If NO |
|-------|-----------------|-------|
| HYPOTHESIZE | Is investigation ready? | Fill in context/hypotheses |
| HYPOTHESIZE | Memory queried? | Run memory_search_with_experience |
| EXPLORE | Are all steps executed? | Continue exploration |
| EXPLORE | Are findings documented? | Update Findings section |
| CONCLUDE | Are spawned items created? | Create via /new-* commands |
| CONCLUDE | Are learnings stored? | Run ingester_ingest |
| CHAIN | Is investigation closed? | Run /close {backlog_id} |
| CHAIN | Is next work identified? | Run `just ready` |

**EXPLORE phase guardrails:**
- One hypothesis at a time
- Document findings as discovered
- Query memory before assuming

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Three phases not four | CONCLUDE combines CHECK+DONE | Investigations don't have separate verification |
| No TDD requirement | Investigations produce findings, not code | Research is exploratory, not constructive |
| Memory query at start | HYPOTHESIZE includes prior work check | Avoid re-investigating solved problems |
| Spawned work items | Required exit criterion | Investigations should produce actionable output |

---

## Related

- **implementation-cycle skill:** Parallel workflow for implementation tasks
- **Investigation template:** `.claude/templates/investigation.md`
- **ADR-033:** Work Item Lifecycle (DoD criteria)
- **/new-investigation command:** Creates investigation documents
- **/close command:** Closes completed investigations
