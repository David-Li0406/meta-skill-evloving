---
name: cartographer
description: Meta-skill plugin that generates /atlas skills for any repository, providing AI-optimized codebase navigation plus spec-driven development workflows. Use when the user needs to understand a codebase structure, generate navigation aids, create implementation specs, or review code against documented patterns.
---

# Cartographer

Generate AI-optimized codebase navigation (atlas skills) plus spec-driven development workflows.

## Quick Start

```bash
# Generate atlas for current codebase
/cartographer:chart

# Use atlas for navigation (auto-invoked)
/atlas

# Spec-driven development
/navigator:plan <task>    # Create implementation spec
/navigator:build <spec>   # Execute spec with patterns
/navigator:review <spec>  # Review against patterns
```

## Core Concepts

### Atlas

An atlas is a generated skill (`.claude/skills/atlas/`) that provides:
- **Domain mapping**: Where different features/concerns live
- **Pattern documentation**: How code is structured (controllers, services, etc.)
- **Anti-patterns**: Codebase-specific mistakes to avoid
- **File conventions**: Naming and location patterns

### Spec-Driven Development

Navigator commands use the atlas to:
1. **Plan**: Generate specs with relevant pattern context
2. **Build**: Implement following documented conventions
3. **Review**: Validate against patterns and anti-patterns

## Commands

### Cartographer Commands

| Command | Model | Description |
|---------|-------|-------------|
| `/cartographer:chart` | sonnet | Generate complete atlas |
| `/cartographer:rechart` | sonnet | Incrementally update atlas |
| `/cartographer:health` | sonnet | Comprehensive atlas health check (drift, structure, quality) |
| `/cartographer:explore <domain>` | sonnet | Deep-dive into domain |
| `/cartographer:where <query>` | haiku | Quick path lookup |
| `/cartographer:capture` | haiku | Capture knowledge to atlas |
| `/cartographer:orient` | haiku | Set up CLAUDE.md awareness |
| `/cartographer:embed` | sonnet | Export commands for plugin-free use |
| `/cartographer:help` | haiku | Display usage guide |

### Navigator Commands

| Command | Model | Description |
|---------|-------|-------------|
| `/navigator:plan <task>` | sonnet | Create implementation spec with atlas context |
| `/navigator:build <spec>` | sonnet | Execute spec with pattern guidance |
| `/navigator:review <spec>` | sonnet | Review implementation against spec/patterns |

## Workflows

### New Codebase Setup

```
/cartographer:chart              # Generate atlas (interactive)
/cartographer:orient             # Add atlas awareness to CLAUDE.md
```

### Feature Development

```
/navigator:plan add user profiles    # Generate spec
/navigator:build specs/user-profiles.md    # Implement
/navigator:review specs/user-profiles.md   # Review
```

### Atlas Maintenance

```
/cartographer:health             # Check drift, structure, and quality
/cartographer:rechart            # Update stale areas
/cartographer:capture --pattern  # Add discovered patterns
```

## Agents

The plugin uses specialized agents for complex tasks:

### Analysis Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| surveyor | sonnet | Explores codebase to detect project type, domains, and patterns |
| auditor | sonnet | Validates atlas accuracy against actual codebase state |
| import-analyzer | sonnet | Analyzes import graph for layer boundary detection |

### Review Agents

| Agent | Model | Purpose |
|-------|-------|---------|
| pattern-enforcer | sonnet | Validates code against documented patterns |
| architecture-auditor | sonnet | Validates layer boundaries and import rules |
| anti-pattern-detector | sonnet | Scans for codebase-specific anti-patterns |
| convention-checker | haiku | Validates file naming and locations |
| atlas-validator | haiku | Validates atlas document structure |

## Files

```
cartographer/
├── SKILL.md                  # This file
├── .claude-plugin/
│   └── plugin.json           # Plugin metadata
├── commands/
│   ├── cartographer/         # Atlas management commands
│   └── navigator/            # Spec-driven workflow commands
├── agents/
│   ├── surveyor.md           # Codebase analysis
│   ├── auditor.md            # Atlas validation
│   ├── import-analyzer.md    # Import graph analysis
│   └── review/               # Code review agents
├── assets/
│   ├── atlas-templates/      # Generated atlas templates
│   └── embed-templates/      # Standalone command templates
└── references/
    └── atlas-format.md       # Atlas schema documentation
```

## Plugin-Free Operation

Export commands for use without the plugin installed:

```bash
/cartographer:embed --output .claude/commands/
```

This creates standalone command files that maintain full fidelity with plugin commands.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Atlas not found | `/cartographer:chart` |
| Atlas outdated | `/cartographer:health` then `/cartographer:rechart` |
| Pattern violations | Check atlas anti-patterns, update if needed |
| Missing domain | `/cartographer:explore <path>` to enrich |
