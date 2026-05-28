# Testing Reference

XCTest patterns for iOS app testing.

## Unit Testing Basics

### Test Structure

```swift
import XCTest
@testable import MyApp

final class UserViewModelTests: XCTestCase {
    // MARK: - Properties
    private var sut: UserViewModel!  // System Under Test
    private var mockRepository: MockUserRepository!

    // MARK: - Setup & Teardown
    override func setUp() {
        super.setUp()
        mockRepository = MockUserRepository()
        sut = UserViewModel(repository: mockRepository)
    }

    override func tearDown() {
        sut = nil
        mockRepository = nil
        super.tearDown()
    }

    // MARK: - Tests
    func test_loadUsers_whenSuccess_updatesUsersList() async {
        // Arrange
        let expectedUsers = [User(id: 1, name: "Test User")]
        mockRepository.usersToReturn = expectedUsers

        // Act
        await sut.loadUsers()

        // Assert
        XCTAssertEqual(sut.users.count, 1)
        XCTAssertEqual(sut.users.first?.name, "Test User")
        XCTAssertFalse(sut.isLoading)
        XCTAssertNil(sut.error)
    }

    func test_loadUsers_whenFailure_setsError() async {
        // Arrange
        mockRepository.errorToThrow = APIError.networkFailed

        // Act
        await sut.loadUsers()

        // Assert
        XCTAssertTrue(sut.users.isEmpty)
        XCTAssertFalse(sut.isLoading)
        XCTAssertNotNil(sut.error)
    }
}
```

### Async Testing

```swift
final class AsyncTests: XCTestCase {
    // async/await style
    func test_asyncOperation() async throws {
        let result = try await someAsyncFunction()
        XCTAssertEqual(result, expectedValue)
    }

    // With timeout
    func test_asyncWithTimeout() async throws {
        let expectation = expectation(description: "Async operation")

        Task {
            await performAsyncWork()
            expectation.fulfill()
        }

        await fulfillment(of: [expectation], timeout: 5.0)
    }

    // Testing MainActor code
    @MainActor
    func test_mainActorCode() async {
        let viewModel = UserViewModel(repository: MockUserRepository())
        await viewModel.loadUsers()
        XCTAssertFalse(viewModel.isLoading)
    }
}
```

## Mocking

### Mock Repository

```swift
class MockUserRepository: UserRepositoryProtocol {
    // Stubs
    var usersToReturn: [User] = []
    var userToReturn: User?
    var errorToThrow: Error?

    // Spies
    var fetchUsersCalled = false
    var fetchUsersCallCount = 0
    var createUserCalledWith: User?
    var deleteUserCalledWithId: Int?

    func fetchUsers() async throws -> [User] {
        fetchUsersCalled = true
        fetchUsersCallCount += 1

        if let error = errorToThrow {
            throw error
        }
        return usersToReturn
    }

    func createUser(_ user: User) async throws -> User {
        createUserCalledWith = user

        if let error = errorToThrow {
            throw error
        }
        return userToReturn ?? user
    }

    func deleteUser(_ id: Int) async throws {
        deleteUserCalledWithId = id

        if let error = errorToThrow {
            throw error
        }
    }
}
```

### Mock Network Client

```swift
class MockAPIClient: APIClientProtocol {
    var responseData: Data?
    var responseError: Error?
    var requestedEndpoints: [String] = []

    func request<T: Decodable>(_ endpoint: String) async throws -> T {
        requestedEndpoints.append(endpoint)

        if let error = responseError {
            throw error
        }

        guard let data = responseData else {
            throw APIError.invalidResponse
        }

        return try JSONDecoder().decode(T.self, from: data)
    }
}
```

### Factory for Test Data

```swift
enum TestDataFactory {
    static func makeUser(
        id: Int = 1,
        name: String = "Test User",
        email: String = "test@example.com"
    ) -> User {
        User(id: id, name: name, email: email)
    }

    static func makeUsers(count: Int) -> [User] {
        (1...count).map { id in
            makeUser(id: id, name: "User \(id)")
        }
    }

    static func makeUserJSON(id: Int = 1, name: String = "Test User") -> Data {
        """
        {"id": \(id), "name": "\(name)", "email": "test@example.com"}
        """.data(using: .utf8)!
    }
}
```

## Testing ViewModels

### State Changes

```swift
@MainActor
final class UserListViewModelTests: XCTestCase {
    func test_loadUsers_setsLoadingState() async {
        // Arrange
        let mockRepository = MockUserRepository()
        let viewModel = UserListViewModel(repository: mockRepository)

        // Act - Start loading
        let loadTask = Task {
            await viewModel.loadUsers()
        }

        // Assert - Check initial loading state
        // Note: This may require adding a delay mechanism in mock

        await loadTask.value
        XCTAssertFalse(viewModel.isLoading)
    }

    func test_deleteUser_removesFromList() async {
        // Arrange
        let users = TestDataFactory.makeUsers(count: 3)
        let mockRepository = MockUserRepository()
        mockRepository.usersToReturn = users

        let viewModel = UserListViewModel(repository: mockRepository)
        await viewModel.loadUsers()

        // Act
        await viewModel.deleteUser(users[1])

        // Assert
        XCTAssertEqual(viewModel.users.count, 2)
        XCTAssertFalse(viewModel.users.contains { $0.id == users[1].id })
    }
}
```

### Error Handling

```swift
@MainActor
final class ErrorHandlingTests: XCTestCase {
    func test_loadUsers_networkError_showsRetryableError() async {
        // Arrange
        let mockRepository = MockUserRepository()
        mockRepository.errorToThrow = APIError.networkFailed(NSError(domain: "", code: -1))

        let viewModel = UserListViewModel(repository: mockRepository)

        // Act
        await viewModel.loadUsers()

        // Assert
        XCTAssertNotNil(viewModel.error)
        if case .fetchFailed = viewModel.error {
            // Expected
        } else {
            XCTFail("Expected fetchFailed error")
        }
    }
}
```

## Testing Tips

### Naming Convention

```swift
// Format: test_methodName_condition_expectedBehavior
func test_loadUsers_whenNetworkFails_setsErrorState() async { }
func test_createUser_withValidData_addsToList() async { }
func test_deleteUser_whenUnauthorized_showsLoginPrompt() async { }
```

### Test Organization

```swift
final class UserViewModelTests: XCTestCase {
    // MARK: - Load Users Tests
    func test_loadUsers_success() async { }
    func test_loadUsers_failure() async { }
    func test_loadUsers_emptyResult() async { }

    // MARK: - Create User Tests
    func test_createUser_success() async { }
    func test_createUser_validationError() async { }

    // MARK: - Delete User Tests
    func test_deleteUser_success() async { }
    func test_deleteUser_notFound() async { }
}
```

### Assertions

```swift
// Basic assertions
XCTAssertEqual(value, expected)
XCTAssertNotEqual(value, unexpected)
XCTAssertTrue(condition)
XCTAssertFalse(condition)
XCTAssertNil(optional)
XCTAssertNotNil(optional)

// Throwing assertions
XCTAssertThrowsError(try throwingFunction()) { error in
    XCTAssertEqual(error as? MyError, .expected)
}

XCTAssertNoThrow(try nonThrowingFunction())

// Collection assertions
XCTAssertEqual(array.count, 3)
XCTAssertTrue(array.contains(element))
XCTAssertTrue(array.isEmpty)

// Accuracy for floating point
XCTAssertEqual(value, 3.14, accuracy: 0.01)
```

## Test Doubles Summary

| Type | Purpose | Example |
|------|---------|---------|
| **Mock** | Verify interactions | Check if method was called |
| **Stub** | Provide canned responses | Return predefined data |
| **Spy** | Record calls for verification | Track call count/arguments |
| **Fake** | Working implementation | In-memory database |

## Best Practices

1. **One assert per test** - Keep tests focused
2. **Arrange-Act-Assert** - Clear test structure
3. **Test behavior, not implementation** - Focus on outcomes
4. **Use descriptive names** - Tests as documentation
5. **Fast tests** - Mock external dependencies
6. **Isolated tests** - No shared state between tests
7. **Test edge cases** - Empty, null, error states
