# Coverage Strategies with Claude Code

Systematic approaches for analyzing test coverage, identifying gaps, and achieving thorough test coverage.

## Coverage Fundamentals

### Types of Coverage

| Type | Description | Goal |
|------|-------------|------|
| Line Coverage | Lines of code executed | 80%+ |
| Branch Coverage | Decision paths taken | 75%+ |
| Function Coverage | Functions called | 90%+ |
| Statement Coverage | Statements executed | 80%+ |

### Why Coverage Matters

- **Identifies untested code** - Find what's not tested
- **Prevents regressions** - Tested code is safer to change
- **Guides testing effort** - Focus on low-coverage areas
- **Build confidence** - Higher coverage = safer deployments

### Coverage Limitations

Coverage does not guarantee:
- Tests are meaningful
- Edge cases are handled
- Assertions are correct
- Integration works

**Coverage is a necessary but not sufficient metric.**

## Running Coverage Reports

### JavaScript/TypeScript

#### Jest

```bash
# Basic coverage
bun test --coverage

# With thresholds
bun test --coverage --coverageThreshold='{"global":{"lines":80}}'

# HTML report
bun test --coverage --coverageReporters=html

# Specific files
bun test --coverage --collectCoverageFrom='src/**/*.ts'
```

#### Vitest

```bash
# Basic coverage
bun test --coverage

# With v8 provider
bun test --coverage --coverage.provider=v8

# HTML report
bun test --coverage --coverage.reporter=html

# With thresholds
bun test --coverage --coverage.lines=80
```

#### Vitest Configuration

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'lcov'],
      include: ['src/**/*.ts'],
      exclude: ['**/*.test.ts', '**/*.d.ts'],
      thresholds: {
        lines: 80,
        branches: 75,
        functions: 90,
        statements: 80
      }
    }
  }
});
```

### Python

#### pytest-cov

```bash
# Basic coverage
pytest --cov=src

# HTML report
pytest --cov=src --cov-report=html

# Terminal report
pytest --cov=src --cov-report=term-missing

# With thresholds
pytest --cov=src --cov-fail-under=80

# Branch coverage
pytest --cov=src --cov-branch
```

#### Configuration (pyproject.toml)

```toml
[tool.pytest.ini_options]
addopts = "--cov=src --cov-report=term-missing"

[tool.coverage.run]
branch = true
source = ["src"]
omit = ["**/tests/*", "**/__pycache__/*"]

[tool.coverage.report]
fail_under = 80
exclude_lines = [
    "pragma: no cover",
    "if __name__ == .__main__.:",
    "raise NotImplementedError"
]
```

## Analyzing Coverage with Claude

### Prompt: Analyze Coverage Report

```
Analyze this coverage report and identify:

1. Files with lowest coverage
2. Functions that are not tested
3. Branches that are not taken
4. Critical paths that need testing

[paste coverage report]

Prioritize by:
- Business criticality
- Code complexity
- Change frequency
```

### Prompt: Generate Tests for Uncovered Lines

```
This function has the following uncovered lines:
[paste lines with coverage markers]

Generate tests that will cover:
- Lines [line numbers]
- The untested branches
- Any edge cases implied by the code

Use [framework] with [language].
```

### Example: Analyzing Coverage Output

**Input (coverage report):**
```
Name                     Stmts   Miss Branch BrPart  Cover   Missing
----------------------------------------------------------------------
src/auth/login.ts           45      8     12      4    78%   23-25, 38-42
src/auth/register.ts        62      2     18      1    96%   45-46
src/utils/validation.ts     28     12      8      5    52%   15-26
src/api/users.ts            85     25     24     10    65%   34-58
----------------------------------------------------------------------
TOTAL                      220     47     62     20    75%
```

**Prompt:**
```
Based on this coverage report, prioritize testing:

1. src/utils/validation.ts (52% coverage, 12 missing statements)
2. src/api/users.ts (65% coverage, 25 missing statements)

Read these files and generate tests for the uncovered lines.
Start with validation.ts.
```

## Coverage Gap Patterns

### Pattern 1: Error Handling Gaps

Untested error paths are common gaps.

```
Find all error handling code in [file]:
- catch blocks
- if (error) branches
- throw statements

Generate tests that trigger each error condition.
```

### Pattern 2: Conditional Branch Gaps

```
Identify all conditional branches in [file]:
- if/else statements
- ternary operators
- switch cases
- guard clauses

For each, show:
- Current coverage status
- How to trigger the untested branch
```

### Pattern 3: Edge Case Gaps

```
For the function [name], identify edge cases:

Input boundaries:
- Empty/null/undefined
- Minimum/maximum values
- Type coercion scenarios

Generate tests for each edge case.
```

### Pattern 4: Integration Gaps

```
This unit has high unit test coverage but low integration coverage.

Identify integration scenarios:
- Database interactions
- API calls
- File system operations
- External service calls

Generate integration tests for these.
```

## Coverage Workflow

### Workflow: Improve Coverage for a Module

1. **Generate current report**
   ```bash
   bun test --coverage --collectCoverageFrom='src/module/**'
   ```

2. **Identify gaps**
   ```
   Show me the uncovered lines in src/module/service.ts
   and explain what scenarios would cover them.
   ```

3. **Generate tests**
   ```
   Generate tests for lines 45-52 of src/module/service.ts.
   These lines handle [describe the logic].
   ```

4. **Verify improvement**
   ```bash
   bun test --coverage
   ```

5. **Repeat until target reached**

### Workflow: Coverage-Driven Refactoring

1. **Identify hard-to-test code**
   ```
   This function has 30% coverage and seems hard to test.
   Analyze why and suggest refactoring to improve testability.
   ```

2. **Refactor for testability**
   ```
   Refactor this function to:
   - Extract dependencies for mocking
   - Split complex logic into smaller functions
   - Remove hidden state
   ```

3. **Write tests for refactored code**

4. **Verify coverage improved**

## Coverage Thresholds Strategy

### Setting Thresholds

```javascript
// vitest.config.ts or jest.config.js
{
  coverageThreshold: {
    global: {
      branches: 75,
      functions: 85,
      lines: 80,
      statements: 80
    },
    // Stricter for critical paths
    './src/auth/**': {
      branches: 90,
      functions: 95,
      lines: 90
    },
    // Relaxed for generated code
    './src/generated/**': {
      branches: 50,
      lines: 50
    }
  }
}
```

### Progressive Threshold Increase

```
Current coverage: 65%
Target coverage: 85%

Week 1: Set threshold to 68%
Week 2: Set threshold to 72%
Week 3: Set threshold to 76%
Week 4: Set threshold to 80%
Week 5: Set threshold to 85%

Block PRs that decrease coverage below threshold.
```

## Mocking for Coverage

### When to Mock

Mock external dependencies to:
- Test error handling paths
- Control timing for async code
- Isolate unit under test
- Make tests deterministic

### Mocking Patterns

#### Jest/Vitest

```typescript
// Mock entire module
vi.mock('./database', () => ({
  query: vi.fn()
}));

// Mock to trigger error path
database.query.mockRejectedValue(new Error('Connection failed'));

// Mock to trigger specific branch
database.query.mockResolvedValue([]);  // Empty result
database.query.mockResolvedValue(null); // Null result
```

#### pytest

```python
from unittest.mock import patch, Mock

# Mock function
@patch('module.external_call')
def test_error_handling(mock_call):
    mock_call.side_effect = Exception('Network error')
    with pytest.raises(ServiceError):
        service.process()

# Mock return value
@patch('module.database.query')
def test_empty_result(mock_query):
    mock_query.return_value = []
    result = service.get_all()
    assert result == []
```

## Coverage for Different Test Types

### Unit Test Coverage

Focus on:
- Individual functions
- Class methods
- Pure logic
- Edge cases

```
Generate unit tests for [function] targeting:
- All code paths
- Boundary conditions
- Error cases
```

### Integration Test Coverage

Focus on:
- Component interactions
- Database operations
- API contracts
- Error propagation

```
Generate integration tests that cover:
- Happy path through the system
- Error handling at integration points
- Data flow between components
```

### E2E Test Coverage

Focus on:
- User flows
- Critical paths
- Business scenarios

```
Generate E2E tests that cover:
- Main user journeys
- Error scenarios users encounter
- Edge cases in the UI
```

## Coverage Anti-Patterns

### Anti-Pattern: Coverage Theater

```typescript
// Bad: Test increases coverage but tests nothing useful
it('should cover line 42', () => {
  const result = process(data);
  // No assertions!
});
```

**Fix:** Always include meaningful assertions.

### Anti-Pattern: Testing Private Methods

```typescript
// Bad: Testing implementation details
it('should call private helper', () => {
  expect(service._privateHelper).toHaveBeenCalled();
});
```

**Fix:** Test through public interface.

### Anti-Pattern: Ignoring Branches

```typescript
// Bad: Only testing happy path
it('should process data', () => {
  const result = process(validData);
  expect(result).toBeDefined();
});
// Missing: test for invalid data, null, errors
```

**Fix:** Test all branches and error conditions.

### Anti-Pattern: Over-Mocking

```typescript
// Bad: Everything is mocked, nothing is really tested
it('should work', () => {
  mockA.mockReturnValue(x);
  mockB.mockReturnValue(y);
  mockC.mockReturnValue(z);
  // Testing that mocks work, not real code
});
```

**Fix:** Only mock external dependencies.

## Coverage Checklist

### Before PR

- [ ] Coverage meets threshold
- [ ] New code is tested
- [ ] Critical paths have high coverage
- [ ] Error handling is tested
- [ ] Edge cases are covered

### Coverage Review

- [ ] Tests are meaningful (not just for coverage)
- [ ] Assertions verify behavior
- [ ] Mocks are appropriate
- [ ] Integration points are tested
- [ ] No coverage gaps in critical code

## Coverage Commands Reference

| Action | Jest | Vitest | pytest |
|--------|------|--------|--------|
| Basic coverage | `--coverage` | `--coverage` | `--cov=src` |
| HTML report | `--coverageReporters=html` | `--coverage.reporter=html` | `--cov-report=html` |
| Show missing lines | `--coverageReporters=text` | `--coverage.reporter=text` | `--cov-report=term-missing` |
| Set threshold | `--coverageThreshold` | `--coverage.lines=80` | `--cov-fail-under=80` |
| Specific files | `--collectCoverageFrom` | `--coverage.include` | `--cov=path` |
| Exclude files | Config: `coveragePathIgnorePatterns` | `--coverage.exclude` | `--cov-config` |

## Prompt Templates for Coverage

### Find Coverage Gaps

```
Review this coverage report and source code.
Identify the top 3 coverage gaps that would have the highest impact if fixed.
For each gap, explain what's not covered and why it matters.

Coverage report:
[paste report]

Source code:
[paste or reference files]
```

### Generate Tests for Specific Lines

```
Generate tests to cover lines [X-Y] in [file].
These lines contain [describe the logic].
The current tests don't trigger these lines because [reason].

Include tests that:
1. Trigger the specific code path
2. Verify the behavior
3. Test edge cases in this path
```

### Coverage Improvement Plan

```
Create a coverage improvement plan for this codebase:

Current state:
[paste coverage summary]

Goals:
- Increase overall coverage to [X]%
- Critical paths should have [Y]% coverage
- No file should be below [Z]%

Provide:
1. Priority order for files to improve
2. Estimated effort for each
3. Specific test cases to add
```
