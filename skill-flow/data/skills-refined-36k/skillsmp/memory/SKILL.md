---
name: memory
description: |
  AI agent long-term memory management skill (openmemory-py based).
  Store and retrieve conversation context, user preferences, and important information via semantic search.
  
  Note: Automatic context management is handled by the context-manager plugin.
  This skill is used when the agent **explicitly** manipulates memory.
  
  When to use:
  (1) When user requests memory save/retrieve → /memory add, /memory query
  (2) When agent determines additional context is needed → /memory query
  (3) When deleting unnecessary memories → /memory delete
---

# Memory Skill

OpenMemory-based AI agent long-term memory management.

## Relationship with Plugin

```
┌─────────────────────────────────────────────────────┐
│         memory Skill (Explicit Memory Ops)          │
│     • /memory add - Manually add memory             │
│     • /memory query - Manually search memories      │
│     • /memory list - List memories                  │
│     • /memory delete - Delete memory                │
│     • /memory status - Show memory system status    │
└─────────────────────────────────────────────────────┘
```

## When to Use?

### ✅ Use This Skill

1. **On User Request**
   - "Remember this" → `/memory add`
   - "Find what we analyzed before" → `/memory query`
   - "Delete that memory" → `/memory delete`

2. **Agent Autonomous Decision**
   - When additional context is needed for current task → `/memory query`
   - When saving important learnings permanently → `/memory add`
   - When discovering user preferences or patterns → `/memory add`

### 🔄 Plugin Handles Automatically (Implicit)
- Load related context at task start → `context_start` tool
- Mid-task checkpoints → `context_checkpoint` tool
- Save results at task end → `context_end` tool

## CLI Usage

```bash
# Add memory
/memory add "User prefers Python development" --tags=preferences,programming

# Search memory (semantic search)
/memory query "areas of interest" --limit=5

# List memories
/memory list --limit=10

# Delete memory
/memory delete <memory_id>

# Show status
/memory status

# Clear all memories (caution!)
/memory clear --confirm
```

## Python API

```python
from scripts.memory_client import MemoryClient

with MemoryClient() as mem:
    # Add
    mem.add("Important info", tags=["tag1"], metadata={"source": "chat"})
    
    # Search
    results = mem.query("search term", limit=5)
    
    # Delete
    mem.delete(memory_id)
```

## Tag Guide

| Tag | Purpose |
|-----|---------|
| `preferences` | User preferences |
| `topics` | Topics of interest |
| `projects` | Projects of interest |
| `context` | Conversation context |
| `decision` | Decision history |
| `checkpoint` | Task checkpoint (auto) |
| `result` | Task result (auto) |

## Storage Location

OpenMemory data stored in `data/memory/` directory.
Shares the same DB with Context Manager.

## Dependencies

```
openmemory-py>=1.3.0
langchain>=1.0.0
langchain-core>=1.0.0
```
