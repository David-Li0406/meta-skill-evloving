---
title: Context Management
impact: HIGH
tags: orchestration, context, tokens
---

# Context Management (CRITICAL)

```
CONTEXT IS FINITE. MANAGE IT OR DIE.

Multiple agents = context explosion.
Plan for it. Don't hit the wall.
```

## RLM Pattern (Proactive)

For information-dense tasks, use RLM BEFORE context fills:

1. **Store in REPL State**: Intermediate results go to `~/.claude/state/` not main context
2. **Lean Summaries Only**: Agents return summaries, not full data
3. **Chunked Processing**: Large inputs split and processed recursively
4. **FINAL() Termination**: Use RLM primitives to signal completion

This keeps main context lean from the start. Route to `rlm-processor` agent for tasks that would otherwise flood context with data.

## The Problem

Each agent spawn adds to context:
- Your prompt to the agent (~500-2000 tokens)
- Agent's full response (~1000-5000 tokens)
- Multiply by 4-6 agents = context exhaustion

## The Rules

1. **MAX 3-4 AGENTS PER WAVE** -- Don't spawn 6+ agents simultaneously. Complete wave 1, compact, then wave 2.
2. **COMPACT BETWEEN WAVES** -- After collecting agent outputs, run /compact BEFORE spawning the next batch.
3. **LEAN PROMPTS** -- Don't repeat full context in every prompt. Reference files by path, not by quoting content.
4. **DEMAND CONCISE OUTPUTS** -- Tell agents: "Report in 3-5 sentences max" and "Only report file paths and changes"
5. **CHECKPOINT LARGE TASKS** -- For 10+ file changes, work in phases. Complete phase, commit, compact, continue.

## Output Size Limits (CRITICAL)

```
AGENT OUTPUTS MUST BE SMALL

Max output: 50-100 lines / ~5KB
NEVER return full file contents
NEVER dump large data structures
ALWAYS summarize, list paths, report key facts only
```

**ALWAYS include this in worker prompts:**

```
OUTPUT LIMITS (STRICT):
- MAX 50 lines total output
- List FILE PATHS, don't quote file contents
- Summarize findings in 3-5 bullet points
- If data is large, report COUNT + SAMPLE (3-5 items)
- NEVER dump full arrays, objects, or file contents
```

## Wave Pattern for Large Tasks

```
WAVE 1: Spawn 3 agents
   |
   v
Collect outputs
   |
   v
/compact
   |
   v
WAVE 2: Spawn next 3 agents
   |
   v
Collect outputs
   |
   v
/compact
   |
   v
Continue until done
```

## Proactive Compaction Triggers

**Compact BEFORE you hit the wall:**

| After... | Do... |
|----------|-------|
| 3-4 agent outputs collected | `/compact` |
| Any agent returns 100+ lines | `/compact` |
| Before spawning quality-check agents | `/compact` |
| Mid-way through large feature | `/compact` |

## CRITICAL: Save Memory BEFORE Compacting

```
ALWAYS SAVE MEMORY BEFORE /compact

Compaction wipes conversation history.
Memory extraction only sees what's in the transcript.
Save FIRST, compact SECOND.
```

**Before any /compact, do this:**

```python
# Save session state BEFORE compacting
Task(
    subagent_type="session-saver",
    prompt="Save current session state - about to compact context",
    run_in_background=False  # Wait for completion
)
# THEN compact
# /compact
```

## Context-Aware Phrasing

```python
# BAD: Verbose prompt eating context
Task(prompt="""
CONTEXT: You are a WORKER agent, not an orchestrator.
[... 20 lines of preamble ...]
[... full file contents quoted ...]
[... detailed instructions ...]
""")

# GOOD: Lean prompt preserving context
Task(prompt="""
WORKER. Read src/auth.ts, add JWT validation.
Report: files changed + 1-sentence summary.
""")
```

## Emergency Recovery

If you see "Context low" warnings:

1. **STOP** spawning new agents immediately
2. **COLLECT** all pending agent outputs
3. **SUMMARIZE** results in 2-3 sentences
4. **RUN** `/compact`
5. **CONTINUE** with fresh context

If `/compact` fails:
1. Tell user: "Context full. Saving progress."
2. List what's done and what's left
3. User starts new session, you continue from checkpoint
