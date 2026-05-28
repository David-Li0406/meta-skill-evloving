---
name: tdd-workflows
description: Use this skill when executing a comprehensive Test-Driven Development (TDD) workflow with strict red-green-refactor discipline.
---

# Body of the merged SKILL.md

Execute a comprehensive Test-Driven Development (TDD) workflow with strict red-green-refactor discipline. This workflow enforces test-first development through coordinated agent orchestration, ensuring each phase of the TDD cycle is strictly followed.

## Configuration

### Coverage Thresholds
- Minimum line coverage: 80%
- Minimum branch coverage: 75%
- Critical path coverage: 100%

### Refactoring Triggers
- Cyclomatic complexity > 10
- Method length > 20 lines
- Class length > 200 lines
- Duplicate code blocks > 3 lines

## Core Process

### Phase 1: Test Specification and Design
1. **Requirements Analysis**
   - Analyze requirements for: `<ARGUMENTS>`. Define acceptance criteria, identify edge cases, and create test scenarios. Output a comprehensive test specification.
   
2. **Test Architecture Design**
   - Design test architecture for: `<ARGUMENTS>` based on test specification. Define test structure, fixtures, mocks, and test data strategy.

### Phase 2: RED - Write Failing Tests
3. **Write Unit Tests (Failing)**
   - Write FAILING unit tests for: `<ARGUMENTS>`. Tests must fail initially, including edge cases and error scenarios.

4. **Verify Test Failure**
   - Verify that all tests for: `<ARGUMENTS>` are failing correctly. Ensure failures are for the right reasons.

### Phase 3: GREEN - Make Tests Pass
5. **Minimal Implementation**
   - Implement MINIMAL code to make tests pass for: `<ARGUMENTS>`. Focus only on making tests green.

6. **Verify Test Success**
   - Run all tests for: `<ARGUMENTS>` and verify they pass. Check test coverage metrics.

### Phase 4: REFACTOR - Improve Code Quality
7. **Code Refactoring**
   - Refactor implementation for: `<ARGUMENTS>` while keeping tests green. Apply SOLID principles and optimize performance.

8. **Test Refactoring**
   - Refactor tests for: `<ARGUMENTS>`. Remove test duplication and enhance test readability.

### Phase 5: Integration and System Tests
9. **Write Integration Tests (Failing First)**
   - Write FAILING integration tests for: `<ARGUMENTS>`. Tests must fail initially.

10. **Implement Integration**
    - Implement integration code for: `<ARGUMENTS>` to make integration tests pass.

### Phase 6: Continuous Improvement Cycle
11. **Performance and Edge Case Tests**
    - Add performance tests and additional edge case tests for: `<ARGUMENTS>`.

12. **Final Code Review**
    - Perform a comprehensive review of: `<ARGUMENTS>`. Verify TDD process was followed and suggest improvements.

## Incremental Development Mode
For test-by-test development, write ONE failing test, make ONLY that test pass, refactor if needed, and repeat for the next test.

## Validation Checkpoints
- Ensure all tests are written before implementation.
- Verify all tests fail with meaningful error messages.
- Confirm all tests pass after implementation.
- Maintain coverage metrics throughout the process.

## Failure Recovery
If TDD discipline is broken:
1. **STOP** immediately.
2. Identify which phase was violated.
3. Rollback to last valid state.
4. Resume from the correct phase.

## Success Criteria
- 100% of code written test-first.
- All tests pass continuously.
- Coverage exceeds thresholds.
- Code complexity within limits.

## Notes
- Enforce strict RED-GREEN-REFACTOR discipline.
- Each phase must be completed before moving to the next.
- Refactoring is NOT optional.

TDD implementation for: `<ARGUMENTS>`