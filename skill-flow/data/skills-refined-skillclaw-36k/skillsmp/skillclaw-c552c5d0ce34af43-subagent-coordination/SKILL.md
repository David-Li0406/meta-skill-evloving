---
name: subagent-coordination
description: Use this skill when coordinating agents, delegating tasks to specialists, or when "dispatch agents", "which agent", or "multi-agent" are mentioned.
---

# Subagent Coordination

Orchestrate subagents by matching tasks to the right agent and skill combinations.

## Orchestration Planning

For complex multi-agent tasks, **start with the Plan subagent** to research and design the orchestration strategy before execution.

```
Complex task arrives
    │
    ├─► Plan subagent (research phase)
    │   └─► Explore codebase, gather context
    │   └─► Identify which agents and skills are needed
    │   └─► Design execution sequence (sequential, parallel, or hybrid)
    │   └─► Return orchestration plan
    │
    └─► Execute plan (dispatch agents per plan)
```

**Plan subagent benefits**:
- Runs in isolated context — doesn't consume main conversation tokens
- Can read many files without bloating orchestrator context
- Returns concise plan for execution

**When to use Plan subagent**:
- Task touches multiple domains (e.g., auth + performance + testing)
- Unknown codebase area — needs exploration first
- Sequence of agents matters (dependencies between steps)
- High-stakes changes requiring careful coordination

## Context Management

For long-running orchestration, load the **context-management** skill. It teaches:
- Using tasks as survivable state (persists across compaction)
- Delegating to subagents to preserve main context
- Pre-compaction checklists to capture progress
- Cross-session patterns for multi-day work

**Key principle**: Main conversation context is precious. Delegate exploration and research to subagents — only their summaries return, keeping main context lean.

## Roles and Agents

Coordination uses **roles** (what function is needed) mapped to **agents** (who fulfills it). This allows substitution when better-suited agents are available.

### Baselayer Agents

| Role       | Agent         | Purpose                                      |
|------------|---------------|----------------------------------------------|
| coding     | **senior-dev**| Build, implement, fix, refactor             |
| reviewing   | **ranger**    | Evaluate code, PRs, architecture, security  |
| research   | **analyst**   | Investigate, research, explore               |
| debugging  | **debugger**  | Diagnose issues, trace problems              |
| testing    | **tester**    | Validate, prove, verify behavior             |
| challenging| **skeptic**   | Challenge complexity, question assumptions    |
| specialist | **specialist**| Provide expertise in specific areas          |