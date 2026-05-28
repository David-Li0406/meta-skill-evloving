---
name: test-driven-development
description: Use this skill for implementing Test-Driven Development (TDD) workflows for all code changes, including features, bug fixes, and refactoring.
---

# Test-Driven Development

TDD is the fundamental practice where every line of production code must be written in response to a failing test. 

**For how to write good tests**, refer to the `testing` skill.

---

## RED-GREEN-REFACTOR Cycle

### RED: Write Failing Test First
- NO production code until you have a failing test.
- The test should describe desired behavior, not implementation.
- Ensure the test fails for the right reason.

### GREEN: Minimum Code to Pass
- Write ONLY enough code to make the test pass.
- Resist adding functionality not demanded by a test.
- Commit immediately after achieving green.

### REFACTOR: Assess Improvements
- Assess improvements AFTER every green (only refactor if it adds value).
- Commit before refactoring.
- Ensure all tests pass after refactoring.

---

## TDD Evidence in Commit History

### Default Expectation
Commit history should show a clear RED → GREEN → REFACTOR progression.

**Ideal progression:**
```
commit abc123: test: add failing test for user authentication
commit def456: feat: implement user authentication to pass test
commit ghi789: refactor: extract validation logic for clarity
```

### Rare Exceptions
TDD evidence may not be linearly visible in commits in certain cases:

1. **Multi-Session Work**: Feature spans multiple development sessions with TDD applied in each.
2. **Context Continuation**: Resuming from previous work where the original RED phase was completed earlier.
3. **Refactoring Commits**: Large refactors after GREEN or multiple small refactors combined into a single commit.

### Documenting Exceptions in PRs
When exceptions apply, document in the PR description:

```markdown
## TDD Evidence

RED phase: commit c925187 (added failing tests for shopping cart)
GREEN phase: commits 5e0055b, 9a246d0 (implementation + bug fixes)
REFACTOR: commit 11dbd1a (test isolation improvements)

Test Evidence:
✅ 4/4 tests passing (7.7s with 4 workers)
```

---

## Coverage Verification - CRITICAL

### NEVER Trust Coverage Claims Without Verification
**Always run coverage yourself before approving PRs.**

### Verification Process
**Before approving any PR claiming "100% coverage":**
1. Check out the branch:
   ```bash
   git checkout <feature-branch>
   ```
2. Run coverage verification:
   ```bash
   cd <package-directory>
   pnpm test:coverage
   ```
3. Verify ALL metrics hit 100%:
   - Lines: 100% ✅
   - Statements: 100% ✅
   - Branches: 100% ✅
   - Functions: 100% ✅

4. Ensure tests are behavior-driven (not testing implementation details).

### Red Flags
Watch for signs of incomplete coverage:
- PR claims "100% coverage" but not verified.
- Coverage summary shows <100% on any metric.
- "Uncovered Line #s" column shows line numbers.
- Coverage gaps without explicit exception documentation.

### When Coverage Drops, Ask
**"What business behavior am I not testing?"** 

---

## 100% Coverage Exception Process

### Default Rule: 100% Coverage Required
No exceptions without explicit approval and documentation.

### Requesting an Exception
If 100% coverage cannot be achieved:
1. Document in package README explaining current coverage metrics and reasons for missing coverage.
2. Get explicit approval from project maintainer or team lead.
3. Document in CLAUDE.md under "Test Coverage: 100% Required" section.

---

## Development Workflow

### Adding a New Feature
1. **Write failing test** - describe expected behavior.
2. **Run test** - confirm it fails.
3. **Implement minimum** - just enough to pass.
4. **Run test** - confirm it passes.
5. **Refactor if valuable** - improve code structure.
6. **Commit** - with conventional commit message.

### Workflow Example
```bash
# 1. Write failing test
it('should reject empty user names', () => {
  const result = createUser({ id: 'user-123', name: '' });
  expect(result.success).toBe(false);
}); # ❌ Test fails (no implementation)

# 2. Implement minimum code
if (user.name === '') {
  return { success: false, error: 'Name required' };
} # ✅ Test passes

# 3. Refactor if needed (extract validation, improve naming)

# 4. Commit
git add .
git commit -m "feat: reject empty user names"
```

---

## Commit Messages
Use conventional commits format:
```
feat: add user role-based permissions
fix: correct email validation regex
refactor: extract user validation logic
test: add edge cases for permission checks
docs: update architecture documentation
```

---

## Pull Request Requirements
Before submitting PR:
- [ ] All tests must pass.
- [ ] All linting and type checks must pass.
- [ ] **Coverage verification REQUIRED** - claims must be verified before review/approval.
- [ ] PRs focused on single feature or fix.
- [ ] Include behavior description (not implementation details).

---

## Refactoring Priority
After green, classify any issues:
| Priority | Action | Examples |
|----------|--------|----------|
| Critical | Fix now | Mutations, knowledge duplication, >3 levels nesting |
| High | This session | Magic numbers, unclear names, >30 line functions |
| Nice | Later | Minor naming, single-use helpers |
| Skip | Don't change | Already clean code |

---

## Anti-Patterns to Avoid
- ❌ Writing production code without failing test.
- ❌ Testing implementation details.
- ❌ 1:1 mapping between test files and implementation files.
- ❌ Trusting coverage claims without verification.

---

## Summary Checklist
Before marking work complete:
- [ ] Every production code line has a failing test that demanded it.
- [ ] Commit history shows TDD evidence (or documented exception).
- [ ] All tests pass.
- [ ] Coverage verified at 100% (or exception documented).
- [ ] Tests verify behavior (not implementation details).
- [ ] Refactoring assessed and applied if valuable.
- [ ] Conventional commit messages used.