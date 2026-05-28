---
name: insight-awareness
description: Use this skill when you want to learn about generating high-quality insights that will be automatically captured. Insights using the "★ Insight" format are automatically extracted by hooks - no manual saving required.
---

# Insight Awareness

## Overview

This skill guides you on creating valuable insights that will be **automatically captured by hooks**. You don't need to manually save insights - just generate them in the `★ Insight` format and the Stop/SubagentStop hooks will extract them from the transcript.

## How It Works

```
1. You generate: ★ Insight ─────────────────────────────────────
                 [valuable knowledge]
                 ─────────────────────────────────────────────────

2. Hook automatically:
   - Parses transcript after your response
   - Extracts content between markers
   - Saves to ~/.claude/knowledge-extraction/{session-id}/insights.md
   - Tracks state to avoid duplicates
```

## When to Generate Insights

Generate `★ Insight` markers when you discover:

| Type | Description | Example |
|------|-------------|---------|
| `code-pattern` | Reusable patterns | "Prefer useReducer for complex form state" |
| `workflow` | Efficient processes | "Run tests before commit hooks" |
| `debugging` | Root cause findings | "Memory leak caused by unclosed listener" |
| `architecture` | Design decisions | "Use event sourcing for audit trail" |
| `tool-usage` | Effective techniques | "Combine Grep + Read for targeted searches" |
| `standard` | Standards and conventions | "JSON files use 2-space indentation" |
| `convention` | Naming and file patterns | "Scripts follow entity-action.js naming" |

## Quality Guidelines

### Worth Capturing

- Non-obvious solutions or patterns
- Project-specific conventions discovered
- Tool combinations that worked well
- Debugging techniques that solved real issues
- Architectural rationale with tradeoffs

### Not Worth Capturing

- Basic syntax or API usage (available in docs)
- Temporary workarounds without lasting value
- User-specific preferences without broader applicability
- Information already documented in project

## Insight Format

Use the standard format for automatic extraction:

```
★ Insight ─────────────────────────────────────
[2-5 lines of valuable, reusable knowledge]
─────────────────────────────────────────────────
```

## Commands

After insights accumulate:

- `/insights` - View collected insights
- `/insights extract` - Convert to Skills/Commands/CLAUDE.md/Rules Files
- `/insights clear` - Clear session insights

## Key Points

1. **Just generate** - Hooks handle saving automatically
2. **Quality over quantity** - Only create insights worth preserving
3. **Be specific** - Include context for discoverability
4. **Use standard format** - Ensures hook can extract properly
