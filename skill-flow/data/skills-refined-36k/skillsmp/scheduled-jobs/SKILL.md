---
name: scheduled-jobs
description: Use when automating recurring tasks in spaces, setting up cron-like schedules, running agent prompts on a timer, or configuring periodic automation
---

# Scheduled Jobs

Define automated tasks in space manifests that run on schedules - agent prompts, shell commands, Apple Shortcuts, or workflows.

## When to Use

- Running agent tasks on a schedule (daily summaries, weekly reports)
- Automating shell commands at specific times
- Triggering Apple Shortcuts periodically
- Setting up any recurring automation in a space

## Job Definition

Add to `.manifest/app.json`:

```json
{
  "jobs": [
    {
      "id": "daily-summary",
      "name": "Daily Summary",
      "schedule": { "cron": "0 9 * * *" },
      "action": {
        "type": "agent_prompt",
        "prompt": "Generate a summary of yesterday's activity"
      },
      "notifications": {
        "onComplete": true,
        "onError": true
      },
      "enabled": true,
      "runMissedOnWake": true
    }
  ]
}
```

## Schedule Types

### Cron Expression

Standard 5-field cron format: `minute hour dayOfMonth month dayOfWeek`

```json
{ "cron": "0 9 * * 1-5" }    // Weekdays at 9am
{ "cron": "0 */2 * * *" }    // Every 2 hours
{ "cron": "30 8 1 * *" }     // 8:30am on 1st of month
```

### Natural Language

Converted to cron internally:

```json
{ "natural": "every weekday at 9am" }
{ "natural": "every day at noon" }
{ "natural": "every monday" }
{ "natural": "every hour" }
```

### Interval

Minutes between runs:

```json
{ "interval": 30 }     // Every 30 minutes
{ "interval": 60 }     // Every hour
{ "interval": 1440 }   // Every 24 hours
```

### One-Time

Single execution at specific time:

```json
{ "once": "2025-02-01T09:00:00Z" }
```

## Action Types

### Agent Prompt

Run agent with a prompt and optional tools:

```json
{
  "type": "agent_prompt",
  "prompt": "Search for new job postings matching my preferences",
  "tools": ["web_search", "files"]
}
```

### Shell Command

Execute in space directory:

```json
{
  "type": "shell",
  "command": "python scripts/sync.py",
  "workingDirectory": "scripts"
}
```

### Apple Shortcut

Run Shortcuts.app automation:

```json
{
  "type": "shortcut",
  "name": "My Shortcut",
  "input": { "key": "value" }
}
```

### Temporal Workflow

Trigger durable workflow:

```json
{
  "type": "workflow",
  "name": "data-pipeline",
  "input": { "source": "api" }
}
```

## Notifications

Configure alerts on completion or failure:

```json
{
  "notifications": {
    "onComplete": true,
    "onError": true
  }
}
```

## Job Options

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique identifier |
| `name` | string | Display name |
| `schedule` | object | When to run |
| `action` | object | What to execute |
| `notifications` | object | Alert settings |
| `enabled` | bool | Active status |
| `runMissedOnWake` | bool | Run if missed while asleep |

## Quick Reference

**Common schedules:**

| Pattern | Cron | Natural |
|---------|------|---------|
| Daily 9am | `0 9 * * *` | `every day at 9am` |
| Weekdays 9am | `0 9 * * 1-5` | `every weekday at 9am` |
| Hourly | `0 * * * *` | `every hour` |
| Every 30 min | `*/30 * * * *` | - |
| Monday 10am | `0 10 * * 1` | `every monday at 10am` |
| Monthly 1st | `0 9 1 * *` | - |

**Cron fields:** `minute(0-59) hour(0-23) day(1-31) month(1-12) weekday(0-6)`

## Example: Career Space Jobs

```json
{
  "jobs": [
    {
      "id": "daily-job-search",
      "name": "Daily Job Search",
      "schedule": { "natural": "every weekday at 9am" },
      "action": {
        "type": "agent_prompt",
        "prompt": "Search for new Senior Engineer postings. Update tracking spreadsheet."
      },
      "notifications": { "onComplete": true }
    },
    {
      "id": "weekly-summary",
      "name": "Weekly Application Summary",
      "schedule": { "cron": "0 18 * * 5" },
      "action": {
        "type": "agent_prompt",
        "prompt": "Generate a weekly summary of job applications and interviews."
      }
    },
    {
      "id": "backup-notes",
      "name": "Backup Interview Notes",
      "schedule": { "interval": 1440 },
      "action": {
        "type": "shell",
        "command": "cp -r notes/ ~/Backups/career-notes-$(date +%Y%m%d)/"
      }
    }
  ]
}
```

## Execution

Jobs run via AgentKitD daemon:

1. **Discovery**: Jobs loaded from space manifests on daemon start
2. **Scheduling**: Timer evaluates schedules every minute
3. **Execution**: Due jobs dispatched to JobExecutor
4. **Logging**: Results stored in `~/.agents/jobs/`
5. **Notifications**: User notified on complete/error

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Job never runs | Check `enabled: true`, verify cron syntax |
| Missed while asleep | Add `runMissedOnWake: true` |
| Wrong timezone | Cron uses system timezone |
| Agent prompt fails | Ensure tools exist and are available |
| No notifications | Add `notifications` object to job |
