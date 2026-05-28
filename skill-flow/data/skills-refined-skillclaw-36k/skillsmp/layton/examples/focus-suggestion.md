---
name: focus-suggestion
description: Suggest what to focus on based on context, energy, and available tasks
triggers:
  - what should I work on
  - suggest focus
  - help me decide
  - what's next
  - I'm not sure what to do
---

## Objective

Help the user decide what to focus on by considering temporal context, energy levels, and available tasks from their integrated skills. Present 2-3 options with clear rationale.

## Steps

### 1. Get Temporal Context

Understand the current time and work status:

```bash
layton context
```

Use this to inform energy expectations:

- Morning work hours → high energy available
- After lunch → moderate energy
- Evening → winding down
- Outside work hours → personal time

### 2. Check Current Focus

See if there's already an active focus:

```bash
bd list --label focus --json
```

If focus exists, ask if user wants to:

- Continue with current focus
- Set a new focus (will clear current)

### 3. Query Available Work

Gather available tasks from configured skills.

**From GTD (if configured):**

Read `.layton/skills/gtd.md` and execute its commands to get:

- Active next actions
- Task contexts (focus, async, meetings)
- High-priority items

**From Beads:**

```bash
bd list --label watching --json
```

Get tracked items that might need attention.

### 4. Match Tasks to Context

Score tasks based on current context:

| Context | Preferred Task Types |
| --- | --- |
| Morning + high energy | Deep work, complex problems, creative tasks |
| Mid-day | Meetings, collaborative work, communication |
| Afternoon | Routine tasks, follow-ups, documentation |
| Evening (work) | Planning, organizing, low-stakes tasks |
| Outside work hours | Defer work tasks, suggest breaks |

### 5. Present Options

Present 2-3 focus options with rationale:

```markdown
Based on your current context, here are my suggestions:

## Option 1: [Task Name] ⭐ Recommended
**Why now**: [Time/energy match rationale]
**From**: [GTD/Beads/etc]
**Estimated effort**: [Quick/Medium/Deep work]

## Option 2: [Task Name]
**Why now**: [Rationale]
**From**: [Source]
**Estimated effort**: [Effort level]

## Option 3: [Task Name]
**Why now**: [Rationale]
**From**: [Source]
**Estimated effort**: [Effort level]

What would you like to focus on?
```

### 6. Set Focus

When user selects an option, use the set-focus workflow:

Read `skills/layton/workflows/set-focus.md` and follow its steps to:

- Clear any existing focus
- Set the new focus item
- Confirm the change

## Context Adaptation

- **Low energy / end of day**: Suggest shorter, easier tasks or wrapping up
- **High energy morning**: Prioritize important, challenging work
- **Many urgent items**: Suggest triage first
- **No tasks available**: Suggest capturing new work or taking a break
- **Outside work hours**: Gently redirect to rest, unless user insists

## Success Criteria

- Context is considered in suggestions
- 2-3 options presented with clear rationale
- Energy level matched to task difficulty
- Source of each task is clear
- User can select and focus is set via set-focus workflow
