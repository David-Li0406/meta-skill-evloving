---
name: session-close
description: Complete the session close protocol. Runs git status, stages changes, syncs beads, commits, pushes to remote, and optionally deploys to Shopify. Use when ending a work session.
---

# Session Close

Automates the session close checklist from CLAUDE.md to ensure work is properly saved and pushed.

## Codex Notes

- Run from the repo root.
- Surface script output in your response (git status, commit, push, deploy choice).
- If the script fails, stop and report the error without retrying.

## Usage

Execute the session close script:

```bash
./scripts/session-close.sh
```

The script will:
1. Show git status (what changed during session)
2. Stage code changes (interactive confirmation)
3. Sync beads issues to git
4. Commit code changes (prompts for commit message)
5. Sync beads again (capture any changes from commit hooks)
6. Push to git remote
7. **Optional:** Prompt to deploy to Shopify live

## Session Close Protocol

This skill implements the critical session close checklist from CLAUDE.md:

```
[ ] 1. git status              (check what changed)
[ ] 2. git add <files>         (stage code changes)
[ ] 3. bd sync                 (commit beads changes)
[ ] 4. git commit -m "..."     (commit code)
[ ] 5. bd sync                 (commit any new beads changes)
[ ] 6. git push                (push to remote)
```

**NEVER skip this protocol.** Work is not done until pushed.

## When to Use This Skill

Run `/session-close` when:
- You're ending a work session
- You've completed a feature or bug fix
- You're switching to a different task
- Codex is about to compact the conversation

Do NOT use this skill if:
- You have no changes to commit (just exit the session)
- You're in the middle of debugging (finish debugging first)
- Tests are failing (fix tests first)

## Deployment Option

At the end of the session close protocol, the script will ask:

```
Deploy to Shopify now? (y/n)
```

- **Yes:** Calls `/deploy-to-shopify` skill to deploy changes to live theme
- **No:** Skips deployment (you can run `/deploy-to-shopify` manually later)

Deployment is optional because:
- You might want to test locally first
- You might be deploying multiple commits at once
- You might want Jared to review changes before they go live

## Error Handling

**If git status shows no changes:**
- Script will inform you and exit
- No action needed

**If bd sync fails:**
- Script will exit with error
- Check beads status: `bd stats`
- Report issue to Jared

**If git push fails:**
- Script will exit with error
- Likely cause: remote has changes you don't have
- Run: `git pull --rebase` then retry

**If deployment is requested:**
- The `/deploy-to-shopify` skill will run
- See that skill's documentation for deployment-specific errors

## Reporting to Jared

After successful session close, report:
- What files were changed (from git status)
- Commit message used
- Whether beads were synced
- Whether deployment was performed
- Any errors encountered

## Notes

- This skill enforces the session close protocol
- Running this at the end of every session ensures no work is lost
- The optional deployment step provides a convenient path to make changes live
- If you're unsure whether to deploy, choose "no" and ask Jared
