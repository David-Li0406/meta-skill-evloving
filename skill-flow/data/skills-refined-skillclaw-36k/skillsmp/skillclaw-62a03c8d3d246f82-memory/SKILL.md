---
name: memory
description: Use this skill for managing project memory, allowing for persistent context and decision-making across sessions.
---

# Memory Skill

This skill manages project memory, enabling the persistence of context and decisions across sessions.

## Core Principles

> **Fact-based**: Only store facts and decisions in memory, avoiding assumptions.

## Automatic Triggers

| Trigger Condition | Action |
|:---|:---|
| Start of conversation | `memory.recall(project_path)` |
| User says "Please remember: xxx" | Summarize and then `memory.add(content, category)` |
| Important decision completed | Store decision with `memory.add` |
| Repeated patterns discovered | `memory.add(category: "pattern")` |

## Core Operations

### Recall
```javascript
// Must be called at the start of the session
memory.recall({
  project_path: "/path/to/project"
})
```

### Add Memory
```javascript
memory.add({
  content: "The project uses Result type for error handling",
  category: "pattern"  // rule|preference|pattern|context
})
```

## Category Classification

| Type | Purpose | Example |
|:---|:---|:---|
| `rule` | Project rules | "Prohibit the use of any type" |
| `preference` | User preferences | "Prefers functional programming style" |
| `pattern` | Common patterns | "Unified error handling using Result type" |
| `context` | Project background | "This is a SaaS backend management system" |

## Memory Solidification Timing

### R2 Stage (Only for significant changes)
```javascript
memory.add({
  content: "<Concise description>",
  category: "rule|preference|pattern|context"
})
```

### User Explicit Request
```
User: "Please remember I prefer using Tailwind"
→ memory.add({ content: "User prefers using Tailwind CSS", category: "preference" })
```

## Degradation Plan

If memory is unavailable → Use local Markdown notes for recording.