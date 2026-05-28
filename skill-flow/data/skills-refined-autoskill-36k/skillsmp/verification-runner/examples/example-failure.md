# Example: Verification Failure

## Scenario
Type check fails with 3 errors.

## Verification Output

```
Running Verification Pipeline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Step 1: Type Check
$ npm run typecheck
✗ FAIL (2.3s)

Errors detected:
src/components/UserForm.tsx:15:5
  error TS2322: Type 'string' is not assignable to type 'number'.
    15 |     const age: number = userData.age;
       |     ~~~

src/components/UserForm.tsx:28:3
  error TS2345: Argument of type 'User' is not assignable to parameter of type 'UserInput'.
    28 |   submitUser(user);
       |   ~~~~~~~~~~~~~~~~

src/utils/format.ts:8:1
  error TS7006: Parameter 'x' implicitly has an 'any' type.
     8 | function format(x) {
       | ^

Found 3 errors in 2 files.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Verification Results:
  Typecheck: ❌ FAILED (3 errors)
  Lint:      ⏭️ skipped (blocked by typecheck)
  Tests:     ⏭️ skipped (blocked by typecheck)
  Build:     ⏭️ skipped (blocked by typecheck)

Status: FAILED - Fix type errors before proceeding
```

## Filtered Output (Anthropic Best Practice)

Instead of full error output (~300 tokens), filtered (~100 tokens):

```
✗ VERIFICATION FAILED
─────────────────────
src/components/UserForm.tsx:15:5
  TS2322: Type 'string' not assignable to 'number'

src/components/UserForm.tsx:28:3
  TS2345: 'User' not assignable to 'UserInput'

src/utils/format.ts:8:1
  TS7006: Parameter 'x' has 'any' type
─────────────────────
Found 3 errors in 2 files
Exit code: 1
```

## What NOT to Include

❌ Do NOT include:
- Full stack traces
- All 50 lines of output
- AST details
- Node module paths
- Timing breakdowns per file

## Recovery Action

```
1. Fix UserForm.tsx:15 - parse userData.age to number
2. Fix UserForm.tsx:28 - update User type or use UserInput
3. Fix format.ts:8 - add explicit type annotation
4. Re-run verification
```
