---
name: dev-execution
description: Use this skill when you need a unified execution engine for all development workflows, allowing for efficient phase execution, quick feature implementation, story completion, and scaffolding.
---

# Dev Execution Skill

Unified guidance for executing development workflows with token-efficient progressive disclosure.

## Quick Start

| Mode | When to Use | Command |
|------|-------------|---------|
| Phase | Multi-phase plans with YAML tracking | `/dev:execute-phase` |
| Quick | Simple features, single-session | `/dev:quick-feature` |
| Story | User story with existing plan | `/dev:implement-story` |
| Full Story | Complete story end-to-end | `/dev:complete-user-story` |
| Scaffold | New feature structure | `/dev:create-feature` |

## Execution Modes

Load only the mode-specific content you need:

| Mode | Guide | When to Load |
|------|-------|--------------|
| [Phase Execution](./modes/phase-execution.md) | Multi-phase YAML-driven work with batch delegation |
| [Quick Execution](./modes/quick-execution.md) | Simple single-session features (~1-3 files) |
| [Story Execution](./modes/story-execution.md) | User story implementation with plan |
| [Scaffold Execution](./modes/scaffold-execution.md) | New feature structure creation |

## Core Principles

### 1. Delegate Everything

- **Opus orchestrates; subagents execute**
- Never write implementation code directly
- Use batch delegation for parallel work
- Reference @CLAUDE.md for agent assignments

### 2. Token Efficiency

- Load only mode-specific content when needed
- Use YAML head extraction for large files
- Request-log operations via `/mc` (token-efficient)
- Read progress YAML only (~2KB), not full files (~25KB)

### 3. Quality Gates

All modes share these gates - run after each significant change:

```bash
pnpm test && pnpm typecheck && pnpm lint
```

Detailed gate requirements: [./validation/quality-gates.md]

## Agent Assignment Quick Reference

| Task Type | Agent |
|-----------|-------|
| Find files/patterns | codebase-explorer |
| Deep analysis | explore |
| React/UI components | ui-engineer-enhanced |
| TypeScript backend | backend-typescript-architect |
| Deep debugging | ultrathink-debugger |
| Validation/review | task-completion-validator |
| Most docs (90%) | documentation-writer |