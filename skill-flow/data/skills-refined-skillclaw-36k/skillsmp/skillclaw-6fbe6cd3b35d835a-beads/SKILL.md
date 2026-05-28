---
name: beads
description: Use this skill when tracking complex, multi-session work with dependencies that require persistent context across compaction cycles. For simple single-session tasks, use TodoWrite instead.
---

# Beads

## Overview

Beads is a graph-based issue tracker designed for persistent memory across sessions. It is ideal for managing multi-session work with complex dependencies, while TodoWrite is better suited for simple, single-session tasks.

## When to Use Beads vs TodoWrite

### Use Beads when:
- **Multi-session work**: Tasks that span multiple compaction cycles or days.
- **Complex dependencies**: Work involving blockers, prerequisites, or hierarchical structures.
- **Knowledge work**: Strategic documents, research, or tasks with fuzzy boundaries.
- **Side quests**: Exploratory work that may pause the main task.
- **Project memory**: When you need to resume work after an extended break with full context.

### Use TodoWrite when:
- **Single-session tasks**: Work that can be completed within the current session.
- **Linear execution**: Straightforward tasks with no branching.
- **Immediate context**: All necessary information is already present in the conversation.
- **Simple tracking**: Just a checklist to show progress.

**Key insight**: If resuming work after two weeks would be difficult without Beads, use Beads. If the work can be picked up from a markdown skim, TodoWrite is sufficient.

### Decision Criteria

Ask these questions to decide:

**Choose Beads if:**
- ❓ "Will I need this context in 2 weeks?" → Yes = Beads
- ❓ "Could conversation history get compacted?" → Yes = Beads
- ❓ "Does this have blockers/dependencies?" → Yes = Beads
- ❓ "Is this fuzzy/exploratory work?" → Yes = Beads

**Choose TodoWrite if:**
- ❓ "Will this be done in this session?" → Yes = TodoWrite
- ❓ "Is this just a task list for me right now?" → Yes = TodoWrite
- ❓ "Is this linear with no branching?" → Yes = TodoWrite

**When in doubt**: Use Beads. It's better to have persistent memory you don't need than to lose context you might require.

## Surviving Compaction Events

**Critical**: Compaction events delete conversation history but preserve Beads. After compaction, the Beads state is your only persistent memory.

**What survives compaction:**
- All Beads data (issues, notes, dependencies, status)
- Complete work history and context

**What doesn't survive:**
- Conversation history