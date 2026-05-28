# Sync Workflow Details

Comprehensive guide to the sync.sh tool and two-location architecture.

## Two-Location Architecture

The framework lives in TWO places that must stay synchronized:

### Repository Location
**Path**: `~/Tools/claude-requirements-framework/`

- Git version controlled
- Source of truth for all changes
- Where you commit and push from
- Contains:
  - `hooks/` - Python hooks and libraries
  - `plugin/` - Agents, commands, skills
  - `docs/` - Documentation
  - `sync.sh` - Synchronization tool

### Deployed Location
**Path**: `~/.claude/hooks/`

- Active runtime (where Claude Code loads hooks)
- Where framework actually executes
- Hooks run from here immediately
- Changes here take effect without restart

---

## sync.sh Commands

### Check Status

```bash
cd ~/Tools/claude-requirements-framework
./sync.sh status
```

**Output explanation**:
```
📊 Sync Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Repository:  ~/Tools/claude-requirements-framework
Deployed:    ~/.claude/hooks

File Status:
  ✓ check-requirements.py - In sync
  ↑ requirements-cli.py - Out of sync (run './sync.sh deploy' to update deployed)
  ⚠ lib/new_module.py - Not deployed
  ✗ lib/old_module.py - Missing in repository
```

**Symbols**:
| Symbol | Meaning | Action |
|--------|---------|--------|
| `✓` | In sync | None needed |
| `↑` | Out of sync | Run `./sync.sh deploy` |
| `⚠` | Not deployed | Run `./sync.sh deploy` |
| `✗` | Missing in repo | Copy from deployed or delete |

### Deploy Changes

```bash
./sync.sh deploy
```

Copies all hook files from repository → deployed location.

**What gets synced**:
- `hooks/*.py` → `~/.claude/hooks/*.py`
- `hooks/lib/*.py` → `~/.claude/hooks/lib/*.py`

**What does NOT get synced**:
- `examples/` - Example files
- `docs/` - Documentation
- `plugin/` - Plugin components (symlinked)
- `.git/` - Git files

### View Differences

```bash
./sync.sh diff
```

Shows detailed diff between repository and deployed versions.

---

## Sync Scenarios

### Scenario: Normal Development

You edit files in the repository, then deploy.

```bash
cd ~/Tools/claude-requirements-framework

# 1. Edit file in repo
vim hooks/lib/requirements.py

# 2. Deploy to make changes active
./sync.sh deploy

# 3. Test
python3 ~/.claude/hooks/test_requirements.py

# 4. Commit
git add . && git commit -m "feat: description"
```

### Scenario: Emergency Fix

You edit directly in deployed location for immediate effect.

```bash
# 1. Fix directly (immediate effect)
vim ~/.claude/hooks/check-requirements.py

# 2. Test immediately
python3 ~/.claude/hooks/test_requirements.py

# 3. Copy back to repo
cd ~/Tools/claude-requirements-framework
cp ~/.claude/hooks/check-requirements.py hooks/check-requirements.py

# 4. Deploy to sync
./sync.sh deploy

# 5. Commit
git add . && git commit -m "fix: emergency bug fix"
```

### Scenario: Claude Made Changes

Claude edited files in deployed location during development.

```bash
# 1. Claude edited ~/.claude/hooks/lib/some_module.py

# 2. Copy changes to repo
cd ~/Tools/claude-requirements-framework
cp ~/.claude/hooks/lib/some_module.py hooks/lib/some_module.py

# 3. Deploy to maintain sync
./sync.sh deploy

# 4. Review changes
git diff

# 5. Commit
git add . && git commit -m "feat: changes made by Claude"
```

### Scenario: Merge Conflict

Remote has changes while you have local changes.

```bash
cd ~/Tools/claude-requirements-framework

# 1. Stash local changes
git stash

# 2. Pull remote
git pull origin master

# 3. Reapply changes
git stash pop

# 4. Resolve conflicts manually

# 5. Deploy merged version
./sync.sh deploy

# 6. Test
python3 ~/.claude/hooks/test_requirements.py

# 7. Commit merge
git add . && git commit -m "merge: resolve conflicts"
```

---

## File Patterns Synced

### Hook Files

| File | Purpose |
|------|---------|
| `check-requirements.py` | PreToolUse hook entry point |
| `handle-session-start.py` | SessionStart hook |
| `handle-stop.py` | Stop hook |
| `handle-session-end.py` | SessionEnd hook |
| `handle-plan-exit.py` | PostToolUse for ExitPlanMode |
| `auto-satisfy-skills.py` | PostToolUse for skills |
| `clear-single-use.py` | PostToolUse for Bash |
| `requirements-cli.py` | CLI tool |
| `test_requirements.py` | Test suite |
| `ruff_check.py` | Linting hook |

### Library Files

All `*.py` files in `hooks/lib/` are synced:

| Module | Purpose |
|--------|---------|
| `requirements.py` | Core API |
| `config.py` | Configuration loader |
| `state_storage.py` | State persistence |
| `session.py` | Session tracking |
| `registry_client.py` | Registry management |
| `*_strategy.py` | Requirement strategies |
| `branch_size_calculator.py` | Dynamic calculations |
| `calculation_cache.py` | Result caching |
| `message_dedup_cache.py` | Message deduplication |
| `git_utils.py` | Git operations |
| `colors.py` | Terminal colors |
| `logger.py` | Structured logging |
| `init_presets.py` | Init wizard presets |
| `interactive.py` | UI components |
| `feature_selector.py` | Feature selection |

---

## Pre-Commit Checklist

**ALWAYS run before committing**:

```bash
cd ~/Tools/claude-requirements-framework

# 1. Check sync status
./sync.sh status

# 2. If out of sync, reconcile:
#    - If deployed is newer: copy to repo
#    - If repo is newer: deploy
./sync.sh diff  # See what's different

# 3. Run tests
python3 ~/.claude/hooks/test_requirements.py

# 4. Now safe to commit
git add .
git commit -m "type: description"
git push
```

---

## Plugin Components (Separate Pattern)

Plugin components use symlink, NOT copy:

```bash
# Plugin is symlinked (live updates)
ls -la ~/.claude/plugins/requirements-framework
# → /Users/harm/Tools/claude-requirements-framework/plugin

# Changes to plugin/ directory are immediately active
# No sync.sh deploy needed for plugin changes
```

This means:
- Edit `plugin/agents/*.md` → Immediately available
- Edit `plugin/skills/*/skill.md` → Immediately available
- Edit `plugin/commands/*.md` → Immediately available

---

## Troubleshooting Sync

### Changes Not Taking Effect

```bash
# 1. Check which location you edited
pwd

# 2. If edited in repo, deploy
./sync.sh deploy

# 3. If still not working, check file exists
ls -la ~/.claude/hooks/your-file.py

# 4. Check file permissions
chmod +x ~/.claude/hooks/*.py
```

### sync.sh Not Working

```bash
# Check if executable
ls -la ~/Tools/claude-requirements-framework/sync.sh

# Make executable if needed
chmod +x ~/Tools/claude-requirements-framework/sync.sh

# Run with bash explicitly
bash ~/Tools/claude-requirements-framework/sync.sh status
```

### Files Missing After Sync

```bash
# Check if file is in the sync list
grep "filename" ~/Tools/claude-requirements-framework/sync.sh

# sync.sh uses explicit file patterns
# New files may need to be added to the script
```
