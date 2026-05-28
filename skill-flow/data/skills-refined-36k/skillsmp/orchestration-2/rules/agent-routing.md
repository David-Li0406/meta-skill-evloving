---
title: Agent Routing
impact: HIGH
tags: orchestration, agents, specialists
---

# Specialist Agents

You have access to these global specialist agents. **Invoke them when appropriate:**

## SESSION-SAVER AGENT
`subagent_type="session-saver"`

**When to invoke:**
- User says "save session" or "save and exit"
- Before ending significant work sessions
- After completing major features

**What it does:**
- Saves .claude/memory/state.json (current state)
- Saves .claude/memory/pending.md (unfinished tasks)
- Appends .claude/memory/decisions.md (key decisions)
- Creates structured memory for next session

## AGENT-UPDATER
`subagent_type="agent-updater"`

**When to invoke:**
- Project has outdated agents (missing output limits)
- After updating global agent standards
- User asks to update/upgrade project agents

**What it does:**
- Scans .claude/agents/ for existing agents
- Adds missing sections (output limits, ecosystem, etc.)
- Preserves project-specific context
- Reports what was updated

NOTE: Requires Claude Code restart after updating

## SPAWNER-EXPERT AGENT
`subagent_type="spawner-expert"`

**When to invoke:**
- Before implementing domain-specific features
- When reviewing code for domain best practices
- When you need patterns/anti-patterns for a domain
- To check code against production sharp-edges

**What it does:**
- Reads from 462 Spawner skills (~/.spawner/skills/)
- Extracts patterns, anti-patterns, sharp-edges
- Applies domain expertise to tasks
- Catches production gotchas before they ship

**Enhanced Modes:**

| Mode | Purpose | Returns |
|------|---------|---------|
| DISCOVERY | Auto-detect relevant skills from task | List of applicable skill paths |
| WORKER_INJECTION | Format skills for worker prompts | Condensed skill content |
| PREFLIGHT | Risk analysis before major work | Warnings, gotchas, validations |
| QUALITY_GATE | Validate implementation against skills | Violations, anti-patterns |
| MULTI_SKILL_SYNTHESIS | Combine multiple skills | Merged patterns from domains |

## PROJECT-INIT AGENT
`subagent_type="project-init"`

**When to invoke:**
- At project kickoff, after planning but before coding
- When starting a new workspace/project
- When significant architectural changes are planned

**What it does:**
- Reads the project plan (PLAN.md, README, etc.)
- Analyzes tech stack, architecture, domain
- Generates project-specific agents in .claude/agents/

## PRODUCTION-CODE AGENT
`subagent_type="production-code"`

**When to invoke:**
- After generating significant code
- Before major commits
- When reviewing implementation quality

**What it does:**
- Finds mock implementations -> demands real ones
- Finds placeholders/TODOs -> demands completion
- Finds simulated data -> demands real integrations

## SLOP-REMOVER AGENT
`subagent_type="slop-remover"`

**When to invoke:**
- After code generation (clean up AI artifacts)
- Before commits (final polish pass)
- When code "looks AI-generated"

**What it does:**
- Removes excessive/obvious comments
- Removes unnecessary try/catch and null checks
- Fixes `any` type casts with proper types
- Matches existing file style

## RLM-PROCESSOR AGENT
`subagent_type="rlm-processor"`

**When to invoke:**
- Large context or information-dense tasks
- Aggregate queries across many files
- Tasks that would overwhelm main context with results

**What it does:**
- Uses Recursive Language Model patterns
- Stores intermediate results in REPL state (`~/.claude/state/`)
- Returns lean summaries, not full data
- Processes large inputs in chunks recursively
- Uses FINAL() primitive to signal completion

**Route to rlm-processor vs other agents:**

| Task Characteristic | Use |
|---------------------|-----|
| Large file analysis (10+ files) | rlm-processor |
| Aggregate statistics/counts | rlm-processor |
| Information-dense transformations | rlm-processor |
| Simple single-file edit | production-code |
| Exploration/discovery | scout |
| Code quality review | slop-remover |

---

# Project-Specific Agents

**IMPORTANT:** Always check for project-specific agents when starting work in a workspace.

**ON FIRST TASK IN ANY PROJECT:**

1. Check if .claude/agents/ exists
2. If yes -> list available project agents
3. Use them alongside global agents
4. If no -> consider running project-init

**Discovery command:**
```bash
ls .claude/agents/ 2>/dev/null || echo "No project agents yet"
```

## Project Agent Types

| Agent | Purpose |
|-------|---------|
| `stack-guardian` | Enforces THIS project's tech stack conventions |
| `api-guardian` | Enforces THIS project's API patterns |
| `domain-expert` | Validates THIS project's business logic |
| `test-guardian` | Enforces THIS project's testing patterns |
| `integration-guardian` | Enforces THIS project's external service patterns |

## Agent Priority Order

1. **Project-specific agents** (`.claude/agents/`) -- most context
2. **Global agents** (`~/.claude/agents/`) -- universal standards
3. **Spawner skills** (`~/.spawner/skills/`) -- domain expertise

## Usage Example

```python
# Project agents are invoked by their name, just like global agents
Task(subagent_type="stack-guardian", prompt="Review this PR for stack convention violations", run_in_background=True)
Task(subagent_type="domain-expert", prompt="Validate the checkout flow business logic", run_in_background=True)
```
