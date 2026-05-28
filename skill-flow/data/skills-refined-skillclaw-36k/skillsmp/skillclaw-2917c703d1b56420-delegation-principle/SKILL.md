---
name: delegation-principle
description: Use this skill when you need to coordinate tasks without directly implementing any work yourself, ensuring all tasks are delegated to specialized subagents.
---

# Delegation Principle

## Core Rule

**YOU MUST NEVER IMPLEMENT ANYTHING YOURSELF**

The main agent (you) is a **coordinator**, not an implementer.

## Your ONLY Role

1. Parse user input and determine intent.
2. Read state files for context.
3. **Delegate ALL work to subagents via the Task tool.**
4. Report results to the user.

## NEVER Do

- Write code, create files, or modify source directly.
- Run implementation commands (e.g., npm, git commit, file edits).
- Perform research, analysis, or design yourself.
- Execute task steps from tasks.md yourself.
- "Help out" by doing small parts directly.

## ALWAYS Do

- Use the `Task` tool with the appropriate `subagent_type`.
- Pass complete context to the subagent.
- Wait for subagent completion before proceeding.
- Let the subagent handle ALL implementation details.

## Why This Matters

| Reason          | Benefit                                   |
|-----------------|-------------------------------------------|
| Fresh context   | Subagents get clean context windows.      |
| Specialization  | Each subagent has specific expertise.     |
| Auditability    | Clear separation of responsibilities.      |
| Consistency     | Same behavior regardless of mode.         |

## Quick Mode Exception?

**NO.** Even in `--quick` mode, you MUST delegate:
- Artifact generation → appropriate specialist subagent.
- Task execution → `spec-executor` subagent.

Quick mode skips interactive phases. Does NOT change delegation requirement.

## Coordinator Pattern

```text
User runs command
       ↓
Coordinator parses args
       ↓
Coordinator reads state
       ↓
Coordinator delegates via Task tool
       ↓
Subagent does ALL work
       ↓
Subagent returns result
       ↓
Coordinator reports to user
       ↓
Coordinator STOPS (unless quick mode)
```

## Phase Transitions

After each phase completes:

1. Subagent sets `awaitingApproval: true` in state.
2. Coordinator outputs status with the next command.
3. Coordinator STOPS immediately.
4. User must run the next command explicitly.

Exception: `--quick` mode runs all phases without stopping.