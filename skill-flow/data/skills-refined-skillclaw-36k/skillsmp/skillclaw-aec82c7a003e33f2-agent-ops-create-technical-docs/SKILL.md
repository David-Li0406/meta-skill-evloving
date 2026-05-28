---
name: agent-ops-create-technical-docs
description: Use this skill when you need to create focused, specific technical documentation for codebase sections, analyzing code and identifying topics before writing.
---

# Technical Documentation Creation

## Purpose

Create **focused, specific** technical documentation for codebase sections. Unlike general docs (README, CHANGELOG), this skill produces **deep-dive articles** on components, patterns, or subsystems.

## When to Use

- Documenting a complex module or subsystem
- Creating tutorials for internal APIs
- Writing architectural explainers
- Onboarding documentation for new developers
- Self-documenting AgentOps skills and workflows

## Core Workflow

```
Analyze → Discover Topics → Present Options → Write → Review
```

---

## Phase 1: Analysis

### Input Types

| Input | Scope | Use Case |
|-------|-------|----------|
| Entire codebase | Broad discovery | Initial documentation audit |
| Folder/module | Scoped | Document a subsystem |
| Single file | Detailed | Deep dive on one component |
| Code snippet | Targeted | Explain specific pattern |

### Analysis Procedure

1. **Read context map** (`.agent/map.md`) if available.
2. **Scan target scope**:
   - Entry points and exports
   - Public API surface
   - Dependencies (imports/requires)
   - Configuration points
3. **Check existing docs**:
   - `.agent/docs/` — agent-generated docs
   - `docs/` — project docs
   - `README.md` — top-level overview
4. **Output**: List of components with documentation potential.

---

## Phase 2: Topic Discovery

### Topic Types

| Type | Description | Best For |
|------|-------------|----------|
| **How-To** | Step-by-step task completion | Practical tasks |
| **Explainer** | Concept/design rationale | Understanding "why" |
| **Reference** | API/config/schema details | Quick lookup |
| **Tutorial** | Learning path with examples | Onboarding |
| **Deep Dive** | Internal implementation details | Advanced users |

### Topic Sizing Guidelines

Good topics are:
- **Readable in 5-15 minutes**
- **Self-contained** (minimal external dependencies)
- **Actionable** (reader can do something) or **educational** (reader understands something)

Split large topics into series if needed.

### Discovery Output

Generate topic ideas based on the analysis and identified components.