---
name: strategic-compaction
description: Use this skill to suggest manual context compaction at logical intervals during your workflow to preserve context through task phases.
---

# Strategic Compaction Skill

Suggests manual `/compact` at strategic points in your workflow rather than relying on arbitrary auto-compaction.

## Why Strategic Compaction?

Auto-compaction triggers at arbitrary points, which can lead to:

- Losing important context mid-task
- Lack of awareness of logical task boundaries
- Interruptions during complex multi-step operations

Strategic compaction should occur at logical boundaries:

- **After exploration, before execution** - Compact research context while keeping the implementation plan.
- **After completing a milestone** - Start fresh for the next phase.
- **Before major context shifts** - Clear exploration context before transitioning to a different task.

## How It Works

The `suggest-compact.sh` script runs on PreToolUse (Edit/Write) and:

1. **Tracks tool calls** - Counts tool invocations in the session.
2. **Threshold detection** - Suggests compaction at a configurable threshold (default: 50 calls).
3. **Periodic reminders** - Reminds every 25 calls after the threshold.

## Hook Setup

Add to your `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "tool == \"Edit\" || tool == \"Write\"",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/strategic-compact/suggest-compact.sh"
      }]
    }]
  }
}
```

## Configuration

Environment variables:

- `COMPACT_THRESHOLD` - Tool calls before the first suggestion (default: 50).

## Best Practices

1. **Compact after planning** - Once the plan is finalized, compact to start fresh.
2. **Compact after debugging** - Clear error-resolution context before continuing.
3. **Don't compact mid-implementation** - Preserve context for related changes.
4. **Read the suggestion** - The hook tells you *when* to compact; you decide *if* to do it.

## Related

- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352) - Token optimization section.
- Memory persistence hooks - For state that survives compaction.