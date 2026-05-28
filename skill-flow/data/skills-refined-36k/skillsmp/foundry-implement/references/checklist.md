# Post-Implementation Checklist

Before marking a task complete, verify these items.

## Required Checks

- [ ] Implementation matches task instructions
- [ ] All acceptance criteria met
- [ ] Verification appropriate to task scope (check `context.parent_task.children` for sibling verify tasks):
  - **If sibling verify task exists**: Basic checks only (imports work, compiles, no syntax errors)
  - **If no sibling verify task**: Tests written and passing
- [ ] No regressions introduced
- [ ] Code follows project patterns

## Journal Entry Requirements

Every task completion MUST include a journal entry with:

1. **What was accomplished** - Brief summary of implementation
2. **Verification performed** - Scope depends on sibling verify tasks:
   - **If sibling verify task exists**: "Basic checks passed. Full testing deferred to {verify-task-id}"
   - **If no sibling verify task**: "Tests run and results: {summary}"
3. **Deviations from plan** - Any changes from original instructions
4. **Files created/modified** - List of affected files

## Example Completions

**With sibling verify task (deferred testing):**
```bash
mcp__plugin_foundry_foundry-mcp__task action="complete" spec_id="my-spec-001" task_id="task-1-2" completion_note="Implemented phase-add-bulk handler. Basic verification: imports work, no syntax errors. Full test run deferred to verify-1-1. Created src/tools/authoring.py (200 lines)."
```

**Without sibling verify task (full testing):**
```bash
mcp__plugin_foundry_foundry-mcp__task action="complete" spec_id="my-spec-001" task_id="task-2-3" completion_note="Implemented JWT verification middleware with RS256 support. All 8 unit tests passing. Manual verification: auth flow works in dev. Created src/middleware/auth.ts (120 lines) and tests/middleware/auth.spec.ts (8 tests)."
```

## Never Mark Complete If

- Basic checks fail (imports, syntax, compiles)
- Tests are failing (only applies if no sibling verify task)
- Implementation is partial
- Unresolved errors exist
- Required files not found
- Blockers prevent verification

## Blocked Task Handling

If you cannot complete:

```bash
# Mark as blocked with reason
mcp__plugin_foundry_foundry-mcp__task action="block" spec_id={spec-id} task_id={task-id} reason="Missing API endpoint from task-2-1" blocker_type="dependency"

# Present alternatives to user
AskUserQuestion: "Task blocked. Options: 1) Resolve blocker first, 2) Work on different task, 3) Skip and document"
```
