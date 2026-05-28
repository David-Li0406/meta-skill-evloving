# TDD Patterns for Ziku

This document provides detailed patterns and techniques for Test-Driven Development in the Ziku project.

## Red-Green-Refactor Cycle

### Red Phase: Write a Failing Test

**Goal**: Write the simplest test that fails for the right reason.

**Steps**:
1. Identify the next smallest behavior to implement
2. Write a test that exercises that behavior
3. Run tests to confirm the test fails (red)
4. Verify the failure message is meaningful

**Example - Adding new operator**:
```bash
# 1. Create test file
echo "1 ** 2" > tests/golden/parser/power_operator.ziku

# 2. Add to GoldenTest.lean
# Add "power_operator" to parserTests list

# 3. Run tests - should fail with parse error
lake test
# Expected: Parse error or missing golden file
```

**Common Red Phase Mistakes**:
- Test passes immediately (not testing new behavior)
- Test fails for wrong reason (setup error, not missing implementation)
- Test is too large (testing multiple behaviors)

### Green Phase: Make Test Pass

**Goal**: Write the minimal code to make the test pass.

**Steps**:
1. Implement the simplest code that makes the test pass
2. Don't add extra features or optimize prematurely
3. Run tests to confirm the test passes (green)
4. All previous tests must still pass

**Example - Implementing the operator**:
```lean
-- In Parser.lean or Lexer.lean
-- Add minimal parsing support for **
-- Don't worry about evaluation yet if it's just a parser test

-- Run tests
lake test
-- Expected: Test passes, golden file created
```

**Green Phase Guidelines**:
- Fake it till you make it (hardcode if needed for first test)
- Use obvious implementation for simple cases
- Triangulate with multiple tests for complex cases

### Refactor Phase: Improve Code

**Goal**: Improve code quality while keeping tests green.

**Steps**:
1. Identify code smells or duplication
2. Refactor incrementally
3. Run tests after each small refactor
4. Tests must stay green throughout

**Example - Refactor operator handling**:
```lean
-- Before: Each operator has its own parsing function
-- After: Generic binary operator parsing with precedence table

-- Run tests after each change
lake test
```

**Refactoring Patterns**:
- Extract common patterns into functions
- Rename variables/functions for clarity
- Simplify conditional logic
- Remove duplication

**When to Stop Refactoring**:
- Code is clear and readable
- No obvious duplication
- Tests still pass
- Ready for next feature

## Test-First Feature Development

### Feature: Add New Language Construct

**Workflow**:
1. Write parser tests for syntax
2. Implement parser (green)
3. Write type inference tests
4. Implement type inference (green)
5. Write IR evaluation tests
6. Implement IR evaluation (green)
7. Refactor across all phases

**Example - Adding `while` loop**:

**Phase 1: Parser Tests**
```bash
# Red
cat > tests/golden/parser/while_simple.ziku <<EOF
while x > 0 do
  x - 1
EOF

# Add "while_simple" to parserTests in GoldenTest.lean
lake test  # Should fail - parse error

# Green - Implement parser for while
# Edit Parser.lean to add while parsing

lake test  # Should pass - golden created
```

**Phase 2: Type Inference Tests**
```bash
# Red
cat > tests/golden/infer/while_simple.ziku <<EOF
let x = 10 in
while x > 0 do
  x - 1
EOF

# Add "while_simple" to inferTests
lake test  # Should fail

# Green - Implement type inference
# Edit Infer.lean to handle while

lake test  # Should pass
```

**Phase 3: IR Evaluation Tests**
```bash
# Red
cat > tests/golden/ir-eval/while_countdown.ziku <<EOF
let x = 5 in
while x > 0 do
  x - 1
EOF

# Add "while_countdown" to irEvalTests
lake test  # Should fail or return wrong value

# Green - Implement translation and evaluation
# Edit Translate.lean and IR/Eval.lean

lake test  # Should pass with correct value
```

### Feature: Modify Existing Behavior

**Workflow**:
1. Add characterization tests for current behavior
2. Add tests for desired new behavior (red)
3. Modify implementation (green)
4. Verify old tests still pass or update if behavior intentionally changed
5. Refactor

**Example - Changing operator precedence**:
```bash
# 1. Add test for current behavior (documents existing)
cat > tests/golden/parser/precedence_current.ziku <<EOF
1 + 2 * 3
EOF
lake test  # Creates baseline

# 2. Add test for new behavior
cat > tests/golden/parser/precedence_new.ziku <<EOF
# Should parse as 1 + (2 * 3), not (1 + 2) * 3
1 + 2 * 3 == 7
EOF
lake test  # May fail if precedence is wrong

# 3. Fix implementation
# Edit Parser.lean to adjust precedence

# 4. Verify all tests
lake test  # All should pass
```

## Regression Testing

### Bug Fix Workflow

**Always follow this order**:
1. **Reproduce**: Write test that demonstrates the bug
2. **Red**: Confirm test fails
3. **Fix**: Implement minimal fix
4. **Green**: Confirm test passes
5. **Verify**: Check related tests still pass
6. **Refactor**: Clean up if needed

**Example - Fix evaluation bug**:
```bash
# User reports: "let x = 1 in let x = 2 in x" returns 1 instead of 2

# 1. Reproduce with test
cat > tests/golden/ir-eval/shadow_binding.ziku <<EOF
let x = 1 in
let x = 2 in
x
EOF

# 2. Add to irEvalTests and run (red)
lake test
# Expected output: 2
# Actual output: 1

# 3. Fix the bug in IR/Eval.lean or Translate.lean
# Debug to find shadowing issue

# 4. Run tests (green)
lake test
# Expected and actual now match

# 5. Verify no regressions
lake test  # All tests should pass

# 6. Refactor if needed
```

### Regression Test Naming

Use descriptive names that capture the bug:
- `shadow_binding` - shadowed variables
- `nested_goto_scope` - goto with nested labels
- `codata_hash_binding` - hash (#) in codata
- `negative_literal_precedence` - negative numbers in expressions

**Good**: `tests/golden/ir-eval/recursive_codata_loop.ziku`
**Bad**: `tests/golden/ir-eval/test123.ziku`

## Test Organization

### Test Categories

**Parser Tests** (`tests/golden/parser/`)
- **Purpose**: Verify syntax parsing produces correct AST
- **Scope**: Syntax only, no semantics
- **Output**: AST structure as string
- **When to add**: New syntax, syntax edge cases

**Inference Tests** (`tests/golden/infer/`)
- **Purpose**: Verify type inference produces correct types
- **Scope**: Type checking and inference
- **Output**: Inferred type or type error
- **When to add**: New type rules, polymorphism, type errors

**IR Evaluation Tests** (`tests/golden/ir-eval/`)
- **Purpose**: Verify end-to-end execution produces correct values
- **Scope**: Parse → Elaborate → Translate → Evaluate
- **Output**: Final computed value
- **When to add**: Semantic changes, execution behavior

### Test Granularity

**Atomic Tests** (Preferred)
- Test one thing
- Small, focused input
- Clear failure message
- Fast execution

**Example**:
```bash
# Good - atomic
tests/golden/parser/lambda_simple.ziku        # \x -> x
tests/golden/parser/lambda_multi_param.ziku   # \x y -> x + y
tests/golden/parser/lambda_nested.ziku        # \x -> \y -> x + y

# Bad - combined
tests/golden/parser/lambda_all_cases.ziku     # Multiple lambda forms in one file
```

**Integration Tests** (Sparingly)
- Test interaction of multiple features
- Larger, realistic examples
- Slower execution
- Use when interactions are critical

### Test Data Patterns

**Boundary Values**:
- Zero, negative, positive
- Empty, single, multiple
- Minimum, maximum values

**Equivalence Classes**:
- Group similar inputs
- Test one from each class
- Example: literals → test int, bool, string, unit

**Error Cases**:
- Invalid syntax
- Type mismatches
- Unbound variables
- Division by zero

## Advanced TDD Techniques

### Triangulation

When implementation path is unclear, write multiple tests that force the right abstraction.

**Example - Implementing operator precedence**:
```bash
# Test 1: Forces recognition that * binds tighter than +
echo "1 + 2 * 3" > tests/golden/parser/precedence_mul_add.ziku

# Test 2: Forces recognition that operators of same precedence are left-associative
echo "1 + 2 + 3" > tests/golden/parser/precedence_add_left.ziku

# Test 3: Forces recognition of parentheses override
echo "(1 + 2) * 3" > tests/golden/parser/precedence_parens.ziku

# Implementation must satisfy all three
```

### Test-Driven Debugging

**For Hard-to-Reproduce Bugs**:
1. Create minimal test that reproduces bug
2. Add intermediate assertions/traces
3. Binary search for failure point
4. Fix and verify

**Example**:
```lean
-- Bug: Complex nested expression fails

-- Step 1: Minimal reproduction
-- tests/golden/ir-eval/nested_let_bug.ziku
let a = 1 in let b = 2 in let c = 3 in a + b + c

-- Step 2: Add tracing in IR/Eval.lean
-- dbg_trace s!"Evaluating: {stmt}"

-- Step 3: Identify failure point
-- Step 4: Fix
-- Step 5: Remove tracing, verify test passes
```

### Test-Driven Refactoring

**For Large Refactorings**:
1. Ensure comprehensive test coverage first
2. Refactor incrementally
3. Run tests after each step
4. Commit each green state

**Example - Refactor Parser**:
```bash
# 1. Check test coverage
lake test  # All green

# 2. Extract common pattern (e.g., binary operators)
# Edit Parser.lean

lake test  # Should still be green

# 3. Continue refactoring
# Each refactor step

lake test  # Keep checking

# 4. Commit when done
git commit -m "refactor(parser): extract binary operator parsing"
```

### Property-Based Testing

While Ziku currently uses golden tests, property-based testing can complement:

**Properties to Test**:
- **Parsing**: `parse(print(ast)) == ast` (round-trip)
- **Type inference**: Type of expression is consistent
- **Evaluation**: Equivalent expressions produce same value
- **Translation**: IR evaluation matches surface evaluation

**Note**: Requires additional testing framework (e.g., LeanCheck). Consider for future.

## Common TDD Mistakes

### Mistake 1: Tests Too Large

**Problem**: Test exercises multiple behaviors, hard to understand failure.

**Solution**: Split into atomic tests, each testing one thing.

```bash
# Bad
tests/golden/ir-eval/all_features.ziku  # Tests lambda + let + match + codata

# Good
tests/golden/ir-eval/lambda_closure.ziku
tests/golden/ir-eval/let_shadowing.ziku
tests/golden/ir-eval/match_pattern.ziku
tests/golden/ir-eval/codata_lazy.ziku
```

### Mistake 2: Skipping Red Phase

**Problem**: Test passes immediately, not testing new code.

**Solution**: Always verify test fails before implementing.

```bash
# Wrong
create_test_file.sh parser new_feature
# (Implement feature immediately)
lake test  # Passes - but did it test the right thing?

# Right
create_test_file.sh parser new_feature
lake test  # Should fail or error
# (Now implement)
lake test  # Should pass
```

### Mistake 3: Testing Implementation Details

**Problem**: Tests break when refactoring, even though behavior is unchanged.

**Solution**: Test behavior through public interface, not internal structure.

```lean
-- Bad: Tests internal AST structure details
-- Test expects specific constructor ordering

-- Good: Tests observable behavior
-- Test expects correct evaluation result
```

### Mistake 4: Ignoring Failing Tests

**Problem**: Tests fail, continue coding anyway, accumulates test debt.

**Solution**: Fix or update tests immediately, always keep suite green.

```bash
# Wrong
lake test  # 3 tests failing
# "I'll fix them later"
# (Continues coding)

# Right
lake test  # 3 tests failing
# Fix each failing test immediately
# Or update test if behavior intentionally changed
lake test  # All green before continuing
```

### Mistake 5: No Refactor Phase

**Problem**: Code becomes messy, duplication grows, hard to maintain.

**Solution**: Refactor while tests are green, keep code clean.

```bash
# After implementing 3 similar features:
lake test  # All green

# Notice duplication in Parser.lean
# Refactor to extract common pattern
lake test  # Still green

# Continue with clean code
```

## Ziku-Specific Patterns

### Testing Surface vs IR

**Surface Tests** (`Eval.lean`):
- Use when testing surface language semantics directly
- Faster feedback for surface language features
- Example: Variable scoping in surface let-bindings

**IR Tests** (`IR/Eval.lean`):
- Use when testing full pipeline (elaborate + translate + eval)
- Verifies translation is correct
- Example: Codata translation to IR cocase

**Both**:
- Critical features should have both
- Surface test: Fast feedback
- IR test: Verifies complete pipeline

### Testing Codata

**Key aspects to test**:
1. **Copattern matching**: Each copattern case
2. **Hash binding**: `#` refers to the codata object
3. **Lazy evaluation**: Codata fields evaluated on demand
4. **Translation**: Codata → IR cocase

**Example test sequence**:
```bash
# Parser: Syntax correct
tests/golden/parser/codata_hash.ziku

# Infer: Type inference for codata
tests/golden/infer/codata_field.ziku

# IR-Eval: Full execution
tests/golden/ir-eval/codata_lazy.ziku
```

### Testing Label/Goto

**Key aspects**:
1. **Control flow**: Jump works correctly
2. **Scope**: Label scope is correct
3. **Value passing**: Value passed to label
4. **Nesting**: Nested labels work

**Test organization**:
```bash
tests/golden/parser/label_simple.ziku         # Basic syntax
tests/golden/infer/label_goto.ziku            # Type checking
tests/golden/ir-eval/label_early_exit.ziku    # Control flow
tests/golden/ir-eval/label_nested_goto.ziku   # Nesting
```

### Testing Type Inference

**Key scenarios**:
1. **Let-polymorphism**: `let id = \x -> x` is polymorphic
2. **Type errors**: Unbound variable, type mismatch
3. **Annotation**: Type annotations guide inference
4. **Recursive types**: `letRec` with recursion

**Test both success and failure**:
```bash
tests/golden/infer/let_polymorphic.ziku       # Success case
tests/golden/infer/unbound_variable.ziku      # Error case
tests/golden/infer/type_mismatch.ziku         # Error case
```

## Workflow Integration

### Daily TDD Workflow

**Morning**: Review failing tests
```bash
lake test
# Address any failures immediately
```

**Development**: Red-Green-Refactor
```bash
# For each new feature:
# 1. Write test (red)
create_test_file.sh ir-eval feature_name
# Edit test file
lake test  # Verify red

# 2. Implement (green)
# Edit implementation files
lake test  # Verify green

# 3. Refactor
# Clean up code
lake test  # Stay green
```

**Before Commit**: Verify all tests pass
```bash
lake test  # Must be green
git commit -m "feat: add feature_name"
```

### CI/CD Integration

**Pre-commit Hook**:
```bash
#!/bin/bash
# .git/hooks/pre-commit
lake test
if [ $? -ne 0 ]; then
    echo "Tests failing, commit aborted"
    exit 1
fi
```

**Fast Feedback**:
- Run tests frequently (after each small change)
- Use `check_test_status.sh` for quick checks
- Full test suite before commits

## Further Reading

**Books**:
- "Test Driven Development: By Example" by Kent Beck
- "Growing Object-Oriented Software, Guided by Tests" by Freeman & Pryce

**Articles**:
- Martin Fowler: "Test-Driven Development"
- Robert C. Martin: "The Three Laws of TDD"

**Lean-Specific**:
- Lean 4 documentation: Testing
- Lean testing libraries: LeanCheck, LeanSpec

## Summary

TDD in Ziku follows these principles:

1. **Red-Green-Refactor**: Always follow the cycle
2. **Test-First**: Write test before implementation
3. **Atomic Tests**: Each test tests one thing
4. **Golden Tests**: Leverage automatic .golden generation
5. **Fast Feedback**: Run tests frequently
6. **Keep Green**: Never commit failing tests
7. **Refactor Continuously**: Clean code while tests pass
8. **Regression Protection**: Add test for every bug fix

Use the provided scripts (`add_golden_test.sh`, `check_test_status.sh`, `create_test_file.sh`) to streamline the workflow and maintain discipline in the TDD process.
