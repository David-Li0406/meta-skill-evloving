---
name: manifest-verification
description: Use this skill to orchestrate the verification of criteria from a Manifest by spawning parallel verifiers and reporting results.
---

# /verify - Manifest Verification Runner

## Goal

Orchestrate the verification of all criteria from a Manifest by spawning parallel verifiers. Report results grouped by type.

## Input

`$ARGUMENTS` = "<manifest-file-path> <execution-log-path> [--scope=files]"

## Principles

1. **Orchestrate, don't verify** - Spawn agents to verify. You coordinate results, never run checks yourself.
2. **Single parallel launch** - All criteria in one call, with slow ones (tests, builds, reviewers) first, followed by fast ones (lint, typecheck).
3. **Global failures are critical** - Highlight Global Invariant failures prominently, as they indicate task failure.
4. **Actionable feedback** - Provide detailed feedback including file:line, expected vs actual, and fix hints.

## Verification Methods

| Type       | What                                   |
|------------|----------------------------------------|
| `bash`     | Shell commands (tests, lint, typecheck) |
| `subagent` | Reviewer agents                        |
| `codebase` | Code pattern checks                   |
| `manual`   | Set aside for human verification      |

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

**On failure:**
```markdown
## Verification Results

### Global Invariants

#### Failed (N)
- **INV-G1**: [description]
  Method: [method]
  [failure details with location, expected/actual, fix hint]

#### Passed (M)
- INV-G2, INV-G3

---

### Deliverable 1: [Name]

#### Failed
- **AC-1.2**: [description]
  [failure details]

#### Passed
- AC-1.1

---

**Summary:**
- Global Invariants: X/Y failed (fix first)
- Deliverable 1: A/B ACs failed
```

**On success with manual:**
```markdown
## Verification Results

All automated criteria pass.

### Manual Verification Required
- **AC-1.3**: [description] - How to verify: [from manifest]

Call /escalate to surface for human review.
```

**On full success:**
Call `/done`.