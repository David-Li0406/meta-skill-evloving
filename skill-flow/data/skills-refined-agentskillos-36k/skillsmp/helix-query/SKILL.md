---
name: helix-query
description: Search helix memory by meaning. Returns relevant failures and patterns.
argument-hint: <search text>
---

# Memory Query

Search the learning system for relevant memories.

## Usage

```
/helix-query authentication patterns
/helix-query "database connection errors"
```

## Execution

```bash
python3 $HELIX_PLUGIN_ROOT/lib/memory/core.py recall "$ARGUMENTS" --limit 10
```

## Output

Display each memory with:
- Name and type (failure/pattern)
- Trigger and resolution
- Effectiveness score
- Relevance to query
