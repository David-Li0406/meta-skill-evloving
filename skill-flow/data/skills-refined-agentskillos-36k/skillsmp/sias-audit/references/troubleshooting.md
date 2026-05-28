# SIAS Troubleshooting Guide

## Common Scenarios and How to Handle Them

### Scenario 1: User Missing Points for Completed Action

**User says**: "I watched the video but didn't get my point"

**Investigation**:
1. Check UserProgressEntity for the content
   - `GET /api/course/progress` with `X-User-ID` header
   - Look for `completedAt` timestamp
2. Check ledger for corresponding transaction
   - `GET /api/debug/ledger/{userId}`
   - Search for `lesson_completion` with matching content

**Possible Causes**:
- **Ledger entry missing**: UserProgress shows completed, ledger doesn't have entry
  - Fix: Rebuild ledger (`POST /api/debug/ledger/{userId}/rebuild`)
- **Progress record missing**: Ledger has entry but UserProgress empty
  - Fix: Backfill progress (`POST /api/debug/backfill-progress/{userId}`)
- **Both missing**: Neither has record
  - Investigate: Check if video reached 90% completion threshold

---

### Scenario 2: Points Don't Match Display

**Symptom**: Header shows 150, but breakdown adds to 145

**Investigation**:
```
POST /api/debug/ledger/{userId}/rebuild
Body: { "dryRun": true }
```

Look at:
- `currentState.cachedPoints` (what header shows)
- `currentState.ledgerTotal` (sum of transactions)
- `expectedTotal` (calculated from source entities)

**Possible Causes**:
- **Cache mismatch**: Sync interrupted during write
  - Fix: `POST /api/debug/ledger/{userId}/sync-points`
- **Ledger mismatch**: Transactions don't match source
  - Fix: Rebuild ledger
- **Source mismatch**: Data integrity issue
  - Escalate: Needs deeper investigation

---

### Scenario 3: Duplicate Transactions

**Symptom**: Same action credited twice

**Investigation**:
1. View full ledger: `GET /api/debug/ledger/{userId}`
2. Look for entries with same `relatedEntityId` or similar timestamps
3. Check `idempotencyKey` if present (should be unique)

**Causes**:
- Pre-SIAS data without idempotency protection
- Network retry during submission

**Fix**:
- Delete the duplicate: `DELETE /api/debug/ledger/{userId}/transaction/{txId}`
- Or rebuild (preferred): `POST /api/debug/ledger/{userId}/rebuild`

---

### Scenario 4: Biometric Points Incorrect

**Symptom**: User submitted biometric but got 0 points, or got 25 when shouldn't

**Investigation**:
```
GET /api/debug/biometric-entries/{userId}
```

Check each entry's:
- `projectDay` - is it in a valid window (7-8, 14-15, 21-22, 28-29)?
- `isPointEligible` - does entity think it should score?
- `pointsAwarded` - what was actually awarded?
- `actualLabel` vs `expectedLabel` - do they match?
- `labelMismatch` or `pointsMismatch` flags

**Common Issues**:
- **Outside window**: Submitted on Day 13 (not 14-15)
  - Resolution: Explain window rules to user; no fix if rules are correct
- **Already had entry in window**: First entry scored, second didn't
  - Resolution: Correct behavior; explain to user
- **Missing baseline**: Week 1 didn't score because no baseline
  - Check if Day -2 to 7 had a submission
- **Day 8/15/22/29 not recognized**: The 48-hour windows include BOTH days
  - Example: Day 8 is valid for Week 1 (not just Day 7)
  - If entry on Day 8 shows 0 points, rebuild will fix it

---

### Scenario 4B: Biometric Shows "Tracking Only" Instead of "Scored Entry"

**Symptom**: User sees "Tracking Only" in their Weigh-In Log, but they should have earned points

**Investigation**:
```
GET /api/debug/biometric-entries/{userId}
```

Check:
- Is `actualLabel` showing "Tracking Only"?
- Is `expectedLabel` showing "Scored Entry"?
- Is `labelMismatch: true`?

**Cause**: The `WeeklyBiometricEntity` metadata was not updated when points were awarded:
- `pointsAwarded` is 0 or null
- `isPointEligible` is false
- `weekNumber` is wrong or null

**Fix**: Rebuild ledger - it now updates the entity metadata:
```
POST /api/debug/ledger/{userId}/rebuild
Body: { "dryRun": false }
```

The rebuild will:
- Award points for valid biometric submissions
- Update `WeeklyBiometricEntity` with `pointsAwarded`, `weekNumber`, `isPointEligible`
- This makes the UI show "Scored Entry" correctly

**Verification**:
After rebuild, run biometric-entries again and verify:
- `actualLabel` matches `expectedLabel`
- `labelMismatch: false`
- `pointsMismatch: false`

---

### Scenario 5: Messy Ledger (Reconciliation Entries)

**Symptom**: Ledger has many `reconciliation` or `compensating` entries

**Cause**: Previous SIAS runs or manual fixes

**Assessment**:
1. Run dry-run rebuild to see expected vs actual
2. If significant gap, rebuild is cleaner

**Fix**:
```
POST /api/debug/ledger/{userId}/rebuild
Body: { "dryRun": false, "preserveReferrals": true }
```

This will:
- Delete all non-referral transactions
- Recreate from source entities
- Result in clean ledger

---

### Scenario 6: Missing Activity History (Lessons/Quizzes Not Showing)

**Symptom**: Dashboard Activity History is empty or shows fewer lessons than expected

**Investigation**:
1. Check course history API:
   ```bash
   curl -s "https://28dayreset.com/api/course/history" -H "X-User-ID: {targetUserId}"
   ```
2. Count lessons returned vs expected
3. Check ledger: `GET /api/debug/ledger/{userId}`
4. Look for lesson_completion entries with `relatedEntityId: null`

**Causes**:
- **Null relatedEntityId**: Old entries created before proper tracking
- **Wrong relatedEntityId format**: UI expects `{enrollmentId}:{contentId}`
- **Legacy completions with pointsAwarded=0**: Old records before points tracking

**Fix**: Rebuild ledger - reconstructs all lesson entries with proper format:
```
POST /api/debug/ledger/{userId}/rebuild
Body: { "dryRun": false }
```

The rebuild will:
- Create lesson transactions with `relatedEntityId: {enrollmentId}:{contentId}`
- Award 1 point for completed videos even if source has `pointsAwarded: 0`
- Preserve original `completedAt` timestamps

**Verification**:
After rebuild, check course history again - should now show all lessons with titles

---

### Scenario 7: Referral Points Wrong

**Symptom**: User should have more/fewer referral points

**Investigation**:
1. Count referrals: Look at users with `recruitedById` = this user
2. Check referral ledger entries
3. Verify each recruit is active

**Important**: NEVER reduce referral points without strong evidence of fraud

**If Missing Points**:
- Add transaction:
```
POST /api/debug/ledger/{userId}/add-transaction
Body: {
  "transactionType": "referral_participant",
  "points": 5,
  "relatedUserId": "{recruitId}",
  "description": "Referral credit for {Name}"
}
```

---

### Scenario 8: Daily Habits Not Scoring

**Symptom**: User logs habits but points don't increase

**Investigation**:
1. Check DailyScoreEntity: What date is the entry for?
2. Check project day: Is it Day 1-28?
3. Check ledger: Is there a `daily_habit` entry?

**Common Issues**:
- **Outside window**: Day 0 or Day 29+ doesn't score
- **Already scored today**: Max 3 points per day
- **Timezone mismatch**: Server vs user timezone

---

### Scenario 9: Quiz Didn't Award Points

**Symptom**: User passed quiz but no points

**Investigation**:
1. Check UserProgress for quiz: Was it marked completed?
2. Check score: Was it ≥85% (passing)?
3. Check ledger: Is there a `quiz_completion` entry?
4. Check attempts: Were they within max attempts?

**Causes**:
- Score below passing threshold
- Already completed (duplicate attempt)
- Ledger write failed (rebuild will fix)

---

### Scenario 10: System-Wide Issue

**Symptom**: Multiple users report same problem

**Investigation**:
1. Run batch audit: `GET /api/debug/sias-batch?mode=dry_run&offset=0`
2. Look for patterns in `affectedUsers`
3. Check recent deployments or data migrations

**Escalation**:
- This needs human review
- Document pattern, affected user count, and common characteristics
- Do NOT batch-fix without explicit permission

---

## Scenario 11: Subrequest Limit Error During Rebuild

**Symptom**: Rebuild fails with "Too many API requests by single worker invocation"

**Cause**: User has many transactions (referrals, lessons, habits) and the rebuild exceeds Cloudflare's 1,000 subrequest limit per invocation.

**Fix**: Use **staged rebuild** to process one category at a time:

```bash
# Step 1: Clear ledger completely and rebuild biometrics
POST /api/debug/ledger/{userId}/rebuild
Body: { "dryRun": false, "resetLedger": true, "stage": "biometrics" }

# Step 2: Add habits (no resetLedger - ledger already cleared)
POST /api/debug/ledger/{userId}/rebuild
Body: { "dryRun": false, "stage": "habits" }

# Step 3: Add lessons/quizzes
POST /api/debug/ledger/{userId}/rebuild
Body: { "dryRun": false, "stage": "lessons" }

# Step 4: Add referrals
POST /api/debug/ledger/{userId}/rebuild
Body: { "dryRun": false, "stage": "referrals" }
```

**Key Parameters:**
- `resetLedger: true` - Completely clears the ledger index (use on FIRST stage only)
- `stage: 'biometrics' | 'habits' | 'lessons' | 'referrals'` - Only process that category

**When to use:**
- User has > 50 referrals
- User has > 80 lesson completions
- Previous full rebuild failed with subrequest error
- Ledger has ghost/orphan transactions (points:0, description:"", createdAt:0)

**Why it works:**
- Each stage only fetches data needed for that category
- Skips expensive operations like idempotency key listing
- `resetLedger` uses `Index.clear()` instead of iterating through entries

**For 100+ referrals:** The referrals stage automatically chunks and returns continuation info:
```bash
# First call processes up to 100 referrals
POST /api/debug/ledger/{userId}/rebuild
Body: { "dryRun": false, "stage": "referrals" }
# Response includes: { "referralContinuation": { "nextOffset": 100, "remaining": 50 } }

# Continue from where we left off
POST /api/debug/ledger/{userId}/rebuild
Body: { "dryRun": false, "stage": "referrals", "referralOffset": 100 }
```

---

## Scenario 12: Ghost/Orphan Transactions in Ledger

**Symptom**: Ledger has entries with `points: 0`, `description: ""`, `createdAt: 0`, or `relatedEntityId: null`

**Cause**:
- Partial rebuilds that failed partway through
- Durable Object resets that corrupted index
- Previous SIAS fix attempts that created malformed entries

**Investigation**:
```bash
GET /api/debug/ledger/{userId}
# Look for transactions with empty descriptions or 0 points
```

**Fix**: Use `resetLedger` to completely clear and rebuild:
```bash
# Use staged rebuild for large users, or full rebuild for small users:

# Option A: Full rebuild with resetLedger (small users)
POST /api/debug/ledger/{userId}/rebuild
Body: { "dryRun": false, "resetLedger": true }

# Option B: Staged rebuild with resetLedger (large users)
# See Scenario 11 for full sequence
POST /api/debug/ledger/{userId}/rebuild
Body: { "dryRun": false, "resetLedger": true, "stage": "biometrics" }
```

**Why resetLedger is needed:**
- Normal rebuild tries to delete each transaction individually
- Ghost transactions may not have valid IDs or may return "Transaction does not belong to this user"
- `resetLedger` uses `Index.clear()` which removes ALL index entries regardless of their state

---

### Scenario 13: Habits Show 0 Points but User Logged Daily (NOW AUTO-FIXED)

**Symptom**: User logged habits for weeks but dry-run shows `totalDays: 0`, `expectedPoints: 0`

**Cause**: The `user-scores:{userId}` secondary index was corrupted/empty while DailyScoreEntity records exist.

**GOOD NEWS**: As of January 2026, the SIAS rebuild now **scans entities directly by date pattern**, completely bypassing the secondary index. This means:

- Index corruption no longer causes habits to show 0 points
- Standard rebuild with `stage: "habits"` will find all habit data
- No need to manually rebuild the index first

**Fix** (simple now):
```bash
# Just run the habits stage - it scans directly by date, bypassing the index
curl -s -X POST "https://28dayreset.com/api/debug/ledger/{userId}/rebuild" \
  -H "X-User-ID: 0f950f68-885c-47f9-9cb4-aabbb8bea55f" \
  -H "Content-Type: application/json" \
  -d '{"dryRun": false, "stage": "habits"}'
```

**If you want to also fix the index** (optional):
```bash
# This is now optional - rebuild works without it
curl -s -X POST "https://28dayreset.com/api/debug/rebuild-daily-score-index/{userId}" \
  -H "X-User-ID: 0f950f68-885c-47f9-9cb4-aabbb8bea55f" \
  -H "Content-Type: application/json" \
  -d '{"startDate": "2026-01-01", "endDate": "2026-01-28", "dryRun": false}'
```

**Technical details:**
- The rebuild now iterates through Day 1-28 checking `{userId}:{YYYY-MM-DD}` entities directly
- Each date is checked regardless of whether it's in the index
- The index is also fixed as a side effect of the rebuild
- `continueHabits: true` is no longer needed - standard rebuild works

---

## Error Codes and Responses

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Proceed |
| 400 | Bad request | Check parameters |
| 400 + "No enrollment" | User not enrolled | Can't audit until enrolled |
| 404 | User not found | Verify user ID |
| 409 | Conflict | Retry after delay |
| 429 | Rate limited | Wait 60s |
| 500 | Server error | Check logs, may need support |
| "Too many API requests" | Subrequest limit | Use staged rebuild (Scenario 11) |

---

## When to Escalate

**Always escalate** these situations to human review:
- Discrepancy > 100 points
- User is complaining/disputing
- Pattern affects multiple users
- Data seems fraudulent
- You're not confident in the fix

**How to escalate**:
1. Document findings thoroughly
2. Include all evidence gathered
3. State your hypothesis and confidence level
4. List what you've already tried
5. Recommend next steps for human reviewer
