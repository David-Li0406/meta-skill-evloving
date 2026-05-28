# Jules API Skill

A Claude Code skill for interacting with Google's Jules API to create and manage asynchronous coding sessions.

**Version**: 2.0.0
**Last Updated**: 2026-01-11

## 🆕 What's New in v2.0

- ✅ **Activities API Support**: Read and parse session activities to understand conversation history
- ✅ **Stuck Session Debugging**: Comprehensive workflow for unsticking `AWAITING_USER_FEEDBACK` sessions
- ✅ **Session ID Handling**: All methods accept both `"sessions/123"` and `"123"` formats
- ✅ **CLI Improvements**: Better output formatting, `--json` flag, new `check` command
- ✅ **Real-World Examples**: Case study from successfully unsticking session 14848423526856432295
- ✅ **Helper Methods**: New `check_session_needs_attention()` method

## What This Skill Does

This skill enables Claude Code to:
- Create Jules coding sessions with specific prompts and repository context
- Monitor session progress and states
- Send messages and feedback to active sessions
- Approve generated plans before execution
- Retrieve session outputs and activities

## When to Use This Skill

Invoke this skill when you want to:
- Create a Jules session to work on a coding task
- Check the status of a Jules session
- Interact with an active Jules session
- Review Jules session outputs or pull requests

Simply mention "Jules" in your request, and Claude will automatically invoke this skill.

## Prerequisites

Before using this skill, you need:

1. **Jules API Key** set as an environment variable:
   ```bash
   export JULES_API_KEY="your-api-key-here"
   ```

2. **Python 3.7+** with the `httpx` library (installed automatically with egregora dependencies)

## Files in This Skill

- **SKILL.md** - Main skill definition with comprehensive API documentation
- **jules_client.py** - Python client library and CLI tool for Jules API
- **examples.md** - Practical examples and use cases
- **README.md** - This file

## Quick Start

### Example 1: Create a Session

```bash
python .claude/skills/jules-api/jules_client.py create \
  "Add unit tests for the authentication module" \
  myusername \
  myrepo \
  --branch main \
  --require-plan-approval
```

### Example 2: Check Session Status

```bash
python .claude/skills/jules-api/jules_client.py get <session-id>

# Get raw JSON
python .claude/skills/jules-api/jules_client.py get <session-id> --json
```

### Example 3: Check if Session Needs Attention

```bash
python .claude/skills/jules-api/jules_client.py check <session-id>

# Returns:
# ⚠️ Session is waiting for user feedback
# or
# ✅ Session is active (IN_PROGRESS)
```

### Example 4: View Session Activities (NEW!)

```bash
python .claude/skills/jules-api/jules_client.py activities <session-id>

# Shows last 10 activities with timestamps and messages
```

### Example 5: List All Sessions

```bash
python .claude/skills/jules-api/jules_client.py list
```

### Example 6: Send Message to Session

```bash
python .claude/skills/jules-api/jules_client.py message <session-id> \
  "Please add more test coverage for edge cases"
```

## Using with Claude Code

When working with Claude Code, simply mention Jules in your request:

- "Create a Jules session to add error handling to the API"
- "Check the status of my Jules session abc123"
- "List all my Jules sessions"
- "Send a message to Jules session abc123 asking for more tests"

Claude will automatically invoke this skill and use the appropriate Jules API endpoints.

## Python Library Usage

You can also use the `JulesClient` class directly in your Python code:

```python
from repo_client import JulesClient

# Initialize client
client = JulesClient()

# Create a session
session = client.create_session(
    prompt="Add logging to all API endpoints",
    owner="myusername",
    repo="myrepo",
    branch="main",
    require_plan_approval=True
)

print(f"Created session: {session['id']}")

# Check status
status = client.get_session(session['id'])
print(f"Current state: {status['state']}")

# Send feedback
if status['state'] == 'AWAITING_USER_FEEDBACK':
    client.send_message(session['id'], "Please focus on error handling")

# Approve plan
if status['state'] == 'AWAITING_PLAN_APPROVAL':
    client.approve_plan(session['id'])

# Get activities
activities_data = client.get_activities(session['id'])
activities = activities_data['activities']

# Parse recent activities
for activity in activities[-5:]:  # Last 5 activities
    if activity['originator'] == 'agent':
        print(f"Jules: {activity['agentMessaged']['agentMessage'][:100]}...")
    elif activity['originator'] == 'user':
        print(f"User: {activity['userMessaged']['userMessage'][:100]}...")

# Check if session needs attention
needs_attention, reason = client.check_session_needs_attention(session['id'])
if needs_attention:
    print(f"⚠️ {reason}")
```

## Session States

Jules sessions progress through these states:

- **QUEUED** - Waiting to start
- **PLANNING** - Generating execution plan
- **AWAITING_PLAN_APPROVAL** - Waiting for user to approve plan
- **AWAITING_USER_FEEDBACK** - Needs user input
- **IN_PROGRESS** - Actively executing
- **PAUSED** - Temporarily stopped
- **COMPLETED** - Successfully finished
- **FAILED** - Encountered an error

## API Reference

For complete API documentation, see:
- [SKILL.md](./SKILL.md) - Full API reference
- [examples.md](./examples.md) - Practical examples
- [Official Jules API Docs](https://developers.google.com/repo/api/reference/rest)

## Troubleshooting

### Authentication Issues

If you get authentication errors:
```bash
# Re-authenticate
gcloud auth login

# Verify authentication
gcloud auth print-access-token
```

### Permission Issues

Make sure your Google Cloud project has Jules API enabled and you have the necessary permissions.

### Rate Limiting

If you hit rate limits, the API will return a 429 status code. Wait a minute before retrying.

## Contributing

To improve this skill:
1. Edit `SKILL.md` to update the main skill instructions
2. Update `jules_client.py` to add new functionality
3. Add examples to `examples.md`

## Changelog

### v2.0.0 (2026-01-11)
- Added comprehensive activities API support with parsing examples
- Added stuck session debugging workflow with real case study
- Improved session ID handling (accepts both formats)
- Added `check` command to CLI
- Added `--json` flag for programmatic usage
- Added `check_session_needs_attention()` helper method
- Improved CLI output formatting
- Better error messages

### v1.0.0 (2025-10-24)
- Initial release
