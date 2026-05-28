# Copilot CLI prompt templates (RPI-V)

These are copy/paste starters designed for Copilot CLI (interactive), not Claude Code.

## Phase 1 — Research

```
You are working in the mjr.wtf repo.

TASK (high level): <one sentence>

Research questions:
1) Where is the current implementation for <X>?
2) What patterns should we follow (architecture, naming, error handling)?
3) What tests cover this area today, and what new tests will be needed?

Constraints:
- Do not propose code changes yet.
- Provide file paths + line numbers.
- Call out any "must-run" commands (e.g. sqlc generate, make generate).

Output:
- A short summary
- A bulleted list of relevant files with why they matter
- Open questions / unknowns
```

## Phase 2 — Plan

```
Using this research doc:
@thoughts/shared/research/<file>.md

Create a phased implementation plan (Phase 1..N) that:
- Lists exact files to edit per phase
- Includes automated verification commands per phase
- Includes manual verification checklist per phase (if any)
- Has clear success criteria

Stop after producing the plan (no code changes yet).
```

## Phase 3 — Implement (single phase)

```
Implement ONLY Phase <N> from this plan:
@thoughts/shared/plans/<file>.md

Rules:
- Make minimal changes.
- Follow repo architecture + instructions.
- Run the phase's automated verification commands.
- When done, summarize changes and list any follow-ups needed before the next phase.
```

## Phase 4 — Validate

```
Validate the implementation against this plan:
@thoughts/shared/plans/<file>.md

I implemented: Phase <list>

Please:
1) Compare the diff to the plan and note any deviations.
2) Run/verify the automated checks.
3) Produce a validation report with a pass/fail checklist.
```
