# TDD Test Patterns (Chicago School)

We follow **Chicago school TDD** (state-based testing):

| Chicago School (We Use This)          | London School (Avoid)                    |
|---------------------------------------|------------------------------------------|
| Test state changes and return values  | Test interactions between objects        |
| Mocks stub data, not verify calls     | Mocks verify method calls were made      |
| Focus on "what" (outcomes)            | Focus on "how" (behavior)                |
| Design emerges from tests             | Design upfront, tests verify design      |
| Fewer, coarser-grained tests          | Many fine-grained interaction tests      |

## Swift Testing Framework

Use `@Test` and `@Suite` instead of XCTest:

```swift
import Testing
import Foundation
@testable import Domain

@Suite
struct UsageQuotaTests {
    @Test func `quota at zero percent is depleted`() {
        let quota = UsageQuota(percentRemaining: 0, quotaType: .session, providerId: "test")
        #expect(quota.status == .depleted)
        #expect(quota.isDepleted == true)
    }
}
```

## Given-When-Then Structure

```swift
@Test func `quota between 20 and 50 percent shows warning`() {
    // Given
    let quota = UsageQuota(percentRemaining: 35, quotaType: .session, providerId: "claude")

    // When
    let status = quota.status

    // Then
    #expect(status == .warning)
}
```

## Mocking with @Mockable (Chicago Style)

Define mockable protocols for external dependencies:

```swift
import Mockable

@Mockable
public protocol UsageProbe: Sendable {
    func probe() async throws -> UsageSnapshot
    func isAvailable() async -> Bool
}

@Mockable
public protocol CLIExecutor: Sendable {
    func execute(_ command: String, timeout: TimeInterval) async throws -> CLIResult
    func locateBinary(named: String) async -> URL?
}
```

**Chicago school mock usage** - stub return values, verify resulting state:

```swift
import Mockable

@Suite
struct QuotaMonitorTests {
    @Test func `monitor can refresh a provider by ID`() async throws {
        // Given - STUB dependencies to return data
        let probe = MockUsageProbe()
        given(probe).isAvailable().willReturn(true)
        given(probe).probe().willReturn(UsageSnapshot(
            providerId: "claude",
            quotas: [UsageQuota(percentRemaining: 65, quotaType: .session, providerId: "claude")],
            capturedAt: Date()
        ))
        let provider = ClaudeProvider(probe: probe)
        let monitor = QuotaMonitor(providers: [provider])

        // When
        await monitor.refresh(providerId: "claude")

        // Then - verify STATE, not that methods were called
        #expect(provider.snapshot != nil)
        #expect(provider.snapshot?.quotas.count == 1)
        // ❌ AVOID: verify(probe).probe().called(1)  // London school - don't do this
    }
}
```

**Key principle**: Use `given().willReturn()` to stub data. Avoid `verify().called()` for interactions.

## Parsing Tests

Test parsing logic separately from behavior:

```swift
@Suite
struct ClaudeUsageProbeParsingTests {
    static let sampleOutput = """
        Session: 65% remaining
        Weekly: 35% remaining
        Resets: 11am
        """

    @Test func `parses session quota from CLI output`() throws {
        let data = Data(Self.sampleOutput.utf8)
        let snapshot = try ClaudeUsageProbe.parseResponse(data, providerId: "claude")

        #expect(snapshot.quotas.count >= 1)
        #expect(snapshot.quota(for: .session)?.percentRemaining == 65)
    }

    @Test func `handles missing data gracefully`() throws {
        let data = Data("Invalid output".utf8)

        #expect(throws: ProbeError.parseFailed) {
            try ClaudeUsageProbe.parseResponse(data, providerId: "claude")
        }
    }
}
```

## Async Test Patterns

```swift
@Test func `probe returns snapshot on success`() async throws {
    // Given
    let mockExecutor = MockCLIExecutor()
    given(mockExecutor).execute(any(), timeout: any()).willReturn(
        CLIResult(output: "65% remaining", exitCode: 0)
    )
    let probe = ClaudeUsageProbe(cliExecutor: mockExecutor)

    // When
    let snapshot = try await probe.probe()

    // Then
    #expect(snapshot.providerId == "claude")
}

@Test func `probe throws when unavailable`() async {
    // Given
    let mockExecutor = MockCLIExecutor()
    given(mockExecutor).locateBinary(named: any()).willReturn(nil)
    let probe = ClaudeUsageProbe(cliExecutor: mockExecutor)

    // When/Then
    await #expect(throws: ProbeError.cliNotFound) {
        try await probe.probe()
    }
}
```

## Test Organization

```
Tests/
├── DomainTests/
│   ├── Provider/
│   │   ├── UsageQuotaTests.swift      # Domain model behavior
│   │   ├── QuotaStatusTests.swift     # Enum behavior
│   │   └── UsageSnapshotTests.swift   # Aggregate behavior
│   └── Monitor/
│       └── QuotaMonitorTests.swift    # Actor behavior
└── InfrastructureTests/
    └── CLI/
        ├── ClaudeUsageProbeParsingTests.swift  # Parsing logic
        └── ClaudeUsageProbeTests.swift         # Probe behavior
```

## Running Tests

```bash
# Run all tests
swift test

# Run specific test file
swift test --filter DomainTests

# Run specific test
swift test --filter "UsageQuotaTests/quota at zero percent is depleted"
```

## Chicago School Summary

### What to Test

| Test Type           | What to Assert                                    |
|---------------------|---------------------------------------------------|
| Domain models       | Computed properties, state after mutations        |
| Services/Probes     | Return values, thrown errors, resulting state     |
| Actors              | State after operations complete                   |

### What NOT to Test

- That a method was called N times
- The order of internal method calls
- Implementation details that don't affect observable state

### Red-Green-Refactor Cycle

```
1. RED    - Write a failing test that asserts expected STATE
2. GREEN  - Write minimal code to make the test pass
3. REFACTOR - Improve code while keeping tests green
```

Design emerges from this cycle - don't design upfront, let tests guide you.