---
description: Clean up old auto-captured files with retention policy
---

# Cleanup - Retention Policy Manager

จัดการไฟล์เก่าด้วย retention policy พร้อม archive และ dry-run mode

## Usage

```
/cleanup                    # Preview ด้วย default settings (30 days)
/cleanup [days]             # Preview with custom retention period
/cleanup [days] --execute   # Execute cleanup
/cleanup --archive          # Archive before delete
```

## Instructions

### Step 1: Parse Arguments and Show Current State

```bash
export TZ='Asia/Bangkok'

echo "=== Auto-captured Files ==="
find docs/auto-captured -type f -name "*.md" 2>/dev/null | wc -l | xargs echo "Total files:"

echo ""
echo "=== Learnings Files ==="
find docs/learnings -type f -name "*.md" 2>/dev/null | wc -l | xargs echo "Total files:"

echo ""
echo "=== Archives ==="
ls -la docs/archives/ 2>/dev/null || echo "No archives yet"
```

### Step 2: Determine Mode

| Argument | Mode |
|----------|------|
| (none) | Dry-run, 30 days retention |
| `[days]` | Dry-run with custom retention |
| `[days] --execute` | Execute cleanup |
| `--archive` | Enable archiving |
| `--all` | Clean all targets |

### Step 3: Run Cleanup Script

**Dry-run mode (default):**

```bash
cd "$PROJECT_ROOT"
./scripts/cleanup.sh --days [DAYS] --dry-run [--archive] [--all]
```

**Execute mode:**

```bash
cd "$PROJECT_ROOT"
./scripts/cleanup.sh --days [DAYS] [--archive] [--all]
```

### Step 4: Show Results

Display the script output showing:
- Files that would be / were deleted
- Total space freed
- Archives created (if enabled)

### Step 5: Confirm and Suggest Next Steps

```markdown
## Cleanup Summary

| Metric | Value |
|--------|-------|
| Retention Period | [days] days |
| Files Processed | [count] |
| Space Freed | [size] |
| Archives Created | [count] |

### Next Steps

1. Review remaining files in `docs/auto-captured/`
2. Run `/distill` to extract patterns from learnings
3. Schedule periodic cleanup (cron job recommendation)
```

## Examples

```bash
# Preview what would be deleted (30 days default)
/cleanup

# Preview with 7 days retention
/cleanup 7

# Execute cleanup with archiving
/cleanup 14 --archive --execute

# Clean all targets (auto-captured + draft learnings)
/cleanup --all --execute
```

## Retention Policy

| Target | Policy |
|--------|--------|
| `docs/auto-captured/` | Delete all files older than retention period |
| `docs/learnings/` | Delete only `status: draft` files older than retention period |
| `docs/retrospective/` | Never auto-delete (permanent records) |
| `docs/knowledge-base/` | Never auto-delete (distilled knowledge) |

## Archive Format

When `--archive` is enabled:
- Archives stored in `docs/archives/`
- Format: `archive_[target]_YYYYMMDD_HHMMSS.tar.gz`
- Contains all files that will be deleted

## Scheduling Recommendation

Add to crontab for automatic cleanup:

```bash
# Weekly cleanup, keep 30 days, archive old files
0 0 * * 0 cd /path/to/project && ./scripts/cleanup.sh --days 30 --archive --all
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/distill` | Extract patterns from learnings |
| `/mem` | Quick knowledge capture |
| `/td` | Session retrospective |
