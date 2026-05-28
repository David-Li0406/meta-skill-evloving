---
name: mutation-tester
description: >
  This skill should be used when the user asks to "verify test quality",
  "run mutation testing", "prove tests catch bugs", "check test effectiveness",
  or automatically after the TDD cycle completes in task-executor.
  Mutation testing proves that your tests actually catch bugs by introducing
  deliberate mutations and verifying tests fail.
---

# Mutation Testing Skill

Verify that your tests actually catch bugs by running mutation testing on changed code.

## What is Mutation Testing?

Mutation testing inserts deliberate bugs (mutations) into your code, then runs tests. If tests don't fail, they're not catching that type of bug.

**Example:**
```typescript
// Original code
if (age >= 18) {
  return "adult";
}

// Mutation: >= becomes >
if (age > 18) {
  return "adult";
}
```

If your tests pass on the mutated code, you're missing edge case coverage for `age === 18`.

## When to Run

1. **After TDD GREEN phase** - Verify tests are meaningful
2. **Before integration** - Ensure quality before merge
3. **On critical paths** - Auth, payments, security code
4. **On demand** - When user requests test verification

## Protocol

### Step 1: Check Project Profile

```bash
cat .claude/project-profile.yaml
```

Identify the language/framework to select the right mutation tool.

### Step 2: Identify Changed Files

Only mutate files that changed (incremental testing):

```bash
git diff --name-only HEAD~1 | grep -E '\.(ts|tsx|js|jsx|py|go|rs)$'
```

### Step 3: Run Mutation Testing

Select tool based on language:

| Language | Tool | Command |
|----------|------|---------|
| TypeScript/JS | Stryker | `npx stryker run --mutate 'src/**/*.ts'` |
| Python | mutmut | `mutmut run --paths-to-mutate=src/` |
| Go | go-mutesting | `go-mutesting ./...` |
| Rust | cargo-mutants | `cargo mutants` |

### Step 4: Analyze Results

**Mutation Score = Killed Mutants / Total Mutants**

- **> 80%**: Good - tests are effective
- **60-80%**: Acceptable - consider adding edge case tests
- **< 60%**: Poor - tests are weak, add more coverage

### Step 5: Report Surviving Mutants

For each surviving mutant, explain:
1. What was mutated
2. Why test didn't catch it
3. What test to add

## Configuration

Create `.stryker.conf.json` or configure in `package.json`:

```json
{
  "mutate": ["src/**/*.ts", "!src/**/*.test.ts"],
  "testRunner": "vitest",
  "reporters": ["progress", "clear-text"],
  "coverageAnalysis": "perTest",
  "timeoutMS": 10000
}
```

## Optimization Strategy

**Problem:** Full mutation testing is SLOW (minutes to hours).

**Solution:** Incremental testing on changed lines only.

```yaml
# .claude/auto-config.yaml
mutation_testing:
  enabled: true
  scope: changed_lines_only  # Not full codebase
  minimum_score: 80
  block_on_failure: true
  priority_paths:
    - src/lib/auth/
    - src/lib/payments/
    - src/api/
  skip_patterns:
    - "*.test.ts"
    - "*.spec.ts"
    - "*.d.ts"
```

## Output Format

```markdown
## Mutation Testing Results

**Scope:** src/lib/auth/validate.ts (changed files only)

### Summary
- Mutations generated: 24
- Mutations killed: 21 ✓
- Mutations survived: 3 ⚠️
- **Score: 87.5%** (threshold: 80%) ✅

### Surviving Mutants

#### 1. Boundary Condition (line 45)
```typescript
// Original
if (token.exp > Date.now())

// Mutation (survived)
if (token.exp >= Date.now())
```
**Issue:** No test covers exact expiry boundary
**Fix:** Add test: `test("rejects token at exact expiry time")`

#### 2. Default Value (line 67)
```typescript
// Original
return user?.role ?? 'guest'

// Mutation (survived)
return user?.role ?? 'admin'
```
**Issue:** No test verifies default role
**Fix:** Add test: `test("returns guest role when user.role is undefined")`

#### 3. Off-by-One (line 89)
```typescript
// Original
if (attempts >= MAX_ATTEMPTS)

// Mutation (survived)
if (attempts > MAX_ATTEMPTS)
```
**Issue:** Boundary at MAX_ATTEMPTS not tested
**Fix:** Add test: `test("blocks at exactly MAX_ATTEMPTS")`

### Recommendation
Add 3 edge case tests before proceeding.
Score after fixes (estimated): 100%
```

## Integration with TDD

The TDD cycle becomes:

```
RED → GREEN → REFACTOR → MUTATE → ✓ Done
                           ↓
                  Score < 80%?
                       ↓
                  Add more tests
                       ↓
                  Back to RED
```

## Additional Resources

### Reference Files

- **`references/mutation-operators.md`** - All mutation types explained
- **`references/tools-by-language.md`** - Tool setup for each language

## Quality Standards

**Block if:**
- Score < 80% on critical paths (auth, payments)
- Score < 60% on any changed code
- Security-related mutations survive

**Warn if:**
- Score between 60-80%
- Non-critical mutations survive

**Pass if:**
- Score >= 80%
- All critical path mutations killed

## When NOT to Use This Skill

Do NOT use this skill when:

1. **No mutation testing tool is configured** - Requires Stryker, mutmut, or similar
2. **Tests are not yet written** - Run after TDD GREEN phase, not during RED
3. **Pure UI/styling changes** - Mutation testing is for logic, not visuals
4. **Generated code** - Don't mutate auto-generated files (Prisma clients, etc.)
5. **Time-critical tasks** - Full mutation runs are slow; skip in urgent situations
6. **Configuration files** - Mutation testing is for code logic only
