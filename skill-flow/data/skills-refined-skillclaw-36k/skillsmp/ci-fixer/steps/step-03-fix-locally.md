---
name: step-03-fix-locally
description: Fix errors and verify locally - tests and lint MUST pass
prev_step: steps/step-02-analyze-errors.md
next_step: steps/step-04-commit-push.md
---

# Step 3: Fix Locally

## MANDATORY EXECUTION RULES (READ FIRST):

- 🛑 **ABSOLUTELY NO HACKS OR BYPASSES** - Fix the real problem
- 🛑 NEVER skip tests or linting - EVERYTHING must pass
- 🛑 NEVER use --no-verify, --skip, or any bypass flags
- 🛑 NEVER hack around issues (disabling rules, skipping files)
- ✅ ALWAYS run full test suite locally before committing
- ✅ ALWAYS run lint/format check before committing
- ✅ ALWAYS fix the root cause, not the symptom
- 📋 YOU ARE A FIXER, doing proper fixes only
- 💬 FOCUS on minimal, targeted fixes
- 🚫 FORBIDDEN to commit without local verification passing

---

## 🚫 FORBIDDEN HACKS - NEVER DO THESE

**These are STRICTLY FORBIDDEN. If you catch yourself doing any of these, STOP and fix properly:**

### Code Hacks (NEVER USE):

- `// @ts-ignore` or `// @ts-expect-error` - Fix the type instead
- `// eslint-disable` or `// eslint-disable-next-line` - Fix the lint error
- `// prettier-ignore` - Fix the formatting
- `as any` or `: any` - Use proper types
- `!` non-null assertion to silence errors - Handle null properly
- Empty catch blocks `catch {}` - Handle errors properly
- `console.log` left in code - Remove debugging code

### Test Hacks (NEVER USE):

- `.skip` or `it.skip` or `describe.skip` - Run all tests
- `.only` or `it.only` - Run all tests
- `--testPathIgnorePatterns` to skip tests - Run all tests
- `--passWithNoTests` - Ensure tests exist
- Commenting out failing tests - Fix them
- Changing assertions to match wrong output - Fix the code

### Git Hacks (NEVER USE):

- `--no-verify` on commit - Let hooks run
- `--force` push without reason - Push normally
- Amending commits to bypass checks - Create proper commits

### Config Hacks (NEVER USE):

- Adding files to `.eslintignore` to hide errors - Fix the errors
- Disabling rules in eslint config - Fix the code
- Lowering TypeScript strictness - Fix the types
- Skipping files in tsconfig - Include all files

### Dependency Hacks (NEVER USE):

- `--legacy-peer-deps` without understanding why - Fix dependencies
- `--force` install - Resolve conflicts properly
- Pinning to old broken versions - Update properly

**If a proper fix seems impossible, ASK THE USER for help instead of hacking.**

---

## EXECUTION PROTOCOLS:

- 🎯 Fix → Verify locally → Iterate until green
- 💾 Track fixes in `{fixes_applied}`
- 📖 Complete ALL local verification before loading next step
- 🚫 FORBIDDEN to load step-04 until local tests/lint pass

## CONTEXT BOUNDARIES:

From previous steps:

| Variable          | Description                                       |
| ----------------- | ------------------------------------------------- |
| `{auto_mode}`     | Skip confirmations                                |
| `{error_source}`  | Source of error (github-actions, vercel, netlify) |
| `{error_logs}`    | Captured error logs with details                  |
| `{fixes_applied}` | List to track applied fixes                       |

## YOUR TASK:

Fix the identified errors with minimal changes, then verify locally that ALL tests and linting pass before proceeding. **NO SHORTCUTS.**

---

## EXECUTION SEQUENCE:

### 1. Prepare Local Environment

**Ensure dependencies are installed:**

```bash
npm install 2>/dev/null || yarn install 2>/dev/null || pnpm install 2>/dev/null
```

**Check for running dev servers (if needed for tests):**

```bash
lsof -i :3000 2>/dev/null || lsof -i :8080 2>/dev/null
```

**If tests need a server and none is running:**
Start the server in background:

```bash
bun run dev &
sleep 5  # Wait for server to start
```

### 2. Apply PROPER Fixes Based on Error Type

**For test failures:**

- Read the failing test file
- Read the source file being tested
- **Fix the actual bug in the source code** (not the test, unless test is genuinely wrong)
- If test expectation is wrong, understand WHY before changing it
- Track fix in `{fixes_applied}`

**For lint errors:**

- Run auto-fix first:

```bash
bun run lint -- --fix 2>/dev/null || npx eslint --fix . 2>/dev/null
```

- For remaining errors, **fix the code properly** - don't disable rules
- Track fixes in `{fixes_applied}`

**For type errors:**

- Read the affected files
- **Fix type definitions or implementations properly**
- Add proper type annotations
- Never use `any` or `@ts-ignore`
- Track fixes in `{fixes_applied}`

**For build errors:**

- Check import paths
- Verify dependencies exist
- Fix configuration if needed
- Track fixes in `{fixes_applied}`

**For dependency errors:**

- Understand WHY there's a conflict
- Update package.json with compatible versions
- Regenerate lock file:

```bash
rm -f package-lock.json yarn.lock pnpm-lock.yaml
npm install  # or yarn/pnpm
```

- Track in `{fixes_applied}`

### 3. Local Verification Loop

**This is CRITICAL - loop until ALL checks pass genuinely:**

```
local_verification_passed = false
local_attempts = 0
max_local_attempts = 5

WHILE NOT local_verification_passed AND local_attempts < max_local_attempts:
    local_attempts += 1

    # Step 3a: Run linting (NO --quiet, NO ignoring errors)
    lint_result = RUN: bun run lint

    IF lint_result FAILED:
        → Parse lint errors
        → Fix lint errors PROPERLY (no eslint-disable)
        → CONTINUE LOOP

    # Step 3b: Run type checking (if TypeScript)
    IF project uses TypeScript:
        type_result = RUN: npx tsc --noEmit

        IF type_result FAILED:
            → Parse type errors
            → Fix type errors PROPERLY (no @ts-ignore, no any)
            → CONTINUE LOOP

    # Step 3c: Run ALL tests (no .skip, no --testPathIgnorePatterns)
    test_result = RUN: npm test

    IF test_result FAILED:
        → Parse test failures
        → Fix the SOURCE CODE (not the test assertions, unless test is wrong)
        → CONTINUE LOOP

    # Step 3d: Run build (if applicable)
    IF project has build command:
        build_result = RUN: bun run build

        IF build_result FAILED:
            → Parse build errors
            → Fix build issues PROPERLY
            → CONTINUE LOOP

    # All checks passed GENUINELY!
    local_verification_passed = true
```

### 4. Verification Commands Reference

**Common verification commands (run ALL without skip flags):**

```bash
# Lint - no --quiet, no --max-warnings
bun run lint
npx eslint .
npx prettier --check .

# Type check - strict mode
npx tsc --noEmit
bun run typecheck

# Tests - no .skip, no .only, run everything
npm test
bun run test:ci
npx jest
npx vitest run

# Build - full build
bun run build
npx next build
npx vite build
```

**Run ALL that apply to the project. No shortcuts.**

### 5. Confirm All Checks Pass

**Display verification results:**

```
## Local Verification Results

✅ Lint: Passed (0 errors, 0 warnings)
✅ Type check: Passed (strict mode)
✅ Tests: 42/42 passed (none skipped)
✅ Build: Successful

Fixes applied:
1. Fixed type error in src/utils.ts:45
2. Fixed failing test in tests/api.test.ts
3. Auto-fixed lint issues in 3 files
```

**Set `{local_verified}` = true**

### 6. Handle Verification Failures

**If max local attempts reached:**

Use AskUserQuestion:

```yaml
questions:
  - header: 'Stuck'
    question: "Can't fix these errors properly after 5 attempts. Need your help."
    options:
      - label: 'Keep trying'
        description: 'Continue attempting proper fixes'
      - label: 'Show current errors'
        description: "Display what's still failing"
      - label: 'Stop for manual fix'
        description: "I'll investigate and fix manually"
    multiSelect: false
```

**NEVER suggest using hacks to make it pass. If you can't fix it properly, ask for help.**

---

## SUCCESS METRICS:

✅ All identified errors fixed PROPERLY
✅ Lint passes locally (0 errors, 0 disabled rules)
✅ Type check passes (no @ts-ignore used)
✅ ALL tests pass locally (none skipped)
✅ Build succeeds
✅ `{local_verified}` = true
✅ `{fixes_applied}` contains all changes
✅ **NO HACKS WERE USED**

## FAILURE MODES:

❌ **CRITICAL**: Using ANY hack from the forbidden list
❌ **CRITICAL**: Skipping tests or lint checks
❌ **CRITICAL**: Using --no-verify or skip flags
❌ **CRITICAL**: Disabling lint rules instead of fixing
❌ **CRITICAL**: Using @ts-ignore or any
❌ Committing without local verification
❌ Not tracking fixes applied

## FIX PROTOCOLS:

- Make minimal, targeted changes only
- Don't refactor unrelated code
- Don't add new features while fixing
- Always prefer fixing source over modifying tests (unless test is wrong)
- **NEVER disable checks to make things pass**
- **If you can't fix it properly, ASK FOR HELP**

---

## NEXT STEP:

**Only if `{local_verified}` = true AND no hacks were used:**
Load `./step-04-commit-push.md`

**If verification keeps failing:**
Ask user for help - NEVER use hacks

<critical>
ZERO TOLERANCE FOR HACKS. Everything must genuinely pass with proper fixes. If you can't fix it properly, ask the user for help. Never bypass, skip, or disable anything.
</critical>
