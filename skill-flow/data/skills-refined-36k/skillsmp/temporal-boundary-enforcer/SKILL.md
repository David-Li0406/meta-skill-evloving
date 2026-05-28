---
name: temporal-boundary-enforcer
description: Enforces and validates temporal and phase boundaries while coding by inspecting real event/state artifacts via terminal access. Automatically used whenever code affects time, ticks, phases, windows, or lifecycle boundaries to prevent delayed corruption and illegal cross-phase behavior.
---

# Temporal Boundary Enforcer

This skill enforces **time and phase boundaries as hard laws**, not conventions.

It is designed for an agent that is **actively writing or modifying code** in a
tick-based, phase-driven, event-sourced simulation. Many of the most dangerous
bugs do not crash the system — they **violate boundaries silently** and corrupt
future state.

The Temporal Boundary Enforcer:
- discovers execution artifacts via terminal commands,
- validates that actions occur only in allowed temporal windows,
- detects illegal “after the fact” or “too early” effects,
- identifies the earliest boundary breach,
- produces evidence-backed violations with precise remediation steps,
- writes helper scripts when boundary checks are repeated.

This skill does **not** reason abstractly about time.  
It verifies **what actually happened** against **what is allowed to happen**.

---

## When to use this skill (Agent-centric, mandatory triggers)

The agent MUST invoke this skill automatically in the following situations:

### 1. After modifying phase or lifecycle logic
Use after changes to:
- TripPhase transitions
- boarding open/close logic
- dispatch readiness windows
- arrival, completion, or cleanup logic

Purpose: ensure **no logic crosses forbidden phase boundaries**.

---

### 2. After modifying tick or scheduling logic
Use after changes to:
- per-tick update ordering
- pre-tick vs post-tick execution
- scheduled or delayed actions
- “next tick” or “after N ticks” mechanics

Purpose: ensure **time-relative actions fire only when valid**.

---

### 3. After modifying market or window-based logic
Use after changes to:
- market window open/close rules
- demand allocation timing
- backlog carryover semantics
- pricing window enforcement

Purpose: ensure **windowed logic does not leak across windows**.

---

### 4. After refactors affecting control flow
Use after:
- moving logic between modules
- extracting helpers from tick handlers
- consolidating lifecycle logic

Purpose: detect **boundary checks that were lost or reordered**.

---

### 5. Before finalizing fixes involving delayed effects
Use before concluding work on bugs involving:
- late passenger release
- actions firing after trip completion
- resources consumed after arrival
- UI state changing after backend window closed

Purpose: **prove boundary safety**, not assume it.

---

## Operating principles (Non-negotiable)

1. **Boundaries are absolute**
   - If an action occurs outside its allowed window, it is an error — even if “nothing broke yet”.

2. **Earliest breach wins**
   - The first boundary violation is the root cause, not downstream symptoms.

3. **Evidence-driven**
   - Every violation must reference concrete artifacts (event ids, log lines, snapshot fields).

4. **Deterministic reasoning only**
   - No wall-clock time, no heuristics, no guesses.

5. **Read-only discipline**
   - Diagnose and recommend. Do not modify product code unless explicitly instructed.

6. **Scripts are encouraged**
   - Write scripts when boundary checks are repeated or complex.

---

## Artifact discovery (Terminal usage is mandatory)

If artifact paths are not explicitly provided, the agent MUST locate them.

### Required discovery steps

```bash
ls
find . -maxdepth 4 -type d -name "logs" -o -name "wal" -o -name "events" -o -name "snapshots" 2>/dev/null
rg -n "TripPhase|Boarding|Closed|Opened|tick|window|phase" . 2>/dev/null || true
find . -type f \( -name "*.wal" -o -name "*.ndjson" -o -name "*.log" -o -name "*.snap" \) | head -n 50

If tests are involved:

cargo test -q <suspect_test> -- --nocapture

Record all artifact paths for evidence references.
Temporal boundary model (must be explicit)

The enforcer assumes that the simulation defines explicit boundaries, such as:

    Tick boundaries

        pre-tick

        tick

        post-tick

    Phase boundaries (example: trips)

        Scheduled

        BoardingOpen

        BoardingClosed

        EnRoute

        Arrived

        Completed

    Window boundaries (example: markets)

        MarketWindowOpen

        MarketWindowClosed

If the code does not define these explicitly, the enforcer must:

    infer them from events and state,

    and emit a warning recommending explicit boundary modeling.

Core boundary rules (enforced)
A. Phase boundaries (Trips)

    TB-TRIP-001: No passenger release outside BoardingOpen

    TB-TRIP-002: No boarding changes after BoardingClosed

    TB-TRIP-003: No phase transitions skipping required intermediates

    TB-TRIP-004: No actions on trips after Completed

B. Tick boundaries

    TB-TICK-001: State mutations must occur in allowed tick stage

    TB-TICK-002: Scheduled actions must not fire earlier than scheduled tick

    TB-TICK-003: Delayed actions must not fire after expiry window

C. Market windows

    TB-MKT-001: Demand allocation only while window open

    TB-MKT-002: Window-closed logic must not emit allocation events

    TB-MKT-003: Backlog carryover must occur exactly once per window close

D. UI / Readiness windows

    TB-UI-001: UI-visible actions must not be enabled after backend window closes

    TB-UI-002: Backend must reject commands outside allowed windows

Script authoring policy (empowered)

The agent is explicitly empowered to write scripts to accelerate boundary analysis.
Allowed scripts

    per-entity phase timelines

    per-tick action summaries

    window open/close interval extraction

    late/early action detection

    boundary violation scanners

Where scripts live

.agent/skills/temporal-boundary-enforcer/scripts/

Script requirements

    deterministic

    read-only by default

    supports --help

    idempotent

    outputs human-readable text or structured JSON

Write a script when:

    boundary checks are repeated

    multiple entities/windows must be scanned

    timing relationships are non-trivial

    results need to be compared across runs

Recommended default scripts

Create as needed:

    scripts/extract_phase_timeline.py

    scripts/extract_window_intervals.py

    scripts/scan_boundary_violations.py

    scripts/summarize_tick_actions.py

Enforcement procedure (Step-by-step)
Step 1 — Define allowed boundaries

From code intent, explicitly list:

    allowed phases/windows

    allowed actions per phase/window

    allowed tick stages for mutations

If boundaries are implicit, infer and note assumptions.
Step 2 — Extract actual timelines

Using events/snapshots:

    build phase timelines per entity

    build window open/close intervals

    map actions to ticks and phases

Use scripts if repeated.
Step 3 — Validate actions against boundaries

For each action:

    identify its phase/window/tick

    check if action is allowed there

    flag earliest illegal occurrence

Step 4 — Identify first breach

Determine:

    the earliest boundary violation

    the boundary that was crossed

    the downstream effects caused by the breach

This is the primary finding.
Step 5 — Emit the Temporal Boundary Report

Required output shape:

{
  "summary": {
    "status": "violated",
    "first_violation_tick": 18240,
    "boundary_type": "TripPhase",
    "entity_refs": ["trip:1234"]
  },
  "violations": [
    {
      "id": "TB-TRIP-001",
      "severity": "error",
      "message": "Passenger release occurred after BoardingClosed",
      "tick": 18240,
      "phase": "BoardingClosed",
      "evidence_refs": ["events.wal#89321", "logs/sim.log:4421-4430"],
      "remediation_hint": "Move passenger release logic to BoardingOpen phase or guard by TripPhase"
    }
  ]
}

Remediation hint rules

Every violation must include:

    the specific boundary crossed

    the illegal action

    the most likely missing or misplaced guard

    the concrete location to inspect next

No generic advice.
Optional assets

.agent/skills/temporal-boundary-enforcer/
├── SKILL.md
├── scripts/
│   ├── extract_phase_timeline.py
│   ├── scan_boundary_violations.py
│   └── extract_window_intervals.py
└── examples/
    └── boundary_report_example.json

Final doctrine

Temporal boundaries are where simulations rot silently.

This skill exists to ensure:

    actions happen only when allowed,

    windows and phases remain authoritative,

    delayed corruption is prevented at the source,

    and time remains a reliable axis of truth.

Use it while coding, not after damage accumulates.
