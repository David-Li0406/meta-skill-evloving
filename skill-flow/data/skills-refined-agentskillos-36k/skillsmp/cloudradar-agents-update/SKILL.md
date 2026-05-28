---
name: cloudradar-agents-update
description: Update AGENTS.md in CloudRadar with a fully automated GitHub flow. Use when the user asks to change AGENTS.md, mentions the meta issue #55, or uses the shortcut "/agt-up". This skill edits AGENTS.md, creates a dedicated docs/agents-55-<short> branch, opens a PR referencing #55, enables auto-merge, updates the #55 changelog via gh, cleans up the branch, and syncs the current branch.
---

# CloudRadar AGENTS Update

## Overview

Apply requested changes to `AGENTS.md`, then run the automation script to handle branch creation, PR, auto-merge, meta-issue update, and cleanup.

## Workflow

1. Read the user's instructions and update `AGENTS.md` directly.
2. Run the automation script with a short summary of the changes.
3. Confirm the recap printed by the script.

## Script

Run from the repo root:

```bash
python3 skills/cloudradar-agents-update/scripts/agents_update.py \
  --summary "<short summary of the AGENTS.md change>" \
  --short "<short suffix>"
```

Notes:
- `--short` is optional. Default is UTC date `YYYYMMDD`.
- The branch format is `docs/agents-55-<short>`.
- Requires `gh` to be authenticated.
- The working tree must only have changes in `AGENTS.md`.

## Expected Output

The script prints a recap including:
- Commit id
- PR URL
- Merge commit id
- Confirmation that meta issue #55 received the changelog entry
