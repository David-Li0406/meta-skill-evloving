---
name: ios-testing-strategy
description: Use this skill for comprehensive iOS testing strategies, including unit, integration, and UI testing with XCTest/XCUITest, focusing on reliability and automation.
---

# iOS Testing Strategy — Comprehensive Guide

This skill provides a structured approach to iOS testing using XCTest and XCUITest, emphasizing layered testing strategies, determinism, and automation.

## Core Testing Layers

### Testing Types

- **Unit Tests**: Focus on pure business logic, formatting, and state machines. Fast and deterministic.
- **Snapshot Tests**: Used for view rendering regressions; apply sparingly and review diffs.
- **Integration Tests**: Validate interactions between components, such as persistence and networking.
- **UI Tests (XCUITest)**: Target critical user journeys; keep these tests thin and focused.

## Device Matrix

### Simulator vs Real Devices

- **Simulators**: Use for PR gates and initial testing.
- **Real Devices**: Reserve for nightly builds and release validation.
- **Matrix Strategy**: Include one small phone, one large phone, and one iPad if applicable. Limit OS versions to those actively supported.

## UI Test Flake Control

### Ensuring Determinism

- **Disable Animations**: Limit or disable animations in test builds.
- **Control Time**: Use fixed time zones and locales; avoid wall-clock dependencies.
- **Stub Network Calls**: Stub at the boundary to avoid third-party dependencies.
- **Manage Permissions**: Set predictable permission states to avoid manual prompts.
- **Isolation**: Reset app state between tests to prevent shared state issues.

## CI/CD Integration

### Best Practices

- **PR Gate**: Implement a small smoke UI suite alongside unit and integration tests.
- **Collect Artifacts**: Gather `xcresult` bundles, screenshots, and logs on failure for easier debugging.
- **Fail Fast**: Assert early on navigation and state to avoid timeouts.

## Quick Reference Commands

| Task | Command | When to Use |
|------|---------|-------------|
| List simulators | `xcrun simctl list devices` | Check available devices |
| Boot simulator | `xcrun simctl boot "iPhone 16"` | Start simulator |
| Build app | `xcodebuild build` | Compile iOS app |
| Install app | `xcrun simctl install booted app.app` | Deploy to simulator |
| Run tests | `xcodebuild test` | Execute XCTest suite |
| Take screenshot | `xcrun simctl io booted screenshot` | Capture screen |
| Record video | `xcrun simctl io booted recordVideo` | Record session |

## XCTest Patterns

### Decision Trees for Testing

#### Test Type Selection

```
What are you testing?
├─ Pure business logic (no I/O, no UI)
│  └─ Unit test
├─ Component interactions (services, repositories)
│  └─ Integration test
├─ User-visible behavior
│  └─ Does it require visual verification?
│     ├─ YES → Snapshot test or manual QA
│     └─ NO → UI test (XCUITest)
└─ Performance characteristics
   └─ Performance test
```

#### Mock vs Stub vs Spy

```
What do you need from the test double?
├─ Just return canned data
│  └─ Stub
├─ Verify interactions (was method called?)
│  └─ Spy
└─ Both return data AND verify calls
   └─ Mock
```

### Essential Patterns

#### Structured Mock with Spy

```swift
final class MockUserService: UserServiceProtocol {
    var stubbedUser: User?
    var stubbedError: Error?
    private(set) var fetchUserCallCount = 0
    private(set) var fetchUserLastId: String?

    func fetchUser(id: String) async throws -> User {
        fetchUserCallCount += 1
        fetchUserLastId = id
        if let error = stubbedError { throw error }
        guard let user = stubbedUser else { throw MockError.notConfigured }
        return user
    }
}
```

#### ViewModel Test Pattern

```swift
@MainActor
final class UserViewModelTests: XCTestCase {
    var sut: UserViewModel!
    var mockService: MockUserService!

    override func setUp() {
        super.setUp()
        mockService = MockUserService()
        sut = UserViewModel(userService: mockService)
    }

    override func tearDown() {
        sut = nil
        mockService = nil
        super.tearDown();
    }

    func testInitialState() {
        XCTAssertNil(sut.user)
        XCTAssertFalse(sut.isLoading)
        XCTAssertNil(sut.errorMessage)
    }
}
```

## Automated Screenshot and Recording

### Capture Screenshots

```bash
xcrun simctl io booted screenshot screenshot.png
```

### Record Video

```bash
xcrun simctl io booted recordVideo recording.mov
```

## CI/CD Integration Example

### GitHub Actions

```yaml
name: iOS Build and Test
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: macos-15
    steps:
      - uses: actions/checkout@v4
      - name: Build
        run: |
          xcodebuild build -scheme MyApp -sdk iphonesimulator -destination 'platform=iOS Simulator,name=iPhone 16'
      - name: Test
        run: |
          xcodebuild test -scheme MyApp -sdk iphonesimulator -destination 'platform=iOS Simulator,name=iPhone 16'
```

## Conclusion

Use this skill to implement a robust iOS testing strategy that encompasses unit, integration, and UI testing, ensuring high reliability and automation in your testing processes.