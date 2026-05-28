---
name: test-isolation-slot-hygiene
description: Enforces clean-room test execution while coding by detecting and eliminating leaked state (saved slots, snapshots, caches, temp dirs) using terminal access. Automatically used when writing/modifying simulation tests, diagnosing flakiness, or changing persistence/replay logic. Supports authoring helper scripts to standardize isolation.
---

# Test Isolation & Slot Hygiene (Velocity Protector)

This skill exists to ensure **tests mean what they claim**.

In a simulation project with persistence, snapshots, WAL, and slots, flakiness is
often caused by **state leakage**, not “randomness.” If tests are not isolated:
- green builds become untrustworthy,
- debugging becomes wasted effort,
- regressions hide in noise.

This skill:
- detects leaked state between runs (slots/snapshots/caches),
- forces clean-room execution,
- standardizes where artifacts live,
- proves repeatability by running tests multiple times,
- writes helper scripts to automate hygiene.

This skill does **not** “make tests pass.”  
It makes tests **valid**.

---

## When to use this skill (Agent-centric, mandatory triggers)

The agent MUST invoke this skill automatically in the following situations:

### 1) After writing or modifying tests
Use after changes to:
- integration tests involving ticks, trips, markets, or persistence
- tests that create or reuse slots/snapshots
- tests that depend on time windows or ordering

Purpose: ensure tests are **clean-room** and **repeatable**.

---

### 2) When investigating flaky tests
Use whenever a test:
- passes sometimes and fails other times
- fails only in CI or only locally
- depends on test execution order

Purpose: determine whether flakiness is:
- leaked state,
- nondeterminism,
- or fragile assertions.

---

### 3) After modifying persistence, replay, snapshotting, or slot registry
Use after changes to:
- WAL writing/reading
- snapshot format or location
- recovery pipelines
- slot registry/selection logic

Purpose: prevent **cross-run contamination** and invisible coupling.

---

### 4) Before finalizing fixes that touch global/static state
Use when edits touch:
- global caches
- singleton registries
- lazy static initialization
- environment-derived behavior

Purpose: ensure tests don’t rely on hidden shared state.

---

## Operating principles (Non-negotiable)

1. **Clean-room or it doesn’t count**
   - A test that reuses state without declaring it is invalid.

2. **Artifacts must be explicit**
   - Every run must declare where it writes outputs (slots, logs, snapshots).

3. **Isolation first, determinism second**
   - Prove isolation (no leaked inputs) before diagnosing nondeterminism.

4. **Never “fix” flakiness by retries**
   - Retrying hides bugs. Root-cause the leak or nondeterminism.

5. **Terminal evidence required**
   - Claims must be backed by file paths, timestamps, diffs.

6. **Scripts are encouraged**
   - Automate repeated cleanup and run patterns.

---

# What “slot hygiene” means

A “slot” is any persisted simulation state carrier across runs (explicit or implicit), including:
- snapshot directories
- WAL files
- DB files
- registry entries
- temp worlds written to disk

Slot hygiene ensures tests:
- create fresh slots when required,
- never collide on default paths,
- never reuse stale state unless explicitly intended.

---

# Artifact discovery (Terminal usage is mandatory)

If the repo’s artifact locations aren’t provided, the agent MUST locate them.

### Required discovery steps

```bash
ls
find . -maxdepth 5 -type d -name "slots" -o -name "snapshots" -o -name "wal" -o -name "target" -o -name "tmp" -o -name ".cache" 2>/dev/null
find . -type f \( -name "*.wal" -o -name "*.snap" -o -name "*.db" -o -name "*.sqlite" -o -name "*.ndjson" -o -name "*.log" \) | head -n 80
rg -n "slot|snapshot|wal|persist|replay|registry|tempdir" . 2>/dev/null || true

If Rust:

cargo test -q -- --list | head -n 200

Isolation failure modes (what to detect)
IF-001: Default-path collisions

Multiple tests write to the same default slot/snapshot directory.
IF-002: Stale slot reuse

A test run starts with existing artifacts (prior events/snapshots).
IF-003: Global cache leaks

Static/global caches persist across tests within the same process.
IF-004: Environment leakage

Tests depend on env vars, working directory, locale, or time.
IF-005: Parallelism hazards

Parallel test execution causes races on shared paths/resources.
IF-006: Non-hermetic external dependencies

Network, filesystem outside temp dirs, or OS-dependent state.
Script authoring policy (Empowered)

The agent is explicitly empowered to write scripts to standardize isolation.
Allowed scripts

    clean artifact directories safely

    allocate unique per-run slot directories

    run tests N times and collect artifacts

    detect collisions and stale reuse

    generate a hygiene report JSON

Where scripts live

.agent/skills/test-isolation-slot-hygiene/scripts/

Script requirements

    deterministic

    read-only by default (cleanup requires explicit --clean)

    supports --help

    idempotent

    never deletes outside approved directories

    prints what it will delete before deleting

Write a script when:

    cleanup is repeated

    multi-run testing is required

    identifying collisions needs automation

    CI needs a standardized hygiene step

Recommended default scripts

Create as needed:

    scripts/find_persist_artifacts.sh

    scripts/alloc_run_dir.sh

    scripts/run_test_n_times.sh

    scripts/scan_for_collisions.py

    scripts/clean_artifacts.sh

    scripts/hygiene_report.py

Enforcement procedure (Step-by-step)
Step 1 — Choose target tests and define isolation contract

For each target test:

    Is it supposed to run on a fresh world?

    Is slot reuse allowed (golden replay tests), or forbidden?

If not explicit, assume fresh world required and flag missing contract.
Step 2 — Run the test once and capture artifacts

Run with full output:

cargo test -q <test_name> -- --nocapture

Record:

    paths written

    slot ids used

    snapshot/WAL locations

    timestamps (mtime) of key files

Step 3 — Run again without cleaning

Run the same test again immediately.

If outputs differ or new run reads prior artifacts, isolate why:

    stale file present

    registry selects old slot

    default dir reused

This is the core proof step.
Step 4 — Force a clean-room run

Implement one of these isolation strategies (prefer in order):
Strategy A: Unique per-run artifact root (best)

Set an env var or CLI flag to redirect all persistence outputs to:

    ./.agent/artifacts/test_runs/<test_name>/<run_id>/

Strategy B: Temp directory per test

Use OS temp dirs via test harness (tempfile, etc.) and pass paths into sim init.
Strategy C: Disable parallelism for affected tests

If collisions occur and cannot be fixed immediately:

    run with -- --test-threads=1 for those suites (temporary mitigation only).

Strategy D: Explicit slot creation

Add a helper that creates a new unsaved slot per test, and asserts it’s empty.
Step 5 — Scan for collisions and stale reuse

Use terminal and/or scripts to detect:

    multiple runs writing same path

    pre-existing WAL/snapshots before test begins

    non-empty slot directories at test start

Step 6 — Emit the Hygiene Report (required)

Required output shape:

{
  "isolated": false,
  "summary": {
    "test_name": "test_ui_driven_trip_validation",
    "runs": 3,
    "collisions_detected": 1,
    "stale_reuse_detected": 1
  },
  "findings": [
    {
      "id": "IF-002",
      "severity": "error",
      "message": "Test run reused an existing slot directory containing prior WAL events",
      "evidence_refs": [
        "slots/slot_0007/events.wal (mtime pre-run)",
        "logs/test.log:120-160"
      ],
      "remediation_hint": "Create a unique per-run slot path or force new unsaved slot creation at test setup"
    }
  ],
  "plan": {
    "actions": [
      {
        "id": "A1",
        "description": "Introduce TEST_ARTIFACT_ROOT and route all snapshot/WAL outputs under it per test run",
        "risk": "low"
      },
      {
        "id": "A2",
        "description": "Add assertion: slot must be empty at test start; fail fast if not",
        "risk": "low"
      }
    ]
  }
}

Remediation guidance (concrete patterns)
Pattern 1: Enforce per-test artifact roots

    Add a test harness utility:

        creates a unique directory (UUID or monotonic counter)

        passes it into sim initialization

        ensures cleanup occurs after

Pattern 2: Slot registry hardening

    Add API: create_new_unsaved_slot() for tests

    Ensure tests never call “open_latest_slot” or “open_default_slot”

Pattern 3: Fail-fast contamination checks

At test start:

    assert no WAL exists

    assert snapshot dir empty

    assert slot metadata indicates new world

Pattern 4: Control parallelism precisely

    If tests touch global disk paths, they must not run in parallel until fixed.

Optional assets

.agent/skills/test-isolation-slot-hygiene/
├── SKILL.md
├── scripts/
│   ├── run_test_n_times.sh
│   ├── scan_for_collisions.py
│   └── clean_artifacts.sh
└── examples/
    └── hygiene_report_example.json

Final doctrine

You can’t ship a simulation if the tests lie.

This skill ensures:

    every run starts clean when it should,

    artifacts are isolated and inspectable,

    failures are meaningful,

    and CI becomes a signal, not noise.

Use it while coding, especially when touching persistence, replay, or lifecycle logic.
