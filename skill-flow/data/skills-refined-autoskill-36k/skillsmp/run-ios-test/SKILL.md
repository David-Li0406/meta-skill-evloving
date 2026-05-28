---
name: run-ios-test
description: Run iOS unit tests for the AIQ project. Supports running all tests, a specific test file, or a specific test method. Use this skill whenever you need to verify iOS code changes or run the test suite.
allowed-tools: Bash
---

# Run iOS Test Skill

This skill runs iOS unit tests for the AIQ project using `xcodebuild`.

## Usage

When this skill is invoked, determine what tests to run based on the user's request or the context.

### Run All Tests

If no specific test is requested, run the full test suite:

```bash
cd /Users/mattgioe/aiq/ios && xcodebuild test -project AIQ.xcodeproj -scheme AIQ -destination 'platform=iOS Simulator,name=iPhone 16,OS=18.3.1' 2>&1
```

### Run a Specific Test File

To run tests from a specific test class, use the `-only-testing` flag:

```bash
cd /Users/mattgioe/aiq/ios && xcodebuild test -project AIQ.xcodeproj -scheme AIQ -destination 'platform=iOS Simulator,name=iPhone 16,OS=18.3.1' -only-testing:AIQTests/TestClassName 2>&1
```

**Examples:**
```bash
# Run AuthManagerTests
-only-testing:AIQTests/AuthManagerTests

# Run APIClientTests
-only-testing:AIQTests/APIClientTests

# Run NotificationServiceTests
-only-testing:AIQTests/NotificationServiceTests
```

### Run a Specific Test Method

To run a single test method within a class:

```bash
cd /Users/mattgioe/aiq/ios && xcodebuild test -project AIQ.xcodeproj -scheme AIQ -destination 'platform=iOS Simulator,name=iPhone 16,OS=18.3.1' -only-testing:AIQTests/TestClassName/testMethodName 2>&1
```

**Example:**
```bash
-only-testing:AIQTests/AuthManagerTests/testLoginSuccess
```

### Run Multiple Test Files

Chain multiple `-only-testing` flags to run several test classes:

```bash
cd /Users/mattgioe/aiq/ios && xcodebuild test -project AIQ.xcodeproj -scheme AIQ -destination 'platform=iOS Simulator,name=iPhone 16,OS=18.3.1' -only-testing:AIQTests/AuthManagerTests -only-testing:AIQTests/APIClientTests 2>&1
```

## Common Test Classes

| Test Class | Tests For |
|------------|-----------|
| `AuthManagerTests` | Authentication logic |
| `APIClientTests` | API client functionality |
| `NotificationServiceTests` | Push notification handling |
| `AnalyticsServiceTests` | Analytics tracking |
| `KeychainServiceTests` | Keychain operations |
| `DashboardViewModelTests` | Dashboard view model |

## Arguments

When invoked with arguments, parse them to determine the test scope:

- **No arguments**: Run all tests
- **Class name** (e.g., `AuthManagerTests`): Run that test class
- **Class/method** (e.g., `AuthManagerTests/testLogin`): Run that specific test

## Interpreting Results

- **Test Succeeded**: All tests passed
- **Test Failed**: Check the output for failing test names and assertion failures
- **Build Failed**: Compilation errors prevent tests from running; fix build errors first

## Troubleshooting

### Simulator Not Found
If the destination simulator isn't available, list available simulators:
```bash
xcrun simctl list devices available
```

Then adjust the `-destination` parameter accordingly.

### Tests Timeout
For long-running tests, consider adding `-test-timeouts-enabled NO` or increasing the default timeout.
