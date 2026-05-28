---
name: executing-plans
description: Execute implementation plans step-by-step with quality guardrails (ask when unclear, minimal-change bias, readability checklist, verification). Use when the user asks to execute or follow a plan, run tasks sequentially from a plan file (e.g., docs/plans/*.md), or continue plan steps.
---

# Executing Plans

## Overview

Execute an existing plan task-by-task with strong clarity, minimal change, and verification. The plan is the source of truth; do not improvise or refactor beyond it without asking.

## Quick Start

- **Announce:** "I'm using the executing-plans skill to run the plan."
- **Locate plan:** Use the provided file path or inline plan text; ask if missing.
- **Confirm start:** Ask which task to begin with if not explicit.

## Execution Workflow

### Pre-flight

- Read the target plan section.
- Identify any unclear items (missing files, ambiguous commands, unclear intent).
- Ask a single, precise question if anything is unclear. Do not guess.

### Task Loop (for each Task N)

- Restate the step goal in plain language.
- Open/inspect only the files listed in the task.
- Follow the plan steps in order (test → run → implement → run → checklist).
- Use minimal changes to satisfy the step; avoid refactors unless explicitly required.
- If a new file or modification seems necessary but not listed, ask first.

### Ambiguity Rule

- Ask whenever something is unclear, regardless of the step.
- Ask one question at a time with concrete options when possible.

### Minimal-Change Bias

- Preserve existing style, structure, and formatting.
- Touch only the files listed in the task.
- Avoid reformatting or cleanup unless the plan says so.

### Readability/Style Checklist (after each task or file edit)

- **Naming:** Clear, explicit names; no ambiguity.
- **Structure:** Minimal and localized; no unnecessary nesting or indirection.
- **Readability:** Intent is obvious to a new reader.
- **Errors:** Failure modes are explicit; no silent failure unless intended.
- **Consistency:** Matches existing patterns in the file.
- **Docs/Comments:** Add only if intent is not obvious from code.

If the checklist suggests changes beyond the plan, ask before doing them.

### Verification and Failures

- Run the exact commands specified in the plan when possible.
- Do not claim completion without verification.
- If tests fail or behavior is unexpected, switch to the systematic-debugging skill (if available).
- If verification is blocked (permissions or environment), explain and ask for next steps.

### Reporting and Progress

- After each task: summarize changes with file paths and tests run (plus results).
- Ask to proceed to the next task.
