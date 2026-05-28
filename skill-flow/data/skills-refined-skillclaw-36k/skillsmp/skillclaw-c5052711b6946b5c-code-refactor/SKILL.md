---
name: code-refactor
description: Use this skill when you need to improve the quality of your code while maintaining its functionality, especially after receiving a request to refactor.
---

# Skill body

## Refactor Code

This skill is used to refactor code effectively.

### Refactoring Guidelines

1. **Improve Readability**: Enhance naming, split functions, and organize structure.
2. **Eliminate Duplication**: Apply the DRY (Don't Repeat Yourself) principle.
3. **Simplify**: Remove unnecessary complexity.

### Workflow

1. **Check Current Tests**: Ensure all tests pass before starting the refactor.
   ```bash
   php artisan test  # For PHP
   pytest            # For Python
   ```

2. **Refactor Code**:
   - **DRY**: Consolidate duplicate code.
   - **Constantization**: Remove magic numbers.
   - **Method Splitting**: Break down long methods.
   - **Naming**: Improve variable and method names.

3. **Run Tests**: After refactoring, run all tests to confirm they pass.
   - **Expectation**: All tests should pass successfully.

### Prohibitions

- Do not make changes that break existing tests.
- Avoid adding new features during this phase.
- Do not delete or modify existing tests.

### Output

Provide a comparison of the code before and after refactoring, along with explanations for the changes made.