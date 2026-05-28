---
name: refactor-guardian
description: Guards refactors while coding by enforcing no-behavior-change contracts, validating public API stability, and verifying deterministic behavior via real artifacts using terminal access. Automatically used during code movement, module extraction, renaming, or architectural restructuring.
---

# Refactor Guardian

This skill exists to make **refactors safe by construction**.

It is designed for an agent that is **actively modifying code structure** while
explicitly claiming *“no behavior change”*. The Refactor Guardian ensures that
this claim is **provably true**, not aspirational.

The guardian:
- validates refactor intent and scope,
- enforces refactor safety rules,
- collects real artifacts via terminal access,
- compares pre- and post-change behavior,
- blocks unsafe changes early,
- writes helper scripts when refactor checks are repetitive.

This skill does **not** optimize code.
It ensures **nothing breaks while you rearrange it**.

---

## When to use this skill (Agent-centric, mandatory triggers)

The agent MUST invoke this skill automatically in the following situations:

### 1. During module extraction or file splitting
Use when:
- breaking a large file into smaller modules
- extracting domains, helpers, or subsystems
- moving logic across directories or crates

Purpose: ensure **behavioral equivalence** is preserved.

---

### 2. When refactors claim “no behavior change”
Use whenever:
- PR intent states “pure refactor”
- comments or commit messages assert no semantic changes
- logic is moved but not rewritten

Purpose: **verify the claim**, not trust it.

---

### 3. When renaming or re-exporting APIs
Use after:
- renaming functions, types, or modules
- introducing `pub use` re-exports
- changing import paths while preserving public surface

Purpose: ensure **external callers remain unaffected**.

---

### 4. When reorganizing control flow
Use after:
- extracting helpers from inline logic
- flattening or nesting conditionals
- reordering logic for readability

Purpose: detect **subtle ordering or early-return changes**.

---

### 5. Before merging large structural changes
Use before finalizing:
- wide-impact refactors
- cross-cutting architectural cleanup
- mechanical migrations touching many files

Purpose: provide a **last-line safety net**.

---

## Operating principles (Non-negotiable)

1. **Refactors are guilty until proven innocent**
   - Assume behavior changed unless proven otherwise.

2. **Public contracts are sacred**
   - Public APIs, schemas, and persistence formats must remain stable.

3. **Evidence beats intent**
   - Trust artifacts, not comments or commit messages.

4. **Small diffs are safer**
   - Prefer many small guarded steps over one large leap.

5. **Read-only enforcement**
   - Diagnose and block. Do not “fix forward” unless explicitly asked.

6. **Scripts are encouraged**
   - Automate repetitive verification steps.

---

## Refactor safety rules (Hard constraints)

Unless explicitly overridden, the following rules MUST hold:

### R1. No behavior change
- Identical command → identical events → identical projections.
- Event ordering must not change.
- No new side effects.

### R2. No schema changes
- Event payloads unchanged.
- Snapshot formats unchanged.
- Persistence layouts unchanged.

### R3. Public API stability
- Public functions/types remain callable.
- Re-exports preserve old import paths.
- No breaking signature changes.

### R4. Determinism preserved
- Replays must match bit-for-bit (within allowed tolerances).
- No new randomness, time usage, or unordered iteration.

### R5. Build stays green at every step
- Code must compile and tests must pass incrementally.

---

## Artifact discovery (Terminal usage is mandatory)

If pre/post artifacts are not explicitly provided, the agent MUST collect them.

### Required discovery steps

```bash
ls
git status
git diff --stat
git diff

If tests are available:

cargo test -q -- --list | head -n 200
cargo test -q

If replay tooling exists:

    run baseline replay before refactor

    run candidate replay after refactor

    record artifact paths and hashes

All discovered artifacts must be referenced in findings.
Refactor validation dimensions

The guardian validates refactors across four dimensions:
A. Structural equivalence

    Logic moved but not altered.

    Control-flow shape preserved.

B. Behavioral equivalence

    Same inputs produce same events and state.

    Ordering preserved.

C. Interface equivalence

    Public APIs unchanged.

    Callers remain valid.

D. Persistence equivalence

    Stored data readable across versions.

    No migration required.

Script authoring policy (Empowered)

The agent is explicitly empowered to write scripts to automate refactor checks.
Allowed scripts

    API surface diffing

    replay artifact diffing

    event stream comparison

    snapshot schema comparison

    refactor step checklists

Where scripts live

.agent/skills/refactor-guardian/scripts/

Script requirements

    deterministic

    read-only by default

    supports --help

    idempotent

    outputs human-readable text or JSON

Write a script when:

    the same verification is repeated across steps

    comparing pre/post artifacts

    validating large API surfaces

    enforcing incremental safety

Recommended default scripts

Create as needed:

    scripts/diff_public_api.sh

    scripts/diff_event_streams.py

    scripts/diff_snapshots.py

    scripts/run_replay_pair.sh

    scripts/refactor_checklist.py

Refactor enforcement procedure (Step-by-step)
Step 1 — Declare refactor intent

Explicitly state:

    what is being moved

    what must not change

    expected unaffected callers

If intent is unclear, emit a warning and stop.
Step 2 — Capture baseline artifacts

Before refactor:

    run tests

    run replays (if applicable)

    capture hashes of key artifacts

Store references for comparison.
Step 3 — Perform refactor incrementally

Encourage:

    small, mechanical steps

    frequent checkpoints

    re-exports to preserve APIs

Step 4 — Validate post-refactor artifacts

Compare against baseline:

    build output

    tests

    event streams

    snapshots

    API surface

Step 5 — Emit the Refactor Guardian Report

Required output shape:

{
  "approved": false,
  "summary": {
    "violations": 1,
    "warnings": 0,
    "checked_rules": 5
  },
  "violations": [
    {
      "rule_id": "R1",
      "severity": "error",
      "message": "Event ordering changed after refactor",
      "evidence_refs": [
        "baseline/events.wal#120-140",
        "candidate/events.wal#118-138"
      ],
      "remediation_hint": "Restore original event emission order in extracted helper"
    }
  ],
  "checklist": [
    { "item": "Build passes", "status": "pass" },
    { "item": "Public API unchanged", "status": "pass" },
    { "item": "Replay determinism", "status": "fail" }
  ]
}

Remediation hint rules

Every violation must include:

    the violated rule (R1–R5)

    concrete evidence (diffs, hashes, line ranges)

    the most likely structural cause

    a minimal corrective action

No vague advice.
Optional assets

.agent/skills/refactor-guardian/
├── SKILL.md
├── scripts/
│   ├── diff_public_api.sh
│   ├── diff_event_streams.py
│   └── run_replay_pair.sh
└── examples/
    └── refactor_report_example.json

Final doctrine

Refactors should be mechanical, provable, and boring.

This skill ensures:

    claims of “no behavior change” are verified,

    public contracts remain intact,

    determinism is preserved,

    and large architectural cleanups are safe to attempt.

If a refactor cannot pass this guardian, it is not ready to merge.
