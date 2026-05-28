---
name: agent-ops-constitution
description: Use this skill when commands, boundaries, and constraints must be confirmed before baseline or code changes. Draft the initial constitution from repository evidence, then conduct user interviews to finalize it.
---

# Constitution workflow (mandatory before baseline)

## Goal
Make `.agent/constitution.md` baseline-ready by confirming:
- allowed/restricted/forbidden work areas
- single-line build/lint/test/format commands
- environment assumptions
- project-specific constraints
- issue-first workflow expectations

## Pre-requisite: Context Map

**Before starting the constitution interview, ensure a context map exists:**

1) Check if `.agent/map.md` exists.
2) If NO map exists:
   ```
   📍 No context map found. Creating one first to inform constitution questions...
   ```
   → Invoke `agent-ops-context-map` to generate `.agent/map.md`.
3) If the map exists but is stale (>30 days old or significant changes detected):
   ```
   📍 Context map may be outdated. Refresh? [Y]es / [N]o
   ```
4) Use the map to:
   - Pre-populate candidate work areas
   - Identify build/test tooling
   - Understand project structure for interview questions

## Procedure
1) **Ensure context map exists** (see above).
2) **Run tool detection** — invoke `agent-ops-tools` or `aoc tools scan --save`.
   - Creates `.agent/tools.json` with available development tools.
   - Identifies missing recommended tools based on detected project type.
   - Populates "Available tools" section in the constitution.
3) Inspect repository evidence (README, CI workflows, package/build files). Do not guess.
4) Draft v0 constitution:
   - Every inferred item must cite its evidence ("CANDIDATE from <path>").
   - Anything without evidence is marked as `TODO` + `UNCONFIRMED`.
   - Use detected tools to suggest build/lint/test commands.
5) Interview the user:
   - One question per TODO/UNCONFIRMED item.
   - Ask both "what should it be?" and "why?"
6) Update the constitution until:
   - Build + test commands are **CONFIRMED**.
   - Work boundaries are **CONFIRMED**.
7) Use `agent-ops-state` to update `.agent/focus.md`.
8) Invoke `agent-ops-tasks` for any setup work discovered.

## Issue Discovery During Constitution

**After constitution setup, invoke `agent-ops-tasks` discovery:**

1) **Collect setup items discovered:**
   - Missing configuration → `CHORE` issue.
   - Blockers → `BLOCKER` issue.
   - Any other relevant issues to be documented.