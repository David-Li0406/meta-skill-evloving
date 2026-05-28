# Agent Instructions

## ⚠️ MANDATORY: Session Start Protocol

**BEFORE doing ANYTHING else in a new session, you MUST:**

1. **Invoke the Layton skill**: `/layton` (no parameters)

**NO EXCEPTIONS** — unless the user explicitly says "skip Layton".

## Primary Entry Point: Layton

The `/layton` skill provides:

- **checks**: Status of integrations and config
- **skills**: Available data sources
- **workflows**: Available workflows with trigger phrases

Layton provides context-aware briefings and orchestrates other skills.

## Issue Tracking with Beads

This project uses **bd** (beads) for issue tracking.

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --status in_progress  # Claim work
bd close <id>         # Complete work
bd sync               # Sync with git
```

## Session Completion (Landing the Plane)

**When ending a work session**, complete ALL steps:

1. **File issues** for remaining work
2. **Update issue status** - Close finished, update in-progress
3. **PUSH TO REMOTE** (MANDATORY):

   ```bash
   git pull --rebase && bd sync && git push
   git status  # MUST show "up to date with origin"
   ```

4. **Hand off** - Provide context for next session

## Critical Rules

- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
