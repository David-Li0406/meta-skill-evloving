---
name: discovering-tools
description: Progressive disclosure pattern for MCP tools and skills. Use when tools aren't found or you need to discover available capabilities.
---

# Discovering Tools - Progressive Disclosure Pattern

This skill teaches the progressive disclosure pattern for both MCP tools and skills.

## Core Principle

**NEVER load all schemas/skills upfront** - it wastes your context window.

Instead, use a layered approach: discover servers, then tools, then schemas only when needed.

## MCP Tool Discovery

### Step 1: Discover Servers

```python
list_mcp_servers()
```

Returns server names and connection status (~50 tokens total).

### Step 2: List Tools (Lightweight)

```python
list_tools(server="gobby-tasks")
```

Returns tool names and brief descriptions (~100 tokens per server).

### Step 3: Get Full Schema (When Needed)

```python
get_tool_schema(server_name="gobby-tasks", tool_name="create_task")
```

Returns full inputSchema with all parameters.

### Step 4: Execute

```python
call_tool(server_name="gobby-tasks", tool_name="create_task", arguments={
    "title": "Fix bug",
    "task_type": "bug",
    "session_id": "<your_session_id>"
})
```

## Skill Discovery

Skills follow the same pattern:

### Step 1: List Skills (Lightweight)

```python
list_skills()
```

Returns skill names and descriptions (~100 tokens total).

### Step 2: Get Full Skill (When Needed)

```python
get_skill(name="gobby-tasks")
```

Returns full skill content.

### Step 3: Search by Topic

```python
search_skills(query="authentication testing")
```

Finds relevant skills by semantic search.

## Common Mistakes

### Wrong: Loading Everything Upfront

```python
# Don't do this - wastes 5000+ tokens
for server in servers:
    for tool in list_tools(server):
        get_tool_schema(server, tool)  # Unnecessary!
```

### Right: Just-in-Time Discovery

```python
# Only get schema when you're about to call the tool
get_tool_schema("gobby-tasks", "create_task")
call_tool("gobby-tasks", "create_task", {...})
```

## Available Internal Servers

| Server | Purpose |
|--------|---------|
| `gobby-tasks` | Task management |
| `gobby-sessions` | Session handoff |
| `gobby-memory` | Persistent memory |
| `gobby-workflows` | Workflow control |
| `gobby-agents` | Agent spawning |
| `gobby-worktrees` | Git worktrees |
| `gobby-skills` | Skill management |

Use `list_mcp_servers()` to see all connected servers.
