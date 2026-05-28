---
name: context-optimization
description: Guide for managing and optimizing context in Claude Code. Use when experiencing slow responses, context warnings, or planning large tasks. Covers /compact, /clear, context budgeting, subagent delegation, and efficient session workflows.
allowed-tools: ["Read"]
---

# Context Optimization

Manage Claude Code's context window efficiently for faster responses, better memory, and productive long sessions.

## Quick Reference

| Command | Effect | When to Use |
|---------|--------|-------------|
| `/compact` | Compress context, preserve key info | Approaching limit, slow responses |
| `/clear` | Reset to empty context | Fresh start, topic change |
| `/cost` | Show token usage | Monitor consumption |
| `/resume` | Continue previous session | Multi-session workflows |
| `/rename` | Name current session | Session organization |

## Understanding Context

### What Is Context?

Context is everything Claude "remembers" in your conversation:
- Your messages and Claude's responses
- Files read during the session
- Tool outputs (bash results, search results)
- System prompts and loaded skills

### Context Window Limits

| Model | Context Window | Practical Limit |
|-------|----------------|-----------------|
| Claude Opus 4.5 | 200K tokens | ~150K usable |
| Claude Sonnet 4 | 200K tokens | ~150K usable |
| Claude Haiku | 200K tokens | ~150K usable |

**Note:** Reserve 20-30% for Claude's responses. Hitting the ceiling causes degraded performance before hard failures.

### Token Estimation

| Content Type | Approximate Tokens |
|--------------|-------------------|
| 1 line of code | 10-15 tokens |
| 100 lines of code | 1,000-1,500 tokens |
| Typical source file | 500-3,000 tokens |
| Large file (1000+ lines) | 5,000-15,000 tokens |
| Your message | ~1 token per word |

## Context Pressure Indicators

### Visual Indicators

1. **Token counter** - Watch the usage bar in the UI header
2. **Response time** - Noticeably slower responses
3. **Cost increase** - Higher per-turn costs (use `/cost`)

### Behavioral Signs

| Sign | What's Happening |
|------|------------------|
| Claude "forgets" earlier discussion | Context truncation |
| Repeated questions about context | Information pushed out |
| Slower, choppier responses | Processing large context |
| Incomplete tool outputs | Context conservation |
| Asking to re-read files | File content evicted |

### When to Act

| Usage Level | Recommendation |
|-------------|----------------|
| Under 50% | Continue normally |
| 50-70% | Plan for compaction soon |
| 70-85% | Compact now, consider task splitting |
| 85%+ | Compact immediately or clear |

## /compact - Context Compression

### What /compact Does

1. Summarizes conversation history
2. Preserves key decisions and context
3. Maintains file awareness
4. Keeps recent changes tracked
5. Reduces token count by 50-80%

### When to Use /compact

- Token usage exceeds 70%
- Responses becoming slow
- Before starting a new sub-task
- Transitioning between phases
- After completing a major task

### Compact Workflow

```
> /compact
```

Claude compresses the conversation, keeping:
- Current task objectives
- Key decisions made
- Files modified/created
- Important constraints
- Recent context (last few turns)

### Best Practices

1. **Compact at natural breaks** - Between tasks, not mid-implementation
2. **State important context first** - Mention critical info before compacting
3. **Verify understanding after** - Ask "What are we working on?" post-compact
4. **Don't over-compact** - Once per major phase, not every few turns

## /clear - Fresh Start

### What /clear Does

- Completely resets context to zero
- No memory of previous conversation
- Like starting a new session

### When to Use /clear

| Scenario | Why Clear |
|----------|-----------|
| Switching projects | Different codebase, different context |
| Major topic change | Unrelated to previous work |
| Context too polluted | Too much irrelevant history |
| Starting fresh approach | Previous direction was wrong |
| Testing from scratch | Need clean state |

### /clear vs /compact

| Aspect | /compact | /clear |
|--------|----------|--------|
| Memory retained | Summarized | None |
| Token usage after | ~20-50% | ~0% |
| Context continuity | Preserved | Lost |
| Use case | Continue work | Fresh start |

### Clear Workflow

```
> /clear

Now starting fresh on [task description]...
```

**Always restate your objective after clearing.**

## Context Budgeting

### Planning Sessions

Before starting work, estimate context needs:

```
Task: Implement user authentication
Estimated reads: 10 files (~15,000 tokens)
Expected tool use: High (~20,000 tokens)
Conversation: Medium (~10,000 tokens)
Buffer: 20% (~10,000 tokens)
Total estimate: ~55,000 tokens (28% of window)
```

### Budget Allocation Strategy

| Category | Allocation | Notes |
|----------|------------|-------|
| System prompt + skills | 5-10% | Fixed overhead |
| File reads | 20-40% | Be selective |
| Tool outputs | 15-25% | Limit verbose output |
| Conversation | 20-30% | Your messages + responses |
| Response buffer | 20% | Room for Claude's output |

### Reducing Context Usage

1. **Read selectively** - Request specific functions, not entire files
2. **Use targeted searches** - `grep` patterns instead of reading files
3. **Limit tool verbosity** - Ask for summaries, not full outputs
4. **Break into sessions** - Split large tasks across multiple sessions
5. **Use subagents** - Delegate to separate context windows

## Subagent Delegation

### Why Subagents Help

Subagents have their own context window. Delegating tasks:
- Preserves main conversation context
- Allows parallel exploration
- Isolates experimental changes
- Returns only relevant results

### Delegation Pattern

```
> Use a subagent to analyze the database schema and report the key tables

[Subagent runs in separate context]
[Returns summary to main conversation]
```

### Good Candidates for Delegation

| Task Type | Why Delegate |
|-----------|--------------|
| File exploration | Many reads, minimal output needed |
| Code analysis | Deep dive, summary sufficient |
| Test execution | Verbose output, pass/fail matters |
| Documentation reading | Large content, key points needed |
| Search tasks | Many grep/glob operations |

### Agent Definition for Context Efficiency

```yaml
---
name: explorer
description: Explore codebase and return concise summaries
tools: Read, Glob, Grep
model: haiku
---

You are a code explorer. Investigate thoroughly but report concisely.
Return only essential findings. Summarize, don't quote entire files.
```

See [creating-subagents](../creating-subagents/SKILL.md) for full agent creation guide.

## Session Management

### Naming Sessions

```
> /rename authentication-feature
```

Benefits:
- Easy to identify in history
- Clear purpose documentation
- Resumable with meaningful names

### Resuming Sessions

```
> /resume
```

Shows recent sessions. Select one to continue where you left off.

Or directly:
```
> /resume authentication-feature
```

### Multi-Session Workflows

For large features, plan multiple sessions:

| Session | Focus | Compact At |
|---------|-------|------------|
| Session 1 | Architecture design | End |
| Session 2 | Backend implementation | 70% |
| Session 3 | Frontend implementation | 70% |
| Session 4 | Integration & testing | End |

### Session Checkpoints

Create natural checkpoints:

1. **Before major changes** - Compact to preserve state
2. **After milestones** - Document progress in conversation
3. **At decision points** - State decisions clearly for post-compact memory

## Efficient Workflows

### Task Batching

Instead of interleaving tasks:

**Inefficient:**
```
> Read file A
> Make change to A
> Read file B
> Make change to B
> Read file A again
```

**Efficient:**
```
> Read files A and B
> Make all changes to A
> Make all changes to B
```

### Explicit Context Statements

Help Claude remember across compactions:

```
> We're building a REST API for user management.
> Key constraint: Must use existing auth middleware.
> Files involved: src/api/users.ts, src/middleware/auth.ts
```

### Pre-Compact Checklist

Before running `/compact`:
- [ ] Stated current objective clearly
- [ ] Mentioned key constraints
- [ ] Listed important files/decisions
- [ ] Completed current sub-task

## Monitoring Usage

### /cost Command

```
> /cost
```

Shows:
- Total tokens used
- Input vs output breakdown
- Estimated cost

### When to Check

- After reading large files
- After verbose tool operations
- Every 10-15 exchanges
- Before starting new task

## Reference Files

| File | Contents |
|------|----------|
| [STRATEGIES.md](./STRATEGIES.md) | Detailed optimization strategies |
| [INDICATORS.md](./INDICATORS.md) | Context pressure indicators and monitoring |
| [WORKFLOWS.md](./WORKFLOWS.md) | Efficient workflow patterns |

## Quick Decisions

| Situation | Action |
|-----------|--------|
| Slow responses | `/compact` |
| Topic change | `/clear` |
| Large task ahead | Plan sessions, use subagents |
| Forgot earlier discussion | Restate context, consider clearing |
| Mid-implementation | Avoid compacting, finish first |
| Starting new feature | Name session, budget context |
