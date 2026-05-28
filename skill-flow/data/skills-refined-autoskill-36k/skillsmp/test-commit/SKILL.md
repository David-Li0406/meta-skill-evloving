---
name: test-commit
description: Run tests and create a git commit only if all tests pass. Enforces TDD discipline. Use when you need to run tests before committing code changes, or when following test-driven development workflow.
---

# Test Commit

**Purpose:** Streamlines the test-driven development workflow mandated by project rules.

## Instructions for Claude

When this skill is invoked:

1. **Parse arguments:**
   - `test-path` (optional): specific test file or pattern (default: all tests)
   - `commit-message` (optional): commit message (if empty, will prompt)

2. **Execute workflow:**

   **Step 1: Run tests**
   - If test-path provided: `npm test -- <test-path>`
   - Otherwise: `npm test`
   - Capture output and exit code

   **Step 2: Analyze results**
   - If tests PASS:
     - Show passing test summary
     - Proceed to commit
   - If tests FAIL:
     - Show failures
     - STOP (do NOT commit)
     - Suggest fixes

   **Step 3: Git status**
   - Run `git status --short`
   - Show changed files
   - Confirm files to commit

   **Step 4: Commit (only if tests passed)**
   - If commit message provided: use it
   - Otherwise: ask user for commit message
   - Follow commit message format from CLAUDE.md
   - Add co-author attribution
   - Run `git commit` (respects hooks)

3. **Output format:**
   ```
   TEST & COMMIT WORKFLOW
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   📋 Step 1: Running tests...
   > npm test -- [test-path]

   [test output]

   ✓ Tests passed! ([X] tests, [Y] assertions)

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   📋 Step 2: Git status

   Modified files:
     M src/models/person.js
     M src/__tests__/person.test.js

   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   📋 Step 3: Creating commit...

   ✓ Committed: [commit hash]

   Commit message:
   ─────────────────────────────────
   [commit message]

   🤖 Generated with Claude Code

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
   ─────────────────────────────────

   ✓ All done! Tests passed and changes committed.
   ```

## Error Handling

- If tests fail: block commit, show failures
- If no changes to commit: notify and exit
- If git hooks fail: show error and do not retry
