---
name: requirements-framework-development
description: This skill should be used when the user asks to "develop requirements framework", "fix requirements framework bug", "sync requirements framework", "deploy requirements changes", "update framework code", "test framework changes", or needs help with the framework development workflow including sync.sh usage, TDD for framework itself, and contributing changes.
git_hash: 7953a43
---

# Requirements Framework Development

Guide for developing, fixing, and maintaining the **Claude Code Requirements Framework** with proper sync workflow.

**Repository**: `~/Tools/claude-requirements-framework` (git-controlled source of truth)
**Deployed**: `~/.claude/hooks/` (active runtime)
**Remote**: https://github.com/HarmAalbers/claude-requirements-framework.git

## Core Concept: Two-Location Architecture

The framework lives in TWO places that must stay synchronized:

| Location | Purpose | When Changes Take Effect |
|----------|---------|--------------------------|
| **Repository** | Git source of truth | After `./sync.sh deploy` |
| **Deployed** | Active runtime | Immediately |

**→ Full sync details**: See `references/sync-workflow-details.md`

## sync.sh - The Essential Tool

```bash
cd ~/Tools/claude-requirements-framework

./sync.sh status  # Check sync (ALWAYS run first)
./sync.sh deploy  # Repository → ~/.claude/hooks
./sync.sh diff    # Show differences
```

### Status Symbols

| Symbol | Meaning | Action |
|--------|---------|--------|
| `✓` | In sync | None needed |
| `↑` | Out of sync | Run `./sync.sh deploy` |
| `⚠` | Not deployed | Run `./sync.sh deploy` |
| `✗` | Missing in repo | Copy or delete |

## Development Workflows

### Workflow A: Standard Development

**Pattern**: Edit in repo → Deploy → Test → Commit

```bash
cd ~/Tools/claude-requirements-framework

# 1. Edit in repository
vim hooks/lib/requirements.py

# 2. Deploy
./sync.sh deploy

# 3. Test
python3 ~/.claude/hooks/test_requirements.py

# 4. Commit
git add . && git commit -m "feat: Add feature" && git push
```

### Workflow B: Emergency Fix

**Pattern**: Fix in deployed → Test → Copy back → Commit

```bash
# 1. Fix directly (immediate effect)
vim ~/.claude/hooks/check-requirements.py

# 2. Test immediately
python3 ~/.claude/hooks/test_requirements.py

# 3. Copy to repo
cd ~/Tools/claude-requirements-framework
cp ~/.claude/hooks/check-requirements.py hooks/

# 4. Deploy and commit
./sync.sh deploy
git add . && git commit -m "fix: Bug description" && git push
```

### Workflow C: Claude-Driven Development

**Pattern**: Claude edits deployed → Copy back → Commit

```bash
# 1. Claude edited ~/.claude/hooks/lib/some_module.py

# 2. Copy to repo
cd ~/Tools/claude-requirements-framework
cp ~/.claude/hooks/lib/some_module.py hooks/lib/

# 3. Deploy and commit
./sync.sh deploy
git add . && git commit -m "feat: Description" && git push
```

**→ Example script**: See `examples/claude-driven-workflow.sh`

### Workflow D: Test-Driven Development

**Pattern**: Test (RED) → Implement → Test (GREEN) → Commit

```bash
# 1. Write failing test in repo
vim hooks/test_requirements.py

# 2. Deploy and run (RED)
./sync.sh deploy
python3 ~/.claude/hooks/test_requirements.py  # Fails

# 3. Implement feature
vim hooks/lib/requirements.py

# 4. Deploy and run (GREEN)
./sync.sh deploy
python3 ~/.claude/hooks/test_requirements.py  # Passes

# 5. Commit
git add . && git commit -m "feat: TDD feature" && git push
```

**→ Example script**: See `examples/tdd-workflow.sh`

## Testing

### Run Full Test Suite

```bash
python3 ~/.claude/hooks/test_requirements.py

# Expected: 544/544 tests passed ✓
```

### Run Specific Tests

```bash
# By name pattern
python3 ~/.claude/hooks/test_requirements.py -k "test_session"

# Verbose output
python3 ~/.claude/hooks/test_requirements.py -v
```

### Integration Testing

```bash
# 1. Enable in a project
cd ~/some-project
cat > .claude/requirements.yaml <<EOF
version: "1.0"
enabled: true
requirements:
  commit_plan:
    enabled: true
    scope: session
EOF

# 2. Start Claude, try editing → Should block
# 3. Satisfy: req satisfy commit_plan
# 4. Try editing → Should work
```

## Common Agent Tasks

### Fix a Bug

```bash
# 1. Edit in deployed (immediate effect)
vim ~/.claude/hooks/lib/FILE.py

# 2. Test
python3 ~/.claude/hooks/test_requirements.py

# 3. Copy to repo
cd ~/Tools/claude-requirements-framework
cp ~/.claude/hooks/lib/FILE.py hooks/lib/

# 4. Deploy and commit
./sync.sh deploy
git add . && git commit -m "fix: Bug description" && git push
```

### Add a Feature

```bash
# 1. Check sync first
cd ~/Tools/claude-requirements-framework
./sync.sh status

# 2. Edit in repo
vim hooks/lib/FILE.py

# 3. Deploy and test
./sync.sh deploy && python3 ~/.claude/hooks/test_requirements.py

# 4. Commit
git add . && git commit -m "feat: Feature description" && git push
```

### After ANY Changes

```bash
# ALWAYS check sync before committing
cd ~/Tools/claude-requirements-framework
./sync.sh status
# If not clean, reconcile before committing
```

## Troubleshooting Quick Reference

### Changes Not Taking Effect

```bash
# Check where you edited
pwd

# If in repo, deploy
./sync.sh deploy

# Check file exists
ls -la ~/.claude/hooks/your-file.py
```

### Tests Fail After Deploy

```bash
# Check permissions
chmod +x ~/.claude/hooks/*.py

# Check sync status
./sync.sh status

# Run with verbose
python3 ~/.claude/hooks/test_requirements.py -v
```

### Hook Not Triggering

```bash
# Check registration
cat ~/.claude/settings.local.json | grep hooks

# Check file exists and is executable
ls -la ~/.claude/hooks/check-requirements.py
```

**→ Full troubleshooting**: See `references/troubleshooting-development.md`

## Best Practices

1. **Check sync BEFORE committing** - `./sync.sh status`
2. **Test after every change** - `python3 ~/.claude/hooks/test_requirements.py`
3. **Deploy after editing in repo** - `./sync.sh deploy`
4. **Commit atomically** - One logical change per commit
5. **Use conventional commits** - `feat:`, `fix:`, `docs:`, `test:`

## File Sync Reference

### Hook Files Synced

```
check-requirements.py
handle-session-start.py
handle-stop.py
handle-session-end.py
handle-plan-exit.py
auto-satisfy-skills.py
clear-single-use.py
requirements-cli.py
test_requirements.py
ruff_check.py
```

### Library Files Synced

All `*.py` files in `hooks/lib/` directory.

### NOT Synced

- `examples/` - Example files
- `docs/` - Documentation
- `plugin/` - Plugin (symlinked separately)
- `.git/` - Git files

## Golden Rules

1. **Repository is source of truth** - Always commit from here
2. **Deployed is active** - Changes take effect immediately
3. **sync.sh keeps them aligned** - Use it liberally
4. **Check sync before push** - Reconcile differences first
5. **Test after every sync** - Run test suite to verify

## Resources

- **README**: `~/Tools/claude-requirements-framework/README.md`
- **DEVELOPMENT.md**: Full development guide
- **Sync Tool**: `./sync.sh status|deploy|diff`
- **Tests**: `python3 ~/.claude/hooks/test_requirements.py`

## Reference Files

- `references/sync-workflow-details.md` - Detailed sync.sh usage and scenarios
- `references/troubleshooting-development.md` - Development troubleshooting
- `examples/tdd-workflow.sh` - TDD workflow example script
- `examples/claude-driven-workflow.sh` - Claude development workflow script
