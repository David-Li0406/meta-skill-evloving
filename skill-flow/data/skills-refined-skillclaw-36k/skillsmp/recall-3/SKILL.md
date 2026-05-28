---
name: recall
description: Search and analyze past Claude Code and Codex sessions. Use when user asks about past sessions, tool usage patterns, bash command history, permission suggestions, or wants to find previous work.
allowed-tools: Bash
---

# recall

Search and analyze past AI agent sessions (Claude Code, Codex).

## Installation

```bash
# Install from GitHub
uv tool install "recall @ git+https://github.com/0xbigboss/recall.git#subdirectory=packages/recall"
```

## Quick Start

```bash
# Index sessions (run first, then periodically)
recall index

# Search across all sessions
recall search "authentication"
recall search "git" --tool Bash

# List recent sessions
recall list --since 7d
recall list --project /path/to/repo

# Show session details
recall show <session-id>
recall show <session-id> --tools --thinking

# Analytics
recall stats              # Overview
recall stats tools        # Tool usage counts
recall stats bash         # Bash command breakdown
recall stats bash --suggest  # Permission suggestions
recall stats tokens       # Token usage by project
```

## When to Use Each Command

| Task | Command |
|------|---------|
| Find past work on a topic | `recall search "<topic>"` |
| See what I did recently | `recall list --since 24h` |
| Find work in a specific repo | `recall list --project <path>` |
| Analyze my tool usage | `recall stats tools` |
| Get permission suggestions | `recall stats bash --suggest` |
| Review a specific session | `recall show <id>` |

## Common Workflows

### Find Previous Implementation
```bash
recall search "oauth authentication"
recall show <session-id> --tools
```

### Generate Permission Suggestions
```bash
recall stats bash --suggest
# Returns patterns like: "run tests", "git operations", etc.
```

### Analyze Tool Patterns
```bash
recall stats tools    # See which tools used most
recall stats bash     # Break down bash commands
```

## Further Reading

- [CLI_REFERENCE.md](CLI_REFERENCE.md) - Full command documentation with all flags
- [EXAMPLES.md](EXAMPLES.md) - Detailed usage examples and patterns
