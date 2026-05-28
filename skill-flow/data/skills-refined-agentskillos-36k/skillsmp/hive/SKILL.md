---
name: hive
description: Multi-agent coordination - redirects to hivemind MCP tools
---

# /hive - Multi-Agent Coordination

All Hivemind commands are available as MCP tools. When the user runs `/hive <command>`, call the corresponding MCP tool.

## Command Mapping

| User Command | MCP Tool to Call |
|--------------|------------------|
| `/hive` or `/hive help` | `hive_help` |
| `/hive whoami` | `hive_whoami` |
| `/hive agents` | `hive_agents` |
| `/hive status` | `hive_status` |
| `/hive message <target> <text>` | `hive_message` with `target` and `body` |
| `/hive read` or `/hive messages` | `hive_read_messages` |
| `/hive changes [n]` | `hive_changes` with optional `count` |
| `/hive task [description]` | `hive_task` with optional `description` |

## Instructions

Parse `$ARGUMENTS` and call the corresponding MCP tool:

1. If no arguments or `help`: Call `hive_help`
2. If `whoami`: Call `hive_whoami`
3. If `agents`: Call `hive_agents`
4. If `status`: Call `hive_status`
5. If `message <target> <text>`: Call `hive_message` with `{"target": "<target>", "body": "<text>"}`
6. If `read` or `messages`: Call `hive_read_messages` (reads and consumes messages)
7. If `changes [n]`: Call `hive_changes` with `{"count": n}` (default 20)
8. If `task [description]`: Call `hive_task` with `{"description": "<description>"}` (empty to clear)

The MCP tools handle all coordination logic.

## Examples

```
/hive
```
-> Call `hive_help`

```
/hive whoami
```
-> Call `hive_whoami`

```
/hive message bravo Please hold off on auth.ts
```
-> Call `hive_message` with `{"target": "bravo", "body": "Please hold off on auth.ts"}`

```
/hive task Implementing user authentication
```
-> Call `hive_task` with `{"description": "Implementing user authentication"}`

```
/hive task
```
-> Call `hive_task` with `{"description": ""}` to clear

```
/hive changes 10
```
-> Call `hive_changes` with `{"count": 10}`
