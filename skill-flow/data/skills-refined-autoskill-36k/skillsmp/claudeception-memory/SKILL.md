---
name: claudeception-memory
description: |
  Search through Claude Code session memories and learned skills. Use when: (1) you need
  to find how a similar problem was solved before, (2) looking for relevant skills or
  knowledge, (3) checking if there's existing context about a project or technology,
  (4) the user asks "have we done this before?" or "what do you remember about X?".
  Triggers on: memory search, recall, remember, past sessions, history, previous work.
author: Claude Code
version: 1.0.0
date: 2025-01-22
triggers:
  - "search memory"
  - "what do you remember"
  - "have we done this before"
  - "recall"
  - "past sessions"
  - "check history"
  - "find similar"
---

# Claudeception Memory Search

Search through recorded Claude Code session histories and extracted skills to find
relevant past knowledge.

## When to Use

- Before starting a task, check if similar work was done before
- When debugging, see if similar errors were encountered and solved
- When the user asks about past sessions or previous work
- To find relevant skills that might help with the current task

## How to Search

### Quick Memory Search

Search for any term across all memories and skills:

```bash
~/.claude/hooks/memory-search.sh "search term"
```

### Search Recent Sessions Only

Limit to the last N days:

```bash
~/.claude/hooks/memory-search.sh "search term" --recent 7
```

### Search Specific Project

Filter by project directory:

```bash
~/.claude/hooks/memory-search.sh "search term" --project "project-name"
```

### List Recent Sessions

See summary of recent activity:

```bash
~/.claude/hooks/memory-search.sh
```

## Memory Locations

- **Session Logs**: `~/.claude/sessions/YYYY-MM-DD/*.jsonl` - Raw event logs
- **Memory Index**: `~/.claude/memory/*.json` - Processed session summaries
- **Skills**: `~/.claude/skills/*/SKILL.md` - Extracted knowledge as skills

## What Gets Recorded

Each session records:
- User prompts (truncated for storage)
- Tools used and their frequency
- Errors encountered
- Working directory context
- Session timing

## Search Tips

1. **Be specific**: Search for error messages, tool names, or specific technologies
2. **Use project context**: Filter by project when looking for project-specific knowledge
3. **Check skills first**: Skills contain distilled, high-quality knowledge
4. **Recent is relevant**: Most valuable context is usually recent

## Example Searches

```bash
# Find past work with Remotion
~/.claude/hooks/memory-search.sh "remotion"

# Find sessions with database errors
~/.claude/hooks/memory-search.sh "database error"

# Find recent Next.js work
~/.claude/hooks/memory-search.sh "next.js" --recent 14

# Find work in a specific project
~/.claude/hooks/memory-search.sh "auth" --project "cosplit"
```

## Integration with Claudeception

This skill works alongside the claudeception skill:
- **claudeception** extracts new knowledge into skills
- **claudeception-memory** retrieves existing knowledge

Together they form a continuous learning loop where discoveries are preserved
and can be retrieved when relevant.
