---
name: rp-explorer
description: Use this skill for token-efficient codebase exploration using the RepoPrompt CLI when prompted with actions like explore, find, understand, or search.
---

# RP-Explorer

Token-efficient codebase exploration using RepoPrompt CLI.

## Trigger Phrases

Activates when user combines "use rp" or "use repoprompt" with an action:
- "use rp to explore how auth works"
- "use repoprompt to find similar patterns"
- "use rp to understand the data flow"
- "use repoprompt to search for API endpoints"

## CLI Reference

Read [cli-reference.md](cli-reference.md) for complete command documentation.

## Quick Start

### Step 1: Get Overview
```bash
rp-cli -e 'tree'
rp-cli -e 'structure .'
```

### Step 2: Find Relevant Files
```bash
rp-cli -e 'search "auth" --context-lines 2'
rp-cli -e 'builder "understand authentication"'
```

### Step 3: Deep Dive
```bash
rp-cli -e 'select set src/auth/'
rp-cli -e 'structure --scope selected'
rp-cli -e 'read src/auth/login.ts'
```

### Step 4: Export Context
```bash
rp-cli -e 'context --all > codebase-map.md'
```

## Token Efficiency

- Use `structure` instead of reading full files (10x fewer tokens).
- Use `builder` for AI-powered file discovery.
- Select only relevant files before exporting context.

## Tab Isolation

`builder` creates an isolated compose tab automatically. Use `-t` to target it:
```bash
# Builder returns: Tab: <UUID> • <Name>
rp-cli -w W -t "<Name>" -e 'select add extra.ts && context'

# Or chain commands:
rp-cli -w W -e 'builder "find auth" && select add extra.ts && context'
```

## Requirements

RepoPrompt v1.5.62+ with rp-cli installed.