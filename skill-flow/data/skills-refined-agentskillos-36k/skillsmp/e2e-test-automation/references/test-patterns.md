# E2E Test Patterns

## Core Patterns

### Pattern 1: Send-Wait-Verify

The fundamental pattern for testing async systems.

```
1. SEND: Trigger an action (send message, submit form)
2. WAIT: Allow time for processing (10s for LLM, 30s for email)
3. VERIFY: Check expected outcome (response received, DB updated)
```

**Example - Telegram Bot:**
```
1. mcp__telegram-mcp__send_message → "Hey, how are you?"
2. Wait 10 seconds (LLM processing)
3. mcp__telegram-mcp__get_messages → Verify bot responded
```

**Example - OTP Flow:**
```
1. Trigger OTP (via /start or portal)
2. Wait 30 seconds (email delivery)
3. mcp__gmail__search_emails → Verify email received
```

---

### Pattern 2: State Transition Verification

Verify that actions cause expected state changes.

```
1. CAPTURE: Record initial state
2. ACT: Perform action that should change state
3. COMPARE: Verify state changed as expected
```

**Example - Engagement State:**
```
1. mcp__supabase__execute_sql → Get current engagement_state
2. Send several messages to bot
3. mcp__supabase__execute_sql → Verify state transitioned (calibrating → engaged)
```

**Example - Score Change:**
```
1. Get current relationship_score
2. Have positive conversation
3. Verify score increased
```

---

### Pattern 3: Pipeline Completion

Verify multi-stage async pipelines complete.

```
1. TRIGGER: Start the pipeline
2. POLL: Check for completion markers
3. VALIDATE: Verify all stages completed
```

**Example - Post-Processing:**
```
1. Send message → Conversation created
2. Wait 15+ minutes (or trigger manually)
3. Check: summary populated, entities extracted, status='processed'
```

---

### Pattern 4: Error Recovery

Verify system handles errors gracefully.

```
1. BREAK: Cause an error condition
2. OBSERVE: System should handle gracefully
3. RECOVER: System should continue functioning
```

**Example - Invalid Input:**
```
1. Send empty message to bot
2. Bot should not crash, may ignore or respond gracefully
3. Send normal message - bot still works
```

---

## Verification Patterns

### Database Verification Pattern

```sql
-- 1. Check row exists
SELECT COUNT(*) FROM table WHERE condition;

-- 2. Check values correct
SELECT column1, column2 FROM table WHERE id = X;

-- 3. Check relationships
SELECT a.*, b.* FROM table_a a
JOIN table_b b ON a.id = b.foreign_id
WHERE a.id = X;

-- 4. Check timing
SELECT * FROM table
WHERE created_at > NOW() - INTERVAL '5 minutes';
```

### Log Verification Pattern

```bash
# 1. Get recent logs
gcloud run services logs read SERVICE --limit 100

# 2. Filter for errors
... | grep -i error

# 3. Find specific patterns
... | grep "user_id\|request_id"

# 4. Check timing
... | grep "TIMING"
```

### Response Verification Pattern

```
1. Check response exists (not null/empty)
2. Check response is relevant (contains expected keywords)
3. Check response format (length, structure)
4. Check no error markers ("error", "failed", "sorry")
```

---

## Test Organization

### Scope Hierarchy

```
full
├── telegram
│   ├── basic_interaction
│   ├── multi_turn
│   └── edge_cases
├── portal
│   ├── auth_flow
│   ├── dashboard
│   └── navigation
├── otp
│   ├── email_delivery
│   └── verification
└── database
    ├── user_state
    ├── conversations
    └── engagement
```

### Test Independence

Each test should:
1. **Setup** its own preconditions
2. **Execute** independently
3. **Cleanup** after itself (if needed)
4. **Not depend** on other tests' results

---

## Timing Guidelines

| Operation | Wait Time | Rationale |
|-----------|-----------|-----------|
| Telegram message → Bot response | 10-15s | LLM generation |
| OTP request → Email delivery | 30-60s | Email delivery |
| Form submit → Page update | 2-5s | Server processing |
| DB write → Read consistency | 1-2s | Replication |
| Post-processing trigger | 15+ min | Session timeout |

### Timeout Handling

```
MAX_RETRIES = 3
RETRY_DELAYS = [5, 15, 30]  # seconds

for i, delay in enumerate(RETRY_DELAYS):
    result = attempt_operation()
    if success:
        break
    if i < MAX_RETRIES - 1:
        wait(delay)
```

---

## Data Patterns

### Test Message Templates

**Basic greeting:**
```
Hey, how are you doing today?
```

**Context-building:**
```
I'm thinking about starting a new hobby
```

**Follow-up (tests memory):**
```
Remember what we talked about earlier?
```

**Edge case - long message:**
```
[500+ characters about a topic...]
```

**Edge case - empty:**
```
(empty string)
```

### Expected Response Markers

**Positive indicators:**
- Relevant to topic
- Nikita persona maintained
- Appropriate length
- No error messages

**Negative indicators:**
- "Error", "failed", "sorry"
- Generic/off-topic response
- Extremely short (<10 chars)
- System error messages

---

## Assertion Patterns

### Existence Assertion

```
assert result is not None
assert len(rows) > 0
assert response.strip() != ""
```

### Value Assertion

```
assert value == expected
assert value in allowed_values
assert min_val <= value <= max_val
```

### Timing Assertion

```
assert response_time < max_allowed_time
assert timestamp > start_time
assert updated_at > original_updated_at
```

### Pattern Assertion

```
assert not re.search(r'error|failed', response, re.I)
assert re.match(r'\d{8}', otp_code)  # 8 digits
```

---

## Anti-Patterns to Avoid

### 1. No Wait Between Operations

❌ **Bad:**
```
send_message()
get_messages()  # Immediately - response not ready
```

✅ **Good:**
```
send_message()
wait(10)  # Allow LLM processing
get_messages()
```

### 2. Ignoring Errors

❌ **Bad:**
```
try:
    result = operation()
except:
    pass  # Silently ignore
```

✅ **Good:**
```
try:
    result = operation()
except Exception as e:
    log_error(e)
    mark_test_failed(reason=str(e))
```

### 3. Hardcoded IDs

❌ **Bad:**
```
chat_id = "123456789"  # Hardcoded
```

✅ **Good:**
```
chats = list_chats()
bot_chat = find_bot_chat(chats)
chat_id = bot_chat.id
```

### 4. No Cleanup

❌ **Bad:**
```
# Create test data
# Run test
# (test data left behind)
```

✅ **Good:**
```
# Create test data
# Run test
# Clean up test data (or use unique identifiers)
```
