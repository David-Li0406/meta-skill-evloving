---
name: verification-runner
description: >
  This skill should be used when the user asks to "run verification",
  "check if code passes", "run tests and lint", "verify implementation",
  or after code changes in autonomous mode.
  Runs typecheck, lint, test, and build in optimal order for fast feedback.
---

# Verification Runner Skill

Execute the project verification pipeline in optimal order to catch errors early.

## Verification Order

Run checks in this sequence for fastest feedback:

| Order | Check | Rationale |
|-------|-------|-----------|
| 1 | Typecheck | Fastest, catches most errors |
| 2 | Lint | Fast, catches style issues |
| 3 | Test | Slower, catches logic errors |
| 4 | Build | Slowest, catches bundling issues |

## Protocol

### Step 1: Load Project Profile

Read `.claude/project-profile.yaml` to get verification commands:
```yaml
commands:
  typecheck: "npm run typecheck"
  lint: "npm run lint"
  test: "npm test"
  build: "npm run build"
verification:
  required: ["test", "lint", "typecheck"]
  optional: ["build"]
```

### Step 2: Determine What to Run

Execute verifications based on configuration:
- **Required** - Must pass before marking complete
- **Optional** - Run but don't block on failure

### Step 3: Execute in Order

Run each verification command, stopping on first failure for required checks.

### Step 4: Handle Failures

For each failure type:

| Failure | Action |
|---------|--------|
| Typecheck | Fix type errors, retry |
| Lint | Auto-fix if possible, otherwise fix manually, retry |
| Test | Analyze failure, fix logic, retry |
| Build | Analyze error, fix configuration, retry |

### Step 5: Report Results

Present verification summary:
```
Verification Results:
  Typecheck: passed
  Lint: passed (2 auto-fixed)
  Tests: 42 passed, 0 failed
  Build: success
```

## Result Filtering Protocol (REQUIRED)

**Anthropic Best Practice: Result filtering reduces token usage by 40%+**

### When to Filter Output

ALWAYS filter verification output to minimize context consumption:

| Scenario | Action | Token Budget |
|----------|--------|--------------|
| All checks pass | Summary only | ~50 tokens |
| Check fails | Error lines only | ~200 tokens |
| Multiple failures | First failure + count | ~300 tokens |

### What to NEVER Include

These outputs waste tokens and should NEVER be in the model context:

- ❌ **Stack traces > 10 lines** - Include first 5 lines only
- ❌ **Coverage reports** - Just include pass/fail summary
- ❌ **Timing breakdowns** - Total time only
- ❌ **Verbose logs** - Error messages only
- ❌ **Full test lists** - Failed tests only
- ❌ **Dependency installation logs** - Skip entirely
- ❌ **Progress indicators** - Skip dots, spinners, bars

### Success Output Format (~50 tokens)

```
✓ VERIFICATION PASSED
─────────────────────
Tests: 42 passed, 0 failed
Time: 3.2s
─────────────────────
Exit code: 0
```

### Failure Output Format (~200 tokens)

```
✗ VERIFICATION FAILED
─────────────────────
src/components/Button.tsx:15:3
  error TS2322: Type 'string' is not assignable to type 'number'

src/utils/format.ts:8:1
  error TS7006: Parameter 'x' implicitly has an 'any' type

─────────────────────
Summary: Found 2 errors
Exit code: 1
```

### Using the Filter Script

Use the filter script for all verification commands:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/filter-verification-output.sh "npm test"
${CLAUDE_PLUGIN_ROOT}/scripts/filter-verification-output.sh "npm run typecheck"
```

The script automatically:
- Captures full output
- Extracts summary for success
- Extracts error lines for failure
- Limits output to token budgets

### Implementation in Agents

When running verification in agents:

```bash
# Instead of:
npm test

# Use:
./scripts/filter-verification-output.sh "npm test"

# Or inline filtering:
npm test 2>&1 | head -30  # Limit to 30 lines max
```

## Smart Test Optimization

For Jest/Vitest projects with `--changedSince` support:

1. Run tests only for changed files first:
   ```bash
   npm test -- --changedSince=HEAD~1
   ```

2. If changed tests pass, run full suite
3. This saves significant time on large test suites

## Additional Resources

### Reference Files

For detailed verification commands:
- **`references/verification-commands.md`** - Complete commands for JS/TS, Python, Go, Rust projects

## Script Reference

Execute verification directly:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/run-verification.sh [mode]
```

Modes:
- `all` - Run all verifications
- `required` - Run only required verifications
- `test` / `lint` / etc. - Run specific verification

## When NOT to Use This Skill

Do NOT use this skill when:

1. **No project profile exists** - Run project-detector first
2. **No verification commands configured** - Profile missing commands
3. **User explicitly skips verification** - Respect user choice
4. **Research/audit tasks** - Verification is for implementation only
5. **Configuration-only changes** - Config changes don't need full test suite

## Quality Standards

1. **ALWAYS** run verifications in order: typecheck → lint → test → build
2. **ALWAYS** stop on first required check failure
3. **ALWAYS** attempt auto-fix for lint errors before failing
4. **NEVER** mark task complete if required checks fail
5. **ALWAYS** report clear summary of all verification results
6. **PRIORITIZE** using `--changedSince` for faster test runs when available
