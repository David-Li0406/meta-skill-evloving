---
name: add-todo
description: Use this skill to add properly formatted TODO items to TODOS.md, ensuring integration with existing structures and workflows.
---

# Add TODO Item

Add a new TODO item to `TODOS.md` in the project root with proper formatting that integrates with `/list-todos` and `/run-todos`.

## Directory Guard

Before starting, check if `TODOS.md` exists in the current working directory.

- If it exists, read it to understand the current structure.
- If it does not exist, create it with the standard template.

## TODO Format Reference

TODOs in this system follow a specific format for compatibility with other skills:

### Basic Format

```markdown
- [ ] **[{Priority} / {Effort}]** {Title} — {Brief description}
```

**Components:**

| Component | Format | Examples |
|-----------|--------|----------|
| Checkbox | `- [ ]` (pending) or `- [x]` (done) | `- [ ]` |
| Priority | `P0` (critical), `P1` (high), `P2` (low) | `**[P1 / Medium]**` |
| Effort | `Low`, `Medium`, `High` | `**[P2 / Low]**` |
| Multiplier | Optional `x{N}` (0.5-2.0) | `**[P1 / Medium x1.5]**` |
| Title | Short, actionable description | `Add user authentication` |
| Description | Optional extended description | `— Support OAuth and email/password` |

### Tags

| Tag | Meaning | When to Use |
|-----|---------|-------------|
| `[ready]` | Clarified and ready to implement | After Q&A in /list-todos |
| `[priority: N]` | Personal priority multiplier | Inline override (0.5-2.0) |

### Status Markers

| Marker | Meaning |
|--------|---------|
| `— DONE` | Completed |
| `— DONE ({hash})` | Completed with commit reference |
| `— **DEFERRED** ({reason})` | Postponed with explanation |
| `— **REMOVED** ({reason})` | Canceled with explanation |

## Workflow

### Step 1: Gather Information

Use AskUserQuestion to collect TODO details:

1. **Title**: "What is the TODO item? (brief, actionable title)"
2. **Priority**: "What priority level?"
3. **Effort**: "Estimated effort?"
4. **Description (Optional)**: "Add a description? (optional details, context, or requirements)"
5. **Section**: "Which section should this go in?"

### Step 2: Format the TODO

Construct the TODO line:

```markdown
- [ ] **[{Priority} / {Effort}]** {Title}{if description: — {Description}}
```

### Step 3: Read Current TODOS.md

Read `TODOS.md` to find the appropriate section.

**Section Detection:**
- Look for `## In Progress` heading
- Look for `## Future Concepts` heading
- If neither exists, create the section

### Step 4: Insert TODO

Insert the new TODO at the **end** of the selected section, before the next section heading or end of file.

### Step 5: Confirm

Output confirmation:

```
TODO ADDED
==========

Added to: {Section}

{The formatted TODO line}

Next steps:
- Run /list-todos to analyze and prioritize
- Use Q&A to clarify requirements
- Mark [ready] when requirements are clear
- Run /run-todos to implement
```

## TODOS.md Template

If `TODOS.md` doesn't exist, create it:

```markdown
# TODO

## In Progress

{new TODO here}

## Future Concepts

(Ideas to explore later)
```

## Notes

- **Preserve existing format** — Match the style of existing TODOs in the file.
- **Don't add [ready] automatically** — Let /list-todos Q&A determine readiness.
- **Default to In Progress** — Most new TODOs are active work items.
- **Keep titles actionable** — Start with a verb (Add, Fix, Update, Implement).
- **Descriptions are optional** — Only add if title alone is ambiguous.