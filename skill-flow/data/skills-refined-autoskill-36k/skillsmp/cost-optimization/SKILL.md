---
name: cost-optimization
description: Manage Claude Code API costs - token strategies, model selection, monitoring. Use when concerned about API spend, optimizing token usage, choosing models for tasks, or setting up cost monitoring. Covers /cost command, batching strategies, and budget management.
version: 1.0.0
author: Claude Code SDK
tags: [cost, optimization, tokens, budget]
---

# Cost Optimization

Reduce Claude Code API costs while maintaining quality through smart token management, model selection, and monitoring.

## Quick Reference

| Strategy | Impact | Effort |
|----------|--------|--------|
| Use Haiku for simple tasks | High | Low |
| Batch related operations | Medium | Low |
| Use /compact strategically | Medium | Low |
| Reduce context size | High | Medium |
| Efficient prompting | Medium | Medium |

## Understanding Costs

### How API Costs Work

Claude Code costs are based on tokens:
- **Input tokens**: Everything Claude reads (prompts, files, context)
- **Output tokens**: Everything Claude generates (responses, code)
- **Cached tokens**: Reduced rate for repeated context

### Model Pricing (Relative)

| Model | Input Cost | Output Cost | Best For |
|-------|------------|-------------|----------|
| Haiku | $ | $ | Simple tasks, exploration |
| Sonnet | $$ | $$ | General development (default) |
| Opus | $$$$$ | $$$$$ | Complex reasoning, architecture |

**Rule of thumb**: Opus is ~15x more expensive than Haiku for the same tokens.

### What Consumes Tokens

| Activity | Token Impact | Optimization |
|----------|--------------|--------------|
| Reading files | High | Read selectively, use grep |
| Long conversations | Cumulative | Use /compact regularly |
| Tool outputs | Variable | Request summaries |
| Code generation | Medium | Be specific in requests |
| Error messages | Low | N/A |

## The /cost Command

### Basic Usage

```
> /cost
```

Shows:
- Session token usage (input/output)
- Estimated cost for current session
- Context window usage percentage

### When to Check

- Before starting large tasks
- After reading multiple files
- When responses slow down
- Every 15-20 exchanges
- Before deciding to /compact vs /clear

### Interpreting Results

| Metric | Good | Concern | Action |
|--------|------|---------|--------|
| Context usage | <50% | >70% | Consider /compact |
| Session cost | Varies | Unexpected spike | Review recent operations |
| Output ratio | Balanced | Output >> Input | Responses too verbose |

## The /stats Command

View usage statistics over time:

```
> /stats
```

**Date Range Filtering (2.1.6+):** Press `r` to cycle between:
- Last 7 days
- Last 30 days
- All time

Shows:
- Total tokens used (input/output)
- Number of sessions
- Cost breakdown by period
- Model usage distribution

## MCP Tool Search Auto Mode (2.1.7+)

When you have many MCP tools configured, their descriptions can consume significant context space. Version 2.1.7 introduces automatic MCP tool deferral:

### How It Works

- **Trigger**: When MCP tool descriptions exceed 10% of context window
- **Behavior**: Tools are deferred and discovered via `MCPSearch` instead of loaded upfront
- **Default**: Enabled for all users

### Cost Impact

| MCP Tools | Without Auto Mode | With Auto Mode | Savings |
|-----------|-------------------|----------------|---------|
| 10-20 tools | ~2-5% context | ~1% context | 50-80% |
| 50+ tools | ~10-20% context | ~1% context | 90%+ |

### Disabling Auto Mode

If you need all MCP tools loaded upfront (e.g., for specific workflows):

```json
// settings.json
{
  "disallowedTools": ["MCPSearch"]
}
```

**Note**: Only disable if you have few MCP tools or specifically need immediate tool availability.

## Token Reduction Strategies

### 1. Selective File Reading

**Expensive:**
```
> Read the entire src/ directory to understand the codebase
```

**Efficient:**
```
> @src/api/users.ts @src/types/user.ts - I need to modify the user API
```

### 2. Use Grep Before Read

**Expensive:**
```
> Find all files that use the AuthService class
[Claude reads many files to find them]
```

**Efficient:**
```
> grep for "AuthService" in src/, then I'll look at the most relevant ones
```

### 3. Targeted @ Mentions

| Pattern | Token Cost | Use Case |
|---------|------------|----------|
| `@src/` | Very High | Avoid unless necessary |
| `@src/api/` | High | When exploring a module |
| `@src/api/users.ts` | Low | Specific file work |
| `@src/api/users.ts:50-100` | Very Low | Specific section |

### 4. Limit Output Verbosity

```
> Analyze this file and give me a brief summary of the key functions
```

vs

```
> Explain every line of this file
```

### 5. Batch Related Operations

**Expensive (multiple turns):**
```
> Read file A
> Now modify line 10
> Now read file B
> Modify line 20
```

**Efficient (single turn):**
```
> In file A, update the getUserById function to handle null.
> In file B, add the new UserNotFound error type.
> Run the tests after both changes.
```

## /compact vs /clear

### When to /compact

Use `/compact` when:
- Context is 70%+ full
- You want to continue the same task
- Need to preserve decisions and progress
- Responses are slowing down

**Cost impact**: Reduces ongoing costs by 50-80%

### When to /clear

Use `/clear` when:
- Switching to unrelated task
- Previous context is irrelevant
- Starting fresh approach
- Maximum cost savings needed

**Cost impact**: Resets to zero (but loses all context)

### Decision Matrix

| Situation | Command | Reasoning |
|-----------|---------|-----------|
| Same task, full context | /compact | Preserve progress |
| Different project | /clear | Irrelevant context |
| Stuck on approach | /clear | Fresh perspective |
| After major milestone | /compact | Keep decisions |
| Testing something new | /clear | Clean state |

## Model Selection

### Quick Guide

| Task Type | Recommended Model | Why |
|-----------|-------------------|-----|
| File exploration | Haiku | Fast, cheap, sufficient |
| Simple edits | Haiku | Straightforward |
| General coding | Sonnet | Balanced (default) |
| Bug fixing | Sonnet | Needs reasoning |
| Architecture design | Opus | Deep analysis |
| Security review | Opus | Critical thinking |
| Complex refactoring | Opus | Multi-file reasoning |

### Switching Models

Set model in skill frontmatter:
```yaml
---
model: haiku
---
```

Or request model in prompt:
```
> Using Haiku, list all TypeScript files in src/
```

### Cost Comparison Example

**Task**: Review 10 files for security issues

| Approach | Estimated Cost |
|----------|---------------|
| Opus reviews all | $$$$$ |
| Haiku scans, Opus reviews flagged | $$ |
| Sonnet reviews all | $$$ |

**Best strategy**: Use Haiku for initial scan, escalate to Opus for detailed review of potential issues.

## Efficient Prompting

### Reduce Token Count

| Verbose | Concise | Savings |
|---------|---------|---------|
| "Could you please" | [Just ask] | 3-4 tokens |
| "I want you to" | [State task] | 4-5 tokens |
| Long explanations | Bullet points | 20-50% |
| Repeated context | @ mentions | Significant |

### Be Specific

**Token-heavy:**
```
> I have this function that gets users from the database and I want
> to add some caching because it's being called too often and making
> the app slow. Can you help me figure out a good caching strategy?
```

**Efficient:**
```
> Add Redis caching to getUserById in @src/api/users.ts.
> TTL: 5 minutes. Invalidate on user update.
```

### Use Checklists

```
> Implement user search:
> - [ ] Add search endpoint
> - [ ] Add debounced input
> - [ ] Handle empty results
> Run tests when done.
```

Clearer than long paragraph descriptions.

## Batching Strategies

### Batch Similar Operations

Instead of multiple turns:
```
> Add logging to function A
[response]
> Add logging to function B
[response]
> Add logging to function C
```

Single turn:
```
> Add consistent logging to functions A, B, and C in @src/utils.ts
> Use format: logger.info("[FunctionName] action", { params })
```

### Batch Read-Modify Cycles

```
> Review @src/api/*.ts for missing error handling.
> Add try-catch with proper logging to any functions that need it.
> Summarize changes made.
```

### When NOT to Batch

- Complex, interdependent changes
- When you need to verify each step
- Exploratory work
- Learning a new codebase

## Budget Management

### Setting Expectations

| Session Type | Typical Cost Range |
|--------------|-------------------|
| Quick fix | $ |
| Feature implementation | $$-$$$ |
| Large refactor | $$$-$$$$ |
| Architecture session (Opus) | $$$$$ |

### Cost Controls

1. **Monitor actively**: Check /cost regularly
2. **Set mental limits**: "I'll compact at $X"
3. **Use appropriate models**: Haiku for exploration
4. **Plan sessions**: Know scope before starting

### Daily/Weekly Tracking

```
> /cost
[Note the total]
```

Track across sessions to understand your patterns.

## Subagent Cost Efficiency

### Why Subagents Help

Subagents have isolated context:
- Main context stays lean
- Exploratory work doesn't pollute
- Can use cheaper models

### Cost-Efficient Agent Pattern

```yaml
---
name: explorer
model: haiku
tools: Read, Glob, Grep
---
Explore and summarize. Return only key findings.
```

### Delegation Examples

| Task | Agent Model | Return |
|------|-------------|--------|
| Find all API routes | Haiku | Route list |
| Analyze dependencies | Haiku | Summary |
| Review for patterns | Sonnet | Findings |
| Deep security review | Opus | Detailed report |

## Common Wasteful Patterns

| Pattern | Why Wasteful | Better Approach |
|---------|--------------|-----------------|
| Reading entire directories | Massive token cost | Grep first, read specific |
| Verbose explanations | Unnecessary output | Request concise |
| Repeating context | Already in history | Use @ mentions |
| Not using /compact | Growing costs | Compact at 70% |
| Opus for everything | Expensive overkill | Match model to task |
| Long debugging sessions | Cumulative cost | Clear and restart |

## Reference Files

| File | Contents |
|------|----------|
| [TOKEN-STRATEGIES.md](./TOKEN-STRATEGIES.md) | Detailed token reduction techniques |
| [MODEL-SELECTION.md](./MODEL-SELECTION.md) | Model comparison and selection guide |
| [MONITORING.md](./MONITORING.md) | Cost tracking and budget management |

## Quick Decisions

| Situation | Action |
|-----------|--------|
| Context at 70% | /compact |
| Simple file exploration | Use Haiku |
| Need deep analysis | Use Opus (worth the cost) |
| Unexpected high cost | Check recent operations |
| Switching tasks | /clear to save costs |
| Debugging loop | Clear and try fresh approach |
