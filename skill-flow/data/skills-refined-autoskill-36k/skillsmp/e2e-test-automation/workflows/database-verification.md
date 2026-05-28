# Database Verification Workflow

## Purpose

Verify database state after E2E actions using Supabase MCP tools.

---

## Prerequisites

- Supabase MCP server running
- Database accessible
- Test user ID known

---

## Phase 1: User State Verification

### 1.1 Get User Record

```
mcp__supabase__execute_sql
  query="SELECT id, telegram_id, email, chapter, relationship_score, created_at, updated_at
         FROM users
         ORDER BY created_at DESC
         LIMIT 5"
```

**Verify:**
- [ ] User record exists
- [ ] `chapter` is valid (1-5)
- [ ] `relationship_score` is reasonable (0-100)

### 1.2 Get User Metrics

```
mcp__supabase__execute_sql
  query="SELECT user_id, intimacy, passion, trust, secureness, updated_at
         FROM user_metrics
         ORDER BY updated_at DESC
         LIMIT 5"
```

**Verify:**
- [ ] Metrics record exists for user
- [ ] All 4 scores are present
- [ ] Values are valid (0-100 range)

### 1.3 Check Vice Preferences

```
mcp__supabase__execute_sql
  query="SELECT user_id, vice_category, intensity, confidence, updated_at
         FROM user_vice_preferences
         WHERE user_id = '<USER_ID>'
         ORDER BY intensity DESC"
```

**Verify:**
- [ ] Vice preferences populated (or empty if new user)
- [ ] `intensity` values reasonable (0-5)
- [ ] Valid `vice_category` values

---

## Phase 2: Conversation Verification

### 2.1 Recent Conversations

```
mcp__supabase__execute_sql
  query="SELECT id, user_id, type, user_message, nikita_response, processing_status, created_at
         FROM conversations
         ORDER BY created_at DESC
         LIMIT 10"
```

**Verify:**
- [ ] Conversations being logged
- [ ] `user_message` and `nikita_response` populated
- [ ] `processing_status` = 'processed' or 'pending'

### 2.2 Check Conversation Processing

```
mcp__supabase__execute_sql
  query="SELECT id, processing_status, summary, emotional_tone, entity_count, created_at
         FROM conversations
         WHERE processing_status = 'processed'
         ORDER BY created_at DESC
         LIMIT 5"
```

**Verify:**
- [ ] Processed conversations have `summary`
- [ ] `emotional_tone` populated
- [ ] `entity_count` > 0 (entities extracted)

---

## Phase 3: Engagement State Verification

### 3.1 Current Engagement State

```
mcp__supabase__execute_sql
  query="SELECT user_id, current_state, previous_state, calibration_progress,
                ideal_frequency, tolerance_band, updated_at
         FROM engagement_state
         ORDER BY updated_at DESC
         LIMIT 5"
```

**Verify:**
- [ ] Engagement state exists for active users
- [ ] `current_state` is valid (calibrating, engaged, drifting, concerned, recovering, lost)
- [ ] `calibration_progress` advancing (0-100)

### 3.2 Engagement Transitions

Check for recent state transitions:

```
mcp__supabase__execute_sql
  query="SELECT user_id, current_state, previous_state, updated_at
         FROM engagement_state
         WHERE previous_state IS NOT NULL
         ORDER BY updated_at DESC
         LIMIT 5"
```

---

## Phase 4: Score History Verification

### 4.1 Recent Score Changes

```
mcp__supabase__execute_sql
  query="SELECT id, user_id, score_type, old_value, new_value, change_reason, created_at
         FROM score_history
         ORDER BY created_at DESC
         LIMIT 10"
```

**Verify:**
- [ ] Score changes being logged
- [ ] `change_reason` populated (helps debugging)
- [ ] Changes are reasonable (not massive jumps)

### 4.2 Score Trend

```
mcp__supabase__execute_sql
  query="SELECT DATE(created_at) as date,
                score_type,
                AVG(new_value) as avg_score
         FROM score_history
         WHERE created_at > NOW() - INTERVAL '7 days'
         GROUP BY DATE(created_at), score_type
         ORDER BY date DESC"
```

---

## Phase 5: Generated Prompts Verification

### 5.1 Recent Prompts

```
mcp__supabase__execute_sql
  query="SELECT id, user_id, token_count, generation_time_ms, meta_prompt_template, created_at
         FROM generated_prompts
         ORDER BY created_at DESC
         LIMIT 10"
```

**Verify:**
- [ ] Prompts being logged (spec 012 Phase 4)
- [ ] `token_count` reasonable (~3000-5000)
- [ ] `generation_time_ms` acceptable (<500ms)

### 5.2 Prompt Content Check

```
mcp__supabase__execute_sql
  query="SELECT id, LEFT(prompt_content, 500) as preview, context_snapshot
         FROM generated_prompts
         ORDER BY created_at DESC
         LIMIT 1"
```

**Verify:**
- [ ] `prompt_content` contains personalized elements
- [ ] `context_snapshot` has expected fields

---

## Phase 6: Pending Registrations (OTP)

### 6.1 Check Pending Registrations

```
mcp__supabase__execute_sql
  query="SELECT id, telegram_id, email, otp_code, verification_attempts,
                expires_at, verified_at, created_at
         FROM pending_registrations
         ORDER BY created_at DESC
         LIMIT 5"
```

**Verify:**
- [ ] New registrations being created
- [ ] `expires_at` is in future for pending
- [ ] `verification_attempts` < max (3)

### 6.2 Clean Up Expired

```
mcp__supabase__execute_sql
  query="SELECT COUNT(*) as expired_count
         FROM pending_registrations
         WHERE expires_at < NOW() AND verified_at IS NULL"
```

---

## Phase 7: Table Row Counts

### 7.1 Overall Health Check

```
mcp__supabase__execute_sql
  query="SELECT
           (SELECT COUNT(*) FROM users) as users_count,
           (SELECT COUNT(*) FROM conversations) as conversations_count,
           (SELECT COUNT(*) FROM engagement_state) as engagement_count,
           (SELECT COUNT(*) FROM generated_prompts) as prompts_count,
           (SELECT COUNT(*) FROM score_history) as score_history_count"
```

**Expected (active system):**
- `users_count` > 0
- `conversations_count` > 0
- `engagement_count` ≈ `users_count`
- `prompts_count` > 0 (if spec 012 complete)

---

## Common Issues

| Issue | Query to Diagnose | Fix |
|-------|-------------------|-----|
| No conversations | Check user_id matches | Verify telegram_id → user mapping |
| Engagement missing | Check user has engagement_state | Create via SQL or fix create_with_metrics() |
| No prompts logged | Check spec 012 status | Verify session.commit() in agent.py |
| Stale data | Check updated_at timestamps | Run decay/summary tasks |
| Orphaned records | Check foreign key violations | Run cleanup tasks |

---

## Cleanup Queries (Safe)

### Mark Old Registrations Expired

```sql
UPDATE pending_registrations
SET expires_at = NOW() - INTERVAL '1 hour'
WHERE verified_at IS NULL
  AND expires_at < NOW();
```

### Count Orphaned Conversations

```sql
SELECT COUNT(*)
FROM conversations c
LEFT JOIN users u ON c.user_id = u.id
WHERE u.id IS NULL;
```

---

## Report Template

```markdown
## Database Verification Report

**Date**: [timestamp]
**User ID**: [if specific user]

### Table Health

| Table | Row Count | Recent Activity | Status |
|-------|-----------|-----------------|--------|
| users | X | Y new today | ✅/⚠️ |
| conversations | X | Y new today | ✅/⚠️ |
| engagement_state | X | Y updated | ✅/⚠️ |
| generated_prompts | X | Y new today | ✅/⚠️ |
| score_history | X | Y entries | ✅/⚠️ |

### Data Quality

| Check | Result | Notes |
|-------|--------|-------|
| User-Engagement 1:1 | ✅/❌ | [notes] |
| Conversations processed | X% | [notes] |
| Prompts logging | ✅/❌ | [notes] |

### Issues Found

- [List issues]

### Recommended Actions

- [List actions]
```

---

## Checklist

- [ ] User records valid
- [ ] Metrics populated
- [ ] Conversations being logged
- [ ] Post-processing working
- [ ] Engagement states tracking
- [ ] Scores being recorded
- [ ] Prompts being logged
- [ ] No orphaned records
