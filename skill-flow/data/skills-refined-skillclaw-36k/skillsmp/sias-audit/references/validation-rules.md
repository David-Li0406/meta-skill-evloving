# SIAS Validation Rules

## Biometric 2-Day Scoring Windows

Project Start: Day 1

| Window | Days | Points |
|--------|------|--------|
| Baseline | -2 to 7 | 25 (first entry) |
| Week 1 | 7-8 | 25 (if baseline exists) |
| Week 2 | 14-15 | 25 |
| Week 3 | 21-22 | 25 |
| Week 4 | 28-29 | 25 |

**Maximum**: 125 points (5 windows × 25 pts)

### Window Tracking Logic

```javascript
const windowsAwarded = {
  baseline: false,  // Days -2 to 7 (first entry only)
  week1: false,     // Days 7-8
  week2: false,     // Days 14-15
  week3: false,     // Days 21-22
  week4: false,     // Days 28-29
};

// For each entry (sorted by date):
// 1. Calculate project day
// 2. Check which window it falls into
// 3. If first entry in window and not yet awarded, score it
// 4. Mark window as awarded
// 5. Subsequent entries = "Tracking Only" (0 pts)
```

### Key Rules

1. **Baseline + Week 1 overlap**: Days 7-8 can score for EITHER baseline OR Week 1
2. **First entry wins**: Only FIRST entry per window scores
3. **Entity ID Formats**: `{userId}:2026-01-08` (date) or `{userId}:week1` (legacy)

## Transaction Types

| Type | Description | Points |
|------|-------------|--------|
| `biometric_submit` | Weekly biometric | 25 each |
| `daily_habit` | Daily habit | 1-4/day |
| `lesson_completion` | Lesson watched | 1 each |
| `quiz_completion` | Quiz completed | 1 each |
| `referral_facilitator` | Referral | varies |
| `referral_participant` | Referral | varies |
| `admin_adjustment` | Manual change | varies |
| `reconciliation` | SIAS correction | varies |

## Daily Habit Validation

**Valid Range**: Day 1 (12:00 AM) to Day 28 (11:59 PM)

Points outside this range = `invalid_daily_habit` discrepancy

## Lesson & Quiz Validation

**Valid Range**: Day 1 to Day 28

- Each lesson/quiz awards points only once
- Duplicates should not be counted

## Referral Validation

**Valid Range**: User creation through Day 28

- 1 point per referral
- **NEVER deducted by bulk resets** - always preserved

## Admin Adjustment Detection

`invalid_admin_adjustment` triggers when:
1. Net admin_adjustment is negative
2. At least one adjustment is a "bulk score reset"
3. User has valid earned points incorrectly zeroed

**Detection Pattern**: Description contains "bulk score reset" or "bulk reset"

## Ledger Balance Check

```javascript
const ledgerTotal = transactions.reduce((sum, tx) => sum + tx.points, 0);
const cachedTotal = user.points;

if (Math.abs(ledgerTotal - cachedTotal) > 0.001) {
  // MISMATCH - cached points don't match ledger
}
```

## Idempotency Keys

| Category | Key Format |
|----------|------------|
| Biometrics | `{userId}:week{N}` or `{userId}:{YYYY-MM-DD}` |
| Daily Habits | `{userId}:{YYYY-MM-DD}` |
| Lessons | Content ID |
| Quizzes | Quiz ID |

## Test Users

| Name | User ID | Expected |
|------|---------|----------|
| Elisabeth Hibdon Hunter | `004419b7-50b1-47fd-a887-a00772088af4` | NO changes - 50 pts correct |
| Tai Wotherspoon | `00eff86b-0857-47d4-b9a3-4ae009ded626` | +25 pts Week 1 |
| Bruce Moberg | `0174e5a6-049f-4f2b-aced-b90b576469fe` | Habits: 36 pts (not 38) |
| Kara Wood | `468ebbd5-e2a6-4986-bd5f-1d9129f0c8de` | NO changes - 50 pts correct |
| Russell (Admin) | `0f950f68-885c-47f9-9cb4-aabbb8bea55f` | NO changes - 100 pts correct |
