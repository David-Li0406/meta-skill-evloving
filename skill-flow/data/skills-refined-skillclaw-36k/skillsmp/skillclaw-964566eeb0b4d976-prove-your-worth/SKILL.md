---
name: prove-your-worth
description: Use this skill when you need to rigorously audit project features to ensure each one provides tangible value, challenging their necessity and justifying their existence.
---

# Prove Your Worth — Feature Justification Audit

## Philosophy

> "Every line of code is a liability. Every feature is technical debt until proven otherwise."

This skill embodies extreme pragmatism:
- **Existence is not justification** — Features must earn their place.
- **External is often better** — Well-maintained OSS beats custom code.
- **Simpler is superior** — Complexity requires compelling justification.
- **Facts over feelings** — No "we might need this" or "it's cool."

## When to Use

- Before major architectural decisions.
- When the codebase feels bloated or unfocused.
- When onboarding reveals "why do we have this?"
- Before starting new features (to clean first).
- Periodically (quarterly feature audit).

## MCP Tools Required

This skill leverages MCP tools for evidence-based research. If MCP is unavailable, findings will be limited to agent knowledge (clearly marked).

| Tool | Provider | Purpose |
|------|----------|---------|
| `brave_web_search` | brave-search | Find alternative solutions, compare tools. |
| `get_library_docs` | context7 | Get documentation for potential replacements. |
| `search_repositories` | github | Find similar OSS implementations. |
| `get_readme` | github | Evaluate alternatives' capabilities. |

## Procedure

### Phase 1: Feature Inventory

**Step 1: Generate or read context map**
- If `.agent/map.md` exists and is recent, use it.
- Otherwise, invoke `agent-ops-context-map` first.

**Step 2: Extract feature list**

Enumerate all features by category:

```markdown
## Feature Inventory

### CLI Commands
- `aoc issues list` — List and filter issues.
- `aoc kg build` — Build knowledge graph.
- ...

### Internal Modules
- `mcp/` — MCP integration module.
- `kg/` — Knowledge graph module.
- ...

### Skills/Agents
- `agent-ops-planning` — Multi-iteration planning.
- ...

### API Endpoints (if any)
- `GET /api/issues` — List issues.
- ...
```

**Step 3: Classify each feature**

| Classification | Meaning | Scrutiny Level |
|----------------|---------|----------------|
| **Core** | Essential to project identity | Low (but still verify) |
| **Optional** | Useful but not critical | Medium (verify necessity) |
| **Redundant** | Duplicate or unnecessary | High (consider removal) |