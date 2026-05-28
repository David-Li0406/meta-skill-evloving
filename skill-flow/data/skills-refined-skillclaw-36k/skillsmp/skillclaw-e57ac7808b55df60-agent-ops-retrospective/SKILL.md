---
name: agent-ops-retrospective
description: Use this skill when you need to capture durable learnings from a chat session and update the memory file to ensure future sessions can build on past insights.
---

# Skill body

## Goal
Ensure durable, reusable insights from this chat session are captured in `.agent/memory.md` so future sessions can resume without re-discovering them.

## Inputs
- The current chat session transcript (user + assistant messages in this session)
- `.agent/constitution.md`, `.agent/memory.md`, `.agent/focus.md`, `.agent/issues/`

## Extraction rules (strict)
Only capture *durable* items:
- confirmed workflow rules
- stable project conventions (not one-off)
- confirmed commands (but commands/boundaries belong in constitution, not memory)
- user preferences that affect future work on this repo
- corrections to previous misunderstandings
- pitfalls/gotchas discovered during implementation

Do NOT capture:
- transient task state (belongs in focus)
- speculative ideas not adopted
- secrets/tokens
- personal/sensitive data

## Placement rules (strict)
- Project-specific commands/boundaries/constraints → `.agent/constitution.md`
- Durable workflow learnings and recurring conventions → `.agent/memory.md`
- Current session status → `.agent/focus.md`
- Follow-ups and approvals needed → `.agent/issues/`

## Procedure
1) Read: constitution/memory/focus/tasks.
2) Scan the chat session for:
   - explicit corrections ("No, do X instead of Y")
   - newly confirmed commands or tools
   - newly confirmed constraints ("never refactor", "only write docs in …")
   - repeated misunderstandings (add a "pitfall to avoid")
   - preferences expressed by the user
3) Update `.agent/memory.md`:
   - append a dated subsection: `## Retrospective YYYY-MM-DD`
   - add short, atomic bullets phrased as "Do/Don't/Prefer"
   - avoid duplication with constitution (link to constitution section if needed)
4) Update focus if the retrospective reveals unresolved items.
5) Invoke `agent-ops-tasks` discovery if actionable items found.
6) Do not declare completion unless retrospective has been run.

## Issue Discovery During Retrospective
After scanning the session, invoke `agent-ops-tasks` discovery for actionable items.