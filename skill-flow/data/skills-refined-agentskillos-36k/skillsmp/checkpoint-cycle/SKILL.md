---
name: checkpoint-cycle
description: Create checkpoint manifest. Scaffold, populate fields, commit.
recipes:
- checkpoint
- commit-session
- session-end
generated: 2025-12-25
last_updated: '2026-01-19T13:44:59'
---
# Checkpoint Cycle

Create a checkpoint manifest for session handoff.

## When to Use

After `/new-checkpoint` scaffolds the file, this skill guides population.

---

## What to Do

### 1. Populate the Manifest

The checkpoint is a **loading manifest**, not an activity log.

**Fields to fill:**

| Field | What to Put |
|-------|-------------|
| `load_principles` | Files next session MUST read (default: S20, S22) |
| `load_memory_refs` | Concept IDs from this session's `ingester_ingest` calls |
| `pending` | Work item IDs for next session |
| `drift_observed` | Principle violations noticed (if any) |
| `completed` | What was done (for git commit message only) |

### 2. Store Learnings

For each significant decision/learning this session:

```
ingester_ingest(
  content="<learning>",
  source_path="checkpoint:session-{N}",
  content_type_hint="techne"
)
```

Add returned concept IDs to `load_memory_refs`.

### 3. Drift Observation Gate (SHOULD)

**If `drift_observed` is non-empty**, prompt before commit:

```
Drift observed this session:
- {drift_item_1}
- {drift_item_2}

Create formal observation(s) for triage? [Y/n]
```

**If yes:** For each drift item, create observation file:
```bash
# Write to epochs/{current_epoch}/observations/obs-{session}-{n}.md
```

Use observation template:
- `id`: obs-{session}-{n}
- `triage_status`: pending
- `potential_action`: bugfix | investigation | adr | skill-update

**If no:** Proceed (agent judged drift minor, doesn't need formal tracking).

**Rationale:** Drift mentioned in checkpoint but not captured as observation gets lost. This nudge ensures drift surfaces for triage without being a hard gate.

### 5. Commit

```bash
just commit-session {session} "{title}"
just session-end {session}
```

---

## Example Completed Manifest

```yaml
---
template: checkpoint
session: 186
prior_session: 185
date: 2026-01-10

load_principles:
  - .claude/haios/epochs/E2/architecture/S20-pressure-dynamics.md

load_memory_refs:
  - 81222
  - 81248

pending:
  - E2-281
  - E2-282

drift_observed:
  - "survey-cycle is 5 phases, S20 says single-phase"

completed:
  - E2-279
---
```

---

## Key Principle

**The checkpoint is a manifest. The memory is the content. Git is the log.**

No ceremony. No exit criteria checklists. Fill the fields, store learnings, commit.
