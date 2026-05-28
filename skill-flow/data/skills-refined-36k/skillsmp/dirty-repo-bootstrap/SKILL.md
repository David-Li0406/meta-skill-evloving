---
name: dirty-repo-bootstrap
description: Safe recovery procedure for dirty/WIP repositories. This skill provides a standardized workflow for: - Snapshotting uncommitted work to a WIP branch
---

# dirty-repo-bootstrap

## Description

Safe recovery procedure for dirty/WIP repositories. This skill provides a standardized workflow for:
- Snapshotting uncommitted work to a WIP branch
- Pushing the snapshot to origin for safety
- Handling Beads-tracked repositories correctly
- Recovering from repository corruption

**Non-negotiables:**
- Do NOT stash by default - snapshot to a branch and push
- Do NOT print secrets (bearer tokens, headers, etc.)
- Warning-only locally; CI can fail-loud

## When to Use This Skill

Use this skill when:
1. You have uncommitted changes and need to switch contexts
2. You want to save work-in-progress before destructive operations
3. You need to recover from a dirty/corrupted repository state
4. You're starting a new task and the repo has uncommitted changes

Do NOT use this skill if:
- The repository is already clean (`git status` shows no changes)
- You want to discard changes (use `git restore` instead)

## Usage

### Quick Recovery (Copy/Paste)

If you have uncommitted changes and need to snapshot them safely:

```bash
~/.agent/skills/dirty-repo-bootstrap/snapshot.sh
```

### Manual Recovery Flow

For manual control or custom branch names:

```bash
# 1. Check git status
git status

# 2. Create WIP branch with timestamp
git checkout -b wip/$(hostname)-$(date +%Y-%m-%d)-$(basename "$PWD")

# 3. If .beads/issues.jsonl is modified, sync Beads first
if git status --porcelain | grep -q ".beads/issues.jsonl"; then
  bd sync
fi

# 4. Add all changes and commit
git add -A
git commit -m "wip: snapshot before [describe your next task]"

# 5. Push WIP branch to origin
git push -u origin HEAD

# 6. Return to main/master branch
git checkout main  # or master
git pull origin main
```

## WIP Branch Naming Convention

Use descriptive WIP branch names:

```
wip/<hostname>-<date>-<context>
```

Examples:
- `wip/epyc6-2025-12-13-agent-skills`
- `wip/macmini-2025-12-13-affordabot`
- `wip/codex-vm-2025-12-13-prime-radiant`

This naming convention:
- Identifies the machine/environment
- Timestamps the snapshot
- Describes the repository context
- Makes it easy to clean up old WIP branches later

## Beads Integration

**CRITICAL:** If `.beads/issues.jsonl` has been modified, you MUST run `bd sync` before creating the snapshot commit.

Why? Beads tracks issues in JSONL format and syncs them via git. If you commit changes to `issues.jsonl` without syncing:
- You may create merge conflicts with other agents
- You may lose issue updates from the remote
- The Beads state may become inconsistent

The safe flow for Beads-tracked repos:

```bash
# 1. Check if .beads/issues.jsonl is modified
git status --porcelain | grep ".beads/issues.jsonl"

# 2. If modified, sync Beads FIRST
bd sync

# 3. Then proceed with WIP snapshot
git add -A
git commit -m "wip: snapshot after Beads sync"
git push -u origin HEAD
```

## Repository Corruption Recovery

If your repository appears corrupted or `git status` fails:

```bash
# 1. Verify basic git repository structure
git rev-parse --show-toplevel
# Should print the repo root path. If it fails, the .git directory is damaged.

# 2. Check for HEAD corruption
git log -1
# Should show the most recent commit. If it fails, HEAD is corrupted.

# 3. If .beads/issues.jsonl exists, verify it's valid JSONL
if [[ -f .beads/issues.jsonl ]]; then
  jq empty .beads/issues.jsonl 2>/dev/null || echo "JSONL corrupted"
fi

# 4. Force-reimport Beads state (if needed)
bd import -i .beads/issues.jsonl --force

# 5. If git is severely damaged, consider:
#    - Cloning fresh from origin
#    - Manually copying uncommitted work from backup
#    - Consulting git fsck output for recovery hints
git fsck --full
```

## Automation Script

The `snapshot.sh` script automates the safe WIP snapshot flow:

```bash
~/.agent/skills/dirty-repo-bootstrap/snapshot.sh [--branch-name <name>] [--message <msg>]
```

Options:
- `--branch-name <name>`: Custom WIP branch name (default: auto-generated)
- `--message <msg>`: Custom commit message (default: "wip: snapshot before next task")

The script:
1. Checks if the repo is dirty
2. Creates a WIP branch with timestamp
3. Detects and syncs Beads if needed
4. Commits all changes
5. Pushes to origin
6. Returns to the previous branch (or main/master)

Exit codes:
- `0`: Success (snapshot created and pushed)
- `1`: Repository is already clean (no snapshot needed)
- `2`: Git operation failed
- `3`: Beads sync failed (if .beads/issues.jsonl was modified)

## Best Practices

### 1. Snapshot Early, Snapshot Often

Create WIP snapshots before:
- Starting a new feature or bug fix
- Running destructive git operations (rebase, reset, etc.)
- Switching to a different task mid-work
- Making experimental changes

### 2. Clean Up WIP Branches Regularly

WIP branches are temporary. After you've safely merged or abandoned the work:

```bash
# List all WIP branches
git branch -r | grep wip/

# Delete a WIP branch (local and remote)
git branch -d wip/epyc6-2025-12-13-agent-skills
git push origin --delete wip/epyc6-2025-12-13-agent-skills
```

### 3. Never Stash for Long-Term Storage

Git stash is good for temporary context switching (minutes to hours).

For longer-term WIP storage (hours to days):
- Use WIP branches (this skill)
- Push to origin for safety
- Stashes can be lost or forgotten

### 4. Include Context in Commit Messages

When creating WIP snapshots, include context about what you were working on:

```bash
git commit -m "wip: snapshot before implementing user authentication

- Added login form UI
- Started session management logic
- TODO: implement password hashing"
```

This helps you (and other agents) understand the WIP state when you return to it.

## Integration with Other Skills

This skill is referenced by:
- **mcp-doctor**: Checks that the skills mount is correct
- **skills-doctor**: Validates skill availability
- **beads-workflow**: May recommend this skill when detecting dirty repos

Use in combination with:
- **session-end**: Snapshot work before ending a coding session
- **sync-feature-branch**: For committing polished work (not WIP)
- **create-pull-request**: Requires clean repo state

## CI/CD Integration

For CI environments where you want strict enforcement:

```bash
# In .github/workflows/ci.yml or similar:
export MCP_DOCTOR_STRICT=1  # Fail builds if required MCPs missing
~/.agent/skills/mcp-doctor/check.sh

# Or fail if repo is dirty:
if [[ -n "$(git status --porcelain)" ]]; then
  echo "❌ Repository has uncommitted changes"
  exit 1
fi
```

In CI, you typically want to:
- Fail if the repo is dirty (prevents accidental commits)
- Skip the snapshot flow (CI runs on clean checkouts)

Locally, you want to:
- Warn if the repo is dirty
- Offer to run `snapshot.sh` to clean it up

## Troubleshooting

### "fatal: not a git repository"

Your current directory is not a git repository. Navigate to the repository root:

```bash
cd ~/agent-skills  # or your repo path
git status
```

### "error: failed to push some refs"

The WIP branch might already exist on origin with conflicting commits. Options:

1. Use a different branch name:
   ```bash
   git checkout -b wip/epyc6-2025-12-13-agent-skills-v2
   ```

2. Force push (DANGEROUS - only if you're sure):
   ```bash
   git push --force-with-lease origin HEAD
   ```

### "bd: command not found"

Beads CLI is not installed. If your repo doesn't use Beads, you can skip this check.

If your repo DOES use Beads, install it:
```bash
npm install -g @beadshq/beads-cli
```

### ".beads/issues.jsonl: parse error"

The Beads JSONL file is corrupted. Try:

```bash
# 1. Validate the file
jq empty .beads/issues.jsonl

# 2. If it's corrupted, restore from git
git restore .beads/issues.jsonl

# 3. Or re-import from a clean state
bd import -i .beads/issues.jsonl --force
```

## Related Documentation

- [DX Bootstrap Contract](../DX_BOOTSTRAP_CONTRACT.md) - Session start requirements
- [mcp-doctor](../mcp-doctor/SKILL.md) - MCP server health checks
- [beads-workflow](../beads-workflow/SKILL.md) - Issue tracking integration
- [sync-feature-branch](../sync-feature-branch/SKILL.md) - Polished commit workflow

## Version History

- **v1.0.0** (2025-12-13): Initial implementation for bd-3871.15
  - Safe WIP snapshot workflow
  - Beads integration support
  - Repository corruption recovery guidance
  - Automation script (snapshot.sh)
