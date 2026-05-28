# E2E Test Failure Modes

## Quick Diagnosis

| Symptom | Most Likely Cause | First Check |
|---------|-------------------|-------------|
| No bot response | Cloud Run cold start | Wait 30s, retry |
| Empty response | LLM error | Check gcloud logs |
| 500 error | Code exception | Check stack trace |
| No email | Rate limit/config | Check Supabase logs |
| DB empty | Session not committed | Check code for commit() |
| Timeout | Slow service | Check performance metrics |

---

## Category 1: Infrastructure Failures

### Cloud Run Cold Start

**Symptom:** First request takes 30-60s or times out.

**Diagnosis:**
```bash
gcloud run services logs read nikita-api --limit 50 | grep -i "cold\|startup"
```

**Resolution:**
1. Wait for cold start to complete
2. Retry request
3. Consider min-instances if frequent

### Cloud Run Not Deployed

**Symptom:** Connection refused or 404.

**Diagnosis:**
```bash
gcloud run services describe nikita-api --region us-central1
```

**Resolution:**
1. Verify service exists
2. Check deployment status
3. Redeploy if needed

### Database Connection Failed

**Symptom:** 500 errors mentioning database/Supabase.

**Diagnosis:**
```bash
gcloud run services logs read nikita-api --limit 100 | grep -i "database\|supabase\|connection"
```

**Resolution:**
1. Check DATABASE_URL env var
2. Verify Supabase is up
3. Check RLS policies

---

## Category 2: Authentication Failures

### Invalid Webhook Signature

**Symptom:** 401/403 on Telegram webhook.

**Diagnosis:**
```bash
gcloud run services logs read nikita-api --limit 100 | grep -i "signature\|auth\|401"
```

**Resolution:**
1. Verify TELEGRAM_WEBHOOK_SECRET in Cloud Run
2. Check secret matches Telegram bot settings
3. Verify signature validation code

### JWT Verification Failed

**Symptom:** Portal API returns 401.

**Diagnosis:**
```bash
gcloud run services logs read nikita-api --limit 100 | grep -i "jwt\|token\|unauthorized"
```

**Resolution:**
1. Check SUPABASE_JWT_SECRET
2. Verify token not expired
3. Check token format

### Rate Limit Exceeded

**Symptom:** 429 responses.

**Diagnosis:**
```bash
mcp__supabase__execute_sql query="SELECT * FROM rate_limits ORDER BY last_request DESC LIMIT 10"
```

**Resolution:**
1. Wait for rate limit window to reset
2. Clear rate limit entries for test user
3. Adjust rate limit config if too aggressive

---

## Category 3: External Service Failures

### OpenAI Quota Exceeded

**Symptom:** No LLM response, memory operations fail.

**Diagnosis:**
```bash
gcloud run services logs read nikita-api --limit 100 | grep -i "openai\|quota\|rate"
```

**Resolution:**
1. Check OpenAI dashboard for quota status
2. Upgrade plan if needed
3. Wait for quota reset

### Neo4j Connection Failed

**Symptom:** Memory operations fail, but LLM still works.

**Diagnosis:**
```bash
gcloud run services logs read nikita-api --limit 100 | grep -i "neo4j\|graphiti\|memory"
```

**Resolution:**
1. Check NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD
2. Verify Neo4j Aura instance is running
3. Check credentials haven't expired

### Email Delivery Failed

**Symptom:** OTP email never arrives.

**Diagnosis:**
1. Check Supabase Auth logs
2. Check Resend dashboard (if SMTP configured)
3. Check spam folder

**Resolution:**
1. Verify SMTP configuration in Supabase
2. Check email rate limits (2/hour on free Supabase)
3. Verify recipient email is valid

---

## Category 4: Code/Logic Failures

### Session Not Committed

**Symptom:** Data not persisted to database.

**Diagnosis:**
```sql
-- Check if rows exist
SELECT COUNT(*) FROM conversations WHERE created_at > NOW() - INTERVAL '1 hour';
```

**Resolution:**
1. Add `session.commit()` after operations
2. Check for exceptions before commit
3. Verify transaction boundaries

### Missing Initialization

**Symptom:** NoneType errors, missing data.

**Diagnosis:**
```bash
gcloud run services logs read nikita-api --limit 100 | grep -i "nonetype\|attributeerror"
```

**Common cases:**
- EngagementState not created for user
- UserMetrics not initialized
- Memory client not initialized

**Resolution:**
1. Add initialization in user creation flow
2. Create missing records via SQL
3. Add defensive checks in code

### Wrong Field Access

**Symptom:** AttributeError in logs.

**Diagnosis:**
```bash
gcloud run services logs read nikita-api --limit 100 | grep -A 5 "AttributeError"
```

**Common cases:**
- Pydantic AI: `result.data` vs `result.output`
- Model fields renamed
- API changes

**Resolution:**
1. Check latest library documentation
2. Update field access
3. Add tests for the pattern

---

## Category 5: Configuration Failures

### Missing Environment Variable

**Symptom:** KeyError or None value for config.

**Diagnosis:**
```bash
gcloud run services describe nikita-api --region us-central1 --format='value(spec.template.spec.containers[0].env)'
```

**Resolution:**
1. Add missing env var to Cloud Run
2. Update deployment config
3. Redeploy

### Wrong Environment Mode

**Symptom:** Development behavior in production (or vice versa).

**Diagnosis:**
```bash
gcloud run services describe nikita-api --format='value(spec.template.spec.containers[0].env)' | grep -i "environment\|debug"
```

**Resolution:**
1. Set ENVIRONMENT=production
2. Set DEBUG=false
3. Redeploy

---

## Category 6: Test Setup Failures

### MCP Server Not Running

**Symptom:** Tool not found errors.

**Diagnosis:**
```
MCPSearch query="telegram"
```

**Resolution:**
1. Check MCP server configuration
2. Restart MCP servers
3. Verify tool names

### Bot Chat Not Found

**Symptom:** Can't find Nikita bot in chat list.

**Diagnosis:**
```
mcp__telegram-mcp__list_chats
```

**Resolution:**
1. User needs to start conversation with bot first
2. Send /start to @Nikita_my_bot in Telegram app
3. Retry list_chats

### Portal Not Deployed

**Symptom:** Chrome DevTools can't load page.

**Diagnosis:**
Check Vercel dashboard for deployment status.

**Resolution:**
1. Verify Vercel deployment
2. Check build logs
3. Redeploy if needed

---

## Recovery Procedures

### Procedure 1: Reset User State

When user data is corrupted or stuck:

```sql
-- Reset engagement state
UPDATE engagement_state
SET current_state = 'calibrating',
    calibration_progress = 0,
    previous_state = NULL
WHERE user_id = '<USER_ID>';

-- Clear rate limits
DELETE FROM rate_limits WHERE user_id = '<USER_ID>';

-- Reset scores
UPDATE users
SET relationship_score = 50,
    chapter = 1
WHERE id = '<USER_ID>';
```

### Procedure 2: Clear Stuck Registrations

When OTP flow is stuck:

```sql
-- Clear expired registrations
DELETE FROM pending_registrations
WHERE expires_at < NOW();

-- Clear specific user's registrations
DELETE FROM pending_registrations
WHERE telegram_id = '<TELEGRAM_ID>';
```

### Procedure 3: Force Reprocessing

When post-processing failed:

```sql
-- Reset conversation for reprocessing
UPDATE conversations
SET processing_status = 'pending',
    summary = NULL,
    emotional_tone = NULL
WHERE id = '<CONVERSATION_ID>';
```

---

## Escalation Matrix

| Severity | Condition | Action |
|----------|-----------|--------|
| P0 | System completely down | Immediate investigation |
| P1 | Core flow broken | Fix within 1 hour |
| P2 | Feature degraded | Fix within 1 day |
| P3 | Minor issue | Log and schedule |

### When to Create GitHub Issue

Create issue when:
- Bug requires code change to fix
- Issue is reproducible
- Issue affects production
- Issue is not a configuration problem

### Issue Template

```markdown
## Bug Report

**Severity**: P0/P1/P2/P3

**Description**: [What's broken]

**Steps to Reproduce**:
1. ...
2. ...

**Expected**: [What should happen]

**Actual**: [What happened]

**Evidence**:
- Logs: [excerpt]
- DB state: [query result]
- Screenshots: [if applicable]

**Root Cause Analysis**: [if known]

**Proposed Fix**: [if known]
```
