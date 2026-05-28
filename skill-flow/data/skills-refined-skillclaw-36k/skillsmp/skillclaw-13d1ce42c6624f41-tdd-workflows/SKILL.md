---
name: tdd-workflows
description: Use this skill when executing a comprehensive Test-Driven Development (TDD) workflow, ensuring strict adherence to the red-green-refactor cycle while incorporating safe refactoring practices.
---

# Skill body

## Overview
This skill guides you through a complete TDD workflow, emphasizing test-first development and safe refactoring. It combines test specification, design, and refactoring techniques to maintain code quality and performance.

## Usage
Use the Task tool with appropriate subagent types to execute each phase of the TDD workflow.

## Core Process

### 1. Pre-Assessment
- Run tests to establish a green baseline.
- Analyze code smells and test coverage.
- Document current performance metrics.
- Create an incremental refactoring plan.

### 2. Requirements Analysis
- Prompt: "Analyze requirements for: $ARGUMENTS. Define acceptance criteria, identify edge cases, and create test scenarios."
- Output: Test specification, acceptance criteria, edge case matrix.

### 3. Test Architecture Design
- Prompt: "Design test architecture for: $ARGUMENTS based on test specification."
- Output: Test architecture, fixture design, mock strategy.

### 4. RED - Write Failing Tests
- Prompt: "Write FAILING unit tests for: $ARGUMENTS. Tests must fail initially."
- Output: Failing unit tests, test documentation.

### 5. Verify Test Failure
- Prompt: "Verify that all tests for: $ARGUMENTS are failing correctly."
- Output: Test failure verification report.

### 6. GREEN - Write Production Code
- Implement the minimum code necessary to pass the tests.
- Ensure all tests pass after implementation.

### 7. REFACTOR - Improve Code
- Identify code smells and apply refactoring techniques:
  - Extract methods, rename for clarity, and encapsulate fields.
  - Apply design patterns where beneficial.
  - Optimize performance by profiling and addressing bottlenecks.

### 8. Incremental Steps
- Make small, atomic changes.
- Run tests after each modification.
- Commit after each successful refactoring.
- Keep refactoring separate from behavior changes.

## Coverage Thresholds
- Minimum line coverage: 80%
- Minimum branch coverage: 75%
- Critical path coverage: 100%

## Refactoring Triggers
- Cyclomatic complexity > 10
- Method length > 20 lines
- Class length > 200 lines
- Duplicate code blocks > 3 lines

## Conclusion
This skill ensures a disciplined approach to TDD, promoting high-quality code through rigorous testing and safe refactoring practices.