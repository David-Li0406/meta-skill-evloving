---
name: strategic-compact
description: Use this skill to suggest context compression at logical breakpoints during development sessions, optimizing efficiency and retaining critical information.
---

# Skill body

## Trigger Conditions

- Tool usage reaches a threshold
- Transitioning from research/exploration to implementation
- Completion of a milestone
- Finalization of planning

## Why Strategic Compaction is Needed

### Issues with Automatic Compaction

- Can occur at any point, often mid-task
- May lose important context
- Disrupts thought continuity

### Advantages of Strategic Compaction

- Compresses at logical phase boundaries
- Retains key decisions and context
- Compresses after exploration and before execution
- Compresses after milestone completion

## Timing for Compaction

### Suitable Times for Compaction

1. Completion of exploration/research, ready to start implementation
2. Planning finalized, ready for execution
3. Completion of a functional module
4. Resolution of a complex issue
5. After processing code review feedback
6. Context usage rate exceeds 70%

### Unsuitable Times for Compaction

1. During debugging
2. When multiple file modifications are incomplete
3. While fixing test failures
4. During important decision discussions
5. Midway through complex logic implementation

## Pre-Compaction Checklist

```markdown
## Pre-Compaction Confirmation

- [ ] Current task status recorded in progress.md
- [ ] Key decisions documented
- [ ] Pending assumptions marked
- [ ] Unfinished code changes saved
- [ ] Next steps clearly defined

## Compaction Content

- Current progress
- Key decisions and reasons
- Pending items
- Next tasks
```

## Usage

### Manual Trigger

```
/compact
```

### Automatic Suggestions

The system will prompt to consider compaction when:

1. Tool usage reaches a threshold (default 50 calls)
2. At regular intervals (default every 25 tool calls)

## Configuration

### Threshold Configuration

```bash
# Environment Variable
export COMPACT_THRESHOLD=50  # Number of tool calls for the first reminder
```

### Hook Configuration

In `settings.local.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash skills/strategic-compact/suggest-compact.sh"
          }
        ],
        "description": "Suggest compaction at logical intervals"
      }
    ]
  }
}
```

## Compaction Summary Template

Ensure the following information is included during compaction:

```markdown
## Session Summary

### Completed Tasks

1. [Task 1 description]
2. [Task 2 description]

### Key Decisions

| Decision | Reason | Confidence |
| -------- | ------ | ---------- |
| [Decision 1] | [Reason] | High/Medium/Low |

### Current Status

- Progress: [Percentage or Stage]
- Blockers: [If any]

### Pending

- [ ] [Pending item 1]
- [ ] [Pending item 2]

### Next Steps

[Clearly defined next task]
```

## Best Practices

1. **Phase Boundary Compaction** - Between exploration and implementation, design and coding
2. **Record Before Compaction** - Update progress.md first
3. **Clarify Next Steps** - Compaction summary should include next steps
4. **Avoid Mid-Task Compaction** - Do not compress during complex tasks
5. **Monitor Context Rate** - Consider compaction when exceeding 70%
6. **Retain Key Decisions** - Important decisions should carry into new context
7. **Mark Pending Items** - Clearly label uncertain content

---

**Remember**: The timing of good compaction is more important than the compaction itself. Compress at logical breakpoints to maintain thought continuity.