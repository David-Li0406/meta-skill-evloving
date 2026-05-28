---
name: generate-tests
description: 'Generate comprehensive, maintainable test suites through code analysis. Use when the user asks to write tests, create unit tests, add test cases, test a function, or improve test coverage.'
compatibility: Requires test framework and code read/write tools
allowed-tools:
    - Bash(node:*, npm:*, npx:*, pnpm:*, yarn:*, python:*, pip:*, pytest:*, go:*, cargo:*, mvn:*, ./mvnw:*, gradle:*, ./gradlew:*, make:*, cmake:*, g++:*, gcc:*, clang:*)
    - Glob
    - Grep
    - Read
    - Write
    - mcp__context7
    - mcp__fetch
    - mcp__jetbrains
    - mcp__markitdown
    - mcp__serena
---

# Test Generation Skill

Generate comprehensive, maintainable tests through code analysis.

## Test Generation Process

1. Analyze code: signature/I-O, branches, deps/side effects.
   Tools: `mcp__serena__find_symbol`(signatures), `mcp__context7__get-library-docs`(framework docs).
2. Check existing patterns:
    - `find . -name "*.test.*" -o -name "*_test.*" -o -name "test_*"`
    - `grep -r "describe\\|it\\|test\\|expect" --include="*.test.*" | head -5`
3. Design cases:
    - AAA: Arrange → Act → Assert.
    - Coverage: happy path, edge(boundary/empty/null), error(invalid/exception), integration interactions.

## Framework Templates

Load only the framework you need:

- Jest(JS/TS): `references/jest.md`
- Vitest(JS/TS): `references/vitest.md`
- pytest(Python): `references/pytest.md`
- Go: `references/go.md`
- JUnit(Java): `references/java-junit.md`
- Kotlin test: `references/kotlin-test.md`

## Test Naming Conventions

### Descriptive test names

- `should_return_expected_result_when_valid_input`
- `returns_empty_array_for_empty_input`
- `throws_error_for_negative_input`

## Mocking Guidelines

### What to Mock

- External API calls
- Database operations
- File system access
- Time-related functions
- Random functions

### Mocking Principles

- Use minimal mocking
- Configure to behave like real implementation
- Mock at interface boundaries
- Test behavior, not implementation details

## Output Format

````markdown
## Test Generation Result

### Target

- File: `path/to/file`
- Function: `functionName`

### Generated Tests

- Total N test cases
- Happy Path: N
- Edge Cases: N
- Error Cases: N

### Test File

`path/to/test/file`

### How to Run

```bash
npm test -- --testPathPattern="filename"
pytest path/to/test_file.py -v
go test ./... -run TestFunctionName
```
````

### Coverage Improvement Suggestions

- [Additional test case suggestions]

## Edge Cases

- **No test file exists**: Create new test file
- **Existing tests**: Maintain consistent style, add only new cases
- **Untestable code**: Suggest refactoring
- **Complex mocking required**: Offer integration test alternative

## Notes

- MCP tools are optional; omit if unavailable or add others as needed
