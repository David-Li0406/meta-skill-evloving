---
name: strategic-context-compaction
description: Use this skill to suggest manual context compaction at logical intervals during your workflow to preserve context through task phases.
---

# Strategic Context Compaction Skill

This skill suggests manual `/compact` at strategic points in your workflow rather than relying on arbitrary auto-compaction.

## Why Strategic Compaction?

Auto-compaction triggers at arbitrary points, which can lead to:

- Loss of important context mid-task
- Lack of awareness of logical task boundaries
- Interruptions during complex multi-step operations

Strategic compaction should occur at logical boundaries, such as:

- **After exploration, before execution** - Compact research context while retaining the implementation plan.
- **After completing a milestone** - Prepare for a fresh start in the next phase.
- **Before major context shifts** - Clear exploration context before transitioning to a different task.

## How It Works

The `suggest-compact.sh` script runs on PreToolUse (Edit/Write) and performs the following:

1. **Tracks tool calls** - Counts tool invocations in the session.
2. **Threshold detection** - Suggests compaction at a configurable threshold (default: 50 calls).
3. **Periodic reminders** - Sends reminders every 25 calls after the threshold is reached.

## Hook Setup

To set up the hook, add the following to your `~/.claude/settings.json`:

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

You can configure the following environment variable:

- `COMPACT_THRESHOLD` - Number of tool calls before the first suggestion (default: 50).

## Best Practices

1. **Compact after planning** - Once the plan is finalized, compact to start fresh.
2. **Compact after debugging** - Clear error-resolution context before continuing.
3. **Avoid compacting mid-implementation** - Preserve context for related changes.
4. **Read the suggestion** - The hook indicates *when* to compact, but you decide *if* to do so.

## Related

- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352) - Token optimization section.
- Memory persistence hooks - For state that survives compaction.