---
name: ralph-autonomous-backlog-processing
description: Use this skill when Ralph is autonomously processing backlogs, selecting tickets, implementing features, and managing workflow without direct supervision.
---

# Ralph Autonomous Backlog Processing Skill

This skill provides a comprehensive workflow for Ralph to autonomously process backlogs, select tickets, implement features, and manage workflow effectively.

## When to Use This Skill

- Processing multiple tickets autonomously
- Working through a product backlog
- Implementing features from a PRD file
- Running in background agent mode

## Autonomous Mode Principles

### Core Philosophy

- **No User Input Required**: Ralph makes decisions independently.
- **Context-Driven**: Uses PRD and progress files for guidance.
- **Incremental Progress**: One ticket per session, verify completion.
- **Self-Documenting**: Logs all decisions and progress.

## The Ralph Workflow

### 1. Read Context Files

```bash
read('plans/prd.json')           # Product requirements (auto-generated from tickets)
read('plans/progress.txt')       # Notes from previous iterations
```

### 2. Set Up Git Branch

Before any code changes:
```bash
git fetch origin
git checkout -b ralph/<ticket-id>-<description> origin/dev
# or origin/main if no dev branch
```

### 3. Ticket Selection Algorithm

From `prd.json`, find a user story where `passes: false`:
- Prioritize by priority field (high > medium > low)
- Only work on ONE task per iteration

```typescript
function selectTicket(tickets: Ticket[]): Ticket {
  const incomplete = tickets.filter((t) => !t.passes);
  const sorted = incomplete.sort((a, b) => {
    if (a.priority !== b.priority) {
      return priorityOrder[a.priority] - priorityOrder[b.priority];
    }
    return dependencyCount(a) - dependencyCount(b);
  });
  return sorted[0]; // Highest priority, least blocked
}
```

### 4. Post Progress Update

```javascript
add_ticket_comment({
  ticketId: "story-id",
  content: "Starting work on user authentication. Will implement login form and API endpoint.",
  author: "ralph",
  type: "comment"
})
```

### 5. Implement Feature

- Write the code
- Run type checks: `pnpm type-check` or `npm run type-check`
- Run tests: `pnpm test` or `npm test`
- Verify acceptance criteria

### 6. Commit Changes

```bash
git add -A
git commit -m "feat(<ticket-id>): <description>"
```

### 7. Update PRD

Edit `plans/prd.json` to set `passes: true` for the completed story.

### 8. Update Progress File

Append to `plans/progress.txt`:
```
## Iteration N - [timestamp]
- Completed: <ticket title>
- Changes: <brief summary>
- Notes: <any learnings or issues>
```

### 9. Update Ticket Status

```javascript
update_ticket_status("ticket-id", "done")

add_ticket_comment({
  ticketId: "ticket-id",
  content: "## Work Summary\n**Changes:**\n- ...\n**Tests:**\n- All passing",
  author: "ralph",
  type: "work_summary"
})
```

### 10. Check Completion

If ALL stories have `passes: true`:
- Push branch: `git push -u origin <branch-name>`
- Create PR using `gh pr create`
- Output: `PRD_COMPLETE`

## Important Rules

1. **One task per iteration** - Keeps context focused.
2. **Always test** - Run tests before marking complete.
3. **Update status** - Use MCP tools to track progress.
4. **Document issues** - Add blockers to progress.txt.
5. **Never commit to main/dev** - Always use feature branches.

## Quality Assurance

### Pre-Completion Checklist

Before calling `complete_ticket_work()`:

```typescript
const completion_checklist = {
  code_quality: verify_style_conventions(),
  error_handling: verify_error_boundaries(),
  performance: no_performance_regressions(),
  documentation: updated_docs_if_needed(),
  testing: all_tests_passing(),
  acceptance: all_criteria_met(),
};

if (!completion_checklist.all_true()) {
  fix_remaining_issues();
}
```

## Troubleshooting

### Common Issues

1. **Ticket selection conflicts** → Use priority matrix.
2. **Implementation ambiguity** → Choose simplest approach that meets AC.
3. **Test failures** → Fix before proceeding.
4. **Scope creep** → Split ticket or defer features.

This skill ensures Ralph works effectively and autonomously while maintaining high code quality and transparency.