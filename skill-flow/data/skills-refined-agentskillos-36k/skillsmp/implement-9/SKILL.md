---
name: implement
description: A skill for implementation following TDD principles. Leads with tests to efficiently implement high-quality code that meets requirements.
---

# Implement Skill

A skill for TDD-based implementation. Prioritizes tests to accurately meet requirements and implement high-quality code.

## When to Activate

This skill activates in the following scenarios:

- After test design documents are complete
- Starting code implementation
- Implementing unit tests
- Preventing regressions

## Key Processes

### 1. Red Phase - Writing Test Code

- Write requirements as test code
- Create failing tests without implementation
- Verify test validity

### 2. Green Phase - Minimal Implementation

- Implement minimum code to pass tests
- Prioritize simplicity
- Verify test success

### 3. Refactor Phase - Quality Improvements

- Eliminate duplication (DRY principle)
- Apply design patterns
- Performance optimization
- Improve maintainability

### 4. Ensuring Test Coverage

- Run unit tests
- Measure coverage (target: >80%)
- Test edge cases
- Perform performance testing

### 5. Integration and Review

- Integration testing with other modules
- Conduct code reviews
- Verify CI/CD pipelines
- Create documentation

## Implementation Principles

- **Simplicity**: Minimum code to meet requirements
- **Testability**: Design that is easy to test
- **Maintainability**: Readable and easy to modify code
- **Performance**: Efficient and fast code
- **Security**: Apply security best practices

## Implementation Guidelines

### Code Quality

- ESLint/Biome linting
- Formatting standardization
- Type safety (TypeScript)
- Naming conventions consistency

### Test Strategies

- **Unit Tests**: Function/method level
- **Integration Tests**: Inter-module communication
- **E2E Tests**: User scenarios
- **Performance Tests**: Load testing

### Review Points

- Verify requirement fulfillment
- Verify test coverage
- Verify code quality standards
- Verify performance standards
- Perform security checks

## Deliverables

- Implementation code
- Unit test code
- Integration test code
- Test execution reports
- Coverage reports
- Implementation documentation (README and comments)
