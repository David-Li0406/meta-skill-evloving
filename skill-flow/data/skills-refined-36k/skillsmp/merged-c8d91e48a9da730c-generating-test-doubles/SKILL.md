---
name: generating-test-doubles
description: Use this skill when you need to generate test doubles, mocks, stubs, spies, or fakes to isolate units of code during testing.
---

## Overview

This skill empowers Claude to streamline unit testing by automatically generating test doubles (mocks, stubs, spies, and fakes). It analyzes the code under test, identifies dependencies, and creates the necessary test doubles, significantly reducing the time and effort required to write effective unit tests.

## How It Works

1. **Dependency Analysis**: Claude analyzes the code to identify dependencies that need to be replaced with test doubles.
2. **Test Double Generation**: Based on the dependencies and specified testing framework, Claude generates appropriate test doubles (mocks, stubs, spies, or fakes).
3. **Code Insertion**: Claude provides the generated test double code, ready for integration into your unit tests.

## When to Use This Skill

This skill activates when you need to:
- Create mocks for external API calls in a unit test.
- Generate stubs for service dependencies to control their behavior.
- Implement spies to track interactions with real objects during testing.

## Examples

### Example 1: Generating Mocks for API Calls

User request: "Generate mocks for the `<function_name>` function in `<file_name>` using `<testing_framework>`."

The skill will:
1. Analyze the `<file_name>` file to identify the `<function_name>` function and its dependencies.
2. Generate a `<testing_framework>` mock for `<function_name>`, allowing you to simulate API responses.

### Example 2: Creating Stubs for Service Dependencies

User request: "Create stubs for the `<service_name>` in `<file_name>` using `<testing_framework>`."

The skill will:
1. Analyze `<file_name>` and identify the `<service_name>` dependency.
2. Generate a `<testing_framework>` stub for `<service_name>`, enabling you to control its behavior during testing of `<file_name>`.

## Best Practices

- **Framework Selection**: Specify the testing framework you are using (e.g., Jest, Sinon) for optimal test double generation.
- **Code Context**: Provide the relevant code snippets or file paths to ensure accurate dependency analysis.
- **Test Double Type**: Consider the purpose of the test double. Use mocks for behavior verification, stubs for controlled responses, and spies for interaction tracking.

## Integration

This skill integrates directly with your codebase by providing generated test double code snippets that can be easily copied and pasted into your unit tests. It supports popular testing frameworks and enhances the overall testing workflow.