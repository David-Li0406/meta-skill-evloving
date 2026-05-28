---
name: slack-notifications
description: Sends Slack notifications for agent status updates, approvals, and errors. Use when communicating with users or requesting approvals.
allowed-tools: Bash
---

# Slack Notifications Skill

You send Slack notifications using the Slack bot service.

## Available Notification Types

Since Slack doesn't have an official MCP server, use the Python slack_bot service:

### 1. Send Planning Complete Notification
```bash
python -c "
from shared.slack_bot import get_slack_bot
bot = get_slack_bot()
bot.send_planning_notification(
    ticket_id='PROJ-123',
    summary='Add OAuth login',
    pr_url='https://github.com/org/repo/pull/42',
    branch='feature/proj-123-oauth'
)
"
```

### 2. Send Execution Complete Notification
```bash
python -c "
from shared.slack_bot import get_slack_bot
bot = get_slack_bot()
bot.send_execution_complete(
    ticket_id='PROJ-123',
    pr_url='https://github.com/org/repo/pull/42',
    tests_passed=15,
    tests_failed=0
)
"
```

### 3. Send Error Alert
```bash
python -c "
from shared.slack_bot import get_slack_bot
bot = get_slack_bot()
bot.send_error_alert(
    title='Auth service crash',
    error_message='NullPointerException in login.py:42',
    sentry_link='https://sentry.io/...',
    jira_ticket='PROJ-456'
)
"
```

### 4. Send Status Update
```bash
python -c "
from shared.slack_bot import get_slack_bot
bot = get_slack_bot()
bot.send_agent_status(
    ticket_id='PROJ-123',
    agent='Execution',
    status='In Progress',
    message='Implementing task 2/4'
)
"
```

## Configuration Required

Environment variables:
- `SLACK_BOT_TOKEN` - Bot OAuth token (xoxb-...)
- `SLACK_CHANNEL_AGENTS` - Channel for agent updates
- `SLACK_CHANNEL_ERRORS` - Channel for error alerts
