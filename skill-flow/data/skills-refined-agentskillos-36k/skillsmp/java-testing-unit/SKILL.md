---
name: java-testing-unit
description: Unit testing patterns with JUnit 5 and Mockito: boundaries, naming, AAA, parameterized tests, and coverage gates. Use when adding features or fixing bugs.
license: Apache-2.0
compatibility: JDK 17+ (recommended 21+). JUnit Jupiter (JUnit 5). Mockito optional. Gradle/Maven.
metadata:
  owner: backend-platform
  version: "1.0"
  tags: [java, testing, unit-test, junit5, mockito, coverage, quality]
---

# Unit Testing Playbook (Java)

## Scope

### In scope

- Test design: what is a unit, how to choose boundaries, what to mock vs not mock.
- Naming, structure, and readability standards.
- JUnit 5 idioms: @Nested, @ParameterizedTest, @Tag, lifecycle.
- Mockito idioms: stubbing, verification, strictness, argument matchers.
- Coverage expectations and pragmatic gating (JaCoCo).

### Out of scope

- Full integration testing with real services (see separate integration testing skill).
- Load testing and performance benchmarking.

## When to use

- Adding a feature: you need fast, deterministic feedback.
- Fixing a bug: you must add a regression test.
- Refactoring: you need safety nets before changes.

## Principles (keep tests fast and deterministic)

- A unit test must run in-memory without network/DB/filesystem.
- Tests should be:
  - deterministic (no time-based flakiness)
  - isolated (no shared global state)
  - readable (future maintainers can diagnose quickly)

## What to mock vs not mock

Mock:

- external dependencies and side effects (HTTP clients, repositories, message brokers)
- time (Clock) and randomness (Random) via injection

Do NOT mock:

- value objects and pure functions
- collections, strings, DTOs
- your own domain logic objects unless necessary

## Naming and structure

### Recommended naming

- `methodName_condition_expectedOutcome`
- Or BDD style: `givenX_whenY_thenZ`

### Arrange-Act-Assert (AAA)

- Arrange: set up fixtures and stubs
- Act: call unit under test
- Assert: verify results + interactions (only meaningful interactions)

## JUnit 5 patterns

- Use `@Nested` to group scenarios.
- Use `@ParameterizedTest` for data-driven cases.
- Use `@Tag("fast")` / `@Tag("unit")` for test selection.
- Prefer constructor injection for dependencies in production; for tests use explicit setup.

## Mockito patterns

- Prefer `MockitoExtension` for clean initialization.
- Prefer stubbing only what matters; avoid over-specifying interactions.
- Use argument matchers carefully: if any matcher is used, all args must use matchers.

## Coverage expectations (pragmatic)

- Coverage is a signal, not a goal.
- Use JaCoCo to prevent “no tests” regressions:
  - enforce minimum line/branch coverage at module level
  - exclude generated code and DTOs if appropriate (document exclusions)

## Procedure (step-by-step)

### Step 1 — Identify the unit boundary

- Choose a single class (or small cluster) as unit under test.
- Replace dependencies with fakes/mocks.
- Ensure no I/O is reachable.

### Step 2 — Write regression test first (for bug fixes)

- Reproduce the bug with minimal inputs.
- Assert the incorrect behavior (pre-fix) → then implement fix.

### Step 3 — Add parameterized tests for edge cases

- Null/empty inputs
- boundary values (0, 1, max)
- invalid formats
- concurrency-sensitive invariants (if applicable)

### Step 4 — Apply Mockito discipline

- Stub only required calls.
- Verify only meaningful side effects.
- Prefer state assertions over interaction assertions when possible.

### Step 5 — Add coverage gate

- Configure JaCoCo to fail build if coverage falls below baseline.
- Keep thresholds realistic; raise gradually.

## Output / Artifacts

- `src/test/java/...` unit tests for changed classes
- `build.gradle` or `pom.xml` with JUnit 5 + (optional) Mockito + JaCoCo
- Regression tests for each fixed bug

## Definition of Done (DoD)

- [ ] New feature has unit tests for core paths and edge cases.
- [ ] Bug fix includes a regression test that fails before fix and passes after.
- [ ] Tests are deterministic and do not touch network/DB.
- [ ] Coverage gate is configured (or documented why not).
- [ ] Tests are readable and grouped logically.

## Guardrails (What NOT to do)

- Never mock the unit under test.
- Avoid brittle tests that assert exact log messages or internal implementation details.
- Avoid sleeping/time-based waits; inject Clock instead.
- Avoid massive fixture builders that hide intent.

## Templates

### JUnit 5 test skeleton

```java
@Tag("unit")
class FooServiceTest {

  @Nested
  class WhenInputIsInvalid {
    @Test
    void getFoo_emptyId_throws() {
      // Arrange
      FooService svc = new FooService(/* deps */);

      // Act + Assert
      assertThrows(IllegalArgumentException.class, () -> svc.getFoo(""));
    }
  }
}
```

### Mockito + JUnit 5 skeleton

```java
@ExtendWith(MockitoExtension.class)
class PaymentServiceTest {

  @Mock PaymentRepository repo;
  @Mock Clock clock;

  @InjectMocks PaymentService service;

  @Test
  void pay_validCommand_persistsAndReturnsReceipt() {
    when(repo.save(any())).thenReturn(savedPayment());

    Receipt r = service.pay(cmd());

    assertEquals(Status.PAID, r.status());
    verify(repo).save(any());
  }
}
```

### Gradle (JaCoCo gate) sketch

- Add JaCoCo plugin
- Configure jacocoTestReport
- Configure jacocoTestCoverageVerification with minimums
- Wire check to depend on verification task

### Common failure modes & fixes

- Symptom: flaky tests → Cause: time/randomness → Fix: inject Clock/Random.
- Symptom: tests break on refactor → Cause: over-verification → Fix: assert outputs, reduce interaction assertions.
- Symptom: slow test suite → Cause: accidental I/O → Fix: enforce “no I/O in unit tests”, move to integration tests.

### References

- Use official JUnit Jupiter user guide for annotations and lifecycle.
- Use Mockito Javadoc for matchers, strictness, and extension usage.
- Use JaCoCo and build tool docs for coverage configuration.
