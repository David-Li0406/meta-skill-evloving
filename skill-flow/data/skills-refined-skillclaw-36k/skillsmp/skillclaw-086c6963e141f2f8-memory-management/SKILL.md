---
name: memory-management
description: Use this skill when you need to manage project memory effectively, ensuring that the file system serves as the ultimate source of truth.
---

# Memory Management Skill

This skill focuses on project memory management. **Remember: the file system is the only truth.**

## Asynchronous Awareness

> You are just one of many concurrently running AI sessions. Do not rely on session memory.

## Dual Persistence

### 1. MCP Memory
```javascript
memory.recall({ project_path: "/path/to/project" })
memory.add({ content: "...", category: "rule" })
```

### 2. File System (Priority)
```
project_document/.ai_state/
├── active_context.md   # Current task status
├── conventions.md      # Project conventions
└── decisions.md        # Decision records
```

## Startup Protocol

```
1. Read project_document/.ai_state/active_context.md
2. memory.recall(project_path)
3. Report current status
```

## Shutdown Protocol

```
1. Update task status
2. memory.add important decisions
3. Save to .ai_state/
```

## Category Classification

| Type        | Purpose         |
|:-----------|:----------------|
| `rule`     | Project rules   |
| `preference` | User preferences |
| `pattern`  | Common patterns  |
| `context`  | Project background |

## Degradation

If memory is unavailable → completely rely on the .ai_state files.