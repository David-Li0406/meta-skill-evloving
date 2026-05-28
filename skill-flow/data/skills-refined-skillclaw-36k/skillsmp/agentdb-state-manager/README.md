---
type: directory-documentation
directory: .claude/skills/agentdb-state-manager
title: AgentDB State Manager Skill
sibling_claude: CLAUDE.md
parent: null
children:
  - ARCHIVED/README.md
---

# AgentDB State Manager Skill

Persistent state management using AgentDB (DuckDB) for workflow analytics and checkpoints.

## Purpose

**Primary purpose:** Data gathering and analysis for workflow state tracking

**Workflow phase:** Cross-phase (Utilities) - All phases (1-6)

Provides read-only analytics cache synchronized from TODO_*.md files, enabling:
- Complex dependency graph queries
- Historical workflow metrics
- Context checkpoint storage/recovery
- State transition analysis

## Quick Start

### 1. Initialize AgentDB

```bash
python .claude/skills/agentdb-state-manager/scripts/init_database.py
```

### 2. Sync TODO Files

```bash
python .claude/skills/agentdb-state-manager/scripts/sync_todo_to_db.py --all
```

### 3. Query State

```bash
# Current state
python .claude/skills/agentdb-state-manager/scripts/query_state.py

# Task dependencies
python .claude/skills/agentdb-state-manager/scripts/query_state.py --dependencies
```

### 4. Analyze Metrics

```bash
python .claude/skills/agentdb-state-manager/scripts/analyze_metrics.py --trends
```

### 5. Manage Checkpoints

```bash
# Store checkpoint
python .claude/skills/agentdb-state-manager/scripts/checkpoint_manager.py store --todo TODO_*.md

# List checkpoints
python .claude/skills/agentdb-state-manager/scripts/checkpoint_manager.py list
```

## Key Features

- **Read-only analytics:** TODO_*.md files remain source of truth
- **Immutable records:** Append-only history preserves full state transitions
- **Token efficiency:** 89% reduction for complex queries vs file parsing
- **Session-scoped:** 24-hour AgentDB lifetime, re-initialize as needed

## Documentation

- **[SKILL.md](SKILL.md)** - Complete documentation
- **[CLAUDE.md](CLAUDE.md)** - Claude Code context
- **[CHANGELOG.md](CHANGELOG.md)** - Version history
- **[templates/workflow-states.json](templates/workflow-states.json)** - State definitions

## Version

v1.0.0 - Initial release (2025-11-02)

## Related Documentation

- **[CLAUDE.md](CLAUDE.md)** - Context for Claude Code
