---
name: master-planner
description: Use this skill when you need to create research-backed, execution-ready plans by transforming user requests into structured implementation strategies, particularly during planning or architecture tasks.
---

# Skill body

## 🎯 Master Planner — PRP Edition v6.0

> **CORE**: Context Density > Brevity | Research-First > Implementation | Planning > Coding

```yaml
METHODOLOGY: "PRP (Product Requirement Prompt) + ACE (Agentic Context Engineering)"
PHILOSOPHY: "One-pass implementation success through comprehensive context"
TRIGGER: "/plan command OR any planning/architecture request"
```

## 🔴 Activation Triggers

This skill is **MANDATORY** when:
1. User executes `/plan` command.
2. Building a plan, roadmap, or architecture (new feature/system/migration).
3. High uncertainty, many unknowns, or risk of hallucination without research.
4. Need to align with **current** best practices / official docs.
5. Multi-step execution requiring task decomposition, validations, and rollback.
6. Integrations (APIs, frameworks, infra, security/compliance).

**Do NOT use** for:
- Pure copywriting/creative tasks with no research needed.
- Simple Q&A with no implementation required.
- Tasks fully solvable from provided context.

## 🧠 Foundational Principles

**PRP = PRD + Curated Codebase Intelligence + Agent Runbook**

```yaml
PRP_LAYERS:
  layer_1: "What + Why (goal)"
  layer_2: "Curated codebase intelligence (files, patterns)"
  layer_3: "Agent execution playbook (steps, validations, rollback)"

ACE_MECHANISM:
  generator: "Executes reasoning, tool calls"
  reflector: "Extracts insights from execution"
  curator: "Applies incremental updates to context"
  grow_and_refine: "Add insights → Track helpfulness → Prune redundancy"
```

## 📊 Complexity Classification

| Level  | Indicators                | Thinking Budget | Research Depth |
| ------ | ------------------------- | --------------- | -------------- |
| L1-L2  | Bug fix, single function  | 1K-4K tokens    | Repo-only      |
| L3-L5  | Feature, multi-file       | 8K-16K tokens   | Docs + repo    |
| L6-L8  | Architecture, integration | 16K-32K tokens  | Deep           |
| L9-L10 | Migrations, multi-service | 32K+ tokens     | Comprehensive  |

## 🔧 MCP Tools (Mandatory Usage)

### Context7 — Official Documentation
```yaml
triggers:
  - Convex (queries, mutations, schema)
  - Cle
```