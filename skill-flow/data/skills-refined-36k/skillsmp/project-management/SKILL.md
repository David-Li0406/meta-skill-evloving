---
name: project-management
description: High-level workflows for proposing, planning, and executing complex changes (OpenSpec style).
---

# Project Management (OpenSpec Style)

## When to use this skill
- Starting a large, multi-file feature.
- When the user asks to "make a plan" or "propose a solution".
- Managing scope creep or ambiguity.

## 1. The Workflow (Propose -> Plan -> Execute)
1.  **Proposal**: Before writing code, create a brief Markdown proposal (in memory or a scratchpad) outlining the *Approach*.
    *   *Why*: Ensures we solve the right problem.
    *   *Check*: Ask "Does this approach make sense?"
2.  **Plan**: Once approved, break it down into a granular checklist (like `task.md` or `current-plan.md`).
3.  **Execute**: rapid iteration on the tasks.

## 2. Managing Context
- **Memory**: Keep `memory.json` updated with the *current phase* of the project.
- **Summarization**: If the plan gets too long, summarize completed items into a single "Completed History" block.

## 3. Communication
- **Clarity**: Use "Decision: X due to Y" format when making architectural choices.
- **Blockers**: Raise blockers immediately. Do not guess.

## 4. Artifacts
- **Proposal Docs**: Save major architectural decisions to `docs/decisions/YYYY-MM-DD-feature-name.md`.
- **Status**: Keep the user informed of the *percentage complete* of the current phase.
