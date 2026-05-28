---
name: replay-dead-letters
description: Replay failed observations after bug fixes or database issues. Shows which observations succeed and fail, helping recover from failures and validate fixes work on real data.
---

# Replay Dead Letters

**Purpose:** Operational task for recovering from failures and validating fixes.

## Instructions for Claude

When this skill is invoked:

1. **Parse flags:**
   - `--limit N`: replay only first N dead letters (default: all pending)
   - `--dry-run`: simulate without actually updating (default: false)
   - `--filter TYPE`: only replay specific source type (visit/scan)

2. **Create and run a Node.js script** that:

   **Step 1: Query dead letters**
   - Find all with `status: 'pending'`
   - Apply filters if provided
   - Show count and sample errors

   **Step 2: Replay each one**
   - Load original observation (Visit or Scan)
   - Attempt PersonController.upsertFromObservation()
   - Track success/failure
   - Update DeadLetter status accordingly

   **Step 3: Report results**
   - Show summary stats
   - List successful replays
   - List still-failing (with new errors)
   - Suggest next actions

3. **Output format:**
   ```
   REPLAY DEAD LETTERS
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   📋 Configuration:
   • Limit: [N] records
   • Dry run: [yes/no]
   • Filter: [type]

   📊 Found [X] pending dead letters

   Common errors:
   • INVALID_IDENTIFIER: [count]
   • MISSING_STABLE_ID: [count]
   • DUPLICATE_PERSON: [count]

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   🔄 Replaying...

   ✓ 1/10 - Observation [id] → Person [canonical_id]
   ✓ 2/10 - Observation [id] → Person [canonical_id]
   ✗ 3/10 - Observation [id] → Still fails: [error]
   ✓ 4/10 - Observation [id] → Person [canonical_id]
   ...

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   📈 RESULTS:
   ✓ Successful:  [Y]  ([Y/X * 100]%)
   ✗ Still failing: [Z]  ([Z/X * 100]%)

   NEXT ACTIONS:
   1. Investigate still-failing observations
   2. Fix root cause of [most common error]
   3. Run /replay-dead-letters again
   ```

## Error Handling

- If no pending dead letters: celebrate and notify
- If DB errors during replay: log, mark as 'failed_again', continue
- If observation not found: mark dead letter as 'skipped'
