---
name: observation-triage-cycle
description: HAIOS Observation Triage Cycle for processing captured observations.
  Use when scanning archived work items to triage and act on observations. Guides
  SCAN->TRIAGE->PROMOTE workflow with dimension validation.
generated: 2025-12-28
last_updated: '2026-01-07T20:28:24'
---
# Observation Triage Cycle

This skill defines the SCAN-TRIAGE-PROMOTE cycle for processing archived observations and routing them to actionable outcomes.

## When to Use

**Manual invocation:** `Skill(skill="observation-triage-cycle")` when processing accumulated observations.
**Via recipe:** `just triage-observations` for quick scan.
**Scheduled:** Can be invoked during heartbeat or session-end.

---

## The Cycle

```
SCAN --> TRIAGE --> PROMOTE
  |         |           |
  |         |           +-> spawn:INV, spawn:WORK, spawn:FIX
  |         |           +-> memory (store insight)
  |         |           +-> discuss (flag for operator)
  |         |           +-> dismiss (no action)
  |         |
  |         +-> Apply dimensions: category, action, priority
  |
  +-> Find archived observations with triage_status: pending
```

---

### 1. SCAN Phase

**Goal:** Find archived work items with untriaged observations.

**Actions:**
1. Run scan command:
   ```bash
   just triage-observations
   ```
2. Report count of items with pending observations
3. List work items and observation summaries

**Exit Criteria:**
- [ ] Scan completed
- [ ] Count and list of pending observations reported

**Tools:** Bash(just triage-observations), Read

---

### 2. TRIAGE Phase

**Goal:** Classify each observation with category, action, and priority.

**Triage Dimensions (Industry Standard):**

| Dimension | Question | Values |
|-----------|----------|--------|
| **Category** | What type? | bug, gap, debt, insight, question, noise |
| **Action** | What to do? | spawn:INV, spawn:WORK, spawn:FIX, memory, discuss, dismiss |
| **Priority** | When? | P0 (blocking), P1 (this session), P2 (next), P3 (backlog) |

**Actions:**
1. For each observation, prompt for dimensions:
   - Category: What type of observation is this?
   - Action: What should happen next?
   - Priority: How urgent is this?
2. Validate dimensions (ValueError if invalid)
3. Collect triaged observations

**Example Triage Prompt:**
```
Observation: "commit-close recipe uses legacy patterns"
Section: Gaps Noticed
Source: E2-217

Category? [bug/gap/debt/insight/question/noise]: gap
Action? [spawn:INV/spawn:WORK/spawn:FIX/memory/discuss/dismiss]: spawn:FIX
Priority? [P0/P1/P2/P3]: P2
```

**Exit Criteria:**
- [ ] All observations triaged with valid dimensions
- [ ] Triaged list ready for promotion

**Tools:** AskUserQuestion (for dimension selection), triage_observation()

---

### 3. PROMOTE Phase

**Goal:** Execute the action for each triaged observation.

**Action Handlers:**

| Action | Execution |
|--------|-----------|
| `spawn:INV` | Create investigation via `/new-investigation` |
| `spawn:WORK` | Create work item via `/new-work` |
| `spawn:FIX` | Create quick fix work item (priority P1) |
| `memory` | Store insight via `ingester_ingest` |
| `discuss` | Flag for operator (report but no action) |
| `dismiss` | Mark as noise (no action needed) |

**Actions:**
1. For each triaged observation, execute action
2. Track results (spawned IDs, memory IDs)
3. Update observations.md with triage log entry
4. Set triage_status: triaged in frontmatter

**Exit Criteria:**
- [ ] All actions executed
- [ ] Observations.md updated with triage log
- [ ] triage_status updated to triaged

**Tools:** /new-investigation, /new-work, ingester_ingest, Edit

---

## Composition Map

| Phase | Primary Tool | Output |
|-------|--------------|--------|
| SCAN | Bash, Read | List of pending observations |
| TRIAGE | AskUserQuestion | Triaged observation list |
| PROMOTE | /new-*, ingester | Action results |

---

## Quick Reference

| Phase | Question to Ask | If NO |
|-------|-----------------|-------|
| SCAN | Any pending observations? | Exit - nothing to triage |
| TRIAGE | All dimensions valid? | Reprompt with validation error |
| PROMOTE | Action executed? | Report error, continue to next |

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Standalone skill | Not embedded in close-work-cycle | Keeps closure lean; triage runs independently |
| Interactive triage | Agent prompts per observation | Avoids automated misclassification |
| triage_status field | In frontmatter | Enables scan to skip processed files |
| Industry dimensions | bug/gap/debt/insight/question/noise | Aligns with bug triage patterns |

---

## Related

- **E2-217:** Observation Capture Gate (capture mechanism)
- **INV-047:** Close Cycle Observation Phase Ordering (capture timing)
- **INV-023:** ReasoningBank Feedback Loop Architecture (same pattern)
- **close-work-cycle skill:** Captures observations during closure
- **observations.py:** Core functions for scan, parse, triage, promote
