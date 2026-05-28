---
name: ClickUp Task Workflow
description: This skill should be used when the user mentions "ClickUp task", "CU-xxx", "task workflow", "clickup integration", or when working with task plugin commands (/task:start, /task:done, /task:merge, /task:status, /task:new). Provides workflow patterns for ClickUp task management integrated with kas.
version: 0.1.0
---

# ClickUp Task Workflow

## Overview

This skill provides workflow patterns for managing ClickUp tasks integrated with kas workflow commands. The core principle: **delegate all ClickUp API calls to the clickup-task-agent** to keep the main conversation context clean.

## Core Principle

**NEVER call ClickUp MCP tools directly in main context.**

All ClickUp operations delegate to the `clickup-task-agent` subagent which returns concise summaries. This prevents verbose API responses from polluting the conversation.

## Command Mapping

| /task Command | kas Command(s) | ClickUp Actions |
|---------------|----------------|-----------------|
| `/task:start CU-xxx` | `/kas:start` | Fetch task, set "in progress", assign |
| `/task:done` | `/kas:verify` → `/kas:done` → PR | Set "ready for review", comment PR |
| `/task:merge` | `/kas:merge` | Set "complete" |
| `/task:status [id]` | None | Fetch and display status |
| `/task:new` | None | Create task via interview |

## Detection Triggers

Activate this skill when detecting:

### Task References
- **URLs**: `https://app.clickup.com/t/...`
- **Task IDs**: `CU-xxx`, `#xxx`, `task xxx`
- **Work phrases**: "work on", "implement", "fix task", "start on"

### Task Creation
- **Creation phrases**: "create task", "new feature", "log bug", "file issue"

## Subagent Delegation Pattern

When needing ClickUp data, spawn the clickup-task-agent:

```
Task tool with subagent_type="task:clickup-task-agent":

"[Operation description]
1. [MCP tool call 1]
2. [MCP tool call 2]

Return ONLY: [concise format]"
```

The agent uses haiku model for speed and returns formatted summaries.

## Git Conventions

- **Branch naming**: `feat/CU-<id>-<slug>` or `fix/CU-<id>-<slug>`
- **Commit messages**: Include `CU-<task-id>` for ClickUp linking
- **PR titles**: Include `[CU-xxx]` prefix

## Error Handling

| Scenario | Action |
|----------|--------|
| Fetch fails at start | Stop, show error, suggest retry |
| Status update fails after kas success | Warn user, show manual command |
| kas command fails | Stop, do NOT update ClickUp |

**Partial failures**: If kas succeeds but ClickUp API fails, warn user and provide manual update command. Don't fail the entire operation for ClickUp sync issues.

## Additional Resources

### Reference Files

For detailed patterns and prompts:
- **`references/subagent-prompts.md`** - Copy-paste subagent prompts for each operation
- **`references/setup.md`** - ClickUp authentication setup
- **`references/task-templates.md`** - Task description templates
