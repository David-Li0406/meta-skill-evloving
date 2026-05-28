# Workflow Authoring Guide

This reference explains how to create workflow files for Layton. Workflow files are AI-readable instructions that define multi-step processes like briefings, reviews, and data gathering.

## Template

The workflow template is in `templates/workflow.md`. The CLI uses this when you run:

```bash
layton workflows add <name>
```

This creates `.layton/workflows/<name>.md` with the template structure.

## Field Guide

### Frontmatter Fields

| Field | Required | Purpose | Example |
|-------|----------|---------|---------|
| `name` | Yes | Lowercase with hyphens, matches filename | `morning-briefing` |
| `description` | Yes | One-line summary of what this workflow does | `Context-aware morning status update` |
| `triggers` | Yes | Phrases that activate this workflow (2-5 recommended) | `["good morning", "daily standup"]` |

### Section Guide

#### `## Objective`

What to include:

- Clear statement of the workflow's purpose
- What the user should have when it completes
- Any important constraints or scope

Good example:

```markdown
## Objective

Provide a context-aware status update at the start of the day. Synthesize current focus, attention items, and schedule into a cohesive briefing using the Layton persona voice.
```

Bad example:

```markdown
## Objective

Do the morning briefing.
```

#### `## Steps`

What to include:

- Numbered steps in execution order
- Concrete commands where applicable
- What to do with the results of each step

Good example:

```markdown
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

### 3. Synthesize Briefing

Combine context and items into a briefing. Present in this order:

1. Current focus (if any)
2. Attention items (sorted by priority)
3. Time-appropriate suggestions

```

Bad example:
```markdown
## Steps

1. Check stuff
2. Get the data
3. Tell the user about it
```

#### `## Context Adaptation`

What to include:

- How the workflow should adapt to different situations
- Time-based variations (morning vs evening, workday vs weekend)
- Load-based variations (high vs low attention count)

Good example:

```markdown
## Context Adaptation

| Context | Adaptation |
|---------|------------|
| Morning + work hours | Full briefing with all details |
| Evening + not work hours | Brief summary only |
| Attention count > 5 | Suggest triage before detailed review |
| Weekend | Lighter touch, acknowledge personal time |
| Monday morning | Include weekly perspective |
```

#### `## Success Criteria`

What to include:

- Checkable conditions for workflow completion
- What the user should have/know when done
- Any side effects that should have occurred

Good example:

```markdown
## Success Criteria

- [ ] Briefing adapts to time of day and work status
- [ ] Focus item mentioned first (if one exists)
- [ ] Attention items summarized with accurate counts
- [ ] Actionable next step suggested
```

## Examples

### Minimal Workflow

```markdown
---
name: quick-status
description: Fast status check of focus and watching items
triggers:
  - quick status
  - what am I doing
  - status check
---

## Objective

Provide a rapid status snapshot without full briefing ceremony.

## Steps

1. Get current focus:
   ```bash
   bd list --label focus --json
   ```

2. Get watching count:

   ```bash
   bd list --label watching --json | jq length
   ```

3. Report in one sentence:
   - "You're focused on [X], watching [N] items."
   - Or: "No current focus. Watching [N] items."

## Context Adaptation

- Always brief, regardless of time
- If focus is stale (> 1 day old), mention it

## Success Criteria

- [ ] Focus reported (or absence noted)
- [ ] Watching count accurate
- [ ] Response is one sentence

```

### Complex Workflow

```markdown
---
name: weekly-review
description: End-of-week reflection on completed work and planning for next week
triggers:
  - weekly review
  - end of week
  - friday review
  - week in review
---

## Objective

Guide user through a structured weekly review: celebrate wins, clear completed items, identify carryover, and set intentions for next week.

## Steps

### 1. Get Context

```bash
layton context
```

Confirm it's end of week (Thursday PM or Friday).

### 2. Review Completed Items

```bash
bd list --label closed --since "7 days ago" --json
```

Summarize what was accomplished this week.

### 3. Review Watching Items

```bash
bd list --label watching --json
```

For each item:

- Still relevant? → Keep
- Completed? → Close it
- Stale? → Discuss with user

### 4. Check Focus

```bash
bd list --label focus --json
```

Is current focus still the right priority for next week?

### 5. Plan Next Week

Ask user:

- What's the most important thing for next week?
- Anything to add to watching list?
- Any deadlines coming up?

### 6. Summarize

Provide a summary:

- This week: [wins]
- Cleared: [closed items]
- Carrying forward: [active watching]
- Next week focus: [intention]

## Context Adaptation

| Context | Adaptation |
|---------|------------|
| Friday afternoon | Full review |
| Friday morning | Abbreviated, offer to continue later |
| Thursday evening | Proactive, "getting a head start" |
| Monday | "Let's do a quick retrospective instead" |

## Success Criteria

- [ ] Wins from this week acknowledged
- [ ] Stale watching items addressed
- [ ] Next week intention captured
- [ ] User feels closure on the week

```

## Optional Sections

### `## Example Output`

Show what the workflow result should look like. This helps AI understand the expected format and tone:

```markdown
## Example Output

> Good morning.
>
> **Focus:** You're currently focused on "API refactoring for v2"
>
> **Watching:** 3 items (1 PR awaiting review, 2 issues tracked)
>
> **GTD:** Inbox clear ✓ | 4 focus tasks ready | 2 active projects
>
> **Suggestion:** Your high-energy morning slot is ideal for the architecture review. I'd start there.
```

This is especially valuable for:

- Briefings (shows expected structure and tone)
- Reports (shows formatting expectations)
- Any workflow where output format matters

## Common Mistakes

1. **Vague steps** - "Check the status" doesn't tell AI what command to run
2. **Missing commands** - If a step needs data, include the exact command
3. **No adaptation** - Workflows should flex based on context
4. **Too many triggers** - 2-5 focused triggers beat 10 overlapping ones
5. **Rigid structure** - Leave room for AI judgment within steps
6. **No success criteria** - How do you know when it's done?
7. **No example output** - For briefings/reports, show what good looks like
