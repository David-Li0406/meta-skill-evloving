---
name: julien-maintenance-claude-json
description: Clean ~/.claude.json when it becomes too large (>25K tokens). Use when Claude cannot read the file, user mentions "claude.json trop gros", "nettoyer claude.json", or "cleanup claude.json".
category: maintenance
triggers:
  - claude.json trop gros
  - nettoyer claude.json
  - cleanup claude.json
  - claude.json too large
  - clean claude config
  - maintenance claude
  - file exceeds maximum tokens
---

# Claude.json Maintenance

Clean and optimize `~/.claude.json` when it becomes too large for Claude to read.

## When to Use

## Observability

**First**: At the start of execution, display:
```
🔧 Skill "julien-maintenance-claude-json" activated
```

- Claude Code shows error: "File content exceeds maximum allowed tokens"
- User reports claude.json is too big
- Periodic maintenance to keep config lean

## Workflow

### Step 1: Diagnose

Run the diagnostic script to see what's taking space:

```bash
python scripts/diagnose-claude-json.py
```

This shows each section's size in characters and tokens (estimated).

### Step 2: Clean (Interactive)

Run the cleanup script:

```bash
python scripts/clean-claude-json.py
```

**Safe cleanups (no data loss):**
- `cachedChangelog` - Will be re-downloaded automatically
- `cachedStatsigGates` - Feature flags cache
- `cachedDynamicConfigs` - Dynamic config cache
- `cachedGrowthBookFeatures` - A/B test cache

**Optional cleanups (may lose preferences):**
- `projects` - Old project permissions (keeps recent 30 days)
- `tipsHistory` - Onboarding tips tracking

### Step 3: Verify

After cleanup, verify the file is readable:

```bash
python scripts/diagnose-claude-json.py
```

## Backup Policy

**Always creates backup** before any modification:
- Location: `~/.claude.json.backup-YYYYMMDD-HHMMSS`
- Keep last 3 backups, older ones auto-deleted

## Common Culprits

| Section | Typical Size | Safe to Clear |
|---------|--------------|---------------|
| `cachedChangelog` | 40-60 KB | Yes |
| `projects` | 30-100 KB | Partial* |
| `cachedStatsigGates` | 1-5 KB | Yes |
| `tipsHistory` | 1 KB | Yes |

*Projects: Can clear old entries (>30 days) but keeps recent ones.

## Skill Chaining

### Skills Required Before
- None (diagnostic/maintenance entry point)

### Input Expected
- User complaint about claude.json being too large
- Or Claude error about file exceeding token limit

### Output Produced
- Cleaned ~/.claude.json file
- Backup of original file
- Size reduction report

### Compatible Skills After
- None (terminal operation)

### Tools Used
- `Bash` (run Python scripts)
- `Read` (verify file after cleanup)
