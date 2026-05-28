---
name: helix-stats
description: Show learning system health - memory counts, effectiveness, feedback loop status.
---

# System Health

Display memory system statistics and learning loop status.

## Execution

```bash
python3 $HELIX_PLUGIN_ROOT/lib/memory/core.py health
```

## After Display

Consider running maintenance:
- `python3 $HELIX_PLUGIN_ROOT/lib/memory/core.py consolidate` to merge similar memories
- `python3 $HELIX_PLUGIN_ROOT/lib/memory/core.py decay` to identify dormant memories
- `python3 $HELIX_PLUGIN_ROOT/lib/memory/core.py prune` to remove ineffective memories
