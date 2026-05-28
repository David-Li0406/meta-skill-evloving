# Task Output Template

Tasks extracted from meetings should be formatted for easy import into project management systems.

## Task File Structure

Create a separate file named `[Meeting Name] - Tasks.md` in the same folder as the summary.

```markdown
# Tasks from [Meeting Title]

**Source:** [Meeting name/date]
**Created:** [Date this file was created]
**Meeting Folder:** [Path to meeting folder]

---

## Summary

- **Total Tasks:** [N]
- **[Party 1] Tasks:** [N]
- **[Party 2] Tasks:** [N]

---

## [Party 1] Tasks

### Task: [Brief task title]

- **Description:** [What needs to be done - be specific]
- **Owner:** [Person responsible]
- **Due:** [Date if specified, otherwise "TBD"]
- **Priority:** [High/Medium/Low if determinable]
- **Context:** [Why this task exists, related decisions]
- **Dependencies:** [What needs to happen first, if any]
- **Status:** Not Started

---

### Task: [Brief task title]

- **Description:** [What needs to be done]
- **Owner:** [Person responsible]
- **Due:** [Date if specified]
- **Priority:** [High/Medium/Low]
- **Context:** [Background]
- **Dependencies:** [If any]
- **Status:** Not Started

---

## [Party 2] Tasks

### Task: [Brief task title]

- **Description:** [What needs to be done]
- **Owner:** [Person responsible]
- **Due:** [Date if specified]
- **Priority:** [High/Medium/Low]
- **Context:** [Background]
- **Dependencies:** [If any]
- **Status:** Not Started

---

## Unassigned Tasks

Tasks where ownership needs clarification:

### Task: [Brief task title]

- **Description:** [What needs to be done]
- **Owner:** ⚠️ NEEDS ASSIGNMENT
- **Suggested Owner:** [Best guess based on context]
- **Due:** [Date if specified]
- **Context:** [Background]

---

## Questions for Clarification

If any task details are unclear:

1. **[Question about task]** - Needed to assign: [Task name]
2. **[Question about ownership]** - Needed to assign: [Task name]
```

## Task Extraction Guidelines

### What Constitutes a Task

**Include:**
- Explicit action items ("I'll send you X", "We need to do Y")
- Follow-up items ("Let's schedule a call with Z")
- Deliverables with owners ("The report is due by...")
- Requests made during meeting ("Can you get me access to...")

**Exclude:**
- Vague intentions without clear actions
- Ongoing responsibilities (unless a specific next action is clear)
- Topics for future discussion (unless there's a clear "schedule discussion" action)

### Determining Task Ownership

**Clear ownership:**
- Person volunteered: "I'll handle that"
- Person was assigned: "Sarah, can you take this?"
- Role-based: "Marketing will prepare..."

**Unclear ownership - flag for clarification:**
- Passive voice: "This needs to be done"
- Group assignment: "We should..."
- No explicit owner mentioned

### Priority Assignment

| Priority | Indicators |
|----------|-----------|
| **High** | Explicit deadline, blocker for other work, mentioned as urgent |
| **Medium** | Important but no hard deadline, part of normal workflow |
| **Low** | Nice-to-have, future consideration, no time pressure |

### Due Date Handling

- **Explicit date:** Use exactly as stated
- **Relative date:** Convert to absolute (e.g., "next Friday" → actual date)
- **No date mentioned:** Mark as "TBD"
- **Implied urgency:** Note in context (e.g., "Mentioned as time-sensitive")

## Integration Notes

This task format is designed to be:
1. Human-readable for review
2. Structured enough for automated parsing
3. Compatible with the `clickup-push-tasks` skill for project management import

When pushing to project management:
- Parent task = Meeting name
- Each task becomes a subtask
- Unassigned tasks are flagged for manual assignment
