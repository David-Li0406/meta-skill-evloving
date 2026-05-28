---
name: test-and-commit
description: Run unit tests, evaluate and fix relevant E2E tests, assess coverage needs, lint, and commit. Use when user says "test and commit", "run tests and commit", "verify and commit", or "CI and commit".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, AskUserQuestion, TodoWrite
version: 5.1.0
---

# Test and Commit

> Run unit tests first, evaluate/fix relevant E2Es, assess coverage, lint, then commit.

<when_to_use>

## When to Use

Invoke when user says:

- "test and commit"
- "run tests and commit"
- "verify and commit"
- "CI and commit"
  </when_to_use>

<workflow>

## Workflow Overview

| Phase | Action                              | Gate             |
| ----- | ----------------------------------- | ---------------- |
| 1     | Run all unit tests                  | Must pass        |
| 2     | Identify relevant E2E tests         | Based on changes |
| 3     | Fix failing E2Es, run relevant only | Must pass        |
| 4     | Evaluate coverage needs             | Ask user         |
| 5     | Write new tests if needed           | Optional         |
| 6     | Lint and fix errors                 | Must pass        |
| 7     | Sync documentation                  | User approval    |
| 8     | Commit changes                      | Only if all pass |

Track progress with TodoWrite.
</workflow>

<phases>

### Phase 1: Run All Unit Tests

Run the full unit test suite first. Stop if tests fail.

```bash
npm run test:unit -- --run
```

| Result   | Action                               |
| -------- | ------------------------------------ |
| All pass | Continue to Phase 2                  |
| Failures | Fix failing tests, re-run until pass |

If failures are in changed files, fix them. If failures are pre-existing/unrelated, inform user and ask how to proceed.

---

### Phase 2: Identify Relevant E2E Tests

1. Get changed files:

```bash
git diff --name-only HEAD
```

2. Map changed files to E2E tests using these rules:

| Changed File Pattern               | Relevant E2E Tests                   |
| ---------------------------------- | ------------------------------------ |
| `src/pages/Sessions*.tsx`          | `playwright/tests/session-*.spec.ts` |
| `src/pages/Accounts*.tsx`          | `playwright/tests/account-*.spec.ts` |
| `src/pages/Contacts*.tsx`          | `playwright/tests/contact-*.spec.ts` |
| `src/components/tables/*Table.tsx` | E2E for that domain                  |
| `src/hooks/use*.ts`                | E2E for features using that hook     |
| `src/services/*.service.ts`        | E2E for features using that service  |

3. List the relevant E2E tests found. If none are relevant, skip to Phase 4.

---

### Phase 3: Run and Fix Relevant E2E Tests

Run only the relevant E2E tests identified in Phase 2:

```bash
npx playwright test <spec-file> --retries=3 --timeout=120000
```

| Result   | Action                                    |
| -------- | ----------------------------------------- |
| All pass | Continue to Phase 4                       |
| Failures | Evaluate if failure is due to our changes |

**If E2E fails due to our changes:**

1. Read the failing test to understand what it expects
2. Fix either the code or the test as appropriate
3. Re-run until pass

**If E2E fails due to pre-existing issues:**

1. Inform user of unrelated failure
2. Ask whether to skip or fix

---

### Phase 4: Evaluate Coverage Needs

Assess if new tests are needed for the changed files.

1. Identify changed testable files (`.ts`, `.tsx` in `src/`, excluding tests)

2. For each file, check:
   - Does a corresponding test file exist?
   - Does the test cover the changed functionality?

3. Use AskUserQuestion if gaps exist:

```typescript
{
  questions: [
    {
      question: "Found coverage gaps. Create tests for these files?",
      header: "Coverage",
      options: [
        {
          label: "Yes, create tests",
          description: "Write missing unit/E2E tests",
        },
        { label: "Skip for now", description: "Commit without new tests" },
      ],
      multiSelect: false,
    },
  ];
}
```

---

### Phase 5: Write New Tests (If Needed)

If user approves, create tests following these patterns:

| Code Type | Test Type | Location                                |
| --------- | --------- | --------------------------------------- |
| Component | Unit      | `src/**/__tests__/[name].test.tsx`      |
| Hook      | Unit      | `src/hooks/__tests__/[name].test.ts`    |
| Service   | Unit      | `src/services/__tests__/[name].test.ts` |
| Page flow | E2E       | `playwright/tests/[feature].spec.ts`    |

Follow patterns in:

- `claude-patterns/testing-patterns.md` (unit tests)
- `claude-patterns/playwright-best-practices.md` (E2E tests)

Run new tests to verify they pass before continuing.

---

### Phase 6: Lint and Fix Errors

Lint all changed files:

```bash
git diff --name-only HEAD | grep -E '\.(ts|tsx)$' | xargs npx eslint --max-warnings 0
```

| Result | Action                                   |
| ------ | ---------------------------------------- |
| Pass   | Continue to Phase 8                      |
| Errors | Run `--fix`, then fix remaining manually |

```bash
# Auto-fix what's possible
git diff --name-only HEAD | grep -E '\.(ts|tsx)$' | xargs npx eslint --fix
```

---

### Phase 7: Sync Documentation

Check if code changes affect documentation in `.claude/rules/` and `claude-patterns/`.

1. Get changed source files:

```bash
git diff --name-only HEAD | grep -E '\.(ts|tsx)$'
```

2. Search documentation for references to changed files:

```bash
# For each changed file, search with multiple patterns
grep -rE "(src/path/to/file\.ts|filename\.ts)" claude-patterns/ .claude/rules/
```

3. For each doc file with references to changed code:
   - **Read the doc** to understand context (not blind find/replace)
   - **Verify the reference**: Does the file/function still exist?
   - **Identify staleness**: Has the path, name, or behavior changed?

4. Categorize updates needed:

| Update Type                       | Action                                             |
| --------------------------------- | -------------------------------------------------- |
| File path renamed                 | Auto-update (context-aware, not blind replacement) |
| Function/type renamed (clear 1:1) | Auto-update with verification                      |
| Code deleted                      | Flag for user - may need doc section removal       |
| Pattern/behavior changed          | Flag for user - requires rewrite                   |
| Line number references            | Flag for user - inherently unstable                |

5. If updates needed, use AskUserQuestion:

```typescript
{
  questions: [
    {
      question: "Found stale documentation references. How to proceed?",
      header: "Doc Sync",
      options: [
        {
          label: "Update docs",
          description: "Apply context-aware updates, include in commit",
        },
        {
          label: "Review each",
          description: "Show me each change before applying",
        },
        { label: "Skip", description: "Commit code without doc updates" },
      ],
      multiSelect: false,
    },
  ];
}
```

| Result              | Action                                         |
| ------------------- | ---------------------------------------------- |
| Update docs         | Apply updates, continue to Phase 7             |
| Review each         | Show diff for each doc, apply approved changes |
| Skip                | Continue to Phase 8 without doc changes        |
| No stale refs found | Continue to Phase 8 (no prompt needed)         |

**Known Limitations:**

- May miss relative paths or partial filename matches
- Line number references become stale on any file edit
- Cannot detect semantic/behavior changes, only structural (renames, deletions)

---

### Phase 8: Commit

1. Stage changed files:

```bash
git add <files>
```

2. Commit with descriptive message:

```bash
git commit -m "$(cat <<'EOF'
<type>(<scope>): <description>

<body>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

</phases>

<approval_gates>

## Approval Gates

| Gate                  | Phase | Question                                              |
| --------------------- | ----- | ----------------------------------------------------- |
| Pre-existing failures | 1, 3  | "Tests failed but unrelated to changes. Skip or fix?" |
| Coverage gaps         | 4     | "Create tests for uncovered files?"                   |
| Doc sync              | 7     | "Found stale doc references. Update?"                 |
| Commit scope          | 8     | "Which files to commit?" (if mixed changes)           |

</approval_gates>

<quick_reference>

## Quick Reference

```bash
# Phase 1: Unit tests
npm run test:unit -- --run

# Phase 3: Specific E2E
npx playwright test <spec-file> --retries=3

# Phase 6: Lint changed files
git diff --name-only HEAD | grep -E '\.(ts|tsx)$' | xargs npx eslint --max-warnings 0
```

For commands: [references/commands.md](references/commands.md)
For test locations: [references/test-locations.md](references/test-locations.md)
</quick_reference>

<guidelines>

## Guidelines

- Run unit tests before E2E (faster feedback loop)
- Only run E2E tests relevant to changes (not full suite)
- Fix test failures before adding new tests
- Lint after all test work is complete
- Ask user before creating new test files
- Sync documentation before committing to keep docs accurate
- Doc updates are context-aware reads, not blind find/replace
  </guidelines>

<references>

## References

- [references/commands.md](references/commands.md) - Full CI command reference
- [references/test-locations.md](references/test-locations.md) - Test file patterns and locations
  </references>

<version_history>

## Version History

- **v5.1.0** (2026-01-20): Add Phase 7 for documentation synchronization
  - Detects when code changes affect `.claude/rules/` and `claude-patterns/`
  - Context-aware updates (reads doc, understands purpose)
  - Auto-updates file paths and clear 1:1 renames
  - Flags deletions, behavior changes, and line numbers for user review
  - Known limitation: May miss some reference patterns

- **v5.0.0** (2026-01-20): Complete workflow restructure
  - Phase 1: Run ALL unit tests first (not just audit)
  - Phase 2-3: Evaluate and fix relevant E2E tests only
  - Phase 4-5: Coverage evaluation moved after test validation
  - Phase 6: Lint after all test work
  - Commit only after everything passes
  - Rationale: Catch test failures early, fix before committing

- **v4.1.0** (2025-01-18): AI optimization updates
  - Add blockquote summary after title
  - Soften directive language

- **v4.0.0** (2025-12-29): Slimmed down - removed checks handled by pre-push
  - Removed: typecheck, unit tests, E2E tests (pre-push hook handles these)
  - Kept: test coverage audit, selective lint, commit

- **v3.0.0** (2025-12-28): Refactored to follow skill-authoring-patterns

- **v1.0.0** (2025-11-30): Initial release
  </version_history>
