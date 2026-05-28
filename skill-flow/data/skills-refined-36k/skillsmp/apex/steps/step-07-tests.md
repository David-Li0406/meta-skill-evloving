---
name: step-07-tests
description: Smart test analysis and creation - analyze patterns, create appropriate tests
prev_step: steps/step-04-validate.md
next_step: steps/step-08-run-tests.md
---

# Step 7: Tests (Analysis & Creation)

## MANDATORY EXECUTION RULES (READ FIRST):

- 🛑 NEVER create tests without analyzing existing patterns first
- 🛑 NEVER use wrong test type (unit when integration needed)
- ✅ ALWAYS analyze test infrastructure BEFORE writing
- ✅ ALWAYS follow existing test conventions exactly
- ✅ ALWAYS map tests to acceptance criteria
- 📋 YOU ARE A TEST ENGINEER, not a code generator
- 💬 FOCUS on "What tests does this ACTUALLY need?"
- 🚫 FORBIDDEN to ignore project test conventions

## EXECUTION PROTOCOLS:

- 🎯 Analyze test infrastructure first
- 💾 Document test strategy (if save_mode)
- 📖 Read similar tests before writing
- 🚫 FORBIDDEN to write tests without reading examples

## CONTEXT BOUNDARIES:

- Implementation is complete and validated
- Test infrastructure exists (discovered in this step)
- Existing tests show conventions to follow
- Focus on creating RIGHT tests, not just tests

## YOUR TASK:

Analyze existing test patterns and create appropriate tests for the implementation.

---

<available_state>
From previous steps:

| Variable             | Description                   |
| -------------------- | ----------------------------- |
| `{task_description}` | What was implemented          |
| `{task_id}`          | Kebab-case identifier         |
| `{auto_mode}`        | Skip confirmations            |
| `{save_mode}`        | Save outputs to files         |
| `{economy_mode}`     | Lighter test analysis         |
| `{output_dir}`       | Path to output (if save_mode) |
| Files modified       | From implementation           |
| Acceptance criteria  | From step-01                  |

</available_state>

---

## EXECUTION SEQUENCE:

### 1. Initialize Save Output (if save_mode)

**If `{save_mode}` = true:**

```bash
bash {skill_dir}/scripts/update-progress.sh "{task_id}" "07" "tests" "in_progress"
```

Append analysis to `{output_dir}/07-tests.md` as you work.

### 2. Analyze Test Infrastructure

**2.1 Discover Framework**

```bash
cat package.json | grep -E "(jest|vitest|mocha|playwright|testing-library)"
```

**2.2 Find Config**

```bash
ls -la | grep -E "(jest|vitest|playwright)"
```

**2.3 Find Test Commands**

```bash
cat package.json | grep -A 5 '"scripts"' | grep -E "(test|spec)"
```

### 3. Analyze Existing Test Patterns

**If `{economy_mode}` = true:**
→ Read 1 similar test file for patterns

**If `{economy_mode}` = false:**
→ Read 2-3 similar test files

**Pattern Checklist:**

- [ ] describe/it vs test() syntax
- [ ] Setup/teardown patterns
- [ ] Mocking approach
- [ ] Assertion style
- [ ] Test data approach

### 4. Determine Test Strategy

| Implementation Type | Test Type                        |
| ------------------- | -------------------------------- |
| API Route           | Integration with supertest/fetch |
| Service/Logic       | Integration with real deps       |
| Utility Function    | Unit with mocks                  |
| React Component     | Component with testing-library   |
| Full Feature        | Integration + E2E                |

### 5. Create Test Plan

```markdown
## Test Plan

**Framework:** {jest/vitest}
**Command:** `pnpm test`

### Tests to Create

**Integration:** `src/auth/register.test.ts`

- creates user with valid data (happy path)
- rejects invalid email (error case)
- handles auth failure (error case)

**Unit:** `src/utils/validation.test.ts`

- validates correct email
- rejects malformed email
```

**If `{auto_mode}` = false:**

```yaml
questions:
  - header: 'Tests'
    question: 'Review the test plan. Ready to create tests?'
    options:
      - label: 'Create tests (Recommended)'
        description: 'Proceed with planned tests'
      - label: 'Add more tests'
        description: 'I want additional test cases'
      - label: 'Modify approach'
        description: 'Change the strategy'
      - label: 'Skip tests'
        description: "Don't create tests"
    multiSelect: false
```

### 6. Create Tests

**CRITICAL: Follow existing patterns EXACTLY**

1. Read similar test for reference
2. Create test file matching structure
3. Write tests following conventions

```typescript
import { describe, it, expect, beforeEach } from 'vitest'

describe('POST /api/auth/register', () => {
  beforeEach(async () => {
    await db.user.deleteMany()
  })

  it('creates user with valid data', async () => {
    const response = await client.post('/api/auth/register', {
      email: 'test@example.com',
      password: 'SecurePass123!'
    })

    expect(response.status).toBe(201)
  })

  it('rejects invalid email', async () => {
    const response = await client.post('/api/auth/register', {
      email: 'invalid',
      password: 'SecurePass123!'
    })

    expect(response.status).toBe(400)
  })
})
```

### 7. Verify Tests

```bash
pnpm typecheck
```

List created tests:

```
**Tests Created:**
- `src/auth/register.test.ts` (3 tests)
- `src/utils/validation.test.ts` (2 tests)
```

### 8. Complete Save Output (if save_mode)

**If `{save_mode}` = true:**

Append to `{output_dir}/07-tests.md`:

```markdown
---

## Step Complete

**Status:** ✓ Complete
**Tests created:** {count}
**Test files:** {list}
**Next:** step-08-run-tests.md
**Timestamp:** {ISO timestamp}
```

---

## SUCCESS METRICS:

✅ Test infrastructure analyzed
✅ Existing patterns studied
✅ Appropriate test types chosen
✅ Tests follow codebase conventions
✅ Tests pass syntax check
✅ All AC have corresponding tests

## FAILURE MODES:

❌ Writing tests without analyzing patterns
❌ Wrong test type for implementation
❌ Ignoring project conventions
❌ Tests don't match acceptance criteria
❌ Over-testing (testing implementation, not behavior)
❌ **CRITICAL**: Not using AskUserQuestion for approval

## TEST PROTOCOLS:

- Analyze BEFORE writing
- Follow existing patterns EXACTLY
- Test behavior, not implementation
- Map to acceptance criteria
- Create minimal, focused tests

---

## NEXT STEP:

After tests created, load `./step-08-run-tests.md`

<critical>
Remember: Create the RIGHT tests - analyze patterns first, then write!
</critical>
