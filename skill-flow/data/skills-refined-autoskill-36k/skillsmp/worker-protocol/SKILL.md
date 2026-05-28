---
name: worker-protocol
description: Worker pool architecture - agents complete work and exit, watchdog orchestrates
category: orchestration
depends-on: [ralph-core]
---

# Worker Protocol

> "The heartbeat of Ralph agents - complete work, send message, exit."

## Overview

The **Worker Protocol** replaces the legacy polling-based architecture with an event-driven worker pool model:

- **Agents** are workers that complete assigned tasks and exit
- **Watchdog** orchestrates by spawning agents sequentially based on completion messages
- **Named pipes** provide bidirectional communication for task assignment and completion signaling
- **NO polling** - agents do not continuously check state
- **NO infinite loops** - agents complete work and exit

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    WATCHDOG (Orchestrator)                       │
│                                                                   │
│  1. Spawn agent with task                                       │
│  2. Wait for completion message via pipe (BLOCKING)            │
│  3. Agent exits                                                │
│  4. Decide next agent based on message type                    │
│  5. Repeat until session complete                               │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                ┌───────────▼─────────────┐
                │  Pipe Message Flow:     │
                │  Agent → Watchdog       │
                │  "task_complete"        │
                │  "validation_request"   │
                │  "validation_result"    │
                └──────────────────────────┘

Agent Lifecycle (NO LOOP!):
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   START     │ ──▶ │  DO WORK     │ ──▶ │   EXIT      │
│ (connect to │     │ (complete    │     │ (send pipe  │
│  pipe)      │     │  single task) │     │  message)   │
└─────────────┘     └──────────────┘     └─────────────┘
```

## Message Format

```json
{
  "type": "task_assign|task_complete|validation_request|validation_result|session_complete",
  "from": "watchdog|pm|developer|qa",
  "to": "watchdog|pm|developer|qa",
  "payload": {
    "taskId": "feat-001",
    "status": "completed|needs_fixes|passed|failed",
    "task": { ... }
  },
  "id": "unique-guid",
  "timestamp": "2026-01-21T10:15:30Z"
}
```

## Message Types and Workflow

| Message Type | From | When Sent | Next Agent | Payload |
| ------------ | ---- | --------- | ---------- | ------- |
| `task_assign` | watchdog | Agent spawned with task | (agent receives) | `{ task: {...} }` |
| `task_complete` | developer | Feature implemented | qa | `{ taskId, status }` |
| `validation_request` | developer | Ready for QA | qa | `{ taskId }` |
| `validation_result` | qa | QA complete | pm (if passed) or developer (if failed) | `{ taskId, status: "passed"\|"failed" }` |
| `need_retrospective` | pm | Trigger retrospective | pm | `{ taskId }` |
| `session_complete` | pm | All PRD items complete | (watchdog exits) | `{ }` |

## Agent Workflow

### 1. Startup

```powershell
# Source agent-pipe.ps1
. .\.claude\scripts\agent-pipe.ps1

# Initialize pipe connection to watchdog
Initialize-AgentPipe

# Send ready message (automatic in Initialize-AgentPipe)
```

### 2. Receive Task

```powershell
# Block until task assignment received from watchdog
$taskMsg = Receive-WatchdogTask

# Task is in $taskMsg.payload.task
$taskId = $taskMsg.payload.task.id
```

### 3. Complete Work

```powershell
# Do the assigned work (implement feature, run validation, etc.)
# ... work here ...
```

### 4. Send Completion Message

```powershell
# Send completion message based on work done
Send-CompletionMessage -MessageType "task_complete" -Payload @{
    taskId = $taskId
    status = "completed"
}
```

### 5. Exit

```powershell
# Clean up pipe resources
Stop-AgentPipe

# Process exits - watchdog will spawn next agent
exit 0
```

## Watchdog Workflow

### 1. Initialize Pipes

```powershell
. .\.claude\scripts\watchdog-pipe.ps1
Initialize-WatchdogPipes
```

### 2. Spawn Agent (BLOCKING)

```powershell
# This blocks until agent completes and sends message
$completionMsg = Start-AgentWithPipes -AgentName "developer" -CommandLine $cmd -TaskPayload $taskPayload
```

### 3. Process Completion Message

```powershell
# Decide next agent based on message type
$nextAgent = switch ($completionMsg.type) {
    "task_complete" { "qa" }
    "validation_result" {
        if ($completionMsg.payload.status -eq "passed") { "pm" } else { "developer" }
    }
    "session_complete" { $null }  # Exit
}
```

### 4. Repeat or Exit

```powershell
if ($nextAgent) {
    # Spawn next agent
    Start-AgentWithPipes -AgentName $nextAgent ...
} else {
    # Session complete
    Write-Host "Session complete!"
}
```

## Key Differences from Polling Protocol

| Aspect | Polling (Legacy) | Worker Pool (Current) |
| ------- | ---------------- | --------------------- |
| Agent lifecycle | Infinite loop | Complete work and exit |
| State checking | Every 30 seconds | Once per task |
| Heartbeat | Periodic (30s) | None (completion message only) |
| Watchdog role | Route messages | Orchestrate agent spawning |
| Message delivery | Restart agent with pending messages | Send via pipe |

## Pipe Communication Scripts

### Shared Utilities (Phase 2 Implementation)

**File:** `.claude/scripts/pipe-transport.ps1` (Created in Phase 2)

```powershell
# === SERVER SIDE (Watchdog) ===
- Initialize-PipeServer        # Create named pipes for all agents
- Send-MessageViaPipe          # Send message to agent via pipe
- Test-PipeConnected           # Check if agent is connected
- Get-PipeStats                # Get pipe statistics
- Close-PipeServer             # Cleanup on shutdown

# === CLIENT SIDE (Agent) ===
- Connect-AgentPipe            # Connect to watchdog pipe
- Read-PipeMessage             # Read message from pipe (blocking)
- Enter-PipeMessageLoop        # Enter continuous message loop
- Close-AgentPipe              # Cleanup and disconnect
```

### Watchdog Integration

The watchdog automatically sources `pipe-transport.ps1` and initializes the pipe server on startup if available:

```powershell
# From watchdog-event.ps1
$pipeTransportModule = Join-Path $PSScriptRoot "pipe-transport.ps1"
if (Test-Path $pipeTransportModule) {
    . $pipeTransportModule
    $Script:UsePipeTransport = $true
    Initialize-PipeServer -SessionDir $paths.SessionDir
}
```

### Agent Integration

Agents can use the pipe transport in two modes:

#### Mode 1: Continuous Execution (Phase 2 - Full Pipe Support)

Agent runs continuously, processing messages from pipe:

```powershell
# Agent connects and processes messages continuously
Enter-PipeMessageLoop -AgentName "developer" -MessageHandler {
    param($msg)
    # Process message based on type
    switch ($msg.type) {
        "task_assign" { Process-TaskAssignment $msg.payload }
        "shutdown" { exit 0 }
        default { Write-Warning "Unknown message type: $($msg.type)" }
    }
}
```

#### Mode 2: Worker Pool (Current - File Queue Fallback)

Agent completes single task and exits. Watchdog restarts with new messages.

This fallback is used when:
- Pipe transport module not available
- Agent not connected to pipe
- Pipe delivery fails

### Message Delivery Priority

1. **Named Pipe** (if available and connected) - <10ms delivery
2. **File Queue + Restart** (fallback) - 2000-5000ms delivery

The watchdog automatically falls back to file queue if pipe delivery fails.

## Example Flow

### Typical Development Cycle

```
1. WATCHDOG spawns PM
   ├─ Pipe: task_assign with { nextTask: "feat-001" }
   └─ PM assigns task to developer

2. PM exits → WATCHDOG spawns Developer
   ├─ Pipe: task_assign with { task: { id: "feat-001", ... } }
   └─ Developer implements feature

3. Developer sends: task_complete
   └─ Developer exits

4. WATCHDOG spawns QA
   ├─ Pipe: task_assign with { validation: { taskId: "feat-001" } }
   └─ QA runs validation

5. QA sends: validation_result with { status: "passed" }
   └─ QA exits

6. WATCHDOG spawns PM (for retrospective)
   ├─ Pipe: task_assign with { retrospective: { taskId: "feat-001" } }
   └─ PM runs retrospective and skill research

7. PM sends: task_complete (next task)
   └─ PM exits

8. WATCHDOG spawns Developer for next task
   ... repeat until all tasks complete
```

## Exit Conditions

Agents exit under these conditions:

1. **Work completed** → Send completion message → Exit
2. **Need PM clarification** → Send `question` message → Exit
3. **Session complete** → Send `session_complete` → Exit

Watchdog exits when:

1. All PRD items have `passes: true`
2. PM sends `session_complete` message
3. `/cancel-ralph` invoked

## See Also

- [ralph-core.md](ralph-core.md) — Session structure
- [event-protocol.md](event-protocol.md) — Event-driven architecture
- [polling-protocol.md](polling-protocol.md) — **LEGACY** - Do not use
