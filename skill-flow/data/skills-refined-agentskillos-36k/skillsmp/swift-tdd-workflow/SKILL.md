---
name: swift-tdd-workflow
description: Swift TDD workflow with XCTest and Swift Testing. NOT for Jest/Vitest or JavaScript testing.
---

# Swift Test-Driven Development Workflow

This skill ensures all Swift development follows TDD principles with comprehensive test coverage.

## When to Activate

- Writing new features or functionality
- Fixing bugs or issues
- Refactoring existing code
- Adding API endpoints
- Creating new views or view models

## Core Principles

### 1. Tests BEFORE Code
ALWAYS write tests first, then implement code to make tests pass.

### 2. Coverage Requirements
- Minimum 80% coverage (unit + integration + UI)
- All edge cases covered
- Error scenarios tested
- Boundary conditions verified

### 3. Test Types

#### Unit Tests
- Individual functions and methods
- View model logic
- Pure functions
- Utilities and extensions

#### Integration Tests
- API client operations
- Database operations
- Service interactions

#### UI Tests (XCUITest)
- Critical user flows
- Complete workflows
- User interactions

## TDD Workflow Steps

### Step 1: Write User Journeys
```
As a [role], I want to [action], so that [benefit]

Example:
As a user, I want to search for markets,
so that I can find relevant markets quickly.
```

### Step 2: Generate Test Cases
For each user journey, create comprehensive test cases:

```swift
final class MarketSearchTests: XCTestCase {
    func test_search_returnsRelevantMarkets() async throws {
        // Test implementation
    }

    func test_search_handlesEmptyQueryGracefully() async throws {
        // Test edge case
    }

    func test_search_returnsEmptyArrayWhenNoMatches() async throws {
        // Test fallback behavior
    }

    func test_search_sortsByRelevanceScore() async throws {
        // Test sorting logic
    }
}
```

### Step 3: Run Tests (They Should Fail)
```bash
swift test
# or
xcodebuild test -scheme MyApp -destination 'platform=iOS Simulator,name=iPhone 15'
```

### Step 4: Implement Code
Write minimal code to make tests pass:

```swift
// Implementation guided by tests
func searchMarkets(query: String) async throws -> [Market] {
    // Implementation here
}
```

### Step 5: Run Tests Again
```bash
swift test
# Tests should now pass
```

### Step 6: Refactor
Improve code quality while keeping tests green:
- Remove duplication
- Improve naming
- Optimize performance
- Enhance readability

### Step 7: Verify Coverage
```bash
swift test --enable-code-coverage
# or use Xcode's coverage report
```

## XCTest Patterns

### Basic Test Structure (AAA Pattern)

```swift
import XCTest
@testable import MyApp

final class CalculatorTests: XCTestCase {

    // System Under Test
    var sut: Calculator!

    override func setUp() {
        super.setUp()
        sut = Calculator()
    }

    override func tearDown() {
        sut = nil
        super.tearDown()
    }

    func test_add_twoPositiveNumbers_returnsSum() {
        // Arrange
        let a = 5
        let b = 3

        // Act
        let result = sut.add(a, b)

        // Assert
        XCTAssertEqual(result, 8)
    }

    func test_divide_byZero_throwsError() {
        // Arrange
        let a = 10
        let b = 0

        // Act & Assert
        XCTAssertThrowsError(try sut.divide(a, by: b)) { error in
            XCTAssertEqual(error as? CalculatorError, .divisionByZero)
        }
    }
}
```

### Async Test Pattern

```swift
final class MarketServiceTests: XCTestCase {

    var sut: MarketService!
    var mockAPIClient: MockAPIClient!

    override func setUp() {
        super.setUp()
        mockAPIClient = MockAPIClient()
        sut = MarketService(apiClient: mockAPIClient)
    }

    func test_fetchMarkets_returnsMarketsFromAPI() async throws {
        // Arrange
        let expectedMarkets = [Market.mock(), Market.mock()]
        mockAPIClient.marketsToReturn = expectedMarkets

        // Act
        let markets = try await sut.fetchMarkets()

        // Assert
        XCTAssertEqual(markets.count, 2)
        XCTAssertEqual(markets, expectedMarkets)
    }

    func test_fetchMarkets_whenAPIFails_throwsError() async {
        // Arrange
        mockAPIClient.shouldThrowError = true

        // Act & Assert
        do {
            _ = try await sut.fetchMarkets()
            XCTFail("Expected error to be thrown")
        } catch {
            XCTAssertTrue(error is NetworkError)
        }
    }
}
```

## Swift Testing Framework (iOS 18+)

### Modern Test Syntax

```swift
import Testing
@testable import MyApp

@Suite("Market Search")
struct MarketSearchTests {

    let service = MarketService()

    @Test("Returns relevant markets for query")
    func searchReturnsRelevantMarkets() async throws {
        let results = try await service.search(query: "election")

        #expect(results.count > 0)
        #expect(results.allSatisfy { $0.name.localizedCaseInsensitiveContains("election") })
    }

    @Test("Handles empty query gracefully")
    func searchHandlesEmptyQuery() async throws {
        let results = try await service.search(query: "")

        #expect(results.isEmpty)
    }

    @Test("Throws error for invalid input", arguments: ["<script>", "'; DROP TABLE"])
    func searchThrowsForInvalidInput(input: String) async {
        await #expect(throws: ValidationError.self) {
            try await service.search(query: input)
        }
    }
}
```

### Parameterized Tests

```swift
@Suite("Calculator")
struct CalculatorTests {

    @Test("Addition works correctly", arguments: [
        (2, 3, 5),
        (0, 0, 0),
        (-1, 1, 0),
        (100, 200, 300)
    ])
    func addition(a: Int, b: Int, expected: Int) {
        let calculator = Calculator()
        #expect(calculator.add(a, b) == expected)
    }
}
```

### Test Traits

```swift
@Suite("Network Tests")
struct NetworkTests {

    @Test("Fetches data from API")
    @Tag(.network)
    func fetchData() async throws {
        // Test that requires network
    }

    @Test("Slow operation completes")
    @TimeLimit(.minutes(2))
    func slowOperation() async throws {
        // Long-running test
    }

    @Test("Feature only on iOS 18+")
    @available(iOS 18, *)
    func newFeature() {
        // Test new feature
    }
}
```

## Mocking Patterns

### Protocol-Based Mocks

```swift
// Protocol for dependency
protocol MarketRepositoryProtocol {
    func fetchMarkets() async throws -> [Market]
    func saveMarket(_ market: Market) async throws
}

// Mock implementation
class MockMarketRepository: MarketRepositoryProtocol {
    var marketsToReturn: [Market] = []
    var savedMarkets: [Market] = []
    var shouldThrowError = false
    var fetchCallCount = 0

    func fetchMarkets() async throws -> [Market] {
        fetchCallCount += 1
        if shouldThrowError {
            throw TestError.mock
        }
        return marketsToReturn
    }

    func saveMarket(_ market: Market) async throws {
        if shouldThrowError {
            throw TestError.mock
        }
        savedMarkets.append(market)
    }
}

// Usage in tests
final class MarketViewModelTests: XCTestCase {

    func test_loadMarkets_updatesPublishedProperty() async {
        // Arrange
        let mockRepo = MockMarketRepository()
        mockRepo.marketsToReturn = [Market.mock(name: "Test Market")]
        let viewModel = MarketViewModel(repository: mockRepo)

        // Act
        await viewModel.loadMarkets()

        // Assert
        XCTAssertEqual(viewModel.markets.count, 1)
        XCTAssertEqual(viewModel.markets.first?.name, "Test Market")
        XCTAssertEqual(mockRepo.fetchCallCount, 1)
    }
}
```

### Spy Pattern

```swift
class SpyAnalyticsService: AnalyticsServiceProtocol {
    var trackedEvents: [(name: String, properties: [String: Any])] = []

    func track(event: String, properties: [String: Any]) {
        trackedEvents.append((event, properties))
    }

    func hasTracked(event: String) -> Bool {
        trackedEvents.contains { $0.name == event }
    }

    func reset() {
        trackedEvents.removeAll()
    }
}

// Usage
func test_purchaseCompleted_tracksAnalyticsEvent() {
    let spy = SpyAnalyticsService()
    let viewModel = PurchaseViewModel(analytics: spy)

    viewModel.completePurchase()

    XCTAssertTrue(spy.hasTracked(event: "purchase_completed"))
}
```

## ViewModel Testing

### Testing @Published Properties

```swift
import Combine

final class MarketViewModelTests: XCTestCase {

    var cancellables = Set<AnyCancellable>()

    func test_loadMarkets_updatesLoadingState() {
        // Arrange
        let mockRepo = MockMarketRepository()
        let viewModel = MarketViewModel(repository: mockRepo)
        var loadingStates: [Bool] = []

        viewModel.$isLoading
            .sink { loadingStates.append($0) }
            .store(in: &cancellables)

        // Act
        let expectation = expectation(description: "Loading completes")
        Task {
            await viewModel.loadMarkets()
            expectation.fulfill()
        }
        wait(for: [expectation], timeout: 1.0)

        // Assert
        XCTAssertEqual(loadingStates, [false, true, false])
    }
}
```

## XCUITest (UI Testing)

### Basic UI Test

```swift
import XCTest

final class MarketFlowUITests: XCTestCase {

    var app: XCUIApplication!

    override func setUp() {
        super.setUp()
        continueAfterFailure = false
        app = XCUIApplication()
        app.launchArguments = ["--uitesting"]
        app.launch()
    }

    func test_userCanSearchAndSelectMarket() {
        // Navigate to markets
        app.tabBars.buttons["Markets"].tap()

        // Verify markets screen
        XCTAssertTrue(app.navigationBars["Markets"].exists)

        // Search for market
        let searchField = app.searchFields["Search markets"]
        searchField.tap()
        searchField.typeText("election")

        // Wait for results
        let firstResult = app.cells.firstMatch
        XCTAssertTrue(firstResult.waitForExistence(timeout: 5))

        // Select market
        firstResult.tap()

        // Verify detail screen
        XCTAssertTrue(app.navigationBars.element.exists)
        XCTAssertTrue(app.staticTexts["Trade"].exists)
    }

    func test_userCanCreateNewMarket() {
        // Navigate to create
        app.buttons["Create Market"].tap()

        // Fill form
        app.textFields["Market Name"].tap()
        app.textFields["Market Name"].typeText("Test Market")

        app.textViews["Description"].tap()
        app.textViews["Description"].typeText("Test description")

        // Submit
        app.buttons["Create"].tap()

        // Verify success
        XCTAssertTrue(app.staticTexts["Market created successfully"].waitForExistence(timeout: 3))
    }
}
```

### Page Object Pattern

```swift
// Page object for reusable UI interactions
struct MarketsPage {
    let app: XCUIApplication

    var searchField: XCUIElement {
        app.searchFields["Search markets"]
    }

    var createButton: XCUIElement {
        app.buttons["Create Market"]
    }

    var marketCells: XCUIElementQuery {
        app.cells.matching(identifier: "MarketCell")
    }

    func search(for query: String) {
        searchField.tap()
        searchField.typeText(query)
    }

    func selectFirstMarket() {
        marketCells.firstMatch.tap()
    }

    func waitForResults(timeout: TimeInterval = 5) -> Bool {
        marketCells.firstMatch.waitForExistence(timeout: timeout)
    }
}

// Usage in tests
func test_searchFlow() {
    let marketsPage = MarketsPage(app: app)

    marketsPage.search(for: "election")
    XCTAssertTrue(marketsPage.waitForResults())
    marketsPage.selectFirstMarket()
}
```

## Test Data Factories

### Using Extensions

```swift
extension Market {
    static func mock(
        id: String = UUID().uuidString,
        name: String = "Test Market",
        status: MarketStatus = .active,
        createdAt: Date = Date()
    ) -> Market {
        Market(
            id: id,
            name: name,
            status: status,
            createdAt: createdAt
        )
    }
}

extension User {
    static func mock(
        id: String = UUID().uuidString,
        name: String = "Test User",
        email: String = "test@example.com"
    ) -> User {
        User(id: id, name: name, email: email)
    }
}

// Usage
func test_example() {
    let market = Market.mock(name: "Custom Name")
    let defaultMarket = Market.mock()
}
```

## Test File Organization

```
MyAppTests/
├── UnitTests/
│   ├── ViewModels/
│   │   ├── MarketViewModelTests.swift
│   │   └── UserViewModelTests.swift
│   ├── Services/
│   │   ├── MarketServiceTests.swift
│   │   └── AuthServiceTests.swift
│   └── Utilities/
│       └── DateFormatterTests.swift
├── IntegrationTests/
│   ├── APIClientTests.swift
│   └── DatabaseTests.swift
├── Mocks/
│   ├── MockMarketRepository.swift
│   ├── MockAPIClient.swift
│   └── MockUserDefaults.swift
└── Helpers/
    ├── TestData.swift
    └── XCTestCase+Extensions.swift

MyAppUITests/
├── Flows/
│   ├── MarketFlowUITests.swift
│   └── AuthFlowUITests.swift
└── PageObjects/
    ├── MarketsPage.swift
    └── LoginPage.swift
```

## Test Commands

### Swift Package Manager

```bash
# Run all tests
swift test

# Run with verbose output
swift test --verbose

# Run specific test
swift test --filter MarketServiceTests

# Run with code coverage
swift test --enable-code-coverage

# Generate coverage report
xcrun llvm-cov report .build/debug/MyAppPackageTests.xctest/Contents/MacOS/MyAppPackageTests \
  -instr-profile=.build/debug/codecov/default.profdata
```

### Xcode / xcodebuild

```bash
# Run unit tests
xcodebuild test \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 15' \
  -only-testing:MyAppTests

# Run UI tests
xcodebuild test \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 15' \
  -only-testing:MyAppUITests

# Run with coverage
xcodebuild test \
  -scheme MyApp \
  -destination 'platform=iOS Simulator,name=iPhone 15' \
  -enableCodeCoverage YES
```

## Best Practices

1. **Write Tests First** - Always TDD
2. **One Assert Per Test** - Focus on single behavior
3. **Descriptive Test Names** - Use `test_method_condition_expectedResult` format
4. **Arrange-Act-Assert** - Clear test structure
5. **Protocol-Based Mocking** - Use dependency injection
6. **Test Edge Cases** - nil, empty, large data, boundaries
7. **Test Error Paths** - Not just happy paths
8. **Keep Tests Fast** - Unit tests < 50ms each
9. **Isolate Tests** - No shared state between tests
10. **Use Test Data Factories** - Consistent mock data

## Common Mistakes to Avoid

### Testing Implementation Details

```swift
// BAD: Testing private methods
XCTAssertEqual(viewModel.privateMethod(), "value")

// GOOD: Test observable behavior
XCTAssertEqual(viewModel.displayText, "Expected Value")
```

### Flaky Tests

```swift
// BAD: Hardcoded delays
Thread.sleep(forTimeInterval: 2.0)

// GOOD: Use expectations
let expectation = expectation(description: "Completes")
viewModel.$isLoading
    .dropFirst()
    .filter { !$0 }
    .sink { _ in expectation.fulfill() }
    .store(in: &cancellables)
wait(for: [expectation], timeout: 5.0)
```

### Shared State

```swift
// BAD: Static shared state
static var sharedMock = MockService()

// GOOD: Fresh instance per test
override func setUp() {
    sut = MarketViewModel(service: MockService())
}
```

---

**Remember**: Tests are your safety net. They enable confident refactoring, catch regressions early, and document expected behavior. Write tests that you'd be proud to maintain.
