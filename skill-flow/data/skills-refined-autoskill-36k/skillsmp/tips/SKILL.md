---
name: tips
description: Use when starting a Claude Code session, feeling overwhelmed by context, or needing workflow tips. Triggers on "how do I manage sessions", "context getting long", "remind me".
---

# Claude Code Session Tips

Quick reference for effective Claude Code usage.

## Session Management

| Action            | How                                                    |
| ----------------- | ------------------------------------------------------ |
| Clear context     | `/clear` (rename first with `/rename` for easy return) |
| Resume session    | `claude --resume <session-id>`                         |
| Clear input area  | `Esc Esc` (double-tap)                                 |
| Clear single line | `Ctrl+U` (shell shortcut)                              |
| Optimize Rules    | `/claude-md-improver`                                  |

## Context Hygiene

* `/clear` aggressively - long contexts slow responses
* `/rename` before clearing to make sessions findable
