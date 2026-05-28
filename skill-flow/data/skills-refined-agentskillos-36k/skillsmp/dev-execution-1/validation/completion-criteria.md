# Completion Criteria

Definition of done for stories, features, and tasks.

## Story Completion

A user story is complete when:

### Implementation

- [ ] All acceptance criteria met
- [ ] All files in plan created/modified
- [ ] Code follows project architecture
- [ ] No `// TODO` comments left behind

### Testing

- [ ] Unit tests added for new logic
- [ ] Integration tests for API flows
- [ ] E2E tests for critical user paths
- [ ] Negative test cases included
- [ ] All tests passing

### Quality

- [ ] TypeScript strict mode, no `any`
- [ ] Lint errors resolved
- [ ] Build succeeds
- [ ] No regressions introduced

### Documentation

- [ ] API docs updated if endpoints added
- [ ] Code comments where logic isn't self-evident
- [ ] README updated if applicable

### Review

- [ ] Code reviewed by senior-code-reviewer
- [ ] Feedback addressed

### Tracking

- [ ] PR created and linked to story
- [ ] Progress tracker shows "complete"
- [ ] Request-log item marked done (if applicable)

## Feature Completion (Quick Feature)

A quick feature is complete when:

### Implementation

- [ ] Feature works as described
- [ ] Follows existing patterns
- [ ] No breaking changes

### Quality Gates

- [ ] `pnpm test` passes
- [ ] `pnpm typecheck` passes
- [ ] `pnpm lint` passes
- [ ] `pnpm build` succeeds

### Tracking

- [ ] Quick plan updated to `status: completed`
- [ ] Request-log item marked done (if from REQ-ID)
- [ ] Issues captured if discovered

## Task Completion

An individual task is complete when:

### Core Criteria

- [ ] Task description fulfilled
- [ ] Success criteria from plan met
- [ ] Files modified as expected

### Code Quality

- [ ] No TypeScript errors
- [ ] Lint clean
- [ ] Tests pass

### Architecture Compliance

- [ ] Follows layered architecture
- [ ] Uses proper patterns (DTOs, ErrorResponse, etc.)
- [ ] Telemetry/logging added where appropriate

### Commit

- [ ] Changes committed with descriptive message
- [ ] References task ID in commit

## Phase Completion

See [./milestone-checks.md] for full phase completion criteria.

Summary:
- [ ] All tasks completed
- [ ] All success criteria met
- [ ] All tests passing
- [ ] Quality gates passed
- [ ] Documentation updated
- [ ] Progress tracker at 100%
- [ ] All commits pushed

## Validation Templates

### Task Validation

```
@task-completion-validator

Task: {task_id}

Expected outcomes:
- {outcome 1}
- {outcome 2}

Files changed:
- {file list}

Validate:
1. Acceptance criteria met
2. Architecture patterns followed
3. Tests exist and pass
4. No regression
```

### Story Validation

```
@task-completion-validator

Story: ${story_id}

Acceptance criteria from story:
- {criterion 1}
- {criterion 2}

Implementation summary:
- Backend: {what was done}
- Frontend: {what was done}
- Tests: {coverage}

Validate complete implementation.
```

### Phase Validation

```
@task-completion-validator

Phase ${phase_num} FINAL VALIDATION

Plan: ${plan_path}
Progress: ${progress_file}

Validate:
1. All tasks complete
2. Success criteria met
3. Tests passing
4. No critical issues
5. Ready for next phase
```

## Common Completion Blockers

### What Blocks Completion

| Issue | Resolution |
|-------|------------|
| Tests failing | Fix before marking complete |
| Type errors | Resolve all TypeScript issues |
| Missing acceptance criteria | Implement missing functionality |
| Unresolved comments | Address all review feedback |
| Breaking changes | Add migration or compatibility |

### When to NOT Mark Complete

Never mark complete if:
- Tests are failing for your changes
- Implementation is partial
- You encountered unresolved errors
- Required files/deps not found
- Review feedback not addressed

### When Blocked

If truly blocked:

1. Document blocker clearly
2. Keep status as `in_progress` or `blocked`
3. Create tracking issue
4. Report to user with:
   - What's blocking
   - What was attempted
   - What's needed to unblock
