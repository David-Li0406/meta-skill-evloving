---
name: java-testing-integration
description: Design and implement deterministic integration tests (DB/queue/external IO) using Testcontainers-style thinking, with a fixture strategy and CI-friendly execution. Use when IO/DB bugs, wiring issues, or production-only behavior must be reproduced.
license: CC-BY-4.0
compatibility:
  jdk: "17+ (recommended 21)"
  build: "Maven or Gradle"
  test: "JUnit 5 (preferred)"
metadata:
  owner: backend-platform
  version: "0.1.0"
  tags: [java, testing, integration, testcontainers, ci]
---

# Java Integration Testing (Reproducible, CI-Friendly)

## Why this skill exists

Integration tests catch failures that unit tests cannot: incorrect wiring, serialization/deserialization, transaction boundaries, connection pool settings, schema drift, message ack/retry behavior, and “works on my machine” config issues.

The goal is NOT to replace unit tests. The goal is to:

- Reproduce IO/DB/queue bugs deterministically
- Validate runtime wiring (config, DI, modules, migrations)
- Provide confidence that changes remain deployable

## Scope

### In scope

- Integration tests for:
  - SQL/NoSQL DB interactions (schema + queries + transactions)
  - Message broker interactions (publish/consume at a boundary level)
  - HTTP client integration with a fake/stub server (WireMock-like thinking)
  - Persistence + serialization + config binding behavior
- Testcontainers-style isolation, ephemeral infra, reproducible setup/teardown
- Fixture strategy (data builders, seed scripts, migrations, reset strategy)
- CI performance and flake-proofing

### Out of scope

- Full end-to-end testing across multiple real services in a shared environment
- Load/performance testing (see `java-load-testing`)
- Security penetration or exploit workflows (see `java-security-audit` for defensive review)

## When to use (Triggers)

- “It fails only in staging/prod”
- “Works locally but fails in CI”
- Bugs involving:
  - transactions / isolation levels / deadlocks
  - schema migrations / SQL differences
  - connection pooling / timeouts
  - message redelivery / ordering / duplicates
- You need a regression test for a production incident that involved IO.

## Required inputs (Context to request/collect)

- Build tool: Maven/Gradle
- Test framework: JUnit 5 (preferred)
- Runtime stack hints:
  - DB type + version (Postgres/MySQL/Mongo/etc.)
  - Broker type + version (Kafka/RabbitMQ/etc.)
- App config entry points:
  - how config is loaded (env vars, properties, yaml)
  - how DB/broker urls are injected
- CI constraints:
  - max test time budget
  - whether Docker is available in CI runners

## Core principles (Non-negotiables)

1) Determinism over realism  
   - “Real enough to catch the bug” is the target, not “simulate production perfectly”.
2) Isolation by default  
   - No shared dev DB, no shared staging topics, no reliance on external services.
3) Minimize flakiness  
   - Avoid timing sleeps; use waits, health checks, and bounded timeouts.
4) Keep it fast  
   - Integration tests should be fewer than unit tests and run in reasonable time.

## Test design: the 3-layer model

### Layer A: Pure unit tests

- No IO. Fast. Most coverage lives here.

### Layer B: “Narrow integration tests”

- One integration boundary at a time:
  - repository ↔ DB
  - publisher ↔ broker
  - client ↔ stub server
- This is your default integration layer.

### Layer C: “Slice tests” / module wiring tests

- Validate module wiring and config, but still isolate external dependencies via containers/stubs.

## Container strategy (Testcontainers-style)

### Container lifetime

Prefer “one container per test class / per suite”:

- Start container once, reuse across test methods
- Reset data between tests (truncate tables / recreate schema / transactional rollback)
- This is typically faster than per-test containers

### Networking & reachability

- Containers should be reachable from tests running on host.
- When multi-container scenarios are needed, use a shared network and stable aliases.

### Version pinning

- Pin container images (avoid “latest”).
- Document why a version is chosen and how to upgrade safely.

## Fixture strategy (Make tests readable and maintainable)

Pick ONE of the following and be consistent:

### Option 1: Migration-first + seed scripts

- Run schema migrations on startup (preferred)
- Seed minimal reference data via SQL scripts or migration “baseline data”
- For each test: insert test-specific rows + cleanup

### Option 2: Programmatic builders

- Use “Test Data Builders” (factory methods) to create domain objects
- Persist through repositories (closer to real app behavior)
- Cleanup through explicit teardown or truncation

### Option 3: Snapshot fixtures (use sparingly)

- Predefined dataset snapshots loaded into DB
- Risk: harder to evolve, can become brittle

## Reset strategy (Pick a reset mechanism)

- If DB supports transactions and app boundaries allow:
  - wrap each test in a transaction and roll back
- Otherwise:
  - truncate relevant tables between tests (fast for relational)
  - or recreate schema for each class (slower but simpler)

## Implementation checklist (Step-by-step)

1) Create test source layout
   - `src/test/java/...`
   - `src/test/resources/...` (sql seeds, config overrides)
2) Add dependencies
   - JUnit 5
   - Testcontainers core + module for your DB/broker
3) Implement container bootstrap
   - Prefer static container per class
   - Expose connection info to the app under test (env vars / system props / config injection)
4) Implement health + readiness checks
   - Avoid arbitrary sleeps
   - Use bounded waits and timeouts
5) Write the test with AAA structure
   - Arrange: set fixtures
   - Act: call the boundary
   - Assert: verify state (DB rows, messages, outputs)
6) Add failure diagnostics
   - On failure, log:
     - container logs (bounded)
     - effective config (redact secrets)
     - SQL statements if relevant (optional)
7) Make it CI-friendly
   - Ensure tests run headless
   - Keep timeouts appropriate
   - Ensure Docker availability in CI or provide a fallback profile

## Example: JUnit 5 + Postgres container (framework-agnostic pseudo-code)

```java
@Testcontainers
class UserRepositoryIT {

  @Container
  static PostgreSQLContainer<?> postgres =
      new PostgreSQLContainer<>("postgres:16.2")
          .withDatabaseName("testdb")
          .withUsername("test")
          .withPassword("test");

  @BeforeAll
  static void init() {
    System.setProperty("DB_URL", postgres.getJdbcUrl());
    System.setProperty("DB_USER", postgres.getUsername());
    System.setProperty("DB_PASS", postgres.getPassword());
    // Run migrations here if your framework doesn't auto-run them.
  }

  @BeforeEach
  void reset() {
    // truncate tables or reset fixtures
  }

  @Test
  void savesAndLoadsUser() {
    // Arrange
    var user = new User("u1", "huy@example.com");
    // Act
    repo.save(user);
    var loaded = repo.findById("u1");
    // Assert
    assertThat(loaded).isPresent();
    assertThat(loaded.get().email()).isEqualTo("huy@example.com");
  }
}
```

### Definition of Done (DoD)

- [] Test is deterministic (no sleeps; bounded waits)

- [] Test can run on a clean machine with only Docker + JDK

- [] Test cleans up after itself (no state leakage)

- [] Test runtime is within budget (document budget)

- [] Failure output includes enough diagnostics to debug

- []Added regression coverage for the original incident/bug

### Guardrails (What NOT to do)

- Never depend on:

  - shared dev databases

  - real staging brokers

  - external internet services

- Never commit secrets into test configs

- Avoid:

  - random ports without discovery

  - time-based sleeps for readiness

  - “mega integration test” covering 10 subsystems in one test

### Common failure modes & fixes

- Flaky startup → readiness checks missing → add health wait + extend startup timeout

- CI fails, local passes → Docker not available / resources limited → adjust CI runner or mark tests as “requires docker”

- Slow tests → per-test container startup → switch to per-class containers + truncation reset

- Data collisions → shared fixtures → generate unique ids + isolate test data

### Outputs / Artifacts

- `src/test/java/**/...IT.java` integration tests

- `src/test/resources/` seed scripts or fixture configs

- CI job updates:

  - ensure docker enabled

  - split unit vs integration stage if needed

Optional:

- `docs/testing/integration-testing.md` runbook

### References (official docs)

- Testcontainers for Java docs: [https://java.testcontainers.org/](https://java.testcontainers.org/)

- JUnit 5 docs: [https://junit.org/junit5/docs/current/user-guide/](https://junit.org/junit5/docs/current/user-guide/)
