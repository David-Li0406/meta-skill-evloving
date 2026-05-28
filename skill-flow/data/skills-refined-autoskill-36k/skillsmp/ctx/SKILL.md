---
name: ctx
description: View and manage hierarchical context for the current directory
user_invocable: true
---

# /ctx - Hierarchical Context Viewer

Shows the resolved context for the current working directory, aggregated from all levels of the hierarchy.

## Usage

```
/ctx           # Show resolved context
/ctx tree      # Show context hierarchy as tree
/ctx edit      # Edit context at current scope
```

## What This Shows

Context is resolved by walking up from the current directory:

1. **Feature/Component level** - `.context/CONTEXT.md` in current or parent dirs
2. **Repo level** - `.claude/CONTEXT.md` at repository root
3. **Project level** - Context above the repo
4. **User level** - `~/.claude/CONTEXT.md` for global preferences

Each level can:
- **Inherit** from parent (default)
- **Override** specific sections with `@override: section_name`
- **Ignore** parent sections with `@ignore: section_name`

## Implementation

When invoked, run:

```bash
python3 ~/.claude/plugins/agent-swarm/ctx/resolver.py resolve .
```

For tree view:
```bash
python3 ~/.claude/plugins/agent-swarm/ctx/resolver.py tree .
```

## Context File Format

```markdown
# Context: [Scope Name]

@inherit: true           # Default, inherit from parent
@override: conventions   # Override this section completely
@priority: high          # Mark as high priority

## Purpose
What this scope is for.

## Conventions
Coding standards for this scope.

## Patterns
Common patterns used here.

## Pitfalls
Known issues to avoid.
```

## Creating Context

To add context at current scope:

1. Create `.context/CONTEXT.md` in the directory
2. Add relevant sections
3. Use `@override` for sections that shouldn't merge with parent

## Memory vs Context

- **CONTEXT.md** - Static, intentionally written knowledge
- **MEMORY.md** - Distilled learnings from sessions (see `/distill`)
