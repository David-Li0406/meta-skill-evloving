---
title: RLM Routing
impact: HIGH
tags: orchestration, rlm, context, aggregation
---

# RLM Routing Rules

When to use RLM (Recursive Language Model) patterns vs traditional orchestration.

## Decision Tree

### Use RLM When

| Pattern | Example | Why RLM |
|---------|---------|---------|
| Aggregate queries | "count all X", "sum across", "total in codebase" | Needs to process many sources, return single result |
| Cross-document analysis | "compare files", "trace through modules" | Information scattered across files |
| Large context processing | >50KB input, many files | Exceeds single-shot context |
| Information-dense queries | Multiple data points needed | Reduces context by processing incrementally |
| Multi-hop reasoning | Answers require chaining results | Each hop builds on previous |

### Do NOT Use RLM When

| Pattern | Why Not |
|---------|---------|
| Simple questions | Direct answer available, no aggregation needed |
| Single-file operations | One file fits in context |
| Code generation | Write tasks, not analyze tasks |
| User wants quick response | RLM adds latency |

---

## How to Activate RLM

### Option 1: Direct Skill Invocation

Spawn rlm-processor agent for aggregate/analysis tasks:

```python
Task(
    subagent_type="rlm-processor",
    model="sonnet",
    prompt="""
Query: <user query>
Use RLM patterns to process efficiently.
Return FINAL() when complete.
"""
)
```

### Option 2: REPL State for Results

Store intermediate results in REPL state (not main context):

```bash
# Store intermediate result
python ~/.claude/scripts/repl_state.py set <key> <value>

# Retrieve when needed
python ~/.claude/scripts/repl_state.py get <key>
```

**Why REPL state:** Results persist across context compactions but don't consume tokens.

### Option 3: Chunked Processing (MapReduce Pattern)

For very large contexts, use recursive decomposition:

```
1. SPLIT: Divide input into chunks (e.g., 10 files each)
2. MAP: Process each chunk with sub-agent
3. REDUCE: Aggregate chunk results
4. STORE: Put final result in REPL state
5. FINAL(): Signal completion with summary
```

---

## Integration with Context Management

| What | Where | Why |
|------|-------|-----|
| Raw intermediate results | REPL state | Persistent, out of context |
| Summaries only | Main context | Minimal token usage |
| Final answer | User response | Via FINAL() pattern |

**Critical:** RLM is a context-saving pattern. If results come back to main context in full, you've defeated the purpose.

---

## RLM vs Wave-Based Orchestration

| Aspect | Wave-Based | RLM |
|--------|------------|-----|
| Best for | Independent tasks | Dependent/aggregating tasks |
| Context usage | Each agent adds to context | Results stay in REPL state |
| Output style | Multiple reports | Single aggregated answer |
| Example | "Fix 5 bugs" (parallel) | "Count bugs in codebase" (aggregate) |

**Hybrid approach:** Use waves to gather data, RLM to aggregate results.

---

## Safety Net

The `rlm-context-router` hook monitors for patterns that suggest RLM would help:

- Large file counts in queries
- Aggregation keywords detected
- Cross-reference patterns

If the hook suggests RLM, consider routing to it even if you didn't initially plan to.

---

## Quick Reference

```
User asks aggregate question?
  |
  v
YES -> Spawn rlm-processor
  |        |
  |        v
  |    Store in REPL state
  |        |
  |        v
  |    Return FINAL() summary
  |
NO -> Traditional wave or direct answer
```
