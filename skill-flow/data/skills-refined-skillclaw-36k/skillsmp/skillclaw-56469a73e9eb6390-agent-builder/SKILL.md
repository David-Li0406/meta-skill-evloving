---
name: agent-builder
description: Use this skill when you need to design and build AI agents for various domains, whether for customer service, research, or creative tasks.
---

# Agent Builder

Build AI agents for any domain - customer service, research, operations, creative work, or specialized business processes.

## Quick Start

**What are you trying to do?**

| Goal | First Step | Resources |
|------|-----------|-----------|
| Understand how agents work | Read philosophy | `references/agent-philosophy.md` |
| Build your first agent | Start with 3-5 capabilities | `references/minimal-agent.py` |
| Fix context pollution | Use subagents | `references/subagent-pattern.py` |
| Generate agent scaffold | Run init script | `scripts/init_agent.py` |

## The Core Philosophy

> **The model already knows how to be an agent. Your job is to get out of the way.**

An agent is not complex engineering. It's a simple loop that invites the model to act:

```
LOOP:
  Model sees: context + available capabilities
  Model decides: act or respond
  If act: execute capability, add result, continue
  If respond: return to user
```

**That's it.** The magic isn't in the code - it's in the model. Your code just provides the opportunity.

## The Three Elements

### 1. Capabilities (What can it DO?)

Atomic actions the agent can perform: search, read, create, send, query, modify.

**Design principle**: Start with 3-5 capabilities. Add more only when the agent consistently fails because a capability is missing.

### 2. Knowledge (What does it KNOW?)

Domain expertise injected on-demand: policies, workflows, best practices, schemas.

**Design principle**: Make knowledge available, not mandatory. Load it when relevant, not upfront.

### 3. Context (What has happened?)

The conversation history - the thread connecting actions into coherent behavior.

**Design principle**: Context is precious. Isolate noisy subtasks. Truncate verbose outputs. Protect clarity.

## Agent Design Thinking

Before building, understand:

- **Purpose**: What should this agent accomplish?
- **Domain**: What world does it operate in? (customer service, research, operations, creative...)
- **Capabilities**: What 3-5 actions are essential?
- **Knowledge**: What expertise does it need access to?
- **Trust**: What decisions can you delegate to the model?

**CRITICAL**: Trust the model. Don't over-engineer. Don't pre-specify workflows. Give it capabilities and let it reason.

## Progressive Complexity

Start simple. Add complexity only when real usage reveals the need.