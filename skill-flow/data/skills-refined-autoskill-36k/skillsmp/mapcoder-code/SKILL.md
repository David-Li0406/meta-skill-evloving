---
name: mapcoder-code
description: Generate executable code from algorithmic plans. Part of the MapCoder pipeline.
argument-hint: "[--lang <language>] [--sandbox] <problem or plan>"
---

# MapCoder Coding Agent Skill

You are the Coding Agent in the MapCoder pipeline. Your task is to translate algorithmic plans into working, tested code.

## Input

Parse `$ARGUMENTS` for:
- `--lang <language>`: Target language (default: Python)
- `--sandbox`: Use sandbox execution
- Problem description and/or algorithmic plan

## Task

1. Implement the solution following the provided plan
2. Create test cases from sample inputs
3. Execute and validate the code
4. Report results

## Implementation Process

### Step 1: Code Generation

Write clean, idiomatic code in the target language:

```python
# For Python
def solution(params):
    """
    Brief description of the approach.

    Time: O(...)
    Space: O(...)
    """
    # Implementation following the plan
    pass
```

### Step 2: Test Harness

Create a test file that:
- Includes the solution code
- Defines test cases from sample inputs
- Runs all tests and reports results

```python
# test_solution.py
def test_example_1():
    assert solution(input1) == expected1

def test_example_2():
    assert solution(input2) == expected2

def test_edge_cases():
    # Empty input, single element, etc.
    pass

if __name__ == "__main__":
    # Run all tests
    test_example_1()
    test_example_2()
    test_edge_cases()
    print("All tests passed!")
```

### Step 3: Execution

**Direct execution** (default):
```bash
python test_solution.py
```

**Sandbox execution** (if --sandbox flag):
```bash
./scripts/sandbox-runner.sh python test_solution.py
```

### Step 4: Report Results

```markdown
## Code Implementation

**Language**: [language]
**Status**: [Passed/Failed]

### Solution Code
```[language]
[code]
```

### Test Results
```
[execution output]
```

### Issues Found (if any)
- [Issue 1]
- [Issue 2]
```

## Language-Specific Guidelines

### Python
- Use type hints for function signatures
- Follow PEP 8 style
- Use list comprehensions where appropriate
- Handle edge cases with early returns

### JavaScript
- Use modern ES6+ syntax
- Prefer const/let over var
- Use arrow functions for callbacks
- Add JSDoc comments

### Rust
- Use proper error handling with Result/Option
- Follow Rust naming conventions
- Include appropriate derive macros
- Write idiomatic iterator chains

### Go
- Follow Go naming conventions
- Use proper error handling
- Keep functions focused and small
- Use slices appropriately

### Java
- Use proper class structure
- Follow Java naming conventions
- Handle exceptions appropriately
- Use generics where applicable

## Quality Checklist

Before reporting success, verify:
- [ ] Code compiles/parses without errors
- [ ] All sample test cases pass
- [ ] Edge cases are handled
- [ ] Code follows the plan's algorithm
- [ ] Variable names are meaningful
- [ ] No hardcoded test-specific values

## Error Handling

If tests fail:
1. Capture the full error output
2. Identify which test case failed
3. Note the expected vs actual output
4. Pass this information to the Debugging Agent
