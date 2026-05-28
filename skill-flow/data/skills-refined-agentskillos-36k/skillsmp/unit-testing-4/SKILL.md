---
name: unit-testing
description: Automates unit test creation for C++ projects using GoogleTest (GTest) framework with consistent software testing patterns including In-Got-Want, Table-Driven Testing, and AAA patterns. Use when creating, modifying, or reviewing unit tests, or when the user mentions unit tests, test coverage, or GTest.
metadata:
  author: sentenz
  version: "1.0"
---

# Unit Testing

Instructions for AI coding agents on automating unit test creation using consistent software testing patterns in this C++ project.

- [1. Benefits](#1-benefits)
- [2. Principles](#2-principles)
  - [2.1. FIRST](#21-first)
- [3. Patterns](#3-patterns)
  - [3.1. In-Got-Want](#31-in-got-want)
  - [3.2. Table-Driven Testing](#32-table-driven-testing)
  - [3.3. Data-Driven Testing (DDT)](#33-data-driven-testing-ddt)
  - [3.4. Arrange, Act, Assert (AAA)](#34-arrange-act-assert-aaa)
  - [3.5. Test Fixtures](#35-test-fixtures)
  - [3.6. Test Doubles](#36-test-doubles)
- [4. Workflow](#4-workflow)
- [5. Commands](#5-commands)
- [6. Style Guide](#6-style-guide)
- [7. Template](#7-template)
- [8. References](#8-references)

## 1. Benefits

- Readability
  > Ensures high code quality and reliability. Tests are self-documenting, reducing cognitive load for reviewers and maintainers.

- Consistency
  > Uniform structure across tests ensures predictable, familiar code that team members can navigate efficiently.

- Scalability
  > Table-driven and data-driven approaches minimize boilerplate code when adding new test cases, making it simple to expand coverage.

- Debuggability
  > Scoped traces and detailed assertion messages pinpoint failures quickly during continuous integration and local testing.

## 2. Principles

### 2.1. FIRST

The `FIRST` principles for unit testing focus on creating effective and maintainable tests.

- Fast
  > Unit tests should execute quickly to provide rapid feedback during development and continuous integration.

- Independent
  > Each unit test should be self-contained and not rely on the state or behavior of other tests.

- Repeatable
  > Unit tests should produce deterministic results every time they are run, regardless of the environment or order of execution.

- Self-Validating
  > Unit tests should have clear pass/fail outcomes without requiring manual inspection.

- Timely
  > Unit tests should be written and executed early in the development process to catch issues as soon as possible.

## 3. Patterns

### 3.1. In-Got-Want

The In-Got-Want pattern structures each test case into three clear sections.

- In
  > Defines the input parameters or conditions for the test.

- Got
  > Captures the actual output or result produced by the code under test.

- Want
  > Specifies the expected output or result that the test is verifying against.

### 3.2. Table-Driven Testing

Table-driven testing organizes test cases in a tabular format, allowing multiple scenarios to be defined concisely.

- Test Case Structure
  > Each row in the table represents a distinct test case with its own set of inputs and expected outputs.

- Iteration
  > The test framework iterates over each row, executing the same test logic with different data.

### 3.3. Data-Driven Testing (DDT)

Data-driven testing separates test data from test logic, enabling the same test logic to be executed with multiple sets of input data.

- External Data Sources
  > Test data can be stored in external files (e.g., JSON, CSV) and loaded at runtime.

- Reusability
  > The same test logic can be reused with different datasets, enhancing maintainability and coverage.

### 3.4. Arrange, Act, Assert (AAA)

The AAA pattern structures each test case into three clear phases.

- Arrange
  > Set up the necessary preconditions and inputs for the test.

- Act
  > Execute the function or method being tested.

- Assert
  > Verify that the actual output matches the expected output.

### 3.5. Test Fixtures

Test fixtures provide a consistent and reusable setup and teardown mechanism for test cases.

- Setup
  > Initialize common objects or state needed for multiple tests.

- Teardown
  > Clean up resources or reset state after each test.

### 3.6. Test Doubles

Test doubles (e.g., mocks, stubs, fakes) are simplified versions of complex objects or components used to isolate the unit under test.

- Mocks
  > Simulate the behavior of real objects and verify interactions.

- Stubs
  > Provide predefined responses to method calls without implementing full behavior.

- Fakes
  > Implement simplified versions of real objects with limited functionality.

## 4. Workflow

1. Identify

    Identify new functions in `src/` (e.g., `src/<module>/<header>.hpp`).

2. Add/Create

    Create new tests colocated with source code in `src/<module>/` (e.g., `src/<module>/<header>_test.cpp`).

3. Register with CMake

    Add the test file to `src/<module>/CMakeLists.txt` using `meta_gtest()` with appropriate options (e.g., `WITH_DDT`).

    The test configuration should use `ENABLE` option with `META_BUILD_TESTING` variable:

    ```cmake
    include(meta_gtest)

    meta_gtest(
        ENABLE ${META_BUILD_TESTING}
        TARGET ${PROJECT_NAME}-test
        SOURCES
            <header>_test.cpp
        LINK
            ${PROJECT_NAME}::<module>
    )
    ```

4. Test Coverage Requirements

    Include comprehensive edge cases:

    - Coverage-guided cases
    - Boundary values (min/max limits, edge thresholds)
    - Empty/null inputs
    - Null pointers and invalid references
    - Overflow/underflow scenarios
    - Special cases (negative numbers, zero, special states)

5. Apply Templates

    Structure all tests using the template pattern below.

## 5. Commands

| Command                             | Description                                           |
| ----------------------------------- | ----------------------------------------------------- |
| `make cmake-gcc-test-unit-build`    | CMake preset configuration and Compile with Ninja     |
| `make cmake-gcc-test-unit-run`      | Execute tests via ctest                               |
| `make cmake-gcc-test-unit-coverage` | Execute tests via ctest and generate coverage reports |

## 6. Style Guide

- Test Framework
  > Use [GoogleTest (GTest)](https://google.github.io/googletest/) framework via `#include <gtest/gtest.h>`.

- Include Headers
  > Include necessary standard library headers (`<vector>`, `<string>`, `<climits>`, etc.) and module-specific headers in a logical order: system headers first, then project headers.

  Include necessary headers in this order:
  1. GMock/GTest headers (`<gmock/gmock.h>`, `<gtest/gtest.h>`)
  2. Standard library headers (`<memory>`, `<string>`, etc.)
  3. Project interface headers
  4. Project implementation headers

- Namespace
  > Use `using namespace <namespace>;` for convenience within test functions to reduce verbosity while maintaining clarity, since test scope is limited.

- Test Organization
  > Consolidate test cases for a single function into **one `TEST(...)` function** using table-driven testing.
  
  This approach:
  - Eliminates redundant test function definitions
  - Simplifies maintenance by grouping related scenarios together
  - Reduces code duplication in setup and teardown phases
  - Makes it easier to add or modify test cases

- Testing Macros
  > Focus each `TEST(...)` function on a single function or cohesive behavior. For complex setups, use `TEST_F` fixtures or helper functions to reduce duplication.

- Mocking
  > Use Google Mock (GMock) for creating test doubles (mocks, stubs, fakes) to isolate the unit under test. See the [mock-testing](../mock-testing/SKILL.md) skill.

- Traceability
  > Employ [`SCOPED_TRACE(tc.label)`](https://google.github.io/googletest/reference/testing.html#SCOPED_TRACE) for traceable failures in table-driven tests.

- Assertions
  > Use `EXPECT_*` macros (not `ASSERT_*`) to allow all test cases to run.

## 7. Template

Use this template (In-Got-Want + Table-Driven + AAA) for new test functions. Replace placeholders with actual values and adjust as needed for the use case.

```cpp
#include <gtest/gtest.h>

#include <vector>
#include <string>

#include "<module>/<header>.hpp"

using namespace <namespace>;

TEST(<Module>Test, <FunctionName>)
{
  // In-Got-Want
  struct Tests
  {
    std::string label;

    struct In
    {
      /* input types and names */
    } in;

    struct Want
    {
      /* expected output type(s) and name(s) */
    } want;
  };

  // Table-Driven Testing
  const std::vector<Tests> tests = {
    {"case-description-1", /* in */ {/* input values */}, /* want */ {/* expected output */}},
    {"case-description-2", /* in */ {/* input values */}, /* want */ {/* expected output */}},
    // add more cases as needed
  };

  for (const auto &tc : tests)
  {
    SCOPED_TRACE(tc.label);

    // Arrange
    <Module> <object>;
    // additional setup as needed

    // Act
    auto got = <object>.<function>(tc.in.<input>);

    // Assert
    EXPECT_EQ(got, tc.want.<expected>);
  }
}
```

## 8. References

- GoogleTest [Primer](https://google.github.io/googletest/primer.html) guide.
- GoogleTest [Advanced](https://google.github.io/googletest/advanced.html) guide.
