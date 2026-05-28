---
name: test-driven-development
description: Use this skill when implementing new features, fixing bugs, or refactoring code to ensure high test coverage and design quality through the Red-Green-Refactor cycle.
---

# Test-Driven Development (TDD)

## Overview

Follow Kent Beck's Test-Driven Development (TDD) methodology using the Red-Green-Refactor cycle. Always write a failing test before any production code, ensuring that you understand what the test is verifying.

## The TDD Cycle

1. **RED**: Write a failing test.
   - Ensure the test fails for the expected reason.
   - Write only one small test at a time.

2. **GREEN**: Write the simplest code to make the test pass.
   - Implement just enough code to pass the test.
   - Avoid premature optimization or generalization.

3. **REFACTOR**: Improve the code structure while keeping all tests passing.
   - Refactor only when all tests are green.
   - Make one change at a time and run tests after each change.

## Core Principles

- **No Production Code Without a Failing Test**: Always start with a failing test.
- **One Test at a Time**: Focus on writing one test before moving on to the next.
- **Small Steps**: Make the smallest possible change to pass the test.
- **Keep It Deployable**: Ensure that the code is always in a deployable state after each cycle.

## Quality Standards

- Eliminate duplication between test and production code.
- Use clear and descriptive names for tests and methods.
- Keep methods small and focused on a single responsibility.
- Run all tests after every change to ensure nothing is broken.

## When to Use

- Implementing new features
- Fixing bugs
- Refactoring existing code
- Practicing test-driven development methodology

## Key Phrases

This skill triggers on phrases like "TDD", "write tests first", "test-driven", "red-green-refactor", "watch it fail", "test first", or "behavior driven".