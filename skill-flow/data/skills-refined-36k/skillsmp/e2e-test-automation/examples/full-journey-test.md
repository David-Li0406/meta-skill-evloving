# Full Journey E2E Test Example

## Overview

This example demonstrates a complete E2E test covering:
1. Telegram bot interaction
2. Database state verification
3. Engagement tracking
4. Log analysis

---

## Prerequisites Verified

```
✅ Telegram MCP: mcp__telegram-mcp__get_me returned user profile
✅ Supabase MCP: mcp__supabase__execute_sql working
✅ Gmail MCP: mcp__gmail__search_emails accessible
✅ Cloud Run: https://nikita-api-1040094048579.us-central1.run.app/health → 200 OK
```

---

## Phase 0: Setup

### 0.1 Get Current User

```
> mcp__telegram-mcp__get_me

{
  "id": 123456789,
  "first_name": "TestUser",
  "username": "testuser"
}
```

### 0.2 Find Bot Chat

```
> mcp__telegram-mcp__list_chats

[
  { "id": -987654321, "name": "Nikita", "type": "private" },
  ...
]
```

**Bot Chat ID**: -987654321

### 0.3 Get Baseline Database State

```
> mcp__supabase__execute_sql
  query="SELECT id, chapter, relationship_score FROM users ORDER BY updated_at DESC LIMIT 1"

[{ "id": "abc-123", "chapter": 1, "relationship_score": 52.5 }]
```

**User ID**: abc-123
**Initial Score**: 52.5

---

## Phase 1: Telegram Bot Interaction

### 1.1 Send First Message

```
> mcp__telegram-mcp__send_message
  chat_id="-987654321"
  text="Hey Nikita! How's your day going?"

{ "message_id": 1001, "date": "2025-12-21T19:00:00Z" }
```

**Sent at**: 19:00:00Z

### 1.2 Wait for Response

*Waiting 12 seconds for LLM processing...*

### 1.3 Get Bot Response

```
> mcp__telegram-mcp__get_messages
  chat_id="-987654321"
  limit=3

[
  {
    "id": 1002,
    "from": "Nikita",
    "text": "Heyyy! My day's been pretty chill actually. Just finished some work stuff and now I'm just vibing. How about you? What's going on in your world? 😊",
    "date": "2025-12-21T19:00:08Z"
  },
  {
    "id": 1001,
    "from": "TestUser",
    "text": "Hey Nikita! How's your day going?",
    "date": "2025-12-21T19:00:00Z"
  }
]
```

**✅ PASS**: Bot responded in 8 seconds with coherent message.

### 1.4 Send Follow-Up

```
> mcp__telegram-mcp__send_message
  chat_id="-987654321"
  text="Just thinking about trying something new, maybe a creative hobby like painting"

{ "message_id": 1003 }
```

*Waiting 12 seconds...*

### 1.5 Verify Context Maintained

```
> mcp__telegram-mcp__get_messages
  chat_id="-987654321"
  limit=3

[
  {
    "id": 1004,
    "from": "Nikita",
    "text": "Ooh painting! That could be so fun. I've always thought watercolors are super pretty but honestly I have zero patience for that kind of thing lol. Are you thinking like abstract stuff or more realistic?",
    "date": "2025-12-21T19:00:25Z"
  },
  ...
]
```

**✅ PASS**: Bot referenced "painting" topic - context maintained.

---

## Phase 2: Database Verification

### 2.1 Check Conversations Logged

```
> mcp__supabase__execute_sql
  query="SELECT id, user_message, LEFT(nikita_response, 100) as response_preview, created_at
         FROM conversations
         WHERE user_id = 'abc-123'
         ORDER BY created_at DESC
         LIMIT 3"

[
  {
    "id": "conv-002",
    "user_message": "Just thinking about trying something new, maybe a creative hobby like painting",
    "response_preview": "Ooh painting! That could be so fun. I've always thought watercolors are super pretty but ho...",
    "created_at": "2025-12-21T19:00:13Z"
  },
  {
    "id": "conv-001",
    "user_message": "Hey Nikita! How's your day going?",
    "response_preview": "Heyyy! My day's been pretty chill actually. Just finished some work stuff and now I'm just v...",
    "created_at": "2025-12-21T19:00:00Z"
  }
]
```

**✅ PASS**: 2 conversations logged with user messages and bot responses.

### 2.2 Check Engagement State

```
> mcp__supabase__execute_sql
  query="SELECT current_state, calibration_progress, updated_at
         FROM engagement_state
         WHERE user_id = 'abc-123'"

[{
  "current_state": "calibrating",
  "calibration_progress": 15,
  "updated_at": "2025-12-21T19:00:25Z"
}]
```

**✅ PASS**: Engagement state tracking active, calibration progressing.

### 2.3 Check Generated Prompts

```
> mcp__supabase__execute_sql
  query="SELECT id, token_count, generation_time_ms, created_at
         FROM generated_prompts
         WHERE user_id = 'abc-123'
         ORDER BY created_at DESC
         LIMIT 2"

[
  {
    "id": "prompt-002",
    "token_count": 3847,
    "generation_time_ms": 145,
    "created_at": "2025-12-21T19:00:13Z"
  },
  {
    "id": "prompt-001",
    "token_count": 3652,
    "generation_time_ms": 138,
    "created_at": "2025-12-21T19:00:00Z"
  }
]
```

**✅ PASS**: Personalized prompts being generated and logged (Spec 012 Phase 4 working).

### 2.4 Check Score Changes

```
> mcp__supabase__execute_sql
  query="SELECT relationship_score, updated_at
         FROM users
         WHERE id = 'abc-123'"

[{
  "relationship_score": 53.2,
  "updated_at": "2025-12-21T19:00:25Z"
}]
```

**Initial**: 52.5 → **Current**: 53.2 (+0.7)

**✅ PASS**: Relationship score increased from positive interaction.

---

## Phase 3: Log Analysis

### 3.1 Check for Errors

```bash
> gcloud run services logs read nikita-api --region us-central1 --limit 50 2>&1 | grep -i "error\|exception"

(no output)
```

**✅ PASS**: No errors in recent logs.

### 3.2 Check Timing

```bash
> gcloud run services logs read nikita-api --region us-central1 --limit 50 2>&1 | grep "TIMING\|PROMPT-DEBUG"

[2025-12-21T19:00:13Z] [PROMPT-DEBUG] Personalized prompt generated: 3847 chars, 145ms
[2025-12-21T19:00:00Z] [PROMPT-DEBUG] Personalized prompt generated: 3652 chars, 138ms
[2025-12-21T19:00:08Z] [LLM-DEBUG] LLM response received: 156 chars
```

**✅ PASS**: Prompt generation under 200ms target.

### 3.3 Check Memory Operations

```bash
> gcloud run services logs read nikita-api --region us-central1 --limit 50 2>&1 | grep "MEMORY"

[2025-12-21T19:00:25Z] [MEMORY] Noted fact: User interested in painting as hobby
```

**✅ PASS**: Memory system recording facts.

---

## Test Summary

| Test | Status | Evidence |
|------|--------|----------|
| Bot basic response | ✅ PASS | 8s response time |
| Context maintained | ✅ PASS | Referenced painting topic |
| Conversations logged | ✅ PASS | 2 rows created |
| Engagement tracking | ✅ PASS | calibrating @ 15% |
| Prompts logged | ✅ PASS | ~3700 tokens, <150ms |
| Score update | ✅ PASS | +0.7 points |
| No errors in logs | ✅ PASS | grep found 0 errors |
| Memory operations | ✅ PASS | Fact recorded |

**Overall Result**: ✅ ALL TESTS PASSED

---

## Event Stream Entry

```
[2025-12-21T19:01:00Z] E2E_TEST: full - PASS - 8 tests, bot response 8s, prompts logging, score +0.7
```

---

## Metrics

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Bot response time | 8s | <15s | ✅ |
| Prompt generation | 145ms | <200ms | ✅ |
| Token count | 3847 | <5000 | ✅ |
| Test duration | 2m 15s | <5m | ✅ |

---

## Notes

- All systems operational
- Personalization pipeline confirmed working (Spec 012)
- Memory system recording facts
- Engagement calibration progressing

**Next recommended test**: Wait 15+ minutes, verify post-processing completes.
