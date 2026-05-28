---
name: tdd-workflow
description: Use this skill when implementing features using the Test-Driven Development (TDD) methodology, following the RED-GREEN-REFACTOR cycle.
---

# TDD Workflow Skill

## Overview

Test-Driven Development (TDD) is a software development approach where tests are written before the code itself. This skill guides you through the TDD cycle, ensuring that you write meaningful tests and maintain high code quality.

## When to Use

- Implementing new features or functions
- Adding new API endpoints
- Creating utility functions
- Building components with complex logic
- When high test coverage is required

## The TDD Cycle

```
🔴 RED → Write a failing test
    ↓
🟢 GREEN → Write minimal code to pass
    ↓
🔵 REFACTOR → Improve code quality
    ↓
   Repeat...
```

## Step-by-Step Process

### Phase 1: RED - Write Failing Test

1. **Understand the requirement**
   - What is the input?
   - What is the expected output?
   - What are the edge cases?

2. **Write the simplest test case first**
   ```javascript
   describe('functionName', () => {
     it('should [expected behavior] when [condition]', () => {
       // Arrange
       // Act
       // Assert
     });
   });
   ```

3. **Run the test - it MUST fail**
   ```bash
   npm test -- functionName
   ```

### Phase 2: GREEN - Make It Pass

1. **Write the minimal code to pass**
   ```javascript
   function functionName(params) {
     // Implementation
   }
   ```

2. **Run the test - it MUST pass**
   ```bash
   npm test -- functionName
   ```

3. **Don't over-engineer** - Only write enough code to pass the current test.

### Phase 3: REFACTOR - Improve the Code

1. **Only refactor when tests are green.**
2. **Keep tests passing throughout.**
3. **Improve code quality:**
   - Remove duplication
   - Improve naming for clarity
   - Simplify logic

### Phase 4: Repeat

Add the next test case and repeat the cycle:

```javascript
it('should [expected behavior] for [new condition]', () => {
  // Arrange
  // Act
  // Assert
});
```

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Writing tests after code | Tests validate implementation, not behavior | Always write tests first |
| Testing implementation details | Brittle tests that break on refactor | Test public behavior only |
| Large test steps | Hard to identify what broke | Smaller increments |
| Skipping refactor phase | Technical debt accumulates | Always refactor after green |
| Testing trivial code | Wasted effort | Focus on logic and edge cases |

## Conclusion

By following the TDD workflow, you can ensure that your code is well-tested, maintainable, and of high quality. Embrace the cycle of RED-GREEN-REFACTOR to enhance your development process.