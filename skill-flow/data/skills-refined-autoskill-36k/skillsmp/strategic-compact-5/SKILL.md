---
name: strategic-compact
description: |
  Smart compaction suggestions at logical session intervals.

  ACTIVATE when: context getting full, transitioning between phases,
  user mentions "running out of context", "conversation too long".

  <example>
  50 tool calls reached during implementation
  → Suggest /compact if transitioning from exploration to implementation
  </example>

  <example>
  User about to start new phase after completing exploration
  → Suggest /handoff or /compact before starting fresh
  </example>
---

# Strategic Compact Skill

Provides intelligent suggestions for when to compact context, prioritizing manual compaction over auto-compaction for better control.

## Philosophy

**Manual compaction > Auto-compaction**

- Auto-compaction happens at arbitrary points, often mid-task
- Strategic compaction preserves context through logical phases
- Compact after exploration, before execution
- Compact after completing milestones, before starting next

## When to Compact

### Good Times to Compact

| Scenario | Why |
|----------|-----|
| After exploration, before implementation | Exploration context often not needed for implementation |
| After completing a milestone | Clean slate for next phase |
| After finalizing a plan | Plan is documented, context can be reduced |
| After debugging, before new feature | Debug context clutters new work |
| Before starting unrelated task | Previous context not relevant |

### Bad Times to Compact

| Scenario | Why |
|----------|-----|
| Mid-implementation | Loses implementation context |
| During debugging | Loses diagnostic information |
| Before completing a task | May need to reference earlier context |
| During code review | Loses review context |

## Compaction Strategy

### Option 1: /compact (Built-in)
- Summarizes conversation
- Frees context space
- May lose some nuance

### Option 2: /handoff (Recommended)
- Creates HANDOFF.md with:
  - Goal
  - Progress
  - What worked
  - What didn't work
  - Next steps
- Start fresh conversation with just the handoff file
- Preserves important context in documented form

### Option 3: /half-clone
- Keeps only later half of conversation
- Good when recent work is important
- Discards earlier exploration

## Hook Configuration

To enable automatic suggestions, add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "tool matches \"Edit|Write\"",
      "hooks": [{
        "type": "command",
        "command": "~/.claude/skills/strategic-compact/suggest-compact.sh"
      }],
      "description": "Suggest compaction at logical intervals"
    }]
  }
}
```

## Suggestion Thresholds

The `suggest-compact.sh` script tracks tool calls and suggests compaction:

| Threshold | Action |
|-----------|--------|
| 50 tool calls | First suggestion |
| Every 25 after | Reminder suggestions |

Customize with environment variable:
```bash
export COMPACT_THRESHOLD=75  # Higher threshold
```

## Integration with Context Management

```
Context Management Ecosystem:
┌─────────────────────────────────────────────────────────┐
│  EXPLORATION PHASE                                       │
│    ↓                                                     │
│  [50 tool calls] → strategic-compact suggests            │
│    ↓                                                     │
│  IMPLEMENTATION PHASE                                    │
│    ↓                                                     │
│  [75 tool calls] → reminder                              │
│    ↓                                                     │
│  COMPLETION                                              │
│    ↓                                                     │
│  User choice:                                            │
│    ├─ /compact (quick, built-in)                        │
│    ├─ /handoff (documented, recommended)                │
│    └─ /half-clone (keep recent work)                    │
└─────────────────────────────────────────────────────────┘
```

## Best Practices

1. **Document Before Compacting**: Use /handoff to preserve important decisions
2. **Compact at Phase Transitions**: Not mid-task
3. **Use /half-clone for Long Sessions**: When recent work is valuable
4. **Disable Auto-Compact**: `/config` → Turn off auto-compact for more control
5. **Monitor Context Bar**: Watch for when context is filling up

## Manual Compaction Workflow

```
1. Notice context getting full or transitioning phases
2. Run /handoff to document current state
3. Review HANDOFF.md
4. Start fresh conversation with: > path/to/HANDOFF.md
5. Continue work with clean context
```

## Configuration

The script uses these defaults:
- `COMPACT_THRESHOLD`: 50 tool calls (customizable via env)
- Counter resets each session
- Suggestions are non-blocking (just stderr messages)
