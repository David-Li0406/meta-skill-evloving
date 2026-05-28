---
name: morning-briefing
description: Context-aware morning status update synthesizing focus, attention items, and schedule
triggers:
  - morning briefing
  - what should I know today
  - daily standup
  - morning update
  - good morning
---

## Objective

Provide a context-aware status update at the start of the day. Synthesize current focus, attention items, and schedule into a cohesive briefing using the Layton persona voice.

## Steps

### 1. Get Context

Gather temporal and environmental context:

```bash
layton context
```

Parse the output to understand:

- Current time of day (morning, afternoon, evening)
- Whether currently in work hours
- Day of week (workday vs weekend)

### 2. Get Attention Items

Query items being actively tracked:

```bash
bd list --label watching --json
```

### 3. Get Current Focus

Check if there's an active focus item:

```bash
bd list --label focus --json
```

### 4. Gather Skill Data (Optional)

If user has skill files configured, run the gather pattern:

For each file in `.layton/skills/`:

- Read the skill file
- Execute commands from `## Commands` section
- Extract information per `## What to Extract` guidance

### 5. Synthesize Briefing

Use the persona voice from `references/persona.md` to deliver the briefing.

**Order of presentation:**

1. **Current Focus** (if any) → "You're currently focused on..."
2. **Attention Items** → "You're watching N items..." (sorted by priority)
3. **Time-appropriate Suggestions** → based on context

## Context Adaptation

Adjust briefing depth based on context:

| Context | Adaptation |
| --- | --- |
| Morning + work hours | Full briefing with all details |
| Evening + not work hours | Brief summary only |
| Attention count > 5 | Suggest triage before detailed review |
| Weekend | Lighter touch, acknowledge personal time |
| Monday morning | Include weekly perspective |

## Success Criteria

- Briefing adapts to time of day and work status
- Focus item mentioned first (if one exists)
- Attention items summarized with accurate counts
- Tone matches Elizabeth Layton persona (professional, warm, helpful)
- Actionable next step suggested
