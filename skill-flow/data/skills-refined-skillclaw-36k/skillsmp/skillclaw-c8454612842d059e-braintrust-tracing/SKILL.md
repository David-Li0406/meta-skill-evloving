---
name: braintrust-tracing
description: Use this skill when you need to trace Claude Code sessions in Braintrust, including managing sub-agent correlations and debugging.
---

# Braintrust Tracing for Claude Code

Comprehensive guide to tracing Claude Code sessions in Braintrust, including sub-agent correlation.

## Architecture Overview

```
                         PARENT SESSION
                    +---------------------+
                    |  SessionStart       |
                    |  (creates root)     |
                    +----------+----------+
                               |
                    +----------v----------+
                    |  UserPromptSubmit   |
                    |  (creates Turn)     |
                    +----------+----------+
                               |
          +--------------------+--------------------+
          |                    |                    |
+---------v--------+  +--------v--------+  +--------v--------+
| PostToolUse      |  | PostToolUse     |  | PreToolUse      |
| (Read span)      |  | (Edit span)     |  | (Task - inject) |
+------------------+  +-----------------+  +--------+--------+
                                                    |
                                         +----------v----------+
                                         |   SUB-AGENT         |
                                         |   SessionStart      |
                                         |   (NEW root_span_id)|
                                         +----------+----------+
                                                    |
                                         +----------v----------+
                                         |   SubagentStop      |
                                         |   (has session_id)  |
                                         +---------------------+
```

## Hook Event Flow

| Hook | Trigger | Creates | Key Fields |
|------|---------|---------|------------|
| **SessionStart** | Session begins | Root span | `session_id`, `root_span_id` |
| **UserPromptSubmit** | User sends prompt | Turn span | `prompt`, `turn_number` |
| **PreToolUse** | Before tool runs | (modifies Task prompts) | `tool_input.prompt` |
| **PostToolUse** | After tool runs | Tool span | `tool_name`, `input`, `output` |
| **Stop** | Turn completes | LLM spans | `model`, `tokens`, `tool_calls` |
| **SubagentStop** | Sub-agent finishes | (no span) | `session_id` of sub-agent |
| **SessionEnd** | Session ends | (finalizes root) | `turn_complete` |