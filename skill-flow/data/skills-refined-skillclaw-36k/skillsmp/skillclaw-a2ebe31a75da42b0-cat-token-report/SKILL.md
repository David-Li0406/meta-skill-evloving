---
name: cat:token-report
description: Use this skill to generate a detailed token usage report with threshold analysis and recommendations for context management.
---

# Token Report

## Purpose

Analyze token consumption from session files to understand context utilization, detect concerning patterns, and provide recommendations for context management. Essential for monitoring session resource consumption and ensuring efficient orchestration.

## Prerequisites

**Session ID**: The session ID is automatically available as `${CLAUDE_SESSION_ID}` in this skill. All bash commands below use this value directly.

## When to Use

- Periodic health checks during long-running orchestration
- After subagent completion to analyze efficiency
- When monitoring detects approaching context limits
- To inform decomposition decisions
- Post-task retrospectives on token efficiency

## Workflow

### 1. Locate Session File

Session file location (uses auto-substituted session ID):

```bash
# Session file location
SESSION_FILE="/home/node/.config/claude/projects/-workspace/${CLAUDE_SESSION_ID}.jsonl"

# Verify file exists
if [ ! -f "${SESSION_FILE}" ]; then
  echo "ERROR: Session file not found for ${CLAUDE_SESSION_ID}"
  exit 1
fi
```

### 2. Check for Pre-Computed Results (MANDATORY)

**CRITICAL**: This skill requires hook-based pre-computation. Check context for:

```
PRE-COMPUTED TOKEN REPORT:
```

### If PRE-COMPUTED TOKEN REPORT is found:

Output the table EXACTLY as provided. Do NOT modify alignment or recalculate values.

**Example pre-computed output:**
```
╭───────────────────┬────────────────────────────────┬──────────┬──────────────────┬────────────╮
│ Type              │ Description                    │ Tokens   │ Context          │ Duration   │
├───────────────────┼────────────────────────────────┼──────────┼──────────────────┼────────────┤
│ Explore           │ Explore codebase               │ 68.4k    │ 34%              │ 1m 7s      │
│ general-purpose   │ Implement fix                  │ 90.0k    │ 45% ⚠️            │ 43s        │
│ general-purpose   │ Refactor module                │ 170.0k   │ 85% 🚨            │ 3m 12s     │
├───────────────────┼────────────────────────────────┼──────────┼──────────────────┼────────────┤
│                   │ TOTAL                          │ 328.4k   │ -                │ 5m 2s      │
╰───────────────────┴────────────────────────────────┴──────────┴──────────────────┴────────────╯
```

### If PRE-COMPUTED TOKEN REPORT is NOT found:

**FAIL immediately** with this message:

```
ERROR: Pre-computed token report not found.

The hook precompute-token-report.sh should have provided the table data.
Do NOT attempt manual computation - the alignment requires deterministic Python-based calculation.

Possible causes:
1. Session file not found
2. No subagent data in session
3. Hook execution failed

Try running /cat:token-report again or check session status.
```

### 3. Extract Subagent Token Usage

**Primary Metric:** Extract `totalTokens` from Task tool completions (matches CLI display).

```bash
# Extract Task tool completions with their descriptions and metrics
# This jq command correlates Task invocations with their results via tool_use_id

SESSION_FILE="/home/node/.config/claude/projects/-workspace/${CLAUDE_SESSION_ID}.jsonl"

# Build lookup tables for Task invocations (description and type) by tool_use_id
SUBAGENT_DATA=$(jq -s '
  # Build map of tool_use_id -> {description, type} from Task invocations
  (
    [.[] | select(.type == "assistant") | .message.content[]? |
     select(.type == "tool_use" and .name == "Task") |
     {key: .id, value: {description: .input.description, type: (.input.subagent_type // "unknown")}}] | from_entries
  ) as $task_map |

  # Extract Task completions with their metrics
  [.[] | select(.type == "user" and .toolUseResult.totalTokens != null) |
   ($task_map[.message.content[0].tool_use_id] // {description: "Unknown", type: "unknown"}) as $task_info |
   {
     tool_use_id: .message.content[0].tool_use_id,
     description: $task_info.description,
     subagent_type: $task_info.type,
     totalTokens: .toolUseResult.totalTokens,
     totalDurationMs: .toolUseResult.totalDurationMs,
     totalToolUseCount: .toolUseResult.totalToolUseCount
   }
  ]
')
```