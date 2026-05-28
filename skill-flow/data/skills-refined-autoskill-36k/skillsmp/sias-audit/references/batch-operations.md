# SIAS Batch Operations

## Constraints

- **Batch size**: 10 users per API call (Cloudflare limit)
- **Total users**: ~2000+
- **Modes**: `dry_run` (preview) or `flexible` (apply fixes)

## Parallel Agent Assignment

| Agent | Offset Range | Users |
|-------|--------------|-------|
| Agent 1 | 0-490 | 1-500 |
| Agent 2 | 500-990 | 501-1000 |
| Agent 3 | 1000-1490 | 1001-1500 |
| Agent 4 | 1500-2010 | 1501-2013 |

```bash
for offset in {START}..{END}..10; do
  curl -s "https://28dayreset.com/api/debug/sias-batch?offset=$offset&mode=dry_run"
done
```

## Phase 1: Dry Run

```bash
node scripts/sias-dryrun.js
```

### Expected Output
```
=== SIAS DRY RUN SUMMARY ===
Total users: 2013
Users with discrepancies: ~800-1000
Discrepancy types:
  ledger_balance_mismatch: ~600
  invalid_daily_habit: ~300
  invalid_admin_adjustment: ~50-100
```

## Phase 2: Analyze Results

### Priority Matrix

| Discrepancy | Priority | Points Impact | Action |
|-------------|----------|---------------|--------|
| invalid_admin_adjustment | HIGH | Positive (restore) | Apply fix |
| ledger_balance_mismatch | MEDIUM | Varies | Investigate |
| invalid_daily_habit | LOW | Negative (deduct) | Apply fix |
| duplicate_transaction | LOW | Negative (deduct) | Apply fix |

## Phase 3: Apply Fixes

### Option A: Full Batch
```bash
for offset in 0 10 20 ... 2010; do
  curl -s "https://28dayreset.com/api/debug/sias-batch?offset=$offset&mode=flexible"
  sleep 1
done
```

### Option B: Targeted (Recommended)
```bash
curl -s "https://28dayreset.com/api/debug/sias/{USER_ID}?mode=flexible"
```

## Verification

After fixes:
1. Re-run dry run to confirm resolution
2. Check specific users with large adjustments
3. Compare totals to expectations

## Error Handling

| Error | Action |
|-------|--------|
| API Timeout | Reduce batch size, add delays |
| Unexpected Results | Use fresh dry run |
| Partial Failures | Log failed IDs, retry individually |

## Safety Checklist

**Before flexible mode:**
- [ ] Completed full dry run
- [ ] Reviewed discrepancy breakdown
- [ ] Confirmed restoration users
- [ ] Verified no unexpected patterns

**After flexible mode:**
- [ ] Verified affected users have correct totals
- [ ] Re-ran dry run for confirmation
- [ ] Documented total points changed
