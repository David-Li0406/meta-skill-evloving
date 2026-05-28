# Git Workflow for Skill Updates

This document details the git workflow for committing skill modifications.

## Overview

Skills are stored in the plugin repository. Changes should be committed to track the evolution of skills over time.

## Directory Structure

```
Plugin level:
${CLAUDE_PLUGIN_ROOT}/skills/reflect/SKILL.md

Repository structure:
plugins/reflect/
├── skills/
│   └── reflect/
│       ├── SKILL.md           # Main skill file
│       └── references/        # Supporting docs
├── commands/
├── scripts/
└── hooks/
```

## Manual Workflow

### Step 1: Navigate to Repository

```bash
cd /path/to/plugin-repo
```

### Step 2: Verify Changes

```bash
# See what changed
git diff plugins/reflect/skills/[skill-name]/SKILL.md

# Check status
git status
```

### Step 3: Stage Changes

```bash
git add plugins/reflect/skills/[skill-name]/SKILL.md
```

### Step 4: Commit

```bash
git commit -m "[skill-name]: [concise summary of changes]"
```

**Commit message guidelines:**
- Format: `[skill-name]: [summary]`
- Keep under 72 characters
- Use imperative mood ("add", "update", "fix")
- Examples:
  - `frontend-design: no gradients, use #000 dark`
  - `code-reviewer: add Python type checking`
  - `reflect: improve signal detection accuracy`

### Step 5: Push

```bash
git push origin main
```

## Automated Workflow (Recommended)

Use the helper script to automate this process:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/reflect-commit-changes.sh \
  [skill-name] \
  "[commit message]"
```

The script handles:
1. Path detection (finds plugin repository)
2. Verification (checks file exists and has changes)
3. Git add (stages the skill file)
4. Git commit (with proper message format)
5. Git push (to origin main)
6. Error handling (rollback on failure)

## Common Scenarios

### Scenario 1: Single Skill Change

```bash
# Manual
cd /path/to/plugin-repo
git add plugins/reflect/skills/frontend-design/SKILL.md
git commit -m "frontend-design: add dark mode constraints"
git push origin main

# Automated
${CLAUDE_PLUGIN_ROOT}/scripts/reflect-commit-changes.sh \
  frontend-design \
  "add dark mode constraints"
```

### Scenario 2: Multiple Skills Changed

```bash
# Commit each separately
cd /path/to/plugin-repo
git add plugins/reflect/skills/frontend-design/SKILL.md
git commit -m "frontend-design: update color guidelines"

git add plugins/reflect/skills/code-reviewer/SKILL.md
git commit -m "code-reviewer: add security checks"

git push origin main
```

### Scenario 3: Skill + Reference Files

```bash
cd /path/to/plugin-repo
git add plugins/reflect/skills/reflect/SKILL.md
git add plugins/reflect/skills/reflect/references/signal-examples.md
git commit -m "reflect: improve signal detection with examples"
git push origin main
```

## Troubleshooting

### Problem: "Not a git repository"

**Cause**: Not in plugin repository directory

**Solution**:
```bash
cd /path/to/plugin-repo
```

### Problem: "No changes to commit"

**Cause**: File wasn't actually modified, or changes already staged

**Solution**:
```bash
# Check what changed
git status
git diff

# If no changes, nothing to commit (expected)
```

### Problem: "Permission denied (push)"

**Cause**: SSH keys not configured or wrong remote

**Solution**:
```bash
# Check remote
git remote -v

# Verify SSH works (GitHub)
ssh -T git@github.com
```

### Problem: "Merge conflict"

**Cause**: Someone else modified the same skill

**Solution**:
```bash
# Pull latest
git pull origin main

# Resolve conflicts in editor
# Look for <<<<<<< markers

# Stage resolved files
git add [file]

# Complete merge
git commit

# Push
git push origin main
```

## Best Practices

1. **Always pull before editing**:
   ```bash
   cd /path/to/plugin-repo && git pull origin main
   ```

2. **Verify changes before committing**:
   ```bash
   git diff plugins/reflect/skills/[skill]/SKILL.md
   ```

3. **Use descriptive commit messages**:
   - Good: `reflect: add metrics tracking for self-improvement`
   - Bad: `update skill`

4. **Commit focused changes**:
   - One skill per commit
   - Related changes together
   - Don't mix unrelated modifications

5. **Test before pushing**:
   - Run `/[skill-name]` to verify it works
   - Check for syntax errors

## Repository Structure

```
plugin-repo/
├── .git/                           # Git repository
├── plugins/
│   └── reflect/
│       ├── .claude-plugin/
│       │   └── plugin.json         # Plugin manifest
│       ├── skills/
│       │   └── reflect/
│       │       ├── SKILL.md        # Edit this file
│       │       └── references/     # Supporting docs
│       ├── agents/
│       ├── commands/
│       ├── scripts/
│       └── hooks/
└── marketplace.json                # Marketplace config
```

## Permissions

Reflect skill has permission to:
- Read skill files: `${CLAUDE_PLUGIN_ROOT}/skills/`
- Edit skill files: After user approval only
- Git operations: `add`, `commit`, `push` in plugin repo

**Security**:
- Never commit secrets to skill files
- User approval required before modifications
- All changes tracked in git history
