---
title: Swarm Patterns
impact: HIGH
tags: orchestration, swarm, parallel, tasks
see-also: task-coordination.md
---

# Swarm Everything

There is no task too small for the swarm.

## Example: Simple Request

```
User: "Fix the typo in README"

You think: "One typo? Let's be thorough."

Agent 1 -> Find and fix the typo
Agent 2 -> Scan README for other issues
Agent 3 -> Check other docs for similar problems

User gets: Typo fixed + bonus cleanup they didn't even ask for. Delighted.
```

## Example: Research Request

```
User: "What does this function do?"

You think: "Let's really understand this."

Agent 1 -> Analyze the function deeply
Agent 2 -> Find all usages across codebase
Agent 3 -> Check the tests for behavior hints
Agent 4 -> Look at git history for context

User gets: Complete understanding, not just a surface answer. Impressed.
```

## Scale Agents to the Work

| Complexity | Agents |
|------------|--------|
| Quick lookup, simple fix | 1-2 agents |
| Multi-faceted question | 2-3 parallel agents |
| Full feature, complex task | Swarm of 4+ specialists |

The goal is thoroughness, not a quota. Match the swarm to the challenge.

---

# The Orchestration Flow

```
    User Request
         |
         v
    +-------------+
    |  Vibe Check |  <- Read their energy, adapt your tone
    +------+------+
           |
           v
    +-------------+
    |   Clarify   |  <- AskUserQuestion if scope is fuzzy
    +------+------+
           |
           v
    +-------------------------------------+
    |     LOAD DOMAIN EXPERTISE           |
    |                                      |
    |   Spawn spawner-expert mode=DISCOVERY|
    |   -> Get relevant domain skills      |
    |   -> Inject into worker prompts      |
    +------------------+------------------+
                       |
                       v
    +-------------------------------------+
    |         DECOMPOSE INTO TASKS        |
    |                                      |
    |   TaskCreate -> TaskCreate -> ...   |
    +------------------+------------------+
                       |
                       v
    +-------------------------------------+
    |         SET DEPENDENCIES            |
    |                                      |
    |   TaskUpdate(addBlockedBy) for      |
    |   things that must happen in order  |
    +------------------+------------------+
                       |
                       v
    +-------------------------------------+
    |         FIND READY WORK             |
    |                                      |
    |   TaskList -> find unblocked tasks  |
    +------------------+------------------+
                       |
                       v
    +-------------------------------------+
    |     SPAWN WORKERS (with preamble)   |
    |                                      |
    |   +-----+ +-----+ +-----+ +-----+   |
    |   |Agent| |Agent| |Agent| |Agent|   |
    |   |  A  | |  B  | |  C  | |  D  |   |
    |   +--+--+ +--+--+ +--+--+ +--+--+   |
    |      |       |       |       |      |
    |      +-------+-------+-------+      |
    |         All parallel (background)   |
    +------------------+------------------+
                       |
                       v
    +-------------------------------------+
    |         MARK COMPLETE               |
    |                                      |
    |   TaskUpdate(status="resolved")     |
    |   as each agent finishes            |
    |                                      |
    |   Loop: TaskList -> more ready?     |
    |     -> Spawn more workers           |
    +------------------+------------------+
                       |
                       v
    +-------------------------------------+
    |         SYNTHESIZE & DELIVER        |
    |                                      |
    |   Weave results into something      |
    |   beautiful and satisfying          |
    +-------------------------------------+
```

---

# Background Agents Only

```python
# ALWAYS: run_in_background=True
Task(subagent_type="Explore", prompt="...", run_in_background=True)
Task(subagent_type="general-purpose", prompt="...", run_in_background=True)

# NEVER: blocking agents (wastes orchestration time)
Task(subagent_type="general-purpose", prompt="...")
```

**Non-blocking mindset:** "Agents are working -- what else can I do?"

- Launch more agents
- Update the user on progress
- Prepare synthesis structure
- When notifications arrive -> process and continue
