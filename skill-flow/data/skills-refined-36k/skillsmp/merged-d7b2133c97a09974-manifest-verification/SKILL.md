---
name: manifest-verification
description: Use this skill to orchestrate the verification of criteria from a Manifest by spawning parallel verifiers and reporting results.
---

# /verify - Manifest Verification Runner

## Goal

Orchestrate verification of all criteria from a Manifest by spawning parallel verifiers. Report results grouped by type.

## Input

`$ARGUMENTS` = "<manifest-file-path> <execution-log-path> [--scope=files]"

## Principles

1. **Orchestrate, don't verify** - Spawn agents to verify. You coordinate results, never run checks yourself.
2. **Single parallel launch** - All criteria in one call, with slow ones (tests, builds, reviewers) first, followed by fast ones (lint, typecheck).
3. **Global failures are critical** - Highlight Global Invariant failures prominently as they indicate task failure.
4. **Actionable feedback** - Provide detailed feedback including file:line, expected vs actual, and fix hints.

## Verification Methods

| Type      | What                                   |
|-----------|----------------------------------------|
| `bash`    | Shell commands (tests, lint, typecheck) |
| `subagent`| Reviewer agents                        |
| `codebase`| Code pattern checks                   |
| `manual`  | Set aside for human verification      |

## Criterion Types

| Type                | Pattern   | Failure Impact                     |
|---------------------|-----------|------------------------------------|
| Global Invariant    | INV-G{N}  | Task fails                         |
| Acceptance Criteria  | AC-{D}.{N} | Deliverable incomplete              |
| Process Guidance    | PG-{N}    | Not verified (guidance only)      |

Note: PG-* items guide HOW to work and are followed during /do but not checked by /verify.

## Outcome Handling

| Condition                               | Action                                           |
|-----------------------------------------|-------------------------------------------------|
| Any Global Invariant failed             | Return all failures, globals highlighted        |
| Any Acceptance Criteria failed          | Return failures grouped by deliverable          |
| All automated pass, manual exists      | Return manual criteria, hint to call /escalate |
| All pass                                | Call /done                                     |

## Output Format

Report verification results grouped by Global Invariants first, then by Deliverable.

**On failure** - For each failed criterion, show:
- Criterion ID and description
- Verification method
- Failure details: location, expected vs actual, fix hint

**On success with manual** - List manual criteria with how-to-verify from manifest, suggest /escalate.

**On full success** - Call `/done`.