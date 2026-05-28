# Telegram Bot Testing Workflow

## Purpose

Test Telegram bot interactions end-to-end using Telegram MCP tools.

---

## Prerequisites

- Telegram MCP server running (`mcp__telegram-mcp__*` tools available)
- Bot chat accessible (user has interacted with @Nikita_my_bot)
- Cloud Run service deployed and healthy

---

## Phase 1: Setup

### 1.1 Get Current User

```
mcp__telegram-mcp__get_me
```

**Expected Response:**
```json
{
  "id": 123456789,
  "first_name": "Test",
  "username": "testuser"
}
```

### 1.2 Find Bot Chat

```
mcp__telegram-mcp__list_chats
```

Look for:
- Chat with bot username (e.g., "Nikita", "@Nikita_my_bot")
- Or search by known bot ID

**If bot chat not found:**
1. User needs to start conversation with bot first
2. Send `/start` to @Nikita_my_bot in Telegram app
3. Retry `list_chats`

### 1.3 Get Bot Chat ID

From `list_chats` response, extract the `id` of the bot chat.
Store as `BOT_CHAT_ID` for subsequent operations.

---

## Phase 2: Basic Interaction Test

### 2.1 Send Test Message

```
mcp__telegram-mcp__send_message
  chat_id="<BOT_CHAT_ID>"
  text="Hey, how are you doing today?"
```

**Expected:** Message sent confirmation

### 2.2 Wait for Response

Bot response requires:
- Webhook processing (~1s)
- LLM generation (~2-5s)
- Response delivery (~1s)

**Wait:** 10 seconds minimum

### 2.3 Get Recent Messages

```
mcp__telegram-mcp__get_messages
  chat_id="<BOT_CHAT_ID>"
  limit=5
```

**Verify:**
- [ ] Bot responded (message from bot after our test message)
- [ ] Response is coherent (not error message)
- [ ] Response arrived within reasonable time

---

## Phase 3: Conversation Flow Test

### 3.1 Multi-Turn Conversation

Send a sequence of messages to test conversation memory:

**Message 1:**
```
mcp__telegram-mcp__send_message
  chat_id="<BOT_CHAT_ID>"
  text="I'm thinking about starting a new hobby"
```

Wait 10s, verify response.

**Message 2:**
```
mcp__telegram-mcp__send_message
  chat_id="<BOT_CHAT_ID>"
  text="Maybe something creative, like painting"
```

Wait 10s, verify response references "hobby" context.

**Message 3:**
```
mcp__telegram-mcp__send_message
  chat_id="<BOT_CHAT_ID>"
  text="What do you think I should try first?"
```

Wait 10s, verify response is contextually relevant.

### 3.2 Verify Conversation Context

Check if bot maintains context across messages:
- [ ] Bot references previous topics
- [ ] No context loss between messages
- [ ] Nikita persona maintained

---

## Phase 4: Database Verification

After conversation, verify database state:

### 4.1 Check Conversations Table

```
mcp__supabase__execute_sql
  query="SELECT id, user_id, type, nikita_response, created_at
         FROM conversations
         ORDER BY created_at DESC
         LIMIT 5"
```

**Verify:**
- [ ] New conversation rows created
- [ ] `nikita_response` populated (not null)
- [ ] Timestamps are recent

### 4.2 Check Engagement State

```
mcp__supabase__execute_sql
  query="SELECT user_id, current_state, calibration_progress, updated_at
         FROM engagement_state
         ORDER BY updated_at DESC
         LIMIT 1"
```

**Verify:**
- [ ] `current_state` reflects interaction (calibrating → engaged)
- [ ] `updated_at` is recent

### 4.3 Check Generated Prompts

```
mcp__supabase__execute_sql
  query="SELECT id, user_id, token_count, generation_time_ms, created_at
         FROM generated_prompts
         ORDER BY created_at DESC
         LIMIT 5"
```

**Verify:**
- [ ] New prompt logs created
- [ ] `token_count` reasonable (~3000-5000)
- [ ] `generation_time_ms` acceptable (<500ms)

---

## Phase 5: Edge Case Testing

### 5.1 Empty Message

```
mcp__telegram-mcp__send_message
  chat_id="<BOT_CHAT_ID>"
  text=""
```

**Expected:** Bot handles gracefully (ignores or asks for clarification)

### 5.2 Long Message

```
mcp__telegram-mcp__send_message
  chat_id="<BOT_CHAT_ID>"
  text="[500+ character message about a complex topic...]"
```

**Expected:** Bot processes and responds appropriately

### 5.3 Rapid Messages

Send 3 messages with 1s gaps:

**Expected:** Bot rate limits or queues appropriately

---

## Phase 6: Report Results

### 6.1 Test Summary

```markdown
## Telegram E2E Test Results

| Test | Status | Evidence |
|------|--------|----------|
| Bot chat found | PASS/FAIL | chat_id: XXX |
| Basic response | PASS/FAIL | Response in Xs |
| Multi-turn context | PASS/FAIL | Referenced previous topic |
| DB persistence | PASS/FAIL | X rows created |
| Engagement update | PASS/FAIL | State: calibrating |
| Prompt logging | PASS/FAIL | X prompts logged |
```

### 6.2 Log to Event Stream

```
[TIMESTAMP] E2E_TEST: telegram - PASS/FAIL - [summary]
```

---

## Common Failures

| Symptom | Likely Cause | Recovery |
|---------|--------------|----------|
| No bot response | Cloud Run cold start | Retry after 30s |
| Response timeout | LLM latency | Check gcloud logs |
| "Error" in response | Internal exception | Check stack trace in logs |
| DB rows missing | Session not committed | Check code for session.commit() |
| Engagement not updated | Missing EngagementState | Create via SQL |

---

## Checklist

- [ ] Bot chat ID obtained
- [ ] Basic interaction successful
- [ ] Multi-turn context maintained
- [ ] Database rows created
- [ ] Engagement state updated
- [ ] No errors in bot responses
- [ ] Response times acceptable
