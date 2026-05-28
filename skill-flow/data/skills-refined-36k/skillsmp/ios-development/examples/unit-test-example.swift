// Unit Test Examples
// XCTest patterns for ViewModel testing with mocks

import XCTest
@testable import MyApp

// MARK: - Domain Models (for reference)

struct User: Identifiable, Equatable {
    let id: Int
    var name: String
    var email: String
}

// MARK: - Repository Protocol

protocol UserRepositoryProtocol: Sendable {
    func fetchUsers() async throws -> [User]
    func fetchUser(id: Int) async throws -> User
    func createUser(_ user: User) async throws -> User
    func deleteUser(id: Int) async throws
}

// MARK: - ViewModel Errors

enum UserListError: LocalizedError, Equatable {
    case fetchFailed(String)
    case deleteFailed(String)

    var errorDescription: String? {
        switch self {
        case .fetchFailed(let message): return message
        case .deleteFailed(let message): return message
        }
    }
}

// MARK: - Mock Repository

final class MockUserRepository: UserRepositoryProtocol, @unchecked Sendable {
    // Stubs - predefined return values
    var usersToReturn: [User] = []
    var userToReturn: User?
    var errorToThrow: Error?

    // Spies - track method calls
    var fetchUsersCalled = false
    var fetchUsersCallCount = 0
    var fetchUserCalledWithId: Int?
    var createUserCalledWith: User?
    var deleteUserCalledWithId: Int?

    // Reset for reuse between tests
    func reset() {
        usersToReturn = []
        userToReturn = nil
        errorToThrow = nil
        fetchUsersCalled = false
        fetchUsersCallCount = 0
        fetchUserCalledWithId = nil
        createUserCalledWith = nil
        deleteUserCalledWithId = nil
    }

    func fetchUsers() async throws -> [User] {
        fetchUsersCalled = true
        fetchUsersCallCount += 1

        if let error = errorToThrow {
            throw error
        }
        return usersToReturn
    }

    func fetchUser(id: Int) async throws -> User {
        fetchUserCalledWithId = id

        if let error = errorToThrow {
            throw error
        }

        guard let user = userToReturn else {
            throw NSError(domain: "Test", code: 404, userInfo: nil)
        }
        return user
    }

    func createUser(_ user: User) async throws -> User {
        createUserCalledWith = user

        if let error = errorToThrow {
            throw error
        }
        return userToReturn ?? user
    }

    func deleteUser(id: Int) async throws {
        deleteUserCalledWithId = id

        if let error = errorToThrow {
            throw error
        }
    }
}

// MARK: - Test Data Factory

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
            User(id: id, name: "User \(id)", email: "user\(id)@example.com")
        }
    }
}

// MARK: - ViewModel (System Under Test)

@Observable
@MainActor
class UserListViewModel {
    private(set) var users: [User] = []
    private(set) var isLoading = false
    private(set) var error: UserListError?

    private let repository: UserRepositoryProtocol

    init(repository: UserRepositoryProtocol) {
        self.repository = repository
    }

    func loadUsers() async {
        isLoading = true
        error = nil
        defer { isLoading = false }

        do {
            users = try await repository.fetchUsers()
        } catch {
            self.error = .fetchFailed(error.localizedDescription)
        }
    }

    func deleteUser(_ user: User) async {
        do {
            try await repository.deleteUser(id: user.id)
            users.removeAll { $0.id == user.id }
        } catch {
            self.error = .deleteFailed(error.localizedDescription)
        }
    }

    func clearError() {
        error = nil
    }
}

// MARK: - ViewModel Tests

@MainActor
final class UserListViewModelTests: XCTestCase {
    // MARK: - Properties
    private var sut: UserListViewModel!
    private var mockRepository: MockUserRepository!

    // MARK: - Setup & Teardown
    override func setUp() {
        super.setUp()
        mockRepository = MockUserRepository()
        sut = UserListViewModel(repository: mockRepository)
    }

    override func tearDown() {
        sut = nil
        mockRepository = nil
        super.tearDown()
    }

    // MARK: - Load Users Tests

    func test_loadUsers_whenSuccess_updatesUsersList() async {
        // Arrange
        let expectedUsers = TestDataFactory.makeUsers(count: 3)
        mockRepository.usersToReturn = expectedUsers

        // Act
        await sut.loadUsers()

        // Assert
        XCTAssertTrue(mockRepository.fetchUsersCalled, "fetchUsers should be called")
        XCTAssertEqual(sut.users.count, 3, "Should have 3 users")
        XCTAssertEqual(sut.users, expectedUsers, "Users should match expected")
        XCTAssertFalse(sut.isLoading, "Should not be loading after completion")
        XCTAssertNil(sut.error, "Should not have an error")
    }

    func test_loadUsers_whenFailure_setsError() async {
        // Arrange
        let testError = NSError(domain: "Test", code: 500, userInfo: [
            NSLocalizedDescriptionKey: "Server error"
        ])
        mockRepository.errorToThrow = testError

        // Act
        await sut.loadUsers()

        // Assert
        XCTAssertTrue(sut.users.isEmpty, "Users should be empty")
        XCTAssertFalse(sut.isLoading, "Should not be loading")
        XCTAssertNotNil(sut.error, "Should have an error")

        if case .fetchFailed(let message) = sut.error {
            XCTAssertTrue(message.contains("Server error"), "Error message should contain 'Server error'")
        } else {
            XCTFail("Expected fetchFailed error")
        }
    }

    func test_loadUsers_whenEmptyResult_updatesWithEmptyList() async {
        // Arrange
        mockRepository.usersToReturn = []

        // Act
        await sut.loadUsers()

        // Assert
        XCTAssertTrue(sut.users.isEmpty, "Users should be empty")
        XCTAssertNil(sut.error, "Should not have an error for empty result")
    }

    func test_loadUsers_calledMultipleTimes_tracksCallCount() async {
        // Arrange
        mockRepository.usersToReturn = []

        // Act
        await sut.loadUsers()
        await sut.loadUsers()
        await sut.loadUsers()

        // Assert
        XCTAssertEqual(mockRepository.fetchUsersCallCount, 3, "Should be called 3 times")
    }

    // MARK: - Delete User Tests

    func test_deleteUser_whenSuccess_removesFromList() async {
        // Arrange
        let users = TestDataFactory.makeUsers(count: 3)
        mockRepository.usersToReturn = users
        await sut.loadUsers()

        let userToDelete = users[1] // Delete second user

        // Act
        await sut.deleteUser(userToDelete)

        // Assert
        XCTAssertEqual(mockRepository.deleteUserCalledWithId, userToDelete.id, "Should call delete with correct ID")
        XCTAssertEqual(sut.users.count, 2, "Should have 2 users remaining")
        XCTAssertFalse(sut.users.contains(userToDelete), "Deleted user should not be in list")
        XCTAssertNil(sut.error, "Should not have an error")
    }

    func test_deleteUser_whenFailure_setsError() async {
        // Arrange
        let users = TestDataFactory.makeUsers(count: 3)
        mockRepository.usersToReturn = users
        await sut.loadUsers()

        mockRepository.errorToThrow = NSError(domain: "Test", code: 500)
        let userToDelete = users[0]

        // Act
        await sut.deleteUser(userToDelete)

        // Assert
        XCTAssertEqual(sut.users.count, 3, "Users should remain unchanged")
        XCTAssertNotNil(sut.error, "Should have an error")

        if case .deleteFailed = sut.error {
            // Expected
        } else {
            XCTFail("Expected deleteFailed error")
        }
    }

    // MARK: - Error Handling Tests

    func test_clearError_removesError() async {
        // Arrange
        mockRepository.errorToThrow = NSError(domain: "Test", code: 500)
        await sut.loadUsers()
        XCTAssertNotNil(sut.error, "Should have an error")

        // Act
        sut.clearError()

        // Assert
        XCTAssertNil(sut.error, "Error should be cleared")
    }

    // MARK: - State Tests

    func test_initialState_isEmpty() {
        // Assert
        XCTAssertTrue(sut.users.isEmpty, "Initial users should be empty")
        XCTAssertFalse(sut.isLoading, "Initial loading state should be false")
        XCTAssertNil(sut.error, "Initial error should be nil")
    }
}

// MARK: - Async Helper Extension

extension XCTestCase {
    /// Wait for an async expression to become true
    func waitFor(
        _ expression: @escaping () -> Bool,
        timeout: TimeInterval = 5.0,
        message: String = "Condition not met within timeout"
    ) async {
        let start = Date()
        while !expression() {
            if Date().timeIntervalSince(start) > timeout {
                XCTFail(message)
                return
            }
            try? await Task.sleep(for: .milliseconds(50))
        }
    }
}

// MARK: - API Error Tests

final class APIErrorTests: XCTestCase {
    func test_networkError_hasCorrectDescription() {
        // Arrange
        let underlyingError = NSError(domain: NSURLErrorDomain, code: -1009)
        let error = APIError.networkError(underlyingError)

        // Assert
        XCTAssertTrue(error.errorDescription?.contains("Network error") == true)
    }

    func test_serverError_includesStatusCode() {
        // Arrange
        let error = APIError.serverError(statusCode: 500, message: "Internal Server Error")

        // Assert
        XCTAssertEqual(error.errorDescription, "Internal Server Error")
    }

    func test_unauthorized_hasCorrectDescription() {
        // Arrange
        let error = APIError.unauthorized

        // Assert
        XCTAssertEqual(error.errorDescription, "Authentication required")
    }
}

enum APIError: LocalizedError {
    case networkError(Error)
    case serverError(statusCode: Int, message: String?)
    case unauthorized

    var errorDescription: String? {
        switch self {
        case .networkError(let error):
            return "Network error: \(error.localizedDescription)"
        case .serverError(_, let message):
            return message ?? "Server error"
        case .unauthorized:
            return "Authentication required"
        }
    }
}

// MARK: - Preview/Run Tests

/*
 To run tests:
 1. Cmd + U in Xcode to run all tests
 2. Click the diamond icon next to a test method to run individual test
 3. Use Test Navigator (Cmd + 6) to see all tests

 Best practices demonstrated:
 - Arrange-Act-Assert pattern
 - Clear test method naming: test_methodName_condition_expectedBehavior
 - Mock repository with stubs and spies
 - Test data factory for consistent test data
 - setUp/tearDown for clean test isolation
 - Testing both success and failure paths
 - Testing state transitions
 */
