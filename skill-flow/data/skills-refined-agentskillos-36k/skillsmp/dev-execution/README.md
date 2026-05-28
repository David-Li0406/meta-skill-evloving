# Dev Execution Skill

A unified execution engine for all development workflows in Claude Code, providing progressive disclosure for token-efficient operations.

## Overview

This skill consolidates guidance for executing development tasks across multiple commands:

| Command | Purpose |
|---------|---------|
| `/dev:execute-phase` | Multi-phase YAML-driven development |
| `/dev:quick-feature` | Simple single-session features |
| `/dev:implement-story` | Execute existing story plans |
| `/dev:complete-user-story` | End-to-end story completion |
| `/dev:create-feature` | Scaffold new feature structures |

## Why This Skill Exists

Previously, each dev command contained 130-716 lines of detailed guidance, loaded entirely on every invocation. This caused:

- **Token waste**: Full guidance loaded even for simple operations
- **Duplication**: Same patterns repeated across commands
- **Maintenance burden**: Updates required in multiple places

This skill solves these problems through **progressive disclosure**: commands are now thin action-oriented wrappers (~65-75 lines) that reference detailed guidance only when needed.

## Directory Structure

```
dev-execution/
├── SKILL.md                 # Main skill index (loaded by Claude)
├── README.md                # This file (for humans)
├── modes/                   # Execution mode guides
│   ├── phase-execution.md   # Multi-phase YAML-driven work
│   ├── quick-execution.md   # Simple single-session features
│   ├── story-execution.md   # User story implementation
│   └── scaffold-execution.md # New feature scaffolding
├── orchestration/           # Task delegation patterns
│   ├── batch-delegation.md  # Parallel Task() patterns
│   ├── parallel-patterns.md # Dependency-aware batching
│   └── agent-assignments.md # Which agent for which task
├── validation/              # Quality and completion checks
│   ├── quality-gates.md     # Test, lint, typecheck requirements
│   ├── milestone-checks.md  # Phase completion criteria
│   └── completion-criteria.md # Definition of done
└── integrations/            # Related skill integrations
    ├── artifact-tracking.md # Progress file workflows
    └── request-log-workflow.md # MeatyCapture integration
```

## How It Works

1. **User invokes command**: `/dev:quick-feature add login button`

2. **Command loads**: The slim command file (~70 lines) provides:
   - Quick action steps
   - References to detailed skill files

3. **Progressive loading**: Claude loads additional skill files only when needed:
   - Simple feature? Just `quick-execution.md`
   - Need agent guidance? Load `agent-assignments.md`
   - Validation time? Load `quality-gates.md`

## Token Savings

| Command | Before | After | Savings |
|---------|--------|-------|---------|
| execute-phase | 716 lines | 70 lines | 90% |
| complete-user-story | 375 lines | 73 lines | 81% |
| quick-feature | 224 lines | 71 lines | 68% |
| implement-story | 168 lines | 74 lines | 56% |
| create-feature | 131 lines | 65 lines | 50% |

**Total reduction**: 1614 → 353 lines (78% savings on command footprint)

## Key Concepts

### Execution Modes

Each mode handles a different type of development work:

- **Phase Execution**: For large features with PRDs, progress tracking, and batch delegation
- **Quick Execution**: For small enhancements that fit in a single session
- **Story Execution**: For user stories with or without existing plans
- **Scaffold Execution**: For creating new feature file structures

### Agent Delegation

The skill follows MeatyPrompts' delegation model:

- **Opus orchestrates**: Plans, coordinates, tracks progress
- **Subagents execute**: Actually write the code

Key agents:
- `codebase-explorer` - Pattern discovery (Haiku)
- `ui-engineer-enhanced` - React/UI components (Sonnet)
- `backend-typescript-architect` - TypeScript backend (Sonnet)
- `task-completion-validator` - Validation (Sonnet)

### Quality Gates

All execution modes share common quality gates:

```bash
pnpm test && pnpm typecheck && pnpm lint
```

These run after each significant change and before any completion.

## Integrations

### artifact-tracking

For phase execution, integrates with artifact-tracking skill for:
- Creating/updating progress files
- Tracking task completion
- Managing YAML frontmatter

### meatycapture-capture

For request-log operations:
- Marking items in-progress/done
- Adding progress notes
- Capturing new issues discovered during work

## Modifying This Skill

### Adding New Modes

1. Create `modes/new-mode-execution.md`
2. Add entry to SKILL.md Quick Start table
3. Update relevant command to reference new mode

### Adding New Orchestration Patterns

1. Create `orchestration/new-pattern.md`
2. Add entry to SKILL.md Orchestration References table
3. Reference from relevant mode files

### Updating Quality Gates

Edit `validation/quality-gates.md` - changes automatically apply to all modes that reference it.

## Related Documentation

- [SKILL.md](./SKILL.md) - Full skill content for Claude
- [artifact-tracking skill](../artifact-tracking/SKILL.md) - Progress tracking
- [meatycapture-capture skill](../meatycapture-capture/SKILL.md) - Request logging
- [Design spec](../../specs/dev-execution-skill-design.md) - Original design document
