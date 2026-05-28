---
name: jules-api
description: Delegate asynchronous coding tasks to Jules (Google's AI coding agent) to maximize efficiency. Use for code reviews, refactoring, adding tests, bug fixes, and documentation. Proactively suggest Jules delegation when appropriate. Invoke when user asks to interact with Jules, create sessions, check task status, or when tasks are suitable for async delegation.
---

# Jules API Integration

This skill enables interaction with Google's Jules API for programmatic creation and management of asynchronous coding tasks.

## Overview

The Jules API allows you to:
- Create coding sessions with specific prompts and repository context
- Monitor session progress through various states
- Send messages and feedback to active sessions
- Approve generated plans before execution
- Retrieve session outputs (pull requests, artifacts)

## Delegation Philosophy

**KEY PRINCIPLE**: Use Jules for asynchronous tasks to maximize efficiency and free up Claude for strategic work.

### When Claude Should Delegate to Jules

Claude should **proactively suggest** creating Jules sessions for:

1. **Code Reviews** - After pushing a branch, delegate review to Jules
2. **Refactoring** - Improve code structure without changing behavior
3. **Adding Tests** - Generate unit/integration tests for existing code
4. **Bug Fixes** - Well-defined bugs with clear reproduction steps
5. **Documentation** - Improve comments, docstrings, READMEs
6. **Iterative Improvements** - Enhance previous work based on feedback

### Effective Delegation Patterns

**Pattern 1: Initial Implementation + Review**
```
1. Claude creates initial feature implementation
2. Push branch to remote
3. Claude creates Jules session: "Review and improve feature X"
4. Jules creates PR with improvements
5. Claude integrates feedback
```

**Pattern 2: Test Generation**
```
1. Claude implements feature
2. Claude creates Jules session: "Add comprehensive tests for module X"
3. Jules generates test suite
4. Merge when tests pass
```

**Pattern 3: Bug Fix Delegation**
```
1. User reports bug
2. Claude investigates and identifies root cause
3. Claude creates Jules session with reproduction steps
4. Jules fixes and adds regression tests
```

### Best Practices for Prompts

**Good prompts are:**
- ✅ **Specific**: "Add unit tests for authentication module"
- ✅ **Contextual**: "Review PR #123, focus on error handling"
- ✅ **Actionable**: "Refactor parser.py to use Polars instead of Pandas"
- ✅ **Scoped**: "Fix the timezone bug in commit abc123"
- ✅ **Test-Driven**: "Use TDD approach with behavior-relevant tests"

**Avoid vague prompts:**
- ❌ "Improve the code"
- ❌ "Make it better"
- ❌ "Fix everything"
- ❌ "Add features"

### Test-Driven Development (TDD) Requirement

**IMPORTANT**: Always instruct Jules to use Test-Driven Development (TDD) approach for better results.

**Why TDD with Jules:**
- ✅ Ensures code correctness before implementation
- ✅ Creates behavior-relevant tests that validate actual requirements
- ✅ Prevents regressions and edge case bugs
- ✅ Provides clear acceptance criteria
- ✅ Makes code more maintainable and documented

**How to Request TDD:**

Include this in every Jules prompt:
```
Use Test-Driven Development (TDD) approach:
1. Write behavior-relevant tests first (cover expected behavior, edge cases, error conditions)
2. Run tests to confirm they fail (red phase)
3. Implement minimal code to make tests pass (green phase)
4. Refactor while keeping tests passing (refactor phase)
5. Ensure all tests have meaningful assertions that validate actual behavior
```

**Example Prompts with TDD:**

**Good - With TDD**:
```
Add user authentication to the API.

Use TDD approach:
1. Write tests for: successful login, invalid credentials, token expiration, rate limiting
2. Implement authentication logic to pass tests
3. Refactor for security best practices

Tests should validate actual behavior, not implementation details.
```

**Good - With TDD**:
```
Refactor the parser to use Polars instead of Pandas.

Use TDD approach:
1. Write behavior tests that validate current parser output
2. Refactor to use Polars while keeping tests green
3. Add performance benchmarks as tests

Focus on behavior: input -> output validation, not internal implementation.
```

**Bad - Without TDD**:
```
Add user authentication to the API.
```

**What are "Behavior-Relevant" Tests:**
- ✅ Test **what** the code does, not **how** it does it
- ✅ Validate actual business requirements
- ✅ Cover edge cases and error conditions
- ✅ Test from user/caller perspective
- ❌ Don't test implementation details
- ❌ Don't test private methods directly
- ❌ Don't create brittle tests that break on refactoring

**Example of Behavior-Relevant Test:**
```python
# ✅ Good - Tests behavior
def test_send_message_creates_event_in_log():
    """When sending a message, it should be appended to the event log."""
    send_message(from_persona="curator", to_persona="refactor", subject="Review", body="Check this")

    events = read_event_log()
    assert len(events) == 1
    assert events[0]['event_type'] == 'send'
    assert events[0]['from_persona'] == 'curator'
    assert events[0]['to_persona'] == 'refactor'

# ❌ Bad - Tests implementation
def test_send_message_calls_append_event():
    """Tests implementation detail, not behavior."""
    with mock.patch('mail.append_event') as mock_append:
        send_message(...)
        assert mock_append.called  # Brittle, breaks on refactoring
```

### 🔄 Jules Automatically Resumes From PR Comments

**IMPORTANT DISCOVERY**: Jules monitors PRs and automatically resumes sessions when you comment!

**How it works:**
1. Jules creates a PR (e.g., #466)
2. You comment on the PR describing an issue or requesting changes
3. **Jules automatically sees your comment** and resumes the session
4. Jules generates a NEW plan to address your feedback
5. Session state changes: `COMPLETED` → `AWAITING_PLAN_APPROVAL`
6. You approve the plan, Jules fixes the issues and updates the PR

**Real example from egregora:**
```
1. Jules session #10887318009267300343 created PR #466 (golden fixtures)
2. State was COMPLETED
3. Claude commented: "Wrong SDK used (google.generativeai vs google.genai)"
4. Jules AUTOMATICALLY resumed - state became AWAITING_PLAN_APPROVAL
5. Jules generated 8-step plan to fix SDK + modify pipeline
6. Claude approved: jules_client.py approve-plan 10887318009267300343
7. Jules executing fixes now
```

**Best practices:**
- ✅ **DO**: Comment on PRs with specific, actionable feedback
- ✅ **DO**: Check if session auto-resumed before creating duplicate session
- ✅ **DO**: Approve Jules' new plan if it looks good
- ✅ **DO**: Use detailed comments - Jules understands context
- ❌ **DON'T**: Create new session if existing one can resume
- ❌ **DON'T**: Use vague PR comments like "fix this"

**This creates a powerful feedback loop!** Comment on PRs to iterate with Jules.

### Claude's Role in Delegation

When delegating to Jules, Claude should:

1. **Prepare the context** - Ensure branch is pushed and up-to-date
2. **Write clear prompts** - Specific, actionable instructions
3. **Create the session** - Use jules_client.py or delegate via skill
4. **Return session info** - Give user the session ID and URL
5. **Suggest next steps** - Explain what Jules will do and when to check back

**Example dialogue:**
```
User: "Can you review my authentication changes?"
Claude: "I'll create a Jules session to review your authentication code.
         Jules works asynchronously and will create a PR with feedback.

         Session ID: 123456789
         URL: https://jules.google.com/sessions/123456789

         ⏱️  Jules typically completes tasks in ~10 minutes.
         You can continue other work while Jules reviews. I can check
         the status in ~10 minutes and help you integrate the changes."
```

**Important timing notes:**
- Jules sessions typically complete in **~10 minutes**
- Claude should check session status after ~10 minutes
- Use this time for other work - don't wait synchronously
- Jules will create a PR when done (AUTO_CREATE_PR mode)

**IMPORTANT**: Always use `"automationMode": "AUTO_CREATE_PR"` when creating sessions. This ensures Jules automatically creates a PR when the work is complete, enabling automated workflows.

## Base Configuration

**Base URL**: `https://jules.googleapis.com`
**API Version**: v1alpha
**Authentication**: API Key via `X-Goog-Api-Key` header

## Tools

### Feed Feedback (CI/Reviews)

This skill includes a script `feed_feedback.py` designed to run in a scheduled workflow. It enables Jules to receive feedback from CI failures and code reviews on its own Pull Requests.

**Purpose**: Closes the feedback loop by reporting CI errors and review comments back to the active Jules session so it can interactively fix issues.

**Usage**:
```bash
# Run locally (requires JULES_API_KEY and GITHUB_TOKEN)
python .claude/skills/jules-api/feed_feedback.py

# Run for a specific bot author (default: jules-bot)
python .claude/skills/jules-api/feed_feedback.py --author my-bot-name
```

**How it works**:
1. Scans for open PRs by `jules-bot`.
2. Checks CI status (failed) and Reviews (changes requested).
3. Extracts the Jules Session ID from the branch name or PR body.
4. Sends a prompt to the session with error logs and feedback.
5. Posts a comment on the PR to prevent spamming the same feedback.

## Usage Philosophy

**IMPORTANT**: This skill prioritizes **direct API usage** via HTTP calls (curl, httpx, requests) rather than relying on custom Python scripts. This ensures:
- ✅ Language-agnostic (works with any language/environment)
- ✅ Portable (no dependency on jules_client.py)
- ✅ Transparent (clear what API calls are being made)
- ✅ Maintainable (follows API documentation directly)

**When using this skill**:
1. **Primary**: Use direct HTTP calls (curl in bash, httpx/requests in Python)
2. **Secondary**: Use jules_client.py only as a convenience for complex workflows

## Core Operations

### 1. Create a Session

Create a new coding session with a prompt and repository context.

**Endpoint**: `POST /v1alpha/sessions`

**Request Body**:
```json
{
  "prompt": "Your coding task description",
  "sourceContext": {
    "source": "sources/github/username/repository",
    "githubRepoContext": {
      "startingBranch": "main"
    }
  },
  "title": "Optional session title",
  "requirePlanApproval": false,
  "automationMode": "AUTO_CREATE_PR"
}
```

**Example using curl**:
```bash
curl -X POST https://jules.googleapis.com/v1alpha/sessions \
  -H "X-Goog-Api-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Add unit tests for authentication module",
    "sourceContext": {
      "source": "sources/github/myorg/myrepo",
      "githubRepoContext": {
        "startingBranch": "main"
      }
    },
    "title": "Add Auth Tests",
    "requirePlanApproval": true,
    "automationMode": "AUTO_CREATE_PR"
  }'
```

### 2. Get Session Status

Retrieve details about a specific session.

**Endpoint**: `GET /v1alpha/sessions/{sessionId}`

**Example**:
```bash
curl https://jules.googleapis.com/v1alpha/sessions/abc123 \
  -H "X-Goog-Api-Key: YOUR_API_KEY"
```

**Session States**:
- `QUEUED`: Session is waiting to start
- `PLANNING`: Generating execution plan
- `AWAITING_PLAN_APPROVAL`: Waiting for user approval
- `AWAITING_USER_FEEDBACK`: Needs user input
- `IN_PROGRESS`: Actively executing
- `PAUSED`: Temporarily stopped
- `COMPLETED`: Successfully finished
- `FAILED`: Encountered error

### 3. List All Sessions

Retrieve all sessions.

**Endpoint**: `GET /v1alpha/sessions`

**Example**:
```bash
curl https://jules.googleapis.com/v1alpha/sessions \
  -H "X-Goog-Api-Key: YOUR_API_KEY"
```

### 4. Send Message to Session

Send user feedback or additional instructions to an active session.

**Endpoint**: `POST /v1alpha/sessions/{sessionId}:sendMessage`

**Request Body**:
```json
{
  "prompt": "Your message or feedback"
}
```

**Example**:
```bash
curl -X POST https://jules.googleapis.com/v1alpha/sessions/abc123:sendMessage \
  -H "X-Goog-Api-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Please add more test coverage for edge cases"}'
```

### 5. Approve Plan

Approve a generated plan (when requirePlanApproval is true).

**Endpoint**: `POST /v1alpha/sessions/{sessionId}:approvePlan`

**Example**:
```bash
curl -X POST https://jules.googleapis.com/v1alpha/sessions/abc123:approvePlan \
  -H "X-Goog-Api-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

### 6. Get Session Activities

Retrieve activity logs for a session to understand the conversation history.

**Endpoint**: `GET /v1alpha/sessions/{sessionId}/activities`

**Response Structure**:
```json
{
  "activities": [
    {
      "name": "sessions/123/activities/abc",
      "createTime": "2026-01-11T12:00:00Z",
      "originator": "agent",  // or "user"
      "agentMessaged": {
        "agentMessage": "Message from Jules..."
      },
      "id": "abc"
    },
    {
      "originator": "user",
      "userMessaged": {
        "userMessage": "Response from user..."
      }
    }
  ]
}
```

**Example**:
```bash
curl https://jules.googleapis.com/v1alpha/sessions/abc123/activities \
  -H "X-Goog-Api-Key: YOUR_API_KEY"
```

**Key Usage Patterns**:

1. **Debugging Stuck Sessions**: When a session is in `AWAITING_USER_FEEDBACK`, read activities to see what Jules is asking:
   ```python
   activities = client.get_activities(session_id)
   for activity in activities['activities'][-5:]:  # Last 5 activities
       if activity['originator'] == 'agent':
           print(activity['agentMessaged']['agentMessage'])
   ```

2. **Understanding Context**: Activities show the full conversation, useful for providing targeted feedback:
   ```python
   # Find last question from Jules
   for activity in reversed(activities['activities']):
       if activity['originator'] == 'agent':
           last_question = activity['agentMessaged']['agentMessage']
           break
   ```

3. **Monitoring Progress**: Track what Jules is doing during implementation:
   ```python
   recent_activities = activities['activities'][-10:]
   agent_messages = [a for a in recent_activities if a['originator'] == 'agent']
   print(f"Jules sent {len(agent_messages)} messages in last 10 activities")
   ```

**Important Notes**:
- Activities can be large (40+ activities in complex sessions)
- Always check `originator` to distinguish agent vs user messages
- Activities are ordered chronologically (oldest first)
- Use slicing to get recent activities: `activities['activities'][-10:]`

## Authentication Setup

To use the Jules API, you need an API key:

1. **Get your API key**:
   - Visit https://jules.google.com/settings#api
   - Create a new API key (max 3 keys allowed)
   - Copy the API key

2. **Set the API key**:
   ```bash
   # Export as environment variable
   export JULES_API_KEY="your-api-key-here"

   # Or pass directly to JulesClient
   client = JulesClient(api_key="your-api-key-here")
   ```

**Security Note**: Keep your API key secure. Don't share it or commit it to version control.

## Direct API Usage (Recommended)

### Python with httpx (Recommended)

```python
import os
import httpx

API_KEY = os.environ.get("JULES_API_KEY")
BASE_URL = "https://jules.googleapis.com/v1alpha"

headers = {
    "X-Goog-Api-Key": API_KEY,
    "Content-Type": "application/json"
}

# Create session
response = httpx.post(
    f"{BASE_URL}/sessions",
    headers=headers,
    json={
        "prompt": "Add error handling to API endpoints",
        "sourceContext": {
            "source": "sources/github/myorg/myproject",
            "githubRepoContext": {"startingBranch": "main"}
        },
        "requirePlanApproval": True,
        "automationMode": "AUTO_CREATE_PR"
    }
)
session = response.json()
session_id = session['name'].split('/')[-1]
print(f"Created: {session_id}")

# Get status
response = httpx.get(f"{BASE_URL}/sessions/{session_id}", headers=headers)
status = response.json()
print(f"State: {status['state']}")

# Get activities
response = httpx.get(f"{BASE_URL}/sessions/{session_id}/activities", headers=headers)
activities = response.json()['activities']

# Send message
if status['state'] == 'AWAITING_USER_FEEDBACK':
    response = httpx.post(
        f"{BASE_URL}/sessions/{session_id}:sendMessage",
        headers=headers,
        json={"prompt": "Proceed with the implementation"}
    )

# Approve plan
if status['state'] == 'AWAITING_PLAN_APPROVAL':
    response = httpx.post(
        f"{BASE_URL}/sessions/{session_id}:approvePlan",
        headers=headers
    )
```

### Bash with curl

```bash
export JULES_API_KEY="your-api-key"
export BASE_URL="https://jules.googleapis.com/v1alpha"

# Create session
curl -X POST "$BASE_URL/sessions" \
  -H "X-Goog-Api-Key: $JULES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Add error handling to API endpoints",
    "sourceContext": {
      "source": "sources/github/myorg/myproject",
      "githubRepoContext": {"startingBranch": "main"}
    },
    "requirePlanApproval": true,
    "automationMode": "AUTO_CREATE_PR"
  }' | jq .

# Get status
curl "$BASE_URL/sessions/123456789" \
  -H "X-Goog-Api-Key: $JULES_API_KEY" | jq .

# Get activities
curl "$BASE_URL/sessions/123456789/activities" \
  -H "X-Goog-Api-Key: $JULES_API_KEY" | jq '.activities[-5:]'

# Send message
curl -X POST "$BASE_URL/sessions/123456789:sendMessage" \
  -H "X-Goog-Api-Key: $JULES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Proceed with implementation"}'

# Approve plan
curl -X POST "$BASE_URL/sessions/123456789:approvePlan" \
  -H "X-Goog-Api-Key: $JULES_API_KEY"
```

## Alternative: Python Client Library

For convenience in complex workflows, you can use the included `jules_client.py`:

```python
import sys
sys.path.insert(0, '.claude/skills/jules-api')
from repo_client import JulesClient

client = JulesClient()

# All the same operations as above
session = client.create_session(
    prompt='Add error handling to API endpoints',
    owner='myorg',
    repo='myproject',
    require_plan_approval=True
)
```

**Note**: The client library is a thin wrapper around the HTTP API. Prefer direct API calls for transparency.

## Best Practices

1. **Use Descriptive Prompts**: Provide clear, specific instructions for the coding task
2. **Monitor State**: Poll session status to track progress
3. **Enable Plan Approval**: Set `requirePlanApproval: true` for sensitive operations
4. **Handle States**: Implement proper handling for AWAITING_USER_FEEDBACK and AWAITING_PLAN_APPROVAL states
5. **Check Outputs**: Review the `outputs` array for generated pull requests and artifacts

## Common Workflows

### Workflow 1: Simple Task
1. Create session with prompt
2. Poll status until COMPLETED or FAILED
3. Retrieve outputs (PRs)

### Workflow 2: Supervised Task
1. Create session with `requirePlanApproval: true`
2. Wait for AWAITING_PLAN_APPROVAL state
3. Review plan in activities
4. Call approvePlan
5. Monitor until completion

### Workflow 3: Interactive Task
1. Create session
2. Monitor for AWAITING_USER_FEEDBACK
3. Use sendMessage to provide feedback
4. Continue monitoring until completion

## Real-World Delegation Scenarios

### Scenario 1: Feature Implementation Review
```
User: "I just implemented user authentication, can you review it?"

Claude Action:
1. Check if branch is pushed to remote
2. Create Jules session with prompt:
   "Review the user authentication implementation in feature/auth-system.
    Check for security issues, test coverage, and code quality.
    Suggest improvements and add missing tests."
3. Inform user of session ID/URL
4. User continues other work while Jules reviews
```

### Scenario 2: Adding Tests to Legacy Code
```
User: "We need tests for the payment processor module"

Claude Action:
1. Review payment processor to understand functionality
2. Create Jules session:
   "Add comprehensive unit and integration tests for the payment
    processor module. Cover success cases, error handling, edge cases,
    and mock external payment gateway calls."
3. Jules generates test suite
4. Review and merge
```

### Scenario 3: Refactoring for Performance
```
User: "The data parser is slow, can we optimize it?"

Claude Action:
1. Identify performance bottleneck
2. Create Jules session:
   "Refactor parser.py to use Polars instead of Pandas for 10x
    performance improvement. Maintain same API and ensure all
    existing tests pass. Add benchmarks."
3. Jules refactors with benchmarks
4. Review performance gains and merge
```

### Scenario 4: Bug Fix with Regression Tests
```
User: "There's a bug in timezone handling"

Claude Action:
1. Investigate and identify root cause in commit abc123
2. Create Jules session:
   "Fix timezone bug in datetime_utils.py (commit abc123).
    The bug causes incorrect UTC conversion for dates before 1970.
    Add regression tests to prevent future issues."
3. Jules fixes and adds tests
4. Verify and merge
```

### Scenario 5: Documentation Improvement
```
User: "Our API documentation is outdated"

Claude Action:
1. Identify outdated sections
2. Create Jules session:
   "Update API documentation in docs/api.md to reflect current
    implementation. Add examples for new endpoints, update
    parameter descriptions, and ensure all code samples work."
3. Jules updates docs with examples
4. Review and merge
```

## Proactive Delegation Triggers

Claude should **automatically suggest** Jules delegation when:

- ✅ User pushes a branch and asks "what do you think?"
- ✅ User says "add tests" or "improve tests"
- ✅ User mentions "review", "refactor", or "optimize"
- ✅ Feature is complete and needs polish
- ✅ Code works but needs improvement
- ✅ User reports a well-defined bug
- ✅ Documentation needs updating

**Example proactive response:**
```
User: "Just pushed the new API endpoint to feature/api-v2"
Claude: "Great! I can see the implementation looks solid. Would you like me to
         create a Jules session to review it and suggest improvements? Jules
         can check for edge cases, add tests, and optimize the code while
         you continue working on other features."
```

## Debugging Stuck Sessions

When a Jules session is stuck in `AWAITING_USER_FEEDBACK` or `AWAITING_PLAN_APPROVAL`, follow this workflow:

### Step 1: Check Session State
```python
session = client.get_session(session_id)
print(f"State: {session['state']}")
print(f"Created: {session['createTime']}")
print(f"Updated: {session['updateTime']}")
```

### Step 2: Read Activities to Understand Context
```python
activities_data = client.get_activities(session_id)
activities = activities_data['activities']

print(f"Total activities: {len(activities)}")

# Show last 10 activities
for activity in activities[-10:]:
    originator = activity['originator']
    create_time = activity['createTime']

    if originator == 'agent':
        msg = activity.get('agentMessaged', {}).get('agentMessage', '')
        print(f"\n[JULES at {create_time}]")
        print(msg[:300] + ('...' if len(msg) > 300 else ''))
    elif originator == 'user':
        msg = activity.get('userMessaged', {}).get('userMessage', '')
        print(f"\n[USER at {create_time}]")
        print(msg[:300] + ('...' if len(msg) > 300 else ''))
```

### Step 3: Identify What Jules Is Asking
Look for the most recent agent message to understand:
- What question Jules is asking
- What blocker Jules encountered
- What decision Jules needs

### Step 4: Provide Targeted Feedback
```python
# Craft a specific, actionable response
feedback = """
Based on your question about X:

1. [Answer the specific question]
2. [Provide context or clarification]
3. [Give clear next steps]

Proceed autonomously with this guidance.
"""

client.send_message(session_id, feedback)
print("✅ Feedback sent - session should resume")
```

### Real Example: Unsticking Session 14848423526856432295

**Situation**: Session stuck for 14+ hours in `AWAITING_USER_FEEDBACK`

**Investigation**:
```python
# Read last 10 activities
activities = client.get_activities('14848423526856432295')['activities'][-10:]

# Found: Jules was stuck on test failures with Ibis schema issues
# Last agent message showed: "The tests are still failing with empty inboxes"
```

**Solution**: Sent targeted message with:
1. Schema fix (remove DuckDB duplication, use only Ibis)
2. Array operation fix (use `isin()` instead of `contains()`)
3. Priority guidance (ship working v1, iterate later)
4. Clear next steps

**Result**: Session changed from `AWAITING_USER_FEEDBACK` → `IN_PROGRESS` within minutes

### Common Stuck Session Patterns

1. **Implementation Blocker**: Jules hit a technical issue and needs guidance
   - **Solution**: Read activities, identify the specific error, provide fix

2. **Unclear Requirements**: Jules needs clarification on what to build
   - **Solution**: Provide specific examples and acceptance criteria

3. **Decision Paralysis**: Jules has multiple options and needs direction
   - **Solution**: Pick one approach and explain the reasoning

4. **Test Failures**: Jules can't get tests passing
   - **Solution**: Debug the test failure, provide specific fix or workaround

## Error Handling

Always check response status codes:
- `200 OK`: Success
- `400 Bad Request`: Invalid request parameters
- `401 Unauthorized`: Authentication failed
- `404 Not Found`: Session doesn't exist
- `403 Forbidden`: Insufficient permissions

**Handling Session ID Formats**:
- API returns session name as `"sessions/123456789"`
- Extract ID: `session_id = session['name'].split('/')[-1]`
- Both formats work in API calls (with or without `sessions/` prefix)
- Client library handles both formats automatically

## References

- Official Documentation: https://developers.google.com/repo/api/reference/rest
- Sessions API: https://developers.google.com/repo/api/reference/rest/v1alpha/sessions
