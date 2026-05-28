---
name: collab-session-management
description: Use this skill to start the mermaid-collab server and manage collaborative design sessions.
---

# Body of the merged SKILL.md

## Overview

This skill orchestrates the setup and management of collaborative design sessions using the mermaid-collab server. It ensures the server is running, manages session creation, and processes work items.

## MCP-First Principle

**Always use MCP tools for session/document operations:**

| Operation | MCP Tool |
|-----------|----------|
| Server health | `check_server_health` |
| List sessions | `list_sessions` |
| Session state | `get_session_state`, `update_session_state` |
| Documents | `get_document`, `list_documents`, `create_document`, `update_document`, `patch_document` |
| Diagrams | `get_diagram`, `list_diagrams`, `create_diagram`, `update_diagram`, `patch_diagram` |
| Snapshots | `has_snapshot`, `save_snapshot`, `load_snapshot`, `delete_snapshot` |
| UI | `render_ui`, `update_ui`, `dismiss_ui` |

**Bash only for:**
- Git commands (`git status`, `git commit`, etc.)
- External tools not available via MCP
- File operations outside `.collab/` folder

## Start Collab

### Step 1: Check Server Status

```bash
curl -s http://localhost:3737 > /dev/null 2>&1 && echo "running" || echo "not running"
```

### Step 2: Start Server If Needed

**If not running:**

Get the plugin install path and start the server:

```bash
bun run <plugin-path>/bin/mermaid-collab.ts start
```

Where `<plugin-path>` is the directory containing this skill (the plugin root).

To find the plugin path, use the path of this skill file and go up two directories.

Wait for the server to start (the CLI will confirm).

**If already running:** Continue to Step 3.

### Step 3: Invoke Collab Skill

```
Invoke skill: collab
```

This hands off to the collab skill which will:
- Show existing sessions or create a new one
- Guide through the full collab workflow

## Collab Sessions

Start or resume a collaborative design session. The mermaid-collab server must be running.

This skill manages session creation, the work item loop, and coordinates other skills.

### Session Management

**Key steps:**
- **Find Sessions** - List existing sessions with their phases
- **Create Session** - Generate name, create files, invoke gather-session-goals
- **Resume Session** - Restore from snapshot or route through ready-to-implement

**Invoke skill: collab-session-mgmt** for detailed session management procedures.

### Work Item Loop

The core orchestration loop that processes work items one at a time.

**Key steps:**
- Read design doc and parse work items
- Find first pending item
- Route by type (bugfix → systematic-debugging, task → task-planning, code → rough-draft)
- Mark item documented and continue loop
- When all items done → invoke ready-to-implement

**Invoke skill: collab-work-item-loop** for detailed work item loop procedures.

## Folder Structure

```
.collab/
└── <session-name>/
    ├── diagrams/
    ├── documents/
    │   └── design.md
    └── collab-state.json
```

## State Tracking (collab-state.json)

```json
{
  "phase": "brainstorming",
  "lastActivity": "2026-01-19T10:30:00Z",
  "currentItem": null,
  "pendingVerificationIssues": []
}
```

**Fields:**
- `phase` - Current workflow phase
- `lastActivity` - ISO timestamp of last activity
- `currentItem` - Item number being processed (null when not in loop)
- `pendingVerificationIssues` - Issues from verification phase

**Phase values:**
- `brainstorming` - Work item loop / brainstorming phase
- `rough-draft/interface` - Defining interfaces
- `rough-draft/pseudocode` - Logic flow
- `rough-draft/skeleton` - Stub files
- `implementation` - Executing the plan

## MCP Tools Reference

| Action | Tool |
|--------|------|
| Generate session name | `mcp__mermaid__generate_session_name()` |
| Create diagram | `mcp__mermaid__create_diagram({ project, session, name, content })` |
| Create document | `mcp__mermaid__create_document({ project, session, name, content })` |
| Preview diagram | `mcp__mermaid__preview_diagram({ project, session, id })` |
| Preview document | `mcp__mermaid__preview_document({ project, session, id })` |

**Note:** `project` is the current working directory (absolute path). `session` is the session name.

## Helper Functions

### parseWorkItems(designDoc)

Parses the design doc and extracts work items.

```
FUNCTION parseWorkItems(doc):
  items = []
  FOR each "### Item N:" section in doc:
    item = {
      number: N,
      title: parse title after "### Item N:",
      type: parse **Type:** field value,
      status: parse **Status:** field value
    }
    ADD item to items
  RETURN items
```

**Example parsing:**
```markdown
### Item 1: Add user authentication
**Type:** feature
**Status:** pending
```
→ `{ number: 1, title: "Add user authentication", type: "feature", status: "pending" }`

## Integration

**Transitions to:**
- **gather-session-goals** - After creating new session (collect work items)
- **brainstorming** - From work item loop for code and task items
- **systematic-debugging** - From work item loop for bugfix items
- **task-planning** - From brainstorming for task items
- **rough-draft** - From brainstorming for code items
- **ready-to-implement** - When all items documented or on resume

**Called by:**
- User directly via `/collab` command
- Any workflow starting collaborative design work

**Collab Workflow Chain:**
```
collab --> gather-session-goals --> work-item-loop --> ready-to-implement --> rough-draft --> executing-plans
                                         |                    ^
                                         |    (all documented)|
                                         v                    |
                                    brainstorming ────────────┤
                                         |                    |
                                    ┌────┴────┐              |
                                    v         v              |
                            task-planning  rough-draft ──────┘
                                    |
                            executing-plans
                                    |
                            systematic-debugging ────────────┘
```