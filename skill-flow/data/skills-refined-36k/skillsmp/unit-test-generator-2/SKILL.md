---
name: unit-test-generator
description: Generate and improve unit tests using the Assured LLMSE approach from Meta's TestGen-LLM. Use this skill when users request help with writing unit tests, improving test coverage, adding test cases to existing test suites, generating tests for new or existing code, or reviewing and enhancing test quality. Applies multi-stage verification filters to ensure generated tests build correctly, pass reliably, and measurably improve coverage without regressing existing behavior.
---

# Unit Test Generator

Generate high-quality, verified unit tests following Meta's TestGen-LLM methodology (Assured LLMSE). This approach ensures all generated tests pass through verification filters before recommendation.

## Core Principles

### Assured LLMSE (Large Language Model-based Software Engineering)

Embed test generation in a verification workflow that guarantees:
1. **Buildable** - Generated tests compile without errors
2. **Reliable** - Tests pass consistently (not flaky)
3. **Improving** - Tests increase coverage or catch new edge cases
4. **Non-regressing** - Existing test behavior is preserved

### Extend, Don't Replace

Improve existing human-written tests rather than replacing them entirely. Add new test cases to existing test classes to fill coverage gaps.

## Workflow

### 1. Analyze the Target

Before generating tests, analyze:
- **Source code**: Understand the class/method under test
- **Existing tests**: Review current test coverage and patterns
- **Dependencies**: Identify mocking requirements
- **Edge cases**: Spot uncovered branches, error paths, boundary conditions

### 2. Generate Test Cases

Generate tests that target:
- Uncovered code paths and branches
- Boundary conditions and edge cases
- Error handling and exception paths
- Null/empty input handling
- Integration points with dependencies

Follow the existing test file's conventions for:
- Test framework (JUnit, pytest, Jest, etc.)
- Naming patterns
- Setup/teardown patterns
- Assertion style
- Mocking approach

### 3. Apply Verification Filters

Run each generated test through this filter cascade:

```
Generated Test
     │
     ▼
┌─────────────┐
│ Build Filter │ → Reject if compilation fails
└─────────────┘
     │ pass
     ▼
┌─────────────────┐
│ Execution Filter │ → Reject if test fails or is flaky
└─────────────────┘
     │ pass
     ▼
┌─────────────────┐
│ Coverage Filter  │ → Reject if no coverage improvement
└─────────────────┘
     │ pass
     ▼
┌────────────────────┐
│ Non-Regression Filter │ → Reject if existing tests break
└────────────────────┘
     │ pass
     ▼
  RECOMMEND TEST
```

### 4. Document Improvement

For each recommended test, document:
- What new code paths are covered
- What edge cases are tested
- Coverage improvement metrics (if measurable)

## Test Generation Patterns

### Coverage-Focused Tests

```java
// Before: Method `calculate(int x)` only tested with positive inputs
// Coverage gap: Negative input branch uncovered

@Test
void calculate_withNegativeInput_returnsAbsoluteValue() {
    Result result = calculator.calculate(-5);
    assertEquals(5, result.getValue());
}
```

### Edge Case Tests

```java
// Target: Boundary conditions for pagination
@Test
void getPage_atExactBoundary_returnsCorrectPage() {
    // Test edge: exactly at page size boundary
    List<Item> items = service.getPage(pageSize, pageSize);
    assertEquals(pageSize, items.size());
}

@Test
void getPage_beyondLastPage_returnsEmptyList() {
    List<Item> items = service.getPage(totalItems + 1, pageSize);
    assertTrue(items.isEmpty());
}
```

### Error Path Tests

```java
// Target: Exception handling paths
@Test
void processFile_withInvalidPath_throwsFileNotFoundException() {
    assertThrows(FileNotFoundException.class, 
        () -> processor.processFile("/nonexistent/path"));
}

@Test
void connect_withTimeout_throwsTimeoutExceptionAfterRetries() {
    when(client.connect()).thenThrow(new SocketTimeoutException());
    assertThrows(ConnectionTimeoutException.class, 
        () -> service.connectWithRetry(3));
    verify(client, times(3)).connect();
}
```

## Language-Specific Guidelines

See `references/` for framework-specific patterns:
- **Java**: `references/java-testing.md` - JUnit 5, Mockito, AssertJ patterns
- **Python**: `references/python-testing.md` - pytest, unittest, mock patterns
- **JavaScript/TypeScript**: `references/js-testing.md` - Jest, Vitest, testing-library patterns

## Quality Checklist

Before recommending a test, verify:

- [ ] **Compiles** - No syntax or type errors
- [ ] **Passes** - Test assertion succeeds
- [ ] **Deterministic** - No flakiness from timing, ordering, or external state
- [ ] **Independent** - No dependency on other test execution order
- [ ] **Fast** - Execution completes quickly (mock external dependencies)
- [ ] **Readable** - Clear test name, arrange-act-assert structure
- [ ] **Valuable** - Tests meaningful behavior, not implementation details

## Anti-Patterns to Avoid

- **Testing implementation details** - Test behavior, not private method calls
- **Brittle assertions** - Avoid exact string matching when substring suffices
- **Test interdependence** - Each test must be runnable in isolation
- **Excessive mocking** - Mock only external dependencies, not the class under test
- **Missing assertions** - Every test must assert something meaningful
- **Flaky time-based tests** - Use controllable clocks, not real time
