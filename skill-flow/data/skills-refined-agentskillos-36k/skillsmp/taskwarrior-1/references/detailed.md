# TaskWarrior Detailed Reference

Complete reference including configuration, troubleshooting, and advanced usage.

## AI Automation Interface

**Interface pattern:** Use `taskai` for all read operations, `task` for writes.

### taskai Function

Single-line output for Unix pipeline compatibility:

```bash
taskai() { task rc.defaultwidth=0 rc.verbose=nothing "$@" | tr -s ' '; }
```

- `rc.defaultwidth=0` - infinite width (no wrapping)
- `rc.verbose=nothing` - data only (no headers/footers)
- `tr -s ' '` - compress column spacing

**Location:** Defined in `~/.zshenv` (not ~/.zshrc) so non-interactive shells can use it.

## Configuration

**Minimal ~/.taskrc:**
```bash
data.location=/Users/tengjizhang/.task
news.version=3.4.1
dateformat=Y-M-D
confirmation=off
```

**Shell integration (~/.zshenv):**
```bash
taskai() { task rc.defaultwidth=0 rc.verbose=nothing "$@" | tr -s ' '; }
alias t=task
```

## Data Storage

**Location:** `~/.task/` - Plain text JSON files, can be version controlled or synced.

## Troubleshooting

### Boolean/Tag Filter Errors

Complex tag queries can be ambiguous:

```bash
# Might not work as expected
task +work +someday list           # AND or OR?

# Use explicit operators
task +work and +someday list       # Explicit AND
task \( +work or +personal \) list # Explicit OR with escaping
```

### Confirmation Prompts in Scripts

Even with `confirmation=off`, bulk modifications prompt:

```bash
# Working solution
echo "all" | task +learning modify +someday

# Doesn't work
task rc.confirmation:off +learning modify +someday  # Still prompts
```

## Backup/Export

```bash
# Full backup
task export > ~/backup/tasks-$(date +%Y%m%d).json

# Restore
task import ~/backup/tasks-20250904.json
```

## Weekly Review Patterns

```bash
# What got done
taskai completed end.after:today-7days

# Browse aspirational
taskai list +someday

# Promote ready items
task 42 modify -someday

# Delete stale (untouched 2-3 months)
task 42 delete
```

## Common Patterns

```bash
# High priority committed work
task -someday priority:H

# Learning items in someday
task +someday +learning

# Project-specific committed work
task project:flashbots -someday
```
