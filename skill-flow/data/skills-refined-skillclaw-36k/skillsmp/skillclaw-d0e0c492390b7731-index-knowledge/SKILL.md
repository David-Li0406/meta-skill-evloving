---
name: index-knowledge
description: Use this skill when you need to generate a hierarchical AGENTS.md knowledge base for a codebase, creating root and complexity-scored subdirectory documentation.
---

# Skill body

## Usage

```
--create-new   # Read existing → remove all → regenerate from scratch
--max-depth=2  # Limit directory depth (default: 5)
```

Default: Update mode (modify existing + create new where warranted)

## Workflow (High-Level)

1. **Discovery + Analysis** (concurrent)
   - Launch parallel explore agents (multiple Task calls in one message)
   - Main session: bash structure + LSP codemap + read existing AGENTS.md
2. **Score & Decide** - Determine AGENTS.md locations from merged findings
3. **Generate** - Root first, then subdirs in parallel
4. **Review** - Deduplicate, trim, validate

<critical>
**TodoWrite ALL phases. Mark in_progress → completed in real-time.**
  
```
TodoWrite([
  { id: "discovery", content: "Fire explore agents + LSP codemap + read existing", status: "pending", priority: "high" },
  { id: "scoring", content: "Score directories, determine locations", status: "pending", priority: "high" },
  { id: "generate", content: "Generate AGENTS.md files (root + subdirs)", status: "pending", priority: "high" },
  { id: "review", content: "Deduplicate, validate, trim", status: "pending", priority: "medium" }
])
```
</critical>

## Phase 1: Discovery + Analysis (Concurrent)

**Mark "discovery" as in_progress.**

### Launch Parallel Explore Agents

Multiple Task calls in a single message execute in parallel. Results return directly.

```
// All Task calls in ONE message = parallel execution

Task(
  description="project structure",
  subagent_type="explore",
  prompt="Project structure: PREDICT standard patterns for detected language → REPORT deviations only"
)

Task(
  description="entry points",
  subagent_type="explore",
  prompt="Entry points: FIND main files → REPORT non-standard organization"
)

Task(
  description="conventions",
  subagent_type="explore",
  prompt="Conventions: FIND config files (.eslintrc, pyproject.toml, .editorconfig) → REPORT project-specific rules"
)

Task(
  description="anti-patterns",
  subagent_type="explore",
  prompt="Anti-patterns: FIND 'DO NOT', 'NEVER', 'ALWAYS', 'DEPRECATED' comments → LIST forbidden patterns"
)

Task(
  description="build/ci",
  subagent_type="explore",
  prompt="Build/CI: FIND .github/workflows, Makefile → REPORT necessary configurations"
)
```