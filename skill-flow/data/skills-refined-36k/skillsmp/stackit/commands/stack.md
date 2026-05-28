# Stack Operations Commands

Commands for managing the entire stack or multiple branches.

> **CRITICAL:** Always run these commands with `command stackit ... --no-interactive`.

## Stack Maintenance

| Command | Description |
|---------|-------------|
| `command stackit restack --no-interactive` | Rebase all branches to ensure proper ancestry |
| `command stackit sync --no-interactive` | Pull trunk, delete merged branches, restack |
| `command stackit info --stack --json --no-interactive` | Export full stack metadata as JSON for analysis |
| `command stackit merge` | Merge approved PRs and cleanup |
| `command stackit fold --no-interactive` | Fold current branch into its parent |

## Bulk Operations

| Command | Description |
|---------|-------------|
| `command stackit foreach --no-interactive` | Run command on each branch in stack |
| `command stackit submit --no-interactive` | Push branches and create/update PRs |
| `command stackit reorder` | Interactively reorder branches |
| `command stackit move` | Rebase branch onto new parent |

## Common Flag Patterns

### command stackit submit --no-interactive
- `--stack` - Submit entire stack (alias: `ss`)
- `--draft` - Create as draft PRs
- `--edit` - Edit PR metadata interactively

**Examples:**
```bash
# Submit current branch and ancestors
command stackit submit --no-interactive

# Submit entire stack
command stackit submit --no-interactive --stack

# Submit as drafts
command stackit submit --no-interactive --draft --stack
```

### command stackit sync --no-interactive
- `--restack` - Auto-restack after cleanup

**What it does:**
1. Pulls latest from trunk/main
2. Deletes branches whose PRs were merged
3. Deletes branches whose PRs were closed
4. Optionally restacks remaining branches

### command stackit foreach --no-interactive
**Usage:** `command stackit foreach --no-interactive "command to run"`

**Examples:**
```bash
# Build all branches (use project's build command from README.md)
command stackit foreach --no-interactive "<build-command>"

# Test all branches (use project's test command from README.md)
command stackit foreach --no-interactive "<test-command>"

# Show status on each
command stackit foreach --no-interactive "git status --short"
```

## Workflow Examples

### Start a feature stack
```bash
git add .
echo "feat: implement user authentication" | command stackit create --no-interactive

# Add tests to the same branch (branches can have multiple commits)
git add .
git commit -m "test: add auth tests"

# Work on next part as a separate stacked branch
git add .
echo "feat: add JWT token validation" | command stackit create --no-interactive
```

### Submit for review
```bash
command stackit submit --no-interactive --stack
```

### After code review changes
```bash
git add .
command stackit modify --no-interactive
command stackit restack --no-interactive
command stackit submit --no-interactive
```

### Sync with main
```bash
command stackit sync --no-interactive --restack
```
