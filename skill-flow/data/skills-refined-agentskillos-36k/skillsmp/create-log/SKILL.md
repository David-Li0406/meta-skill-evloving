---
name: create-log
description: Add a log entry to the workflow log
argument-hint: <workflow-id> <level> <step> <message>
---

# Create Log

## Overview

Add a structured log entry to the workflow's NDJSON log file. Use this skill for progress milestones, errors, warnings, decisions, and context that should be recorded. Creates a structured log entry in the workflow's log file for tracking and debugging.

## Arguments

### Definitions

- **`<workflow-id>`** (required): The workflow identifier for output organization.
- **`<level>`** (required): Log level. Values: `Critical`, `Error`, `Warning`, `Information`.
- **`<step>`** (required): Step name for context (e.g., analyze, plan, review).
- **`<message>`** (required): Log message.

### Values

\$ARGUMENTS

## Core Principles

- Use appropriate log levels for severity
- Include step context for traceability
- Messages should be concise but informative
- Logs are append-only

### Log Levels

| Level       | When to Use                              |
| ----------- | ---------------------------------------- |
| Critical    | Fatal error causing workflow to stop     |
| Error       | Any error that occurred                  |
| Warning     | Unexpected issue that may need attention |
| Information | Regular progress logging                 |

## Instructions

1. Parse the workflow-id, level, step, and message
2. Generate timestamp in ISO 8601 format
3. Create NDJSON log entry
4. Append to `agentic/outputs/{workflow-id}/logs.ndjson`
5. Return confirmation with entry details

## Output Guidance

Return JSON confirmation:

```json
{
  "success": true,
  "entry": {
    "timestamp": "2024-01-15T10:30:00Z",
    "level": "Information",
    "step": "implement",
    "message": "Completed milestone 1"
  }
}
```

## Templates

### Log File Format

Logs are stored in `agentic/outputs/{workflow-id}/logs.ndjson` as NDJSON:

```json
{"timestamp":"2024-01-15T10:30:00Z","level":"Information","step":"implement","message":"Started implementation","context":null}
{"timestamp":"2024-01-15T10:35:00Z","level":"Warning","step":"implement","message":"Rate limit approached","context":{"remaining":10}}
```
