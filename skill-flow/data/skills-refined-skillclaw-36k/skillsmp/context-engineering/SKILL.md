---
name: context-engineering
description: Token optimization and context window management strategies. Load for long sessions, complex tasks, or when approaching context limits.
---

# Context Engineering

> **PRINCIPLE:** Quality > Quantity. High-signal tokens beat exhaustive content.

## When to Activate

- Session approaching 70-80% context utilization
- Multi-agent orchestration tasks
- Large codebase exploration
- Complex implementation spanning many files

---

## Core Strategies

### 1. Progressive Disclosure

**Load information just-in-time, not all-at-once.**

```
❌ BAD: Read 20 files before starting work
✅ GOOD: Read files as you need them during implementation
```

| Scope | Strategy |
|-------|----------|
| Codebase | Use `grep`/`glob` first, `read` only what's needed |
| Documentation | Summarize, don't dump entire docs |
| Research | Delegate to `researcher` agent, get concise results |

### 2. U-Shaped Attention

**Critical information belongs at the beginning OR end of context.**

LLMs have strongest attention at:
- First ~10% of context (recency bias)
- Last ~10% of context (position bias)
- Middle content gets "lost"

```
✅ GOOD: Plan at top of session, current task at bottom
❌ BAD: Critical requirements buried in middle of conversation
```

### 3. Observation Masking

**Replace verbose tool output with compact references.**

```
❌ BAD: Full 500-line file content in every message
✅ GOOD: "See file X (read previously)" with key excerpts only
```

When reading files:
- Quote only the relevant section
- Reference line numbers for context
- Don't repeat what's already in context

---

## Compaction Safety

### Triggers for Optimization

| Signal | Action |
|--------|--------|
| 70% context used | Start summarizing older exchanges |
| 80% context used | Delegate read-only work to sub-agents |
| 90% context used | Consider session fork or compaction |

### During Compaction

The system may compress your history. Protect critical context:

1. **Use the plan** - `plan_save` persists across compaction
2. **Use notepads** - `notepad_write` for learnings/decisions
3. **Use delegations** - Background tasks persist their results

### What Survives Compaction

| Persists | Lost |
|----------|------|
| Plan (plan.md) | Old tool outputs |
| Delegations | Conversation history |
| Notepad entries | File contents read |
| System prompt | Intermediate reasoning |

---

## Multi-Agent Context Isolation

### The Partition Principle

**Keep main agent context clean by delegating "context-heavy" work.**

```typescript
// ❌ BAD: Read 50 files in main session
for (const file of files) {
  read(file) // pollutes main context
}

// ✅ GOOD: Delegate to explorer
task(agent="explore", prompt="Find all usages of X and summarize")
// Returns: concise summary, main context stays clean
```

### Agent Responsibilities

| Agent | Context Strategy |
|-------|-----------------|
| `explore` | Absorbs codebase reads, returns summary |
| `researcher` | Absorbs external docs, returns synthesis |
| `coder` | Focused on single implementation unit |
| `oracle` | Receives synthesized context, not raw data |

### Delegation Pattern

```
1. Main agent identifies need for broad search
2. Delegate to appropriate agent with specific question
3. Agent does heavy lifting (many reads/searches)
4. Returns concise, actionable summary
5. Main agent continues with minimal context impact
```

---

## Tool Optimization

### Efficient Tool Descriptions

Every tool in context should have clear:

| Element | Why |
|---------|-----|
| **What** | Single sentence purpose |
| **When** | Trigger conditions |
| **Inputs** | Required parameters |
| **Returns** | Expected output format |

### Batch Operations

```
✅ GOOD: Single glob("**/*.ts") → process results
❌ BAD: Multiple sequential reads of guessed paths
```

---

## Anti-Patterns

| Anti-Pattern | Cost |
|--------------|------|
| Reading entire files when you need 10 lines | Token waste |
| Repeating context already in conversation | Token waste |
| Critical info in middle of long prompt | Attention loss |
| Single agent for parallelizable work | Context bloat |
| Dumping docs without summarization | Signal dilution |

---

## Checklist

When context is getting heavy:

- [ ] Are you loading info just-in-time or all-at-once?
- [ ] Is critical context at the start or end of messages?
- [ ] Can any work be delegated to sub-agents?
- [ ] Is the plan persisted for compaction safety?
- [ ] Are you quoting only relevant excerpts from files?
