# Context Window Management

Strategies for keeping the main orchestrator's context window lean and preventing auto-compact.

---

## Why Context Management Matters

```
Context Window Lifecycle:
┌─────────────────────────────────────────────────────┐
│ [System Prompt] [Conversation History] [Tool Results]│
│                                                     │
│ As context fills → Auto-compact triggers            │
│ Auto-compact → Earlier context summarized/lost      │
│ Lost context → Degraded reasoning quality           │
│ Degraded quality → Errors, missed requirements      │
└─────────────────────────────────────────────────────┘

Solution: Keep heavy work OUT of main context
```

---

## Context Budget Strategy

### What SHOULD be in main context:

| Content | Why |
|---------|-----|
| User's original request | Core requirements |
| Synthesized subagent results | Compact summaries only |
| Decision points | Orchestrator's reasoning |
| Final implementation plan | Action items |
| Todo list state | Progress tracking |

### What should NOT be in main context:

| Content | Delegate To |
|---------|-------------|
| Raw file contents (10+ files) | Explore agents |
| Search/grep result dumps | Explore agents |
| Full test output | General-purpose agents |
| Detailed code analysis | Plan/Explore agents |
| Trial-and-error debugging | General-purpose agents |

---

## Context-Saving Techniques

### 1. Summarize Before Storing

When a subagent returns results, extract only what's needed:

```
Subagent returns (500 tokens):
"Found 15 files related to auth. The main middleware is in
src/middleware/auth.ts which uses JWT validation. The user model
is in src/models/user.ts with fields: id, email, passwordHash,
createdAt. Tests are in tests/auth/ using vitest. The login
endpoint currently returns 401 for invalid credentials..."

Orchestrator stores (100 tokens):
"Auth: middleware=src/middleware/auth.ts (JWT),
model=src/models/user.ts (email,passwordHash),
tests=tests/auth/ (vitest)"
```

### 2. Use Background Agents for Long Tasks

```
# Launch in background - doesn't block main context
Task(run_in_background=true, prompt="Run full test suite...")

# Continue other work...

# Check when needed
AgentOutputTool(agentId="...", block=false)  # non-blocking check
AgentOutputTool(agentId="...", block=true)   # wait for result
```

### 3. Batch Parallel Launches

```
# ONE message with multiple Task calls = efficient
# Each agent gets its OWN context window
# Only compact results return to main context

Single message:
  Task 1: Explore → returns 50 tokens
  Task 2: Explore → returns 50 tokens
  Task 3: Explore → returns 50 tokens

Total context cost: 150 tokens (vs 1500+ if done directly)
```

### 4. Progressive Delegation

For very large tasks, delegate in waves:

```
Wave 1: Quick exploration (haiku agents)
  → Returns: High-level map of what exists

Wave 2: Focused analysis (sonnet agents)
  → Returns: Detailed findings on specific areas

Wave 3: Implementation (sonnet/opus agents)
  → Returns: Confirmation of changes made

Each wave adds minimal context to main session.
```

---

## Auto-Compact Prevention Thresholds

| Context Usage | Risk | Action |
|---------------|------|--------|
| < 30% | Low | Normal operation, can read files directly |
| 30-60% | Medium | Start delegating exploration to agents |
| 60-80% | High | Delegate ALL reads/searches to agents |
| > 80% | Critical | Only synthesize and make decisions in main |

### Signs You Need to Delegate More

- Conversation has been going for many turns
- Multiple large files have been read into context
- Long search/grep chains have been executed
- Complex multi-step task with many intermediate results
- User explicitly mentioned "apply subagent-teams"

---

## Context-Efficient Patterns

### Pattern: Explore-Then-Act

```
Phase 1: All exploration via subagents (main context stays clean)
Phase 2: Synthesize findings (small summary in main context)
Phase 3: Act on synthesis (implementation with focused context)
```

### Pattern: Divide-and-Conquer

```
Split large codebase into regions:
  Agent 1: src/api/**
  Agent 2: src/models/**
  Agent 3: src/services/**

Each agent explores its region independently.
Orchestrator combines region summaries.
```

### Pattern: Filter-and-Focus

```
Agent 1 (haiku): "Find all files matching [broad pattern]"
  → Returns: file list

Orchestrator: Picks most relevant 3-5 files

Agent 2 (sonnet): "Analyze these specific files: [focused list]"
  → Returns: detailed analysis

Result: Deep analysis without reading everything into main context
```

---

## Measuring Context Efficiency

| Metric | Good | Bad |
|--------|------|-----|
| Files read in main context | 0-3 | 10+ |
| Grep/search chains in main | 0-1 | 5+ |
| Subagent results synthesized | Yes (compact) | No (raw dumps) |
| Background agents used | For long tasks | Never |
| Parallel launches | Single message | Sequential messages |
| Model selection | Matched to complexity | Always opus/sonnet |

---

## Recovery: When Context Is Already Large

If the main context is already bloated:

1. **Stop reading files directly** — delegate everything remaining
2. **Use TodoWrite** to track remaining work (persists across compaction)
3. **Launch background agents** for remaining heavy work
4. **Synthesize aggressively** — extract only key facts from results
5. **Consider fresh subagent** for complex remaining implementation

The todo list survives auto-compact, making it critical for continuity.
