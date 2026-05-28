---
name: validate-planning-inbox
description: Validate planning inbox entries against the repo template and invariants. Use when checking `planning/inbox/` files for required headings, metadata, and placeholder text compliance.
---

# Skill: validate-planning-inbox

## Purpose
Validate `planning/inbox/` entries against the inbox template structure and
basic invariants (required headings, metadata fields, placeholder text).

## When to use
- After creating or editing an inbox entry.
- Before a manual planning session to ensure inputs are well-formed.

## How to run
- Validate all inbox entries:
  - `python .codex/skills/validate-planning-inbox/validate_planning_inbox.py`
- Validate specific files:
  - `python .codex/skills/validate-planning-inbox/validate_planning_inbox.py planning/inbox/<file>.md`

## Output
- Reports errors and warnings per file.
- Exits non-zero when errors are found.

## Constraints
- Do not modify inbox files; report issues only.
