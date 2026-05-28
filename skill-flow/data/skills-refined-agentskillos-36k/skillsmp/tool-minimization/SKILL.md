---
name: tool-minimization
description: 'MCP/tool selection rules and lane-default toolchains for Kyora Agent OS. Use when selecting tools for a task, configuring agent tool lists, or understanding when to use MCP servers. Triggers: tools, MCP, tool selection, least-privilege, Context7, Playwright, GitHub MCP.'
---

# Tool Minimization Workflow

Operational guide for selecting and minimizing tools in Kyora Agent OS. Implements least-privilege tool selection and safe MCP usage.

## When to Use This Skill

- Selecting tools for a new task
- Configuring agent tool lists
- Deciding when to use MCP servers
- Reducing tool overload in agents/prompts
- Understanding lane-default toolchains

## Prerequisites

- Understanding of current task scope and risk level
- Knowledge of available MCP servers (if considering MCP)
- Access to agent/prompt files for tool list auditing

## Core Principle: Least Privilege

> **Start with the minimum tools needed. Add more only when clearly necessary.**

Tool overload hurts reliability:
- More tools = more confusion for the model
- More tools = higher chance of incorrect tool selection
- More tools = longer context

## Tool Selection Protocol

### Step 1: Start with Workspace Read/Search

Default starting tools:
- `read` — Read file contents
- `search` — Find files and text (grep, glob)
- `semantic_search` — Fuzzy concept matching

These solve most discovery and planning tasks.

### Step 2: Add Only What's Needed

| Need | Tool to Add |
|------|-------------|
| Modify files | `edit` |
| Run commands | `execute` |
| Run tests | `tests` / `runTests` |
| Track tasks | `todo` |
| Invoke agents | `agent` |

### Step 3: Consider MCP Only When Beneficial

MCP tools add latency and complexity. Use only when they clearly reduce work or increase certainty.

## Lane-Default Toolchains

| Lane | Default Tools | Add Only If Needed |
|------|---------------|-------------------|
| Discovery | `read`, `search` | GitHub MCP (repo context), Context7 (library uncertainty) |
| Planning | `read`, `search` | Context7 (API usage), diagrams only if asked |
| Implementation | `read`, `search`, `edit`, `execute`, `tests` | Playwright (UI), Context7 (new dep) |
| Validation | `execute`, `tests` | Playwright (UI smoke), DevTools (perf) |
| Recovery | `read`, `search`, `get_changed_files` | None unless blocked |

## Role-Default Tool Lists

### Orchestrator (Least Privilege)
```yaml
tools: ['read', 'search', 'todo']
# edit only for plans/notes, NEVER production code
```

### Leads
```yaml
tools: ['read', 'search', 'edit']  # edit for specs only
# execute optional for validation
```

### Implementers
```yaml
tools: ['read', 'search', 'edit', 'execute']
# tests tool added as needed
```

### QA/Test Specialist
```yaml
tools: ['read', 'search', 'edit', 'execute']
# Playwright preferred for UI flows
```

### Security Reviewer (Read-Only)
```yaml
tools: ['read', 'search']
# NEVER edit or execute
```

## MCP Server Policy

### Approved MCP Servers

| Server | Purpose | When to Use |
|--------|---------|-------------|
| **Context7** | Up-to-date library docs/snippets | New dependency; unfamiliar API |
| **Playwright** | UI automation, screenshots | UI flows, RTL verification, E2E |
| **Chrome DevTools** | Layout/perf/network debug | Performance issues, layout bugs |
| **GitHub MCP** | Issues/PRs/policies | Repo context (NOT local-only tasks) |

### When NOT to Use MCP

- Simple local refactors
- Tasks solvable via workspace search + reading existing code
- Anything requiring secrets or sensitive logs
- Local-only tasks (don't use GitHub MCP)

### MCP Safety Rules

See [MCP Safety Checklist](./references/mcp-safety-checklist.md) for detailed rules.

Key points:
- Treat local MCP servers as code execution
- Never paste secrets; use VS Code input variables
- Keep enabled tools under model/tool limits

## Tool Correctness Rules

1. **Prefer workspace tools** for local codebase truth
2. **Use Context7** only to confirm third-party API usage; stop after minimum needed
3. **Use Playwright/DevTools** when visual/RTL/layout correctness matters
4. **Disable entire servers** if not relevant to current task

## Operational Notes

### Tool List Caching

- Tool lists are cached by VS Code
- Reset cached tools when server tools change
- Use "Copilot: Reset Chat" or restart session

### Tool Sets

- Group related tools into tool sets
- Keep enabled tools under model limits
- Disable unused servers to reduce picker noise

## Success Checklist

- [ ] Started with read/search only
- [ ] Added tools only when clearly needed
- [ ] MCP tools have clear justification
- [ ] No unnecessary tools in final list
- [ ] Tool list matches role defaults
- [ ] Safety rules followed for MCP
- [ ] No surprise docs generated
- [ ] Stop-and-ask triggers checked

## Stop-and-Ask Triggers

**MUST ask before proceeding** if:

- Adding MCP server not in approved list
- Tool requires secrets or sensitive data access
- Tool list exceeds role defaults significantly
- Uncertain if tool is necessary for task

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Tool not available | Not in enabled list | Check agent frontmatter tools: list |
| MCP server slow | Network latency or server load | Consider if workspace tools suffice |
| Tool list too long | Scope creep | Reset to lane defaults, add only essentials |
| Cached tools stale | Server tools changed | Use "Copilot: Reset Chat" or restart |

## Validation Commands

No specific commands for tool selection, but verify:

```bash
# Check agent tool lists
grep -r "tools:" .github/agents/

# Check prompt tool lists
grep -r "tools:" .github/prompts/
```

## References

- [MCP Safety Checklist](./references/mcp-safety-checklist.md)

## SSOT References

- MCP + Tooling Policy: [KYORA_AGENT_OS.md#L791-L879](../../../KYORA_AGENT_OS.md#L791-L879)
- Tool selection in routing: [KYORA_AGENT_OS.md#L477-L489](../../../KYORA_AGENT_OS.md#L477-L489)
- Approved MCP servers: [KYORA_AGENT_OS.md#L825-L845](../../../KYORA_AGENT_OS.md#L825-L845)
