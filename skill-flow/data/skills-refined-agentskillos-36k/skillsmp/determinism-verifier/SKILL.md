---
name: determinism-verifier
description: Verifies deterministic simulation behavior while coding by running repeatable replays/tests via terminal access and diffing event streams, snapshots, and projections. Automatically used after changes to simulation logic, event ordering, persistence, scheduling, or any flaky test/replay divergence.
---

# Determinism Verifier

This skill proves whether the simulation is **deterministic**.

In an event-sourced, tick-driven simulation, determinism is not a nice-to-have:
- replay must reproduce identical outputs,
- snapshots must be stable,
- tests must be trustworthy,
- UI prediction must align with backend outcomes.

This skill:
- runs repeated executions (tests, replays, scenario runs),
- captures comparable artifacts (events, snapshots, projections, hashes),
- diffs them deterministically,
- identifies the first divergence tick/event,
- classifies likely root causes (with evidence),
- writes helper scripts to automate repeat runs and diffs.

This skill does **not** “try again until it passes.”  
It explains *why* it diverges.

---

## When to use this skill (Agent-centric, mandatory triggers)

The agent MUST invoke this skill automatically in the following situations:

### 1) After changing simulation semantics or ordering
Use after edits to:
- tick lifecycle stages (pre/post tick)
- trip lifecycle / phase transitions
- passenger release / boarding logic
- market resolver / allocation logic
- refueling, fuel burn, cash accounting

Purpose: prove **same inputs → same outputs**.

---

### 2) After adding/modifying events or persistence formats
Use after:
- adding new events
- changing event payload semantics
- changing emission order
- changing snapshot/WAL writing logic
- changing recovery/replay logic

Purpose: ensure **replay equivalence** and **format stability**.

---

### 3) After refactors claiming “no behavior change”
Use when reorganizing code:
- module extraction
- moving logic to helpers
- altering iteration constructs

Purpose: catch nondeterminism introduced by:
- unordered iteration
- floating point drift
- hidden randomness
- time usage

---

### 4) After observing flaky tests
Use when tests:
- pass sometimes, fail sometimes
- depend on order
- behave differently across machines

Purpose: determine whether flakiness is:
- nondeterminism,
- state leakage,
- or fragile assertions.

---

### 5) Before finalizing any bug fix in simulation core
Purpose: ensure the fix doesn’t “work by accident” in one run.

---

## Operating principles (Non-negotiable)

1. **Repeat identical inputs**
   - Use the same seed, same scenario, same command stream, same slot (unless testing slot isolation).
2. **Compare canonical artifacts**
   - Prefer event streams + snapshot hashes over logs.
3. **Deterministic diffing**
   - Normalize ordering and ignore non-semantic metadata when configured.
4. **First divergence wins**
   - Identify earliest tick/event index where outputs differ.
5. **Evidence-driven root cause classification**
   - Suspected causes must be tied to observed differences.
6. **Scripts are encouraged**
   - Automate repeat runs, artifact capture, and diffs.

---

# Artifact discovery and execution (Terminal usage is mandatory)

If the project already has replay tools, use them.
If not, use the most stable “scenario runner” available (tests, integration harness).

### Step 0 — Discover how to run deterministic workloads

```bash
ls
rg -n "replay|snapshot|wal|event log|slot" . 2>/dev/null || true
cargo test -q -- --list | head -n 200 || true

Look for:

    “replay” CLI commands

    “export events” tooling

    snapshot output paths

    slot registries

If you can’t find a replay runner, fall back to:

    a stable integration test that exercises lifecycle,

    or a minimal scenario test harness.

What to compare (priority order)
Tier 1 (best)

    Event stream (WAL / ndjson) exact match

    Snapshot hashes exact match

Tier 2

    Projection outputs (serialized DTOs)

    Deterministic checksums emitted by sim (if available)

Tier 3 (last resort)

    Log text (only after normalization; logs are noisy)

Determinism test matrix (how to run)

The verifier uses a simple matrix: run the same workload multiple times and compare.
Minimum requirement

    Run A and Run B with identical inputs.

    Compare artifacts.

    If mismatch, find first divergence.

Recommended

    Run A, B, C (three runs) to avoid “A vs B fluke” and triangulate stability.

Script authoring policy (Empowered)

The agent is explicitly empowered to write scripts to speed up repeat runs and diffs.
Allowed scripts

    run a workload N times and capture artifacts

    canonicalize event streams

    diff event streams and report first divergence

    hash snapshots/projections

    produce a determinism report JSON

Where scripts live

.agent/skills/determinism-verifier/scripts/

Script requirements

    deterministic

    read-only by default

    supports --help

    idempotent

    minimal dependencies (bash + python3 + jq if available)

Write a script when:

    you need more than two runs

    diffs must be repeated after code edits

    comparing artifact directories repeatedly

Recommended default scripts

Create as needed:

    scripts/run_n_times.sh

    scripts/canonicalize_events.py

    scripts/diff_events.py

    scripts/hash_artifacts.sh

    scripts/determinism_report.py

Canonicalization rules (to prevent false positives)

Before diffing, normalize where appropriate:
Allowed ignore fields (only if clearly non-semantic)

    timestamps

    hostnames

    absolute file paths

    debug-only IDs that are not persisted

Do NOT ignore:

    event ordering

    tick numbers

    entity IDs (trip_id, bus_id) if they affect persistence or gameplay

    quantities (cash, fuel, passenger counts)

Ordering normalization

If events are emitted from unordered collections:

    do not sort events globally (that hides bugs)

    instead, detect and report the unordered origin as a suspected cause

You may sort only where the data is explicitly defined as a set (e.g., candidate lists) and the system intends determinism.
Divergence localization (required)

When artifacts differ, the verifier must compute:

    first_divergence_tick (if derivable)

    first_divergence_event_index

    first_divergence_event_type

    entity_refs involved

This is the anchor for remediation.
Root-cause classification (evidence-based)

When divergence is found, classify likely causes using observed patterns:
1) Unordered iteration

Signs:

    event order differs but contents are similar

    differences appear in lists/maps
    Evidence:

    diff shows same items in different order

2) Hidden randomness

Signs:

    event payload values differ (e.g., selection choice) across runs
    Evidence:

    random-looking IDs or selections change

3) Wall-clock / external dependency

Signs:

    timestamps or time-derived behavior leaks into logic
    Evidence:

    payload contains “now” or time-based branching

4) Floating point drift

Signs:

    small numeric differences accumulate over ticks
    Evidence:

    divergence grows gradually; values differ by small epsilons

5) State leakage (not true nondeterminism)

Signs:

    run B starts with extra prior events/snapshots
    Evidence:

    artifact directories differ before execution

If state leakage is suspected, reference the Test Isolation / Slot Hygiene skill.
Determinism verification procedure (Step-by-step)
Step 1 — Choose the workload

Prefer one of:

    replay a fixed command/event stream

    run a deterministic integration test

    run a scenario runner with fixed seed

Record the exact command used.
Step 2 — Run repeated executions

Run at least two times (A and B). Capture:

    event stream outputs

    snapshots

    projections (if available)

    hashes

Store artifacts in:

    ./.agent/artifacts/determinism/<run_id>/... (recommended)
    or the repo’s standard artifact folder.

Step 3 — Canonicalize and diff

    Canonicalize only non-semantic noise

    Diff event streams first

    Then snapshots

    Then projections

Locate first divergence.
Step 4 — Emit the Determinism Report (required)

Required output shape:

{
  "deterministic": false,
  "workload": {
    "command": "cargo test -q test_ui_driven_trip_validation -- --nocapture",
    "runs": ["A", "B"]
  },
  "summary": {
    "diff_count": 3,
    "first_divergence": {
      "kind": "events",
      "tick": 18233,
      "event_index": 89110,
      "event_type": "TripScheduled"
    }
  },
  "diffs": [
    {
      "kind": "events",
      "severity": "error",
      "message": "Event ordering differs at index 89110",
      "baseline_ref": "artifacts/determinism/A/events.wal#89110",
      "candidate_ref": "artifacts/determinism/B/events.wal#89110",
      "suspected_cause": "unordered_iteration",
      "remediation_hint": "Sort candidates deterministically before emitting selection event"
    }
  ]
}

Remediation hint rules

Every error diff must include:

    suspected cause category (from classification above)

    concrete next step

    the most likely code location (module/function) based on event type and context

No generic advice.
Optional assets

.agent/skills/determinism-verifier/
├── SKILL.md
├── scripts/
│   ├── run_n_times.sh
│   ├── canonicalize_events.py
│   ├── diff_events.py
│   └── hash_artifacts.sh
└── examples/
    └── determinism_report_example.json

Final doctrine

A simulation without determinism becomes un-debuggable, un-testable, and un-balanceable.

This skill exists to ensure:

    replays are trustworthy,

    tests are meaningful,

    refactors are safe,

    and the system’s time axis remains a stable foundation.

Use it while coding, not after users discover chaos.

