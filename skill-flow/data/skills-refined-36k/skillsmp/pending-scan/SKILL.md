---
name: pending-scan
description: Scan accounts to find those needing follow-up based on stage and days since last contact. Returns prioritized list.
---

# Pending Scan

## When to use this skill

- User asks "what accounts need follow-up?"
- Scheduled daily/weekly follow-up check
- Looking for accounts that have gone cold

## Scan criteria

Accounts need follow-up when:

1. Stage is actionable (not Bound, Closed Won, Closed Lost)
2. Days since last contact exceeds threshold for stage
3. Has pending actions or next steps

## Stage thresholds

See `references/stage-rules.md` for full details.

| Stage | Normal (days) | Urgent (days) | Primary Channel |
|-------|---------------|---------------|-----------------|
| New Lead | 2 | 4 | email |
| Intake | 2 | 4 | email |
| Application | 3 | 5 | email |
| Submission | 5 | 7 | email |
| Quote Pitched | 2 | 3 | call |
| Quoted | 2 | 3 | call |

## Urgency levels

- **Normal**: Days since contact > threshold
- **High**: Days since contact > urgent threshold
- **Critical**: Days since contact > urgent threshold + 2

## Output format

Returns list of `FollowUpAction`:

```json
{
  "account_id": "29041",
  "account_name": "Sunny Days Childcare",
  "stage": "Quote Pitched",
  "days_since_contact": 4,
  "urgency": "high",
  "recommended_channel": "call",
  "next_steps": ["Follow up on quote decision"],
  "pending_actions": ["Waiting for loss runs"]
}
```

## Filtering options

- By urgency level
- By stage
- By date range
- Limit results count
