---
name: skill-creator
description: "Create and optimize Agent skills interactively. Activate when user wants to create a new skill, write a SKILL.md, or mentions skill creation/optimization."
---

# Skill Creator

Interactive skill creation and optimization with a research-first workflow.

## Workflow (Summary)

1. Research: use `general` subagent + scan local skills; best practices override local patterns.
2. Discovery: ask for skill name, triggers, tools, and file structure.
3. Design: draft structure, present options, iterate with the user.
4. Validation: run checklist, confirm improvements before applying.
5. Context: delegate heavy work to `general` subagent.

## Guardrails

- Never skip research.
- Ask, don't assume.
- Best practices > local patterns.
- Confirm suggested improvements before applying.

## References

- [reference.md](reference.md) - Full workflow, checklists, and formats
