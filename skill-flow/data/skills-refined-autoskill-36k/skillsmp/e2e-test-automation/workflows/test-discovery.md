# Test Discovery Workflow

## Purpose

Identify what tests need to run based on the context:
- Recent changes (git diff)
- Feature being tested
- Time since last E2E run

---

## Phase 1: Determine Test Scope

### 1.1 Parse User Request

| Request Pattern | Suggested Scope |
|-----------------|-----------------|
| "full E2E", "complete test" | `full` |
| "test telegram", "bot test" | `telegram` |
| "test portal", "dashboard" | `portal` |
| "test OTP", "auth flow" | `otp` |
| "test conversation", "message flow" | `conversation` |
| After `/implement` | `full` |
| After bug fix | Targeted scope |

### 1.2 Check Recent Changes

```bash
# What changed since last commit?
git diff --name-only HEAD~3

# Check for relevant file patterns
git diff --name-only HEAD~3 | grep -E "(telegram|api|engine|db)"
```

**Mapping changes to scopes:**

| Changed Files | Recommended Scope |
|---------------|-------------------|
| `nikita/platforms/telegram/` | `telegram` |
| `nikita/api/routes/` | `full` |
| `nikita/engine/` | `conversation` |
| `nikita/db/` | `full` |
| `portal/` | `portal` |

---

## Phase 2: Verify Prerequisites

### 2.1 MCP Server Availability

```
# Use MCPSearch to verify each server
MCPSearch query="select:mcp__telegram-mcp__get_me"
MCPSearch query="select:mcp__gmail__search_emails"
MCPSearch query="select:mcp__supabase__execute_sql"
MCPSearch query="select:mcp__chrome-devtools__navigate_page"
```

### 2.2 Environment Check

```bash
# Verify Cloud Run service is deployed
gcloud run services describe nikita-api --region us-central1 --format='value(status.url)'

# Check service health
curl -s https://nikita-api-1040094048579.us-central1.run.app/health
```

### 2.3 Test User Verification

```
# Get current Telegram user
mcp__telegram-mcp__get_me

# Expected: Returns user profile with id, username
```

---

## Phase 3: Build Test Plan

### 3.1 Scope: `full`

Run all test phases in sequence:
1. Prerequisites check
2. Telegram bot interaction
3. Database state verification
4. OTP flow (if applicable)
5. Log analysis
6. Portal check (optional)

**Estimated time: 5-10 minutes**

### 3.2 Scope: `telegram`

Run Telegram-specific tests:
1. Find bot chat
2. Send test message
3. Verify bot response
4. Check conversation logged in DB
5. Verify post-processing triggered

**Estimated time: 2-3 minutes**

### 3.3 Scope: `portal`

Run portal-specific tests:
1. Navigate to portal URL
2. Take screenshot
3. Check login form
4. Verify dashboard loads
5. Check API connections

**Estimated time: 2-3 minutes**

### 3.4 Scope: `otp`

Run OTP/auth flow tests:
1. Trigger OTP request
2. Search for OTP email
3. Extract OTP code
4. Verify pending_registrations table
5. Complete verification (if safe)

**Estimated time: 1-2 minutes**

### 3.5 Scope: `conversation`

Run conversation flow tests:
1. Send multiple messages
2. Verify responses
3. Check engagement state updates
4. Verify score changes
5. Check memory operations

**Estimated time: 3-5 minutes**

---

## Phase 4: Output Test Plan

Generate structured test plan for execution:

```markdown
## E2E Test Plan

**Scope**: [scope]
**Estimated Duration**: [time]
**Prerequisites**: [status]

### Tests to Execute

1. [Test 1] - [description]
2. [Test 2] - [description]
...

### Skip Conditions

- [Reason to skip certain tests]
```

---

## Decision Tree

```
Start
  │
  ├─ User specified scope?
  │   ├─ Yes → Use specified scope
  │   └─ No → Check context
  │
  ├─ After /implement?
  │   ├─ Yes → Use 'full' scope
  │   └─ No → Continue
  │
  ├─ After bug fix?
  │   ├─ Yes → Use targeted scope based on files changed
  │   └─ No → Continue
  │
  └─ Default → Ask user or use 'telegram' (quick verification)
```

---

## Related Workflows

- @telegram-testing.md - Detailed Telegram testing
- @database-verification.md - Database state checks
- @portal-testing.md - Portal UI testing
- @log-analysis.md - Production log analysis
