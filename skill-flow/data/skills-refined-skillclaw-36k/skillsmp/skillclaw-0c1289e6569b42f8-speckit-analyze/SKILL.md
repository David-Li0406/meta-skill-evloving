---
name: speckit-analyze
description: Use this skill when you need to perform a non-destructive consistency and quality analysis across `spec.md`, `plan.md`, and `tasks.md` after task generation.
---

# Skill body

## Inputs

- Paths to `spec.md`, `plan.md`, and `tasks.md`
- Path to `.specify/memory/constitution.md`
- Any user concerns or focus areas from the request

## Goal

Identify inconsistencies, duplications, ambiguities, and underspecified items across the three core artifacts (`spec.md`, `plan.md`, `tasks.md`) before implementation. This skill MUST run only after a complete `tasks.md` exists (typically after `speckit-tasks`).

## Operating Constraints

- **STRICTLY READ-ONLY**: Do **not** modify any files. Output a structured analysis report. Offer an optional remediation plan (user must explicitly approve before any follow-up edits are performed manually).
- **Constitution Authority**: The project constitution (`.specify/memory/constitution.md`) is **non-negotiable** within this analysis scope. Constitution conflicts are automatically CRITICAL and require adjustment of the spec, plan, or tasks—not dilution, reinterpretation, or silent ignoring of the principle.

## Execution Steps

### 1. Initialize Analysis Context

Run the following command from the repo root to check prerequisites:

```bash
.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
```

Parse the JSON output for `FEATURE_DIR` and `AVAILABLE_DOCS`. Derive absolute paths:

- `SPEC = FEATURE_DIR/spec.md`
- `PLAN = FEATURE_DIR/plan.md`
- `TASKS = FEATURE_DIR/tasks.md`

Abort with an error message if any required file is missing (instruct the user to run the missing prerequisite skill or script).

### 2. Load Artifacts (Progressive Disclosure)

Load only the minimal necessary context from each artifact:

**From `spec.md`:**
- Overview/Context
- Functional Requirements
- Non-Functional Requirements
- User Stories
- Edge Cases (if present)

**From `plan.md`:**
- Architecture/stack choices
- Data Model references
- Phases
- Technical constraints

**From `tasks.md`:**
- Task IDs
- Descriptions
- Phase grouping
- Parallel markers [P]
- Referenced file paths

**From constitution:**
- Load `.specify/memory/constitution.md` for principle validation.

### 3. Build Semantic Models

Create internal representations based on the loaded artifacts to facilitate the analysis.

### 4. Analyze Artifacts

- Identify inconsistencies, duplications, ambiguities, and underspecified items across the loaded artifacts.
- Validate alignment with project principles as defined in the constitution.

### 5. Generate Report

Output a structured analysis report detailing findings and any recommended remediation steps, pending user approval.