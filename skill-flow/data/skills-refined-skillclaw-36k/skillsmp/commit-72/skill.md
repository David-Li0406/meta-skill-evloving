---
name: commit
description: "[EXPLICIT ONLY] Run ONLY when user types /commit - never automatically"
---

# Session-Aware Commit

**IMPORTANT: This skill must ONLY be invoked when the user explicitly types `/commit`. NEVER run this skill automatically after making changes, even if it seems relevant. The user handles commits manually via lazygit.**

Commits only changes from THIS session, not from other parallel Claude instances.

## Procedure

1. Review conversation to understand what files YOU edited
2. Run git diff to see all uncommitted changes
3. For each hunk, decide: is this MY change or another instance's?
4. Use git add -p to interactively stage only YOUR hunks (y/n for each)
5. Run git diff --staged to verify
6. Commit with conventional message
7. Show git status for remaining changes

## Key Rules

- NEVER use git add . or git add -A
- Be conservative - skip hunks you are unsure about
- State reasoning for each hunk decision
