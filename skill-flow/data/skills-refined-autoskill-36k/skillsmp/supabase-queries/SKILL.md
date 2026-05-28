---
name: supabase-queries
description: Quick database queries and notification testing for sbhq-mobile. Use when querying contests, users, notifications, or testing push notifications.
allowed-tools: mcp__supabase__execute_sql, mcp__supabase__list_tables, mcp__supabase__get_edge_function
---

# Supabase Queries & Notification Testing

Quick reference for running database queries and testing notifications in sbhq-mobile.

## Database Schema Overview

### Core Tables

- **contests**: Contest data with state machine (UPCOMING → LOBBY_OPEN → ROUND_IN_PROGRESS → ROUND_CLOSED → FINISHED)
- **users**: User accounts with expo_push_token for notifications
- **participants**: Links users to contests, tracks elimination_round
- **questions**: Questions per contest/round with correct_option array
- **answers**: User answers per round
- **notification_log**: Deduplication log for sent notifications (dedupe_key is unique)

### Key Fields for Notifications

```sql
users.expo_push_token          -- Push notification token
users.push_token_updated_at    -- Token freshness
notification_log.dedupe_key    -- Format: {contestId}:{userId}:{suffix}
notification_log.notification_type -- STARTS_IN_10M, STARTS_IN_60S, QUESTION_OPEN, RESULT_POSTED
```

## RPC Functions

Call these using `mcp__supabase__execute_sql` with `SELECT * FROM function_name(args)`:

### check_username_available
```sql
SELECT * FROM check_username_available('desired_username')
-- Returns: boolean
```

### get_answer_distribution
```sql
SELECT * FROM get_answer_distribution(
  'contest-uuid-here'::uuid,
  1  -- round number
)
-- Returns: TABLE(answer text, count bigint)
```

## Common Queries

### Check Active Contests
```sql
SELECT id, name, state, current_round, start_time
FROM contests
WHERE state != 'FINISHED'
ORDER BY start_time DESC
```

### Get Users with Push Tokens
```sql
SELECT id, username, expo_push_token, push_token_updated_at
FROM users
WHERE expo_push_token IS NOT NULL
ORDER BY push_token_updated_at DESC NULLS LAST
LIMIT 10
```

### Check Notification History
```sql
SELECT
  nl.notification_type,
  nl.sent_at,
  u.username,
  c.name as contest_name,
  nl.round
FROM notification_log nl
JOIN users u ON nl.user_id = u.id
LEFT JOIN contests c ON nl.contest_id = c.id
ORDER BY nl.sent_at DESC
LIMIT 20
```

### Find Contest Participants (Active)
```sql
SELECT
  p.id,
  u.username,
  u.expo_push_token IS NOT NULL as has_push_token,
  p.elimination_round
FROM participants p
JOIN users u ON p.user_id = u.id
WHERE p.contest_id = 'contest-uuid-here'
  AND p.elimination_round IS NULL  -- Still active
ORDER BY u.username
```

### Check Answers for a Round
```sql
SELECT
  u.username,
  a.answer,
  a.timestamp
FROM answers a
JOIN participants p ON a.participant_id = p.id
JOIN users u ON p.user_id = u.id
WHERE a.contest_id = 'contest-uuid-here'
  AND a.round = 1
ORDER BY a.timestamp
```

## Edge Function: send-notification

Get the function code:
```
mcp__supabase__get_edge_function("send-notification")
```

### Notification Types

- **STARTS_IN_10M**: Contest starting in 10 minutes → /lobby
- **STARTS_IN_60S**: Contest starting in 60 seconds → /game/{contestId}
- **QUESTION_OPEN**: New round is live → /game/{contestId}?round={round}
- **RESULT_POSTED**: Results available → /game/{contestId}

### Test Notification Payload

To test notifications, you'll need to invoke the edge function via HTTP (outside Claude):

```bash
curl -X POST https://your-project.supabase.co/functions/v1/send-notification \
  -H "Authorization: Bearer YOUR_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contestId": "uuid-here",
    "type": "STARTS_IN_10M"
  }'
```

For round-specific notifications:
```json
{
  "contestId": "uuid-here",
  "type": "QUESTION_OPEN",
  "round": 1
}
```

For targeted notifications:
```json
{
  "contestId": "uuid-here",
  "type": "RESULT_POSTED",
  "round": 1,
  "targetUserIds": ["user-uuid-1", "user-uuid-2"]
}
```

### Deduplication Logic

The edge function uses `notification_log.dedupe_key` to prevent duplicate sends:

- **STARTS_IN_10M**: `{contestId}:{userId}:starts_in_10m`
- **STARTS_IN_60S**: `{contestId}:{userId}:starts_in_60s`
- **QUESTION_OPEN**: `{contestId}:{userId}:round_{round}:open`
- **RESULT_POSTED**: `{contestId}:{userId}:round_{round}:result`

Query to check if notification was already sent:
```sql
SELECT * FROM notification_log
WHERE dedupe_key = '{contestId}:{userId}:starts_in_10m'
```

## Quick Testing Workflow

### 1. Find a Test Contest
```sql
SELECT id, name, state FROM contests ORDER BY created_at DESC LIMIT 5
```

### 2. Check Who Can Receive Notifications
```sql
SELECT
  u.id,
  u.username,
  u.expo_push_token IS NOT NULL as can_notify
FROM users u
JOIN participants p ON u.id = p.user_id
WHERE p.contest_id = 'YOUR_CONTEST_ID'
  AND p.elimination_round IS NULL
```

### 3. Check Notification History for Contest
```sql
SELECT
  notification_type,
  COUNT(*) as sent_count,
  MAX(sent_at) as last_sent
FROM notification_log
WHERE contest_id = 'YOUR_CONTEST_ID'
GROUP BY notification_type
ORDER BY last_sent DESC
```

### 4. Clear Notification History (if testing)
```sql
DELETE FROM notification_log
WHERE contest_id = 'YOUR_CONTEST_ID'
  AND notification_type = 'STARTS_IN_10M'
-- Returns count of deleted rows
```

## Pro Tips

1. **Always check notification_log first** to see what's been sent
2. **Verify expo_push_token exists** before expecting notifications
3. **Use dedupe_key format** to understand what prevents duplicates
4. **Contest state matters** - participants check `elimination_round IS NULL`
5. **Round numbers start at 1** (not 0)
6. **Notification batching** - edge function chunks messages into batches of 100

## Debugging Notifications

### No notifications sent?
```sql
-- Check 1: Do users have tokens?
SELECT COUNT(*) FROM users WHERE expo_push_token IS NOT NULL;

-- Check 2: Are there active participants?
SELECT COUNT(*)
FROM participants
WHERE contest_id = 'YOUR_ID'
  AND elimination_round IS NULL;

-- Check 3: Was it already sent?
SELECT * FROM notification_log
WHERE contest_id = 'YOUR_ID'
  AND notification_type = 'YOUR_TYPE';
```

### Check edge function logs
```
mcp__supabase__get_logs("edge-function")
```

### List all edge functions
```
mcp__supabase__list_edge_functions()
```

## MCP Tools Reference

- `mcp__supabase__execute_sql(query)` - Run any SQL query
- `mcp__supabase__list_tables(schemas)` - List all tables
- `mcp__supabase__get_edge_function(function_slug)` - Get function code
- `mcp__supabase__list_edge_functions()` - List all edge functions
- `mcp__supabase__get_logs(service)` - Get logs (api, postgres, edge-function, auth, etc.)
- `mcp__supabase__apply_migration(name, query)` - Run migrations (DDL only)
- `mcp__supabase__get_advisors(type)` - Security/performance advisories
