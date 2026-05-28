---
name: task-completer
description: Complete individual tasks with test-first development, quality gates, and proper commits. Use when working on bugs, features, or tasks that result in a single commit.
---

# Task Completer

Complete tasks with rigorous test-first development and quality gates.

## 1. Claim the Task

```bash
bd update <task-id> --status in_progress --json
```

## 2. Test-First Development

**The One Rule: CHANGED CODE = NEW TESTS**

No commits without new tests for changed code.

### Pre-Commit Questions

1. **Did I change production code?** -> Must add tests
2. **Do existing tests pass?** -> NOT ENOUGH. Did you add NEW tests?
3. **Did I add NEW tests for EVERY file I changed?** -> If NO, STOP
4. **Do ALL tests pass (including new ones)?** -> Run `npm test`
5. **Any TypeScript errors?** -> Run `npx tsc --noEmit`

### Workflow

1. Write test FIRST (it should fail)
2. Implement the fix/feature
3. Run tests (they should pass)
4. Commit BOTH production + test files together

### Common Violations

- "Tests already pass" - Did you ADD tests for YOUR changes?
- "It's a small change" - Still needs tests
- "Bug fix only" - Needs regression test
- "I updated existing tests" - Did you ADD new tests too?
- "Frontend change" - Needs component tests
- "Changed 3 files, added tests for 1" - Need tests for ALL 3

## 3. Fail Fast, Fail Loud

**Never silently work around problems. Fix them or let them fail visibly.**

### Principles

- **Missing env vars**: Throw an error, don't silently skip functionality
- **Invalid state**: Crash early with a clear message, don't limp along
- **Missing dependencies**: Fail at startup, not at runtime
- **Tests need mocking**: Mock properly in tests, don't add fallbacks to production code

### Anti-Patterns to Avoid

```typescript
// BAD: Silent failure hides production bugs
if (!process.env.API_KEY) {
  return; // Silently does nothing
}

// GOOD: Fail loudly so the problem is fixed
if (!process.env.API_KEY) {
  throw new Error('API_KEY environment variable is required');
}
```

**The app should work correctly or not at all. Silent misbehavior is worse than a crash.**

## 4. Quality Gates

Run these before committing:

```bash
# Run all tests
npm test

# Type check
npx tsc --noEmit
```

Both must pass with zero errors.

## 5. Commit Checklist

Before EVERY commit, verify ALL of these:

- [ ] **TESTS WRITTEN** - Unit tests exist for ALL new/modified code
- [ ] **TESTS COVER ALL CHANGES** - If you modified N files, you have tests for N files
- [ ] All tests passing (`npm test`)
- [ ] No TypeScript errors (`npx tsc --noEmit`)
- [ ] No `as any` or `as unknown` in production code
- [ ] No optional chaining on required properties

**If you cannot check ALL boxes, DO NOT COMMIT.**

## 6. Make the Commit

```bash
git add -A
git commit -m "$(cat <<'EOF'
<type>: <description>

<optional body>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

## 7. Close the Task

```bash
bd close <task-id> --reason "Completed"
```

## 8. Landing the Plane (Session Completion)

When ending a work session, complete ALL steps:

### Mandatory Workflow

1. **File issues for remaining work**
   ```bash
   bd create "Remaining work description" -t task -p 2 --json
   ```

2. **Run quality gates** (if code changed)
   ```bash
   npm test && npx tsc --noEmit
   ```

3. **Update issue status**
   ```bash
   bd close <completed-task-id> --reason "Done"
   ```

4. **PUSH TO REMOTE** (MANDATORY)
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```

5. **Clean up**
   - Clear stashes: `git stash list` then `git stash drop` if needed
   - Prune remote branches: `git remote prune origin`

6. **Verify**
   - All changes committed AND pushed
   - `git status` shows clean working tree

7. **Hand off**
   - Summarize what was done
   - Note any follow-up tasks created

### Critical Rules

- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds
