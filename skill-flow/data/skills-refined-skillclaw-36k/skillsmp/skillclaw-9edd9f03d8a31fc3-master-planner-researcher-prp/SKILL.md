---
name: master-planner-researcher-prp
description: Use this skill when you need to turn a request into a research-backed, implementation-ready plan (PRP) using structured reasoning and relevant tools.
---

# Skill body

## Mission
Transform any user request into a **research-backed, execution-ready plan** (PRP: Product Requirement Prompt) that maximizes one-pass success by delivering:
- **Dense context** (sources, constraints, patterns, edge cases)
- **Atomic, validated task plan** (dependencies, rollback, quality gates)
- **Clear output contract** (what “done” means)

**Core principle:** Context Density > Brevity | Research-First > Implementation | Planning > Coding | Validation > Assumption

## When to use this skill
Use this skill when the user request includes one or more of the following:
- Building a plan, roadmap, or architecture (new feature/system/migration)
- High uncertainty, many unknowns, or risk of hallucination without research
- Need to align with **current** best practices / official docs
- Multi-step execution requiring task decomposition, validations, and rollback
- Integrations (APIs, frameworks, infra, security/compliance)

Do **not** use this skill for:
- Pure copywriting/creative tasks with no need for research or planning
- Simple Q&A where no implementation or planning is required
- Tasks fully solvable from the provided context without external references

## Operating modes (choose explicitly)
### 1) CONSERVATIVE (default)
Use when the user asked for **plan/research**, not code changes.
- Deliver research synthesis + plan + validation gates
- Do not produce code unless explicitly requested

### 2) PROACTIVE
Use only when the user clearly asked to **implement**.
- Proceed from plan → implementation steps
- Still follow research-first and validation gates

## Tooling requirements
This skill assumes access to these MCP tools:

### Tavily MCP (web research)
Use for:
- Current best practices, deprecations, security advisories
- Comparisons, community consensus, recent releases
- Real-world edge cases and failure modes

**Usage pattern (conceptual):**
- `tavily.search(query, recency_days, include_domains?, exclude_domains?)`
- Prefer recency filters for fast-moving topics (security, APIs, frameworks)

### Context7 MCP (official docs)
Use for:
- Official documentation and guidelines relevant to the task at hand.