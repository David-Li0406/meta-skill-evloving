---
name: swift-testing-guidelines
description: Use when writing tests for Swift StateTree - ensures proper Swift Testing framework usage
---

# Swift Testing Guidelines

## Overview

Guidelines for writing tests using Swift Testing framework (Swift 6's new testing framework, not XCTest).

**Announce at start:** "I'm using the swift-testing-guidelines skill to write proper tests."

## When to Use

- Writing unit tests
- Adding tests for new features
- Reviewing test code
- Ensuring test quality

## Framework: Swift Testing

**Important:** Swift StateTree uses **Swift Testing** (Swift 6's new testing framework), **NOT XCTest**.

### Key Differences from XCTest

- Use `@Test` attribute instead of `func test...()`
- Use `#expect()` instead of `XCTAssert*`
- Use `Issue.record()` for test failures
- Test functions can have descriptive names

## Test Module Organization

Tests are organized by module:

- **SwiftStateTreeTests**: Core library tests
- **SwiftStateTreeTransportTests**: Transport layer tests
- **SwiftStateTreeHummingbirdTests**: Hummingbird integration tests
- **SwiftStateTreeMacrosTests**: Macro tests
- **SwiftStateTreeMatchmakingTests**: Matchmaking service tests
- **SwiftStateTreeDeterministicMathTests**: Deterministic math tests

## Test File Structure

### File Naming

- Test files should be suffixed with `*Tests.swift`
- Match the type under test (e.g., `StateTreeTests.swift`)

### Test Function Structure

**Basic test:**
```swift
import Testing

@Test("Description of what is being tested")
func testBasicFunctionality() {
    let result = functionUnderTest()
    #expect(result == expectedValue)
}
```

**Test with setup/teardown:**
```swift
@Test("Test with setup and assertions")
func testWithSetup() {
    // Arrange
    let input = createTestInput()
    
    // Act
    let result = functionUnderTest(input)
    
    // Assert
    #expect(result.isValid)
    #expect(result.value == expectedValue)
}
```

## Test Attributes

### @Test Attribute

**Basic usage:**
```swift
@Test
func testSomething() {
    // ...
}
```

**With description:**
```swift
@Test("Verifies that state sync works correctly")
func testStateSync() {
    // ...
}
```

**With arguments:**
```swift
@Test(arguments: [1, 2, 3, 4, 5])
func testWithNumber(_ number: Int) {
    #expect(number > 0)
}
```

### Expectations

**Basic expectation:**
```swift
#expect(condition)
```

**Equality:**
```swift
#expect(actual == expected)
```

**Inequality:**
```swift
#expect(actual != expected)
```

**Comparison:**
```swift
#expect(value > threshold)
#expect(value < limit)
```

**Optional unwrapping:**
```swift
#expect(optional != nil)
let value = #require(optional)  // Unwraps or fails test
```

### Issue Recording

**Record test failure:**
```swift
if condition {
    Issue.record("Condition not met: \(reason)")
}
```

## Arrange-Act-Assert Pattern

**Structure tests with clear sections:**
```swift
@Test("Test state update propagation")
func testStateUpdate() {
    // Arrange
    let initialState = createInitialState()
    let syncEngine = SyncEngine()
    
    // Act
    let update = try syncEngine.generateDiff(
        for: playerID,
        from: initialState
    )
    
    // Assert
    #expect(update.patches.count > 0)
    #expect(update.type == .diff)
}
```

## Test Organization

### Group Related Tests

```swift
struct StateTreeTests {
    @Test("Initial state is empty")
    func testInitialState() {
        // ...
    }
    
    @Test("State update creates patches")
    func testStateUpdate() {
        // ...
    }
    
    @Test("State sync includes all fields")
    func testStateSync() {
        // ...
    }
}
```

### Use Descriptive Names

**Good:**
```swift
@Test("State sync includes broadcast fields for all players")
func testBroadcastFieldsIncluded() {
    // ...
}
```

**Bad:**
```swift
@Test
func test1() {
    // ...
}
```

## Test Coverage Requirements

### When Adding Tests

- **Public APIs**: Always add tests
- **Core game logic**: Always add tests
- **Concurrency paths**: Aim to cover
- **Edge cases**: Include when relevant

### Before Submitting PRs

- ✅ All `swift test` must pass
- ✅ All E2E tests must pass
- ✅ No linter errors
- ✅ Code comments in English

## Running Tests

### Run All Tests
```bash
swift test
```

### Run Specific Test
```bash
swift test --filter StateTreeTests.testGetSyncFields
```

### List All Tests
```bash
swift test list
```

### Run Tests in Release Mode
```bash
swift test -c release
```

## Test Best Practices

### 1. Keep Tests Independent

- Don't share mutable state between tests
- Each test should be able to run in isolation
- Use setup/teardown if needed

### 2. Test One Thing

- Each test should verify one behavior
- If testing multiple things, use multiple tests
- Keep tests focused and clear

### 3. Use Descriptive Assertions

**Good:**
```swift
#expect(result.count == expectedCount, "Expected \(expectedCount) items, got \(result.count)")
```

**Bad:**
```swift
#expect(result.count == expectedCount)
```

### 4. Test Edge Cases

- Empty inputs
- Nil values
- Boundary conditions
- Error conditions

### 5. Avoid Test Implementation Details

- Test public APIs, not internal methods
- Focus on behavior, not implementation
- Don't test private methods directly

## Common Patterns

### Testing Async Code

```swift
@Test("Async operation completes")
func testAsyncOperation() async throws {
    let result = try await asyncFunction()
    #expect(result != nil)
}
```

### Testing Throwing Functions

```swift
@Test("Function throws on invalid input")
func testThrowsOnInvalidInput() {
    #expect(throws: SomeError.self) {
        try functionThatThrows(invalidInput)
    }
}
```

### Testing Collections

```swift
@Test("Collection contains expected items")
func testCollection() {
    let items = createItems()
    #expect(items.count == 3)
    #expect(items.contains(expectedItem))
}
```

## Integration with Other Testing

### WebClient Tests

**Location:** `Examples/HummingbirdDemo/WebClient`

**Command:**
```bash
cd Examples/HummingbirdDemo/WebClient && npm test
```

**Framework:** Vitest (for Vue component and business logic tests)

### E2E Tests

**Location:** `Tools/CLI`

**Command:**
```bash
cd Tools/CLI && npm test
```

**See:** `SwiftStateTree/run-e2e-tests` skill for details

## Test Anti-Patterns to Avoid

### ❌ Don't Use XCTest

```swift
// ❌ DON'T DO THIS
import XCTest

class StateTreeTests: XCTestCase {
    func testSomething() {
        XCTAssertEqual(actual, expected)
    }
}
```

### ❌ Don't Share Mutable State

```swift
// ❌ DON'T DO THIS
var sharedState = State()

@Test
func test1() {
    sharedState.value = 1  // Affects other tests!
}

@Test
func test2() {
    #expect(sharedState.value == 0)  // May fail due to test1
}
```

### ❌ Don't Test Implementation Details

```swift
// ❌ DON'T DO THIS
@Test
func testInternalMethod() {
    let result = object.internalMethod()  // Testing private API
    #expect(result == expected)
}
```

## Code Review Checklist

When reviewing test code:

- [ ] Uses `@Test` attribute (not XCTest)
- [ ] Uses `#expect()` for assertions
- [ ] Test file named `*Tests.swift`
- [ ] Tests organized by type under test
- [ ] Descriptive test names
- [ ] Arrange-Act-Assert structure
- [ ] No shared mutable state
- [ ] Tests are independent
- [ ] Edge cases covered
- [ ] Public APIs tested
