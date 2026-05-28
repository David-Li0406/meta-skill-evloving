---
name: message-handling
description: Pending message delivery and processing for Ralph agents - watchdog restart, message reading
category: coordination
depends-on: [ralph-core, ralph-event-protocol]
---

# Message Handling Skill

> "The watchdog delivers messages by restarting your process - always check for pending messages on startup."

## When to Use This Skill

Use this when you are **any Ralph agent** (PM, Developer, QA) in event-driven mode.

## How Message Delivery Works

**IMPORTANT**: The watchdog delivers messages to you by **restarting your agent process**.

When the watchdog has messages for you, it:

1. Writes messages to `.claude/session/pending-messages-{agent}.json`
2. Restarts your agent process
3. You must read and process the file on startup

## Startup Message Check (CRITICAL)

**On EVERY startup (or after context reset), check for delivered messages:**

```powershell
# Source message queue
. .\.claude\scripts\message-queue.ps1

# Check for messages delivered by watchdog
$pendingFile = ".claude/session/pending-messages-{agent}.json"
if (Test-Path $pendingFile) {
    $pending = Get-Content $pendingFile -Raw | ConvertFrom-Json
    Write-Host "Received $($pending.messageCount) message(s) from watchdog" -ForegroundColor Cyan

    # Process each message
    foreach ($msg in $pending.messages) {
        switch ($msg.type) {
            "task_assign" {
                # Task assignment from PM/watchdog
                Write-Host "Task assigned: $($msg.payload.taskId)" -ForegroundColor Green
            }
            "priority_response" {
                # PM responded to your question
                Write-Host "PM response: $($msg.payload.decision)" -ForegroundColor Yellow
            }
            "validation_request" {
                # QA requested validation
                Write-Host "Validation requested: $($msg.payload.taskId)" -ForegroundColor Green
            }
            "retrospective_initiate" {
                # PM triggers retrospective
                Write-Host "Retrospective initiated for: $($msg.payload.taskId)" -ForegroundColor Magenta
            }
            default {
                Write-Host "Received message type: $($msg.type) from $($msg.from)" -ForegroundColor Gray
            }
        }
    }

    # Delete the file after processing
    Remove-Item $pendingFile -Force
}
```

## Message Types by Agent

### PM Agent Receives

| Type | From | Action Required |
|------|------|-----------------|
| `question` | developer/qa | Research and respond |
| `work_blocked` | developer/qa | Assess severity, provide guidance |
| `task_abandoned` | developer/qa | Reassign or escalate |
| `skill_request` | developer/qa | Add to retrospective, address later |

### Developer Agent Receives

| Type | From | Action Required |
|------|------|-----------------|
| `task_assign` | watchdog | Read task, begin implementation |
| `priority_response` | pm | PM answered your question, continue work |
| `bug_report` | qa | Fix bugs, re-submit |

### QA Agent Receives

| Type | From | Action Required |
|------|------|-----------------|
| `validation_request` | developer/pm | Run validation suite |
| `priority_response` | pm | PM answered your question, continue validation |
| `retrospective_initiate` | pm | Add your perspective to retrospective |

## Sending Messages

### Source message queue functions

```powershell
# Source message queue
. .\.claude\scripts\message-queue.ps1
```

### Common Message Sends

**Send a question to PM:**

```powershell
Send-Question -From "developer" -To "pm" -Question "How should I...?" -TaskId "feat-001"
```

**Report blocker to PM:**

```powershell
Send-WorkBlocked -TaskId "feat-001" -Blocker "Can't find specification"
```

**Send completion message (Developer → QA):**

```powershell
Send-ImplementationComplete -TaskId "feat-001" -Commit "abc123" -Summary "Implemented feature"
```

**Send validation result (QA → PM):**

```powershell
# Pass
Send-AgentMessage -From "qa" -To "pm" -Type "task_complete" -Payload @{
    taskId = "feat-001"
    summary = "Validation passed"
    validationPassed = $true
} -Priority "normal"

# Fail
$bugs = @(@{ severity = "high"; issue = "..." })
Send-AgentMessage -From "qa" -To "pm" -Type "bug_report" -Payload @{
    taskId = "feat-001"
    bugs = $bugs
} -Priority "high"
```

## Message Processing Priority

Process in this order:

| Priority | Message Types | Action |
|----------|---------------|--------|
| URGENT | `work_blocked`, `task_abandoned` | Immediate attention |
| HIGH | `question`, `bug_report` | Respond promptly |
| NORMAL | `task_complete`, `skill_request` | Process in order |
| LOW | `status_update` | Log and continue |

## Idempotency

After processing a message, **delete it from your inbox**:

```powershell
Remove-AgentMessage -Agent "{agent}" -MessageId $msg.id
```

This prevents reprocessing the same message if your agent restarts.

## Pending Message File Format

```json
{
  "messageCount": 2,
  "messages": [
    {
      "id": "msg-123",
      "type": "task_assign",
      "from": "pm",
      "timestamp": "2026-01-21T10:15:30Z",
      "payload": {
        "taskId": "feat-001",
        "title": "Task Title"
      }
    },
    {
      "id": "msg-456",
      "type": "priority_response",
      "from": "pm",
      "timestamp": "2026-01-21T10:16:00Z",
      "payload": {
        "decision": "Use approach A",
        "reason": "..."
      }
    }
  ]
}
```

## Troubleshooting

### No pending messages found

If the file doesn't exist or is empty:
- No messages waiting for you
- Continue with normal workflow

### Messages not processed

If you exit without processing:
- Messages will remain in the file
- Watchdog will restart you again
- You'll get the same messages

### File corrupted

If JSON is invalid:
- Log error to progress file
- Contact PM for help
- Do NOT modify the file yourself

## Anti-Patterns

❌ **DON'T:**
- Skip checking pending messages on startup
- Process messages but forget to delete the file
- Modify pending messages file (only read/delete)
- Send messages without sourcing message-queue.ps1

✅ **DO:**
- Always check on startup (before any other work)
- Delete file immediately after processing all messages
- Use proper helper functions for sending messages
- Handle unexpected message types gracefully

## Reference

- [`.claude/skills/ralph-core.md`](ralph-core.md) — Session structure
- [`.claude/skills/ralph-event-protocol.md`](ralph-event-protocol.md) — Complete message protocol
- [`.claude/skills/worker-protocol.md`](worker-protocol.md) — Worker pool workflow
