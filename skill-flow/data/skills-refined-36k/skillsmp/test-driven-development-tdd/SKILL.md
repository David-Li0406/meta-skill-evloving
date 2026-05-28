---
name: Test-Driven Development (TDD)
description: This skill should be used when the user asks to "use TDD", "write tests first", "test-driven", "add a test for", "fix bug with TDD", "implement using TDD", "red-green-refactor", or mentions developing features test-first. Provides guidance for TDD workflow in Ziku with golden tests.
version: 1.1.0
---

# Test-Driven Development for Ziku

Guide Claude through Test-Driven Development (TDD) workflows in the Ziku programming language project. TDD emphasizes writing tests before implementation, following the red-green-refactor cycle to ensure code correctness and maintainability.

## Core Principles

**Test-First Development**: Write failing tests before implementing features.

**Red-Green-Refactor Cycle**:
1. **Red**: Write a failing test that specifies desired behavior
2. **Green**: Write minimal code to make the test pass
3. **Refactor**: Improve code quality while keeping tests passing

**Fast Feedback**: Run tests frequently (after each small change) to catch issues early.

**Regression Protection**: Every bug fix includes a test that would have caught the bug.

## Ziku Test Infrastructure

### Golden Tests

Ziku uses golden tests with automatic baseline generation:

**Test Categories**:
- **parser** (`tests/golden/parser/`): Verify syntax parsing produces correct AST
- **infer** (`tests/golden/infer/`): Verify type inference produces correct types
- **ir-eval** (`tests/golden/ir-eval/`): Verify end-to-end execution (parse → elaborate → translate → evaluate)

**Test Workflow**:
1. Create `.ziku` test file in appropriate category directory
2. Add test name to list in `tests/GoldenTest.lean` (e.g., `parserTests`, `inferTests`, `irEvalTests`)
3. Run `lake test` to auto-generate `.golden` baseline file
4. Subsequent runs compare actual output against `.golden` baseline

**Key Files**:
- `tests/GoldenTest.lean`: Test definitions and test name lists
- `tests/golden/{category}/{name}.ziku`: Test input files
- `tests/golden/{category}/{name}.golden`: Expected output (auto-generated)

## Red-Green-Refactor Workflow

### Red Phase: Write Failing Test

**Objective**: Create a test that fails for the right reason.

**Steps**:
1. Identify the smallest next behavior to implement
2. Create test file: `tests/golden/{category}/{test_name}.ziku`
3. Add `{test_name}` to appropriate list in `tests/GoldenTest.lean`
4. Run `lake test` to verify the test fails
5. Confirm failure message indicates missing implementation (not a test setup error)

**Using Scripts**:
```bash
# Create test file with template
.claude/skills/tdd/scripts/create_test_file.sh parser lambda_curry lambda

# Add test to GoldenTest.lean
.claude/skills/tdd/scripts/add_golden_test.sh parser lambda_curry

# Verify test fails (red)
.claude/skills/tdd/scripts/check_test_status.sh
```

**Red Phase Success Criteria**:
- Test fails with expected error (parse error, type error, wrong value)
- Failure is due to missing implementation, not test bugs
- Test is minimal and focused on one behavior

### Green Phase: Make Test Pass

**Objective**: Write the simplest code to make the test pass.

**Steps**:
1. Implement minimal code in relevant module:
   - Parser tests → Edit `Ziku/Parser.lean`, `Ziku/Lexer.lean`, or `Ziku/Surface/Syntax.lean`
   - Inference tests → Edit `Ziku/Infer.lean` or `Ziku/Type.lean`
   - IR evaluation tests → Edit `Ziku/Translate.lean`, `Ziku/IR/Eval.lean`, or `Ziku/IR/Syntax.lean`
2. Run `lake test` to verify the test now passes
3. Confirm all existing tests still pass (no regressions)

**Implementation Guidelines**:
- Write only enough code to pass the current test
- Resist adding extra features or premature optimization
- If implementation path is unclear, use triangulation (write multiple tests to force the right abstraction)

**Green Phase Success Criteria**:
- New test passes (golden file created if first run)
- All existing tests still pass
- Code compiles without errors

### Refactor Phase: Improve Code Quality

**Objective**: Enhance code structure while maintaining green tests.

**Steps**:
1. Identify code smells: duplication, unclear names, complex logic
2. Refactor incrementally (small changes)
3. Run `lake test` after each refactoring step
4. Ensure all tests remain green throughout
5. Stop when code is clear, simple, and well-structured

**Refactoring Targets**:
- Extract duplicated code into helper functions
- Rename variables/functions for clarity
- Simplify conditional logic
- Improve error messages
- Add documentation for non-obvious behavior

**Refactor Phase Success Criteria**:
- Code is more readable and maintainable
- No duplication or code smells
- All tests still passing
- No new functionality added

## Test-First Feature Development

### Multi-Phase Implementation

For new language features, implement in phases with tests at each level:

**Phase 1: Parser Tests**
- Write parser tests for new syntax
- Implement parsing
- Verify AST structure is correct

**Phase 2: Type Inference Tests**
- Write inference tests for type checking
- Implement type inference rules
- Verify types are inferred correctly

**Phase 3: IR Evaluation Tests**
- Write end-to-end evaluation tests
- Implement translation to IR and evaluation
- Verify execution produces correct results

**Example - Adding New Operator**:
```bash
# Phase 1: Parser
create_test_file.sh parser power_operator
# Add "1 ** 2" to test file
add_golden_test.sh parser power_operator
lake test  # Red
# Implement parsing
lake test  # Green

# Phase 2: Inference
create_test_file.sh infer power_operator
# Add "1 ** 2" with type checking
add_golden_test.sh infer power_operator
lake test  # Red
# Implement type inference
lake test  # Green

# Phase 3: Evaluation
create_test_file.sh ir-eval power_operator
# Add "2 ** 8" expecting 256
add_golden_test.sh ir-eval power_operator
lake test  # Red
# Implement evaluation
lake test  # Green

# Refactor across all phases
```

## Regression Testing for Bugs

### Bug Fix Workflow

**Always follow this sequence**:

1. **Reproduce**: Create test that demonstrates the bug
2. **Red**: Verify test fails with the bug
3. **Fix**: Implement minimal fix
4. **Green**: Verify test passes
5. **Verify**: Check all existing tests still pass
6. **Refactor**: Clean up if needed

**Example**:
```bash
# Bug report: Shadowed variables return wrong value

# 1. Reproduce
cat > tests/golden/ir-eval/shadow_variable_bug.ziku <<'EOF'
let x = 1 in
let x = 2 in
x
EOF

# 2. Add test and verify failure (red)
add_golden_test.sh ir-eval shadow_variable_bug
lake test  # Should output wrong value (1 instead of 2)

# 3. Fix implementation
# Debug and fix in Translate.lean or IR/Eval.lean

# 4. Verify fix (green)
lake test  # Should now output correct value (2)

# 5. Verify no regressions
lake test  # All tests should pass

# 6. Refactor if needed
```

**Test Naming for Bugs**: Use descriptive names that capture the bug:
- `shadow_variable_bug` - variable shadowing issue
- `nested_label_scope` - label scoping problem
- `codata_hash_reference` - hash (#) binding issue

## Utility Scripts

Scripts in `.claude/skills/tdd/scripts/` automate common TDD operations:

### `create_test_file.sh`

Create new test file with optional template.

```bash
./create_test_file.sh <category> <test_name> [template]

# Examples:
create_test_file.sh parser lambda_simple lambda
create_test_file.sh infer type_annotation empty
create_test_file.sh ir-eval factorial_letrec empty

# Templates: empty, lambda, let, match, codata, label
```

### `add_golden_test.sh`

Add test name to appropriate list in GoldenTest.lean.

```bash
./add_golden_test.sh <category> <test_name>

# Examples:
add_golden_test.sh parser lambda_nested
add_golden_test.sh infer let_polymorphic
add_golden_test.sh ir-eval codata_lazy
```

### `check_test_status.sh`

Check test status (red/green state) with clear visual feedback.

```bash
./check_test_status.sh [category] [timeout_seconds]

# Examples:
check_test_status.sh              # All tests, 30s timeout
check_test_status.sh parser       # Just parser tests
check_test_status.sh infer        # Just inference tests
check_test_status.sh all 60       # All tests, 60s timeout

# Output:
# 🔴 RED: Tests failing (exit code 1)
# 🟢 GREEN: All tests passing (exit code 0)
# ⏱️ TIMEOUT: Tests exceeded timeout (exit code 2)
```

## Test Organization Best Practices

### Test Granularity

**Atomic Tests** (Preferred):
- Test one behavior per test
- Small, focused input
- Clear failure messages
- Fast execution

**Example**: Instead of `lambda_all_cases.ziku`, create:
- `lambda_simple.ziku` - Basic lambda
- `lambda_multi_param.ziku` - Multiple parameters
- `lambda_nested.ziku` - Nested lambdas
- `lambda_higher_order.ziku` - Lambda returning lambda

### Test Coverage

**Essential Test Types**:
- **Happy path**: Normal, expected usage
- **Edge cases**: Boundary values (zero, empty, maximum)
- **Error cases**: Invalid input, type mismatches, unbound variables

**For Each Feature, Test**:
1. Basic usage (happy path)
2. With edge case inputs
3. Error conditions
4. Integration with other features

### Test Naming

Use descriptive names that clearly indicate what is being tested:

**Good Names**:
- `lambda_closure` - Tests closure behavior
- `let_shadowing` - Tests variable shadowing
- `codata_hash_binding` - Tests hash (#) in codata
- `label_nested_goto` - Tests nested label/goto

**Bad Names**:
- `test1`, `test2`, `test3` - Non-descriptive
- `complex_case` - Unclear what complexity
- `lambda` - Too generic

## Workflow Integration

### Daily TDD Practice

**Start of Day**: Ensure tests are green
```bash
lake test  # Fix any failures before new work
```

**During Development**: Red-Green-Refactor for each feature
```bash
# For each small feature:
# 1. Red: Write failing test
# 2. Green: Make it pass
# 3. Refactor: Improve code
# 4. Repeat
```

**Before Commit**: Verify all tests pass
```bash
lake test  # Must be green
git commit -m "feat: add feature_name"
```

### Running Tests

**Full Test Suite**:
```bash
lake test  # Run all tests (parser + infer + ir-eval)
```

**Quick Feedback**:
```bash
# Use check_test_status.sh for quick pass/fail
.claude/skills/tdd/scripts/check_test_status.sh

# Or build without running full test suite
lake build
```

**Timeout Handling**:
- Tests have 30-second timeout in `check_test_status.sh`
- For longer-running tests, use `lake test` directly
- Consider adding `timeout 10 lake test` for faster feedback

## Common TDD Mistakes to Avoid

### Mistake 1: Skipping Red Phase

**Problem**: Test passes immediately, not testing new behavior.

**Solution**: Always verify test fails before implementing. The failure confirms the test actually tests new code.

### Mistake 2: Tests Too Large

**Problem**: Test exercises multiple behaviors, unclear what failed.

**Solution**: Split into atomic tests, each focused on one behavior.

### Mistake 3: Ignoring Failing Tests

**Problem**: Accumulates test debt, suite becomes unreliable.

**Solution**: Fix or update failing tests immediately. Never commit with failing tests.

### Mistake 4: No Refactoring

**Problem**: Code becomes messy, hard to maintain.

**Solution**: Refactor after each green phase. Keep code clean continuously.

### Mistake 5: Testing Implementation Details

**Problem**: Tests break during refactoring even though behavior unchanged.

**Solution**: Test observable behavior (outputs, types, values), not internal structure.

## Additional Resources

### Reference Files

For detailed patterns and advanced techniques:

- **`references/tdd-patterns.md`** - Comprehensive TDD patterns, triangulation, test-driven debugging, property-based testing ideas, and Ziku-specific testing strategies

### Example Workflows

Working examples of complete TDD workflows:

- **`examples/workflow-new-feature.md`** - Adding a new `for` loop construct using TDD across all three phases (parser, infer, ir-eval)
- **`examples/workflow-bug-fix.md`** - Fixing a nested label/goto bug with regression test creation

### Scripts

Automation utilities for common TDD operations:

- **`scripts/create_test_file.sh`** - Create test files with templates
- **`scripts/add_golden_test.sh`** - Add tests to GoldenTest.lean
- **`scripts/check_test_status.sh`** - Quick test status check

## Summary

TDD in Ziku follows these core practices:

1. **Write Tests First**: Before implementation, write the test
2. **Red-Green-Refactor**: Follow the cycle strictly
3. **Fast Feedback**: Run tests frequently (after each small change)
4. **Atomic Tests**: One test per behavior
5. **Golden Tests**: Leverage automatic baseline generation
6. **Three Phases**: Parser → Inference → Evaluation for language features
7. **Regression Protection**: Every bug gets a test
8. **Keep Suite Green**: Never commit failing tests
9. **Continuous Refactoring**: Clean code while tests pass
10. **Use Scripts**: Automate repetitive operations

TDD provides confidence in code correctness, prevents regressions, and improves design through test-first thinking. The red-green-refactor cycle creates a sustainable development rhythm with continuous validation.

## Quick Reference

### TDD Cycle

```
Red (failing test) → Green (minimal implementation) → Refactor (improve code) → Repeat
```

### Test Creation Workflow

```bash
# 1. Create test file
create_test_file.sh <category> <name> [template]

# 2. Edit test file with test case
# Edit tests/golden/<category>/<name>.ziku

# 3. Add to test list
add_golden_test.sh <category> <name>

# 4. Run tests (should fail - red)
lake test

# 5. Implement feature
# Edit relevant source files

# 6. Run tests (should pass - green)
lake test

# 7. Refactor
# Improve code while keeping tests green

# 8. Final verification
lake test
```

### Bug Fix Workflow

```bash
# 1. Create reproduction test
create_test_file.sh <category> <bug_name>
# Edit test file to demonstrate bug

# 2. Verify failure (red)
lake test

# 3. Fix bug
# Edit implementation

# 4. Verify fix (green)
lake test

# 5. Commit with test
git commit -m "fix: <bug_name>"
```

Use this skill to maintain high code quality, prevent regressions, and develop features systematically through test-first development in Ziku.
