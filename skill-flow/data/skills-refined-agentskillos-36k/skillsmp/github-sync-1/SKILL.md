---
name: github-sync
description: Automatically sync with GitHub at session start and remind Claude to push/pull changes as it works. Triggers on session start, reactivation, or when working in git repositories.
---

# github-sync - Session Git Synchronization

Ensures Claude Code sessions stay synchronized with GitHub, preventing lost work and merge conflicts across machines.

## When to Use This Skill

**AUTOMATICALLY TRIGGER** once per day at session start:
- The script self-limits to once every 24 hours
- Use `--force` flag to bypass the daily limit
- After completing a significant milestone (use --force)

## Session Start Routine

**At session start**, run this check (auto-skips if already run today):

```bash
# Quick git health check - automatically finds all repos in ~/
# The actual script scans for .git directories up to 4 levels deep
for dir in $(find ~ -maxdepth 4 -name ".git" -type d | xargs dirname); do
  if [ -d "$dir/.git" ]; then
    echo "=== Git status for $dir ==="
    cd "$dir"
    git fetch origin 2>/dev/null

    # Check for uncommitted changes
    if [ -n "$(git status --porcelain)" ]; then
      echo "WARNING: Uncommitted changes detected"
      git status --short
    fi

    # Check for unpushed commits
    UNPUSHED=$(git log origin/main..HEAD --oneline 2>/dev/null | wc -l | tr -d ' ')
    if [ "$UNPUSHED" != "0" ]; then
      echo "WARNING: $UNPUSHED unpushed commit(s)"
    fi

    # Check if behind remote
    BEHIND=$(git log HEAD..origin/main --oneline 2>/dev/null | wc -l | tr -d ' ')
    if [ "$BEHIND" != "0" ]; then
      echo "NOTICE: $BEHIND commit(s) to pull from remote"
    fi
  fi
done
```

## What to Do Based on Status

### If behind remote:
```bash
git pull origin main
```
Tell user: "Pulled X new commits from GitHub."

### If uncommitted changes exist:
Ask user: "There are uncommitted changes from a previous session. Should I commit them or review first?"

### If unpushed commits exist:
Ask user: "You have X commits that haven't been pushed to GitHub. Push now?"

### If everything is clean:
Silently proceed with the session (don't mention git is clean unless asked).

## Ongoing Work Reminders

### While Working in a Git Repository

**After completing a significant piece of work:**
1. Run `git status` to see changes
2. Suggest committing with a descriptive message
3. Ask if user wants to push

**Significant milestones include:**
- Completing a feature
- Fixing a bug
- Finishing a refactor
- Creating a new skill or command
- Any work that took >15 minutes

### Before Ending a Session

If the user says goodbye, ends work, or the conversation seems to be concluding:
1. Check for uncommitted changes
2. Check for unpushed commits
3. Remind user: "Don't forget to push your changes to GitHub if you haven't already."

## Quick Reference Commands

```bash
# Check status across key repos
~/claudesync/skills/github-sync/git-sync-check.sh

# Push changes to current repo
git add -A && git commit -m "message" && git push origin main
```

## Repositories to Monitor

The script automatically discovers all git repositories in your home directory (up to 4 levels deep), excluding:
- `~/.claude/` (Claude Code config - managed separately)
- `Library/`, `.Trash/`, `node_modules/`, `.npm/`, `.cache/`
- `.local/`, `.cargo/`, `.rustup/`, `vendor/`, `.gem/`
- `go/pkg/`, `.cocoapods/`, `Pods/`

## MCP OAuth Credential Sync

The github-sync skill also handles **automatic syncing of MCP OAuth tokens** across Macs via iCloud.

### How It Works

- **Session start:** Automatically pulls latest OAuth tokens from iCloud (merges with local)
- **Session end:** Automatically pushes updated OAuth tokens to iCloud
- Uses deep-env's encryption (AES-256-CBC) and password
- Tokens are merged intelligently: fresher tokens (later `expiresAt`) are kept

### First-Time Setup

After authenticating MCP servers (Zapier, Browserbase, etc.) for the first time:
```bash
~/claudesync/skills/github-sync/sync-mcp-oauth.sh push
```

After that, everything is automatic. Your other Macs will automatically get the tokens.

### Manual Commands

```bash
# Push credentials to iCloud
~/claudesync/skills/github-sync/sync-mcp-oauth.sh push

# Pull credentials from iCloud (merges with local)
~/claudesync/skills/github-sync/sync-mcp-oauth.sh pull

# Check sync status
~/claudesync/skills/github-sync/sync-mcp-oauth.sh status
```

### Technical Details

- Credentials stored at: `~/.claude/.credentials.json`
- Encrypted backup at: `~/Library/Mobile Documents/com~apple~CloudDocs/.deep-env/mcp-oauth.enc`
- Uses same password as deep-env (`~/.config/deep-env/.sync_pass`)
- Merge strategy: For each OAuth entry, keeps the one with later `expiresAt` timestamp

## Important Notes

- Never force push without explicit user permission
- Always pull before pushing to avoid conflicts
- If merge conflicts occur, help user resolve them
- The `~/.claude` repo has a daily auto-sync, but manual sync is still good practice
- Credential files (`.env.local`, `.credentials.json`) should never be committed to git (gitignored)
