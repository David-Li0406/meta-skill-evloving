---
name: cass-search
description: |
  Coding Agent Session Search (CASS) for semantic search over past agent sessions.
  Use when looking for how something was solved before, finding past solutions, or searching conversation history.
  Keywords: search, history, session, past, solved, conversation, semantic
tags: [search, history, knowledge]
compatibility: Requires CASS binary installed. GLIBC 2.39+ on Linux.
allowed-tools:
  - Bash(cass:*)
  - Bash(which:*)
  - Read
---

# CASS - Coding Agent Session Search

Search across all past agent sessions (Claude, Codex, OpenCode, Gemini).

## Quick Reference

| Command | Use Case |
|---------|----------|
| `cass search "query"` | One-off search |
| `cass tui` | Interactive TUI |
| `cass stats` | Show indexed sessions |
| `cass status` | Health check |
| `cass capabilities` | API discovery |

## Search Past Sessions

```bash
# Find how authentication was implemented
cass search "authentication oauth"

# Find how a specific error was fixed
cass search "GLIBC not found"

# JSON output for scripting
cass search "database migration" --json
```

## Agent Integration

```bash
# Pre-flight health check
cass health  # Exit 0 = healthy, 1 = unhealthy

# Discover available features
cass capabilities

# API schema for automation
cass introspect
```

## Index Sessions

Run periodically to index new sessions:
```bash
cass index
```

## Verify Installation

```bash
# Check installed
which cass && cass stats

# Check health
cass status
```

## When to Use

- "I solved this before" → `cass search "topic"`
- "How did we fix X?" → `cass search "error message"`
- "What approach did we use for Y?" → `cass search "feature name"`

## Limitations

- **epyc6**: Requires GLIBC 2.39 (Debian 12 has 2.36)
- **Index lag**: New sessions need `cass index` to be searchable

---

**Last Updated:** 2026-01-14
**Repository:** https://github.com/Dicklesworthstone/coding_agent_session_search
