---
name: event-flow-tracer
description: Traces causal execution flow while coding by reconstructing Command → Validation → Events → State → Projections from real artifacts using terminal access. Automatically used after changes to event emission, ordering, lifecycle logic, or when diagnosing stalls, missing transitions, or unexpected state outcomes.
---

# Event Flow Tracer (Time-to-Insight King)

This skill answers one question, fast:

**“What actually happened, in what order, and where did it go wrong?”**

It is designed for an agent that is **actively writing or modifying code** in an
event-sourced, tick-driven system. The tracer reconstructs **causal flow** from
real execution artifacts and pinpoints:
- where execution stalled,
- where an expected event never fired,
- where ordering changed,
- or where state diverged from intent.

The tracer:
- discovers artifacts via terminal commands,
- reconstructs ordered flows across ticks and subsystems,
- highlights gaps, stalls, and illegal branches,
- produces a minimal, navigable trace with evidence,
- writes helper scripts when repetition would slow progress.

This skill does **not** reason abstractly. It **replays reality**.

---

## When to use this skill (Agent-centric, mandatory triggers)

The agent MUST invoke this skill automatically in the following situations:

### 1. After changing event emission or ordering
Use after:
- adding a new event
- changing when an event fires
- reordering emissions within a tick
- moving logic across pre/post-tick phases

Purpose: confirm **causal ordering** still matches intent.

---

### 2. After modifying lifecycle or phase logic
Use after changes to:
- trip phase transitions
- dispatch readiness
- boarding / departure / arrival logic
- market window open/close boundaries

Purpose: ensure **expected transitions actually occur**.

---

### 3. When diagnosing stalls or freezes
Use when code changes could cause:
- ticks to stop advancing
- no new events emitted
- UI projections to stop updating

Purpose: find the **last successful causal step** and the **first missing one**.

---

### 4. When expected outcomes do not occur
Use when:
- a trip never enters a phase
- passengers are never released
- a market window resolves but no downstream effects appear
- projections show stale or partial state

Purpose: identify **where the causal chain breaks**.

---

### 5. After refactors touching control flow
Use after:
- extracting handlers
- splitting large functions
- moving logic across modules
- replacing inline logic with helpers

Purpose: detect **lost calls, reordered effects, or swallowed branches**.

---

## Operating principles (Non-negotiable)

1. **Causality over volume**
   - Prefer a small, precise trace over dumping logs.
2. **Order is everything**
   - Event order, tick order, and phase order must be explicit.
3. **Evidence only**
   - Every claim must reference concrete artifacts.
4. **First break wins**
   - The earliest missing or illegal step is the primary finding.
5. **Scripts are encouraged**
   - Write scripts when reconstructing flows repeatedly.

---

## Artifact discovery (Terminal usage is mandatory)

If artifact paths are not provided, the agent MUST locate them.

### Required discovery steps

```bash
ls
find . -maxdepth 4 -type d -name "logs" -o -name "wal" -o -name "events" -o -name "snapshots" 2>/dev/null
rg -n "dispatch|TripPhase|Boarding|EnRoute|Arrived|event" . 2>/dev/null || true
find . -type f \( -name "*.wal" -o -name "*.ndjson" -o -name "*.log" \) | head -n 50

If tests are involved (Rust example):

cargo test -q <suspect_test> -- --nocapture

Record all artifact paths for evidence references.
What the tracer reconstructs

The tracer builds an explicit causal chain:

[Command]
   ↓
[Validation / Readiness]
   ↓
[Event Emission]
   ↓
[State Mutation]
   ↓
[Derived Events]
   ↓
[Projection Updates]

For each step, the tracer answers:

    Did it occur?

    When (tick, order)?

    With what inputs?

    What came next?

    What should have come next but didn’t?

Trace dimensions (always capture)

For each trace node:

    tick

    sequence index (global or per-tick)

    entity id(s) (trip_id, route_id, market_window_id)

    source module/function (if available)

    input → output summary

    artifact reference

Common trace patterns to detect
A. Silent swallow

    Command accepted

    Validation passes

    No event emitted

B. Early abort

    Validation fails unexpectedly

    No downstream effects

C. Ordering inversion

    Event B emitted before Event A

    Phase transition precedes prerequisite event

D. Phase stall

    Last event emitted correctly

    No subsequent phase transition ever occurs

E. Projection disconnect

    Events and state update

    Projection does not reflect change

Script authoring policy (empowered)

The agent is explicitly empowered to write scripts to accelerate tracing.
Allowed scripts

    event filters (by type/entity/tick)

    causal chain reconstruction

    per-entity timelines

    missing-event detection

    trace graph generation (DOT/JSON)

Where scripts live

.agent/skills/event-flow-tracer/scripts/

Script requirements

    deterministic

    read-only by default

    supports --help

    outputs either readable text or structured JSON

    idempotent

Write a script when:

    you reconstruct the same trace more than once

    you need to compare two runs

    you are narrowing a stall point

    you are visualizing causality

Recommended default scripts

Create as needed:

    scripts/filter_events.py

    scripts/trace_entity.py

    scripts/trace_tick_window.py

    scripts/build_trace_graph.py

    scripts/diff_traces.py

Trace procedure (Step-by-step)
Step 1 — Identify the expected flow

From code intent, state explicitly:

    the command or trigger

    the expected event sequence

    the expected final state or projection

Write this down before tracing.
Step 2 — Extract the actual flow

Using logs/WAL:

    locate the triggering command

    extract all events for the relevant tick range

    filter by entity ids

If repeated, write a filter script.
Step 3 — Align expected vs actual

For each expected step:

    mark present, missing, or out-of-order

    record first divergence point

Step 4 — Identify the break

Determine:

    last successful causal node

    first missing or illegal node

This is the primary finding.
Step 5 — Emit the Event Flow Trace Report

Required output shape:

{
  "summary": {
    "status": "broken",
    "break_type": "missing_event",
    "first_break_tick": 18233,
    "entity_refs": ["trip:1234"]
  },
  "expected_flow": [
    "DispatchCommand",
    "DispatchValidated",
    "TripScheduled",
    "BoardingOpened",
    "PassengerReleased"
  ],
  "actual_flow": [
    "DispatchCommand",
    "DispatchValidated",
    "TripScheduled"
  ],
  "trace": [
    {
      "tick": 18230,
      "event": "TripScheduled",
      "source": "dispatch_logic.rs",
      "evidence_ref": "events.wal#89110"
    }
  ],
  "findings": [
    {
      "severity": "error",
      "message": "BoardingOpened was never emitted after TripScheduled",
      "evidence_refs": ["events.wal#89110-89200"],
      "remediation_hint": "Ensure boarding open is emitted during post-dispatch phase in trip_logic.rs"
    }
  ]
}

Remediation hint rules

Every error must include:

    the missing or misordered step

    the most likely control-flow location

    a concrete next inspection step

Avoid speculation. Tie hints to trace evidence.
Optional assets

.agent/skills/event-flow-tracer/
├── SKILL.md
├── scripts/
│   ├── filter_events.py
│   ├── trace_entity.py
│   ├── build_trace_graph.py
│   └── diff_traces.py
└── examples/
    └── trace_report_example.json

Final doctrine

This skill exists to compress time-to-insight.

When invariants fail, the Event Flow Tracer explains why.
When nothing crashes but nothing works, it shows where flow stopped.
When refactors subtly break behavior, it reveals what was lost.

Use it while coding, not after frustration sets in.
