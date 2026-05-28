---
name: aico-backend-implement
description: |
  Execute backend implementation with TDD (Test-Driven Development). Write failing test first, then implement, verify each step.

  Use this skill when:
  - User asks to "implement this backend task", "implement backend"
  - Have an implementation plan ready and need to execute it
  - Executing steps from /backend.plan output
  - User says "start coding backend", "write backend code"
  - User asks to "use TDD", "write test first", "test-driven" for backend code
  - Fixing backend bugs (write failing test that reproduces bug first)

  TDD Iron Law: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
  TDD Cycle: RED (write failing test) → Verify fails → GREEN (minimal code) → Verify passes → REFACTOR

  Prerequisites:
  - MUST have task file in docs/reference/backend/tasks/ (use /backend.tasks first if not exists)
  - MUST read constraints.md before writing any code.
  Flow: Check Task File → Read Constraints → TDD Cycle (RED→GREEN→REFACTOR) → Verify Each → Run All Tests → Update Task Status → Notify PM
---

# Implement

## Language Configuration

Before generating any content, check `aico.json` in project root for `language` field to determine the output language. If not set, default to English.

## Process

0. **Check task file EXISTS** (MANDATORY):
   - Look for `docs/reference/backend/tasks/{story-id}.md`
   - If NOT exists → STOP and tell user: "Please run /backend.tasks first to break down the story"
   - If exists → proceed to step 1

1. **Read constraints FIRST**: Load `docs/reference/backend/constraints.md`
2. **Execute each step in order**:
   - If test step: write failing test, verify it fails
   - If impl step: write code, verify test passes
   - Run verification command
   - If fail → fix before proceeding
3. **After all steps**:
   - Run full test suite
   - Run type check
   - Run linter
4. **Update task status** in `docs/reference/backend/tasks/{story}.md`
5. **Notify PM for acceptance** - Notify PM to verify (PM checks all related tasks and updates Story status)
6. **Report completion** (user decides when to commit)

## Execution Flow

```
Check Task File → Read Constraints → Execute Steps (TDD) → Verify Each → Run All Tests → Mark Complete → Notify PM
```

## TDD Integration

```
Step N: Write failing test
    ↓ Verify: test fails ❌
Step N+1: Implement code
    ↓ Verify: test passes ✅
```

## Step Execution Rules

### Rule 1: Follow Constraints

```typescript
// ❌ Wrong: Ignore constraints
const password = user.password; // plaintext

// ✅ Right: Follow security constraints
const passwordHash = await bcrypt.hash(password, 10);
```

### Rule 2: Verify Before Proceeding

Each step has a Verify section - MUST run it and confirm expected output.

### Rule 3: Test First (TDD)

```markdown
// ❌ Wrong order
Step 1: Implement createUser method
Step 2: Write test for createUser

// ✅ Correct order
Step 1: Write failing test for createUser
Step 2: Implement createUser method
```

### Rule 4: No Skipping

- Execute ALL steps in order
- Do NOT combine steps
- Do NOT skip verification

## Post-Implementation Checklist

1. **Run full test suite**: `npm test`
2. **Run type check**: `npx tsc --noEmit`
3. **Run linter**: `npm run lint`
4. **Update task status** in tasks file
5. **Notify PM**: Tell PM backend tasks are complete, request acceptance
6. **Report completion** - user decides when to commit

## Error Handling

| Error Type   | Action               |
| ------------ | -------------------- |
| Test failure | Debug, fix, re-run   |
| Type error   | Fix types, re-verify |
| Lint error   | Fix style issues     |

## Key Rules

- ALWAYS read constraints before writing any code
- MUST follow TDD: test first, then implementation
- ALWAYS run verification for each step
- MUST run full test suite before marking complete
- MUST notify PM after completing all tasks (PM handles story verification)
- Let user decide when to commit

## Common Mistakes

- ❌ Implement without task file → ✅ ALWAYS run /backend.tasks first to break down story
- ❌ Skip reading constraints → ✅ ALWAYS read before coding
- ❌ Write code before test → ✅ TDD: test first
- ❌ Skip verification → ✅ Run verify command for each step
- ❌ Skip full test suite → ✅ Run all tests before complete
- ❌ Directly update story status → ✅ Notify PM, let PM verify and update story

---

## TDD Deep Dive

### The TDD Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? **Delete it. Start over.**

### Red-Green-Refactor Cycle

```
RED → Verify Fails → GREEN → Verify Passes → REFACTOR → Repeat
```

#### 1. RED - Write Failing Test

Write ONE minimal test showing expected behavior:

```typescript
test('createUser hashes password before storing', async () => {
  const user = await userService.createUser({
    email: 'test@example.com',
    password: 'plaintext123',
  });

  expect(user.passwordHash).not.toBe('plaintext123');
  expect(await bcrypt.compare('plaintext123', user.passwordHash)).toBe(true);
});
```

#### 2. Verify RED - Watch It Fail

**MANDATORY. Never skip.**

```bash
npm test path/to/test.ts
```

#### 3. GREEN - Write Minimal Code

Write simplest code to pass the test. **Don't add features not in test.**

#### 4. Verify GREEN - Watch It Pass

```bash
npm test path/to/test.ts
```

#### 5. REFACTOR - Clean Up

Only after green. Keep tests passing.

### Test Types

| Type        | Purpose         | Example                          |
| ----------- | --------------- | -------------------------------- |
| Unit        | Single function | `authService.validatePassword()` |
| Integration | With real DB    | `userRepository.create()`        |
| API         | HTTP endpoints  | `POST /auth/register`            |

### TDD Red Flags - STOP and Start Over

- Code before test
- Test passes immediately
- Can't explain why test failed
- Rationalizing "just this once"

---

## Iron Law

**NO CODE WITHOUT APPROVED PLAN**

This rule is non-negotiable. Before writing code:

1. Task breakdown must exist and be approved
2. Acceptance criteria must be defined
3. Dependencies must be identified and available

### Rationalization Defense

| Excuse                         | Reality                                     |
| ------------------------------ | ------------------------------------------- |
| "It's a simple change"         | Simple changes often have hidden complexity |
| "I'll document after coding"   | Post-hoc documentation is always incomplete |
| "Tests can wait until later"   | Untested code is broken code                |
| "I know what needs to be done" | Assumptions without validation cause bugs   |
