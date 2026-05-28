---
name: generating-unit-tests
description: Use this skill when you need to automatically generate comprehensive unit tests from source code for various testing frameworks.
---

## Overview

This skill empowers Claude to rapidly create robust unit tests, saving developers time and ensuring code quality. It analyzes source code, identifies key functionalities, and generates test cases covering various scenarios, including happy paths, edge cases, and error conditions.

## How It Works

1. **Analyze Source Code**: The skill analyzes the provided source code file to understand its functionality, inputs, and outputs.
2. **Determine Testing Framework**: The skill either detects the appropriate testing framework based on the file type and project structure or uses the framework specified by the user.
3. **Generate Test Cases**: The skill generates comprehensive test cases, including tests for valid inputs, invalid inputs, boundary conditions, and error scenarios.
4. **Create Mock Dependencies**: The skill automatically creates mocks and stubs for external dependencies to isolate the code being tested.
5. **Output Test File**: The skill outputs a new test file containing the generated test cases, imports, setup, and assertions.

## When to Use This Skill

This skill activates when you need to:
- Create unit tests for a specific file or code snippet.
- Generate test cases for a function, class, or module.
- Quickly add test coverage to existing code.
- Ensure code quality and prevent regressions.

## Examples

### Example 1: Generating Tests for a JavaScript Utility Function

User request: "generate tests <input_path>"

The skill will:
1. Analyze the specified file to understand its functions and dependencies.
2. Detect the file type and default to the appropriate testing framework (e.g., Jest for JavaScript).
3. Generate a corresponding test file with test cases covering various scenarios.

### Example 2: Generating Tests for a Python API Endpoint using pytest

User request: "generate tests --framework pytest <input_path>"

The skill will:
1. Analyze the specified file to understand its API endpoints and dependencies.
2. Use the specified testing framework (e.g., pytest).
3. Generate a test file with test cases covering various API scenarios, including successful requests, error handling, and authentication.

## Best Practices

- **Framework Specification**: Explicitly specify the testing framework when the default is not desired or ambiguous.
- **File Granularity**: Generate tests for individual files or modules to maintain focus and testability.
- **Review and Refine**: Always review and refine the generated tests to ensure they accurately reflect the desired behavior and coverage.

## Integration

This skill can be used in conjunction with other code analysis and refactoring tools to improve code quality and maintainability. It also integrates with CI/CD pipelines to automatically run tests and prevent regressions.