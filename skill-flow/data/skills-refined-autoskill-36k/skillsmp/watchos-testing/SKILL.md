---
name: watchos-testing
description: watchOS and iOS testing expert for unit tests, UI tests, and test-driven development. Use when working with XCTest, testing SwiftUI views, testing WatchKit components, or implementing test strategies for watch apps.
allowed-tools: Read, Grep, Glob, Bash(xcodebuild:*), Bash(xcrun simctl:*)
---

# watchOS Testing Expert

## Instructions

When helping with watchOS/iOS testing:

1. Analyze existing test coverage
2. Identify untested code paths
3. Generate comprehensive test cases
4. Use XCTest and Swift Testing frameworks appropriately

## watchOS-Specific Testing

### Challenges
- Limited UI testing on watchOS
- Notification testing requires mocking
- WebSocket testing needs stub servers
- Complication testing is complex

### Approaches
- Use dependency injection for testability
- Mock network services (WebSocket, APNs)
- Test view models separately from views
- Use `@testable import` for internal access

## Test Patterns

### Unit Test Template
```swift
import XCTest
@testable import ClaudeWatch

final class WatchServiceTests: XCTestCase {
    var sut: WatchService!

    override func setUp() {
        super.setUp()
        sut = WatchService()
    }

    override func tearDown() {
        sut = nil
        super.tearDown()
    }

    func testExample() {
        // Given
        // When
        // Then
        XCTAssertNotNil(sut)
    }
}
```

### Async Test Pattern
```swift
func testAsyncOperation() async throws {
    // Given
    let expectation = XCTestExpectation(description: "Async operation")

    // When
    let result = try await sut.performAsyncAction()

    // Then
    XCTAssertTrue(result)
}
```

## Best Practices
- Test behavior, not implementation details
- Use dependency injection for all external services
- Mock WebSocket connections for network tests
- Target 80%+ coverage for critical paths (Services, ViewModels)
- Use `@MainActor` annotation for UI-related tests
