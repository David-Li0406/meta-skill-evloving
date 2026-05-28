---
name: tdd-workflow
description: Guide test-driven development workflow for PowerShell code in this project. Use when: (1) Implementing new features or functions, (2) Modifying existing functions, (3) Fixing bugs, (4) Refactoring code. This skill provides the Red-Green-Refactor cycle workflow and ensures tests and implementation are always committed together.
---

# TDD Workflow

Step-by-step test-driven development workflow for PowerShell code following Red-Green-Refactor principles.

## The Red-Green-Refactor Cycle

### RED: Write a Failing Test

1. Write a test that describes the desired behavior
2. Run the test - it should FAIL (red)
3. Verify the failure is for the right reason

### GREEN: Make the Test Pass

1. Write the minimum code needed to pass the test
2. Run the test - it should PASS (green)
3. Don't worry about code quality yet

### REFACTOR: Improve the Code

1. Clean up the code while keeping tests passing
2. Remove duplication (DRY)
3. Improve readability
4. Run tests frequently during refactoring

## Workflow Steps

### For New Features

1. **Write the test** (RED phase)
   ```powershell
   Describe "New-FeatureName" {
       It "Should handle basic case" {
           $result = New-FeatureName -Input "test"
           $result | Should -Be "expected"
       }
   }
   ```

2. **Run tests - confirm failure**
   ```bash
   pwsh -File ".\test\bin\testrunner.ps1" -Unit
   ```
   Expected output: Test fails because function doesn't exist

3. **Implement minimal code** (GREEN phase)
   ```powershell
   function New-FeatureName {
       param([string]$Input)
       return "expected"
   }
   ```

4. **Run tests - confirm pass**
   ```bash
   pwsh -File ".\test\bin\testrunner.ps1" -Unit
   ```
   Expected output: Test passes

5. **Refactor if needed** (REFACTOR phase)
   - Improve implementation
   - Add error handling
   - Remove duplication
   - Keep tests passing

6. **Commit test + implementation together**
   ```bash
   git add tools/pslib/utils.ps1 tools/pslib/utils.Tests.ps1
   git commit -m "feat: add New-FeatureName function"
   ```

### For Modifying Existing Functions

**CRITICAL: Never modify implementation without updating tests!**

1. **Read existing tests**
   - Understand what behavior is currently tested
   - Identify gaps in test coverage

2. **Update tests for new behavior** (RED phase)
   ```powershell
   It "Should handle new case" {
       $result = Existing-Function -NewParameter "value"
       $result | Should -Be "expected-new-behavior"
   }
   ```

3. **Run tests - confirm failure**
   ```bash
   pwsh -File ".\test\bin\testrunner.ps1" -Unit
   ```
   Expected: New test fails, existing tests pass

4. **Update implementation** (GREEN phase)
   ```powershell
   function Existing-Function {
       param(
           [string]$OldParameter,
           [string]$NewParameter  # New parameter
       )
       
       # Updated logic
   }
   ```

5. **Run tests - confirm all pass**
   ```bash
   pwsh -File ".\test\bin\testrunner.ps1" -Unit
   ```
   Expected: All tests pass

6. **Commit test + implementation together**
   ```bash
   git add tools/pslib/utils.ps1 tools/pslib/utils.Tests.ps1
   git commit -m "feat: add NewParameter to Existing-Function"
   ```

### For Bug Fixes

1. **Write test that reproduces the bug** (RED phase)
   ```powershell
   It "Should handle edge case that was failing" {
       $result = Function-With-Bug -EdgeCase "value"
       $result | Should -Be "correct-behavior"
   }
   ```

2. **Run test - confirm it fails**
   - Test should fail, demonstrating the bug

3. **Fix the bug** (GREEN phase)
   - Modify implementation to pass the new test
   - Ensure existing tests still pass

4. **Run all tests**
   ```bash
   pwsh -File ".\test\bin\testrunner.ps1" -Unit
   ```

5. **Commit test + fix together**
   ```bash
   git add file.ps1 file.Tests.ps1
   git commit -m "fix: handle edge case in Function-With-Bug"
   ```

## Quick Reference Commands

### Run Unit Tests (Fast Feedback Loop)

```bash
pwsh -File ".\test\bin\testrunner.ps1" -Unit
```

### Run Integration Tests

```bash
pwsh -File ".\test\bin\testrunner.ps1" -Integration
```

### Run All Tests

```bash
pwsh -File ".\test\bin\testrunner.ps1"
```

### Run Tests with Coverage

```bash
pwsh -File ".\test\bin\testrunner.ps1" -Unit -Coverage
```

### Run Specific Test File

```bash
pwsh -File ".\test\bin\testrunner.ps1" -TestPath "tools\pslib\utils.Tests.ps1"
```

## TDD Best Practices

1. **Write the smallest test possible** - Test one behavior at a time
2. **See it fail first** - Never skip the RED phase
3. **Write minimal code** - Only enough to pass the test
4. **Refactor with confidence** - Tests protect against regressions
5. **Keep tests fast** - Mock external dependencies in unit tests
6. **Test behavior, not implementation** - Focus on what, not how
7. **One assertion per test** - Each test verifies one thing
8. **Commit tests and implementation together** - They are inseparable

## Common Mistakes to Avoid

1. **Skipping the RED phase** - Writing tests after implementation
2. **Committing implementation without tests** - Tests must be in same commit
3. **Committing tests without implementation** - Implementation must be in same commit
4. **Not running tests before committing** - All tests must pass
5. **Testing implementation details** - Test public interface, not internals
6. **Writing too much code** - Implement only what's needed to pass tests
7. **Ignoring failing tests** - All tests must pass before proceeding

## Example Workflow

See [tdd-examples.md](references/tdd-examples.md) for complete step-by-step examples from the codebase.

## Integration with pester-exec Skill

For detailed testing execution guidance, use the `pester-exec` skill:
- Running tests on different PowerShell versions
- CI/CD integration patterns  
- Troubleshooting test failures
- Advanced Pester features
