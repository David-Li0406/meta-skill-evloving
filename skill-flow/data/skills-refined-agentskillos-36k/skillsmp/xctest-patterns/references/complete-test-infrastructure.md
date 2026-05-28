# XCTest Patterns — Complete Test Infrastructure

> **Loading Trigger**: Load when setting up test infrastructure, creating shared mocks, or implementing test helpers from scratch.

---

## Complete Mock Factory System

```swift
// MARK: - MockFactory.swift

import Foundation

/// Central factory for creating configured mocks
enum MockFactory {
    // MARK: - Services

    static func makeUserService(
        stubbedUser: User? = .preview,
        stubbedUsers: [User] = [],
        stubbedError: Error? = nil
    ) -> MockUserService {
        let mock = MockUserService()
        mock.stubbedUser = stubbedUser
        mock.stubbedUsers = stubbedUsers
        mock.stubbedError = stubbedError
        return mock
    }

    static func makeNetworkService(
        stubbedData: Data = Data(),
        stubbedError: Error? = nil,
        delay: TimeInterval = 0
    ) -> MockNetworkService {
        let mock = MockNetworkService()
        mock.stubbedData = stubbedData
        mock.stubbedError = stubbedError
        mock.delay = delay
        return mock
    }

    static func makeAuthService(
        isAuthenticated: Bool = true,
        currentUser: User? = .preview
    ) -> MockAuthService {
        let mock = MockAuthService()
        mock.isAuthenticated = isAuthenticated
        mock.currentUser = currentUser
        return mock
    }

    // MARK: - Repositories

    static func makeUserRepository(
        localUsers: [User] = [],
        remoteUsers: [User] = []
    ) -> MockUserRepository {
        let mock = MockUserRepository()
        mock.localUsers = localUsers
        mock.remoteUsers = remoteUsers
        return mock
    }
}
```

---

## Comprehensive Mock Implementation

```swift
// MARK: - MockUserService.swift

final class MockUserService: UserServiceProtocol {
    // MARK: - Stubs

    var stubbedUser: User?
    var stubbedUsers: [User] = []
    var stubbedError: Error?

    // MARK: - Spy Tracking

    private(set) var fetchUserCallCount = 0
    private(set) var fetchUserLastId: String?
    private(set) var updateUserCallCount = 0
    private(set) var updateUserLastUser: User?
    private(set) var deleteUserCallCount = 0
    private(set) var deleteUserLastId: String?

    // MARK: - Capture Lists (for multiple calls)

    private(set) var fetchUserCalls: [String] = []
    private(set) var updateUserCalls: [User] = []

    // MARK: - Protocol Implementation

    func fetchUser(id: String) async throws -> User {
        fetchUserCallCount += 1
        fetchUserLastId = id
        fetchUserCalls.append(id)

        if let error = stubbedError {
            throw error
        }

        guard let user = stubbedUser ?? stubbedUsers.first(where: { $0.id == id }) else {
            throw ServiceError.notFound
        }

        return user
    }

    func fetchAllUsers() async throws -> [User] {
        if let error = stubbedError {
            throw error
        }
        return stubbedUsers
    }

    func updateUser(_ user: User) async throws -> User {
        updateUserCallCount += 1
        updateUserLastUser = user
        updateUserCalls.append(user)

        if let error = stubbedError {
            throw error
        }

        return user
    }

    func deleteUser(id: String) async throws {
        deleteUserCallCount += 1
        deleteUserLastId = id

        if let error = stubbedError {
            throw error
        }
    }

    // MARK: - Verification Helpers

    func verify(fetchUserCalledWith id: String) -> Bool {
        fetchUserCalls.contains(id)
    }

    func verify(fetchUserCalledTimes count: Int) -> Bool {
        fetchUserCallCount == count
    }

    func verify(updateUserCalledWith user: User) -> Bool {
        updateUserCalls.contains(where: { $0.id == user.id })
    }

    // MARK: - Reset

    func reset() {
        stubbedUser = nil
        stubbedUsers = []
        stubbedError = nil
        fetchUserCallCount = 0
        fetchUserLastId = nil
        fetchUserCalls = []
        updateUserCallCount = 0
        updateUserLastUser = nil
        updateUserCalls = []
        deleteUserCallCount = 0
        deleteUserLastId = nil
    }
}

// MARK: - MockNetworkService.swift

final class MockNetworkService: NetworkServiceProtocol {
    var stubbedData: Data = Data()
    var stubbedError: Error?
    var delay: TimeInterval = 0

    private(set) var requestCallCount = 0
    private(set) var requestLastURL: URL?
    private(set) var requestCalls: [URLRequest] = []

    func request(_ request: URLRequest) async throws -> Data {
        requestCallCount += 1
        requestLastURL = request.url
        requestCalls.append(request)

        if delay > 0 {
            try await Task.sleep(for: .seconds(delay))
        }

        if let error = stubbedError {
            throw error
        }

        return stubbedData
    }

    func reset() {
        stubbedData = Data()
        stubbedError = nil
        delay = 0
        requestCallCount = 0
        requestLastURL = nil
        requestCalls = []
    }
}

// MARK: - MockAuthService.swift

final class MockAuthService: AuthServiceProtocol {
    var isAuthenticated = false
    var currentUser: User?
    var stubbedLoginError: Error?
    var stubbedLogoutError: Error?

    private(set) var loginCallCount = 0
    private(set) var loginLastCredentials: (email: String, password: String)?
    private(set) var logoutCallCount = 0

    func login(email: String, password: String) async throws {
        loginCallCount += 1
        loginLastCredentials = (email, password)

        if let error = stubbedLoginError {
            throw error
        }

        isAuthenticated = true
    }

    func logout() async throws {
        logoutCallCount += 1

        if let error = stubbedLogoutError {
            throw error
        }

        isAuthenticated = false
        currentUser = nil
    }
}
```

---

## Test Data Builders

```swift
// MARK: - UserBuilder.swift

final class UserBuilder {
    private var id = UUID().uuidString
    private var name = "Test User"
    private var email = "test@example.com"
    private var avatarURL: URL? = nil
    private var createdAt = Date()
    private var isActive = true
    private var role: User.Role = .user

    static var `default`: UserBuilder { UserBuilder() }

    func withId(_ id: String) -> Self {
        self.id = id
        return self
    }

    func withName(_ name: String) -> Self {
        self.name = name
        return self
    }

    func withEmail(_ email: String) -> Self {
        self.email = email
        return self
    }

    func withAvatar(_ url: URL?) -> Self {
        self.avatarURL = url
        return self
    }

    func withCreatedAt(_ date: Date) -> Self {
        self.createdAt = date
        return self
    }

    func inactive() -> Self {
        self.isActive = false
        return self
    }

    func asAdmin() -> Self {
        self.role = .admin
        return self
    }

    func asModerator() -> Self {
        self.role = .moderator
        return self
    }

    func build() -> User {
        User(
            id: id,
            name: name,
            email: email,
            avatarURL: avatarURL,
            createdAt: createdAt,
            isActive: isActive,
            role: role
        )
    }
}

// MARK: - Convenience Extensions

extension User {
    static var preview: User {
        UserBuilder.default.build()
    }

    static var admin: User {
        UserBuilder.default.asAdmin().withName("Admin User").build()
    }

    static var inactive: User {
        UserBuilder.default.inactive().build()
    }

    static func list(count: Int) -> [User] {
        (0..<count).map { index in
            UserBuilder.default
                .withId("user-\(index)")
                .withName("User \(index)")
                .withEmail("user\(index)@example.com")
                .build()
        }
    }
}

// MARK: - OrderBuilder.swift

final class OrderBuilder {
    private var id = UUID().uuidString
    private var userId = "user-1"
    private var items: [OrderItem] = []
    private var status: Order.Status = .pending
    private var createdAt = Date()
    private var total: Decimal = 0

    static var `default`: OrderBuilder {
        OrderBuilder()
            .withItem(ProductBuilder.default.build(), quantity: 1)
    }

    func withId(_ id: String) -> Self {
        self.id = id
        return self
    }

    func withUserId(_ userId: String) -> Self {
        self.userId = userId
        return self
    }

    func withItem(_ product: Product, quantity: Int) -> Self {
        let item = OrderItem(product: product, quantity: quantity)
        self.items.append(item)
        self.total += product.price * Decimal(quantity)
        return self
    }

    func withStatus(_ status: Order.Status) -> Self {
        self.status = status
        return self
    }

    func shipped() -> Self {
        withStatus(.shipped)
    }

    func delivered() -> Self {
        withStatus(.delivered)
    }

    func cancelled() -> Self {
        withStatus(.cancelled)
    }

    func build() -> Order {
        Order(
            id: id,
            userId: userId,
            items: items,
            status: status,
            createdAt: createdAt,
            total: total
        )
    }
}
```

---

## XCTestCase Extensions

```swift
// MARK: - XCTestCase+Async.swift

import XCTest
import Combine

extension XCTestCase {

    // MARK: - Async Helpers

    /// Waits for an async operation with timeout
    func awaitResult<T>(
        timeout: TimeInterval = 5.0,
        file: StaticString = #file,
        line: UInt = #line,
        operation: @escaping () async throws -> T
    ) async throws -> T {
        try await withThrowingTaskGroup(of: T.self) { group in
            group.addTask {
                try await operation()
            }

            group.addTask {
                try await Task.sleep(for: .seconds(timeout))
                throw XCTestError(.timeoutWhileWaiting)
            }

            let result = try await group.next()!
            group.cancelAll()
            return result
        }
    }

    /// Asserts that an async operation throws a specific error
    func assertThrowsAsync<T, E: Error & Equatable>(
        _ expression: @autoclosure () async throws -> T,
        throws expectedError: E,
        file: StaticString = #file,
        line: UInt = #line
    ) async {
        do {
            _ = try await expression()
            XCTFail("Expected error \(expectedError) but no error was thrown", file: file, line: line)
        } catch let error as E {
            XCTAssertEqual(error, expectedError, file: file, line: line)
        } catch {
            XCTFail("Expected error \(expectedError) but got \(error)", file: file, line: line)
        }
    }

    /// Asserts that an async operation does not throw
    func assertNoThrowAsync<T>(
        _ expression: @autoclosure () async throws -> T,
        file: StaticString = #file,
        line: UInt = #line
    ) async -> T? {
        do {
            return try await expression()
        } catch {
            XCTFail("Unexpected error: \(error)", file: file, line: line)
            return nil
        }
    }

    // MARK: - Publisher Helpers

    /// Awaits the first value from a publisher
    func awaitPublisher<T: Publisher>(
        _ publisher: T,
        timeout: TimeInterval = 1.0,
        file: StaticString = #file,
        line: UInt = #line
    ) throws -> T.Output where T.Failure == Never {
        var result: T.Output?
        let expectation = expectation(description: "Awaiting publisher")

        let cancellable = publisher.first().sink { value in
            result = value
            expectation.fulfill()
        }

        wait(for: [expectation], timeout: timeout)
        cancellable.cancel()

        return try XCTUnwrap(result, file: file, line: line)
    }

    /// Collects all values from a publisher until completion
    func collectPublisher<T: Publisher>(
        _ publisher: T,
        timeout: TimeInterval = 1.0
    ) throws -> [T.Output] where T.Failure == Never {
        var results: [T.Output] = []
        let expectation = expectation(description: "Collecting publisher")

        let cancellable = publisher.sink(
            receiveCompletion: { _ in expectation.fulfill() },
            receiveValue: { results.append($0) }
        )

        wait(for: [expectation], timeout: timeout)
        cancellable.cancel()

        return results
    }

    // MARK: - Eventually Assertions

    /// Asserts a condition eventually becomes true
    func assertEventually(
        timeout: TimeInterval = 3.0,
        interval: TimeInterval = 0.1,
        file: StaticString = #file,
        line: UInt = #line,
        condition: @escaping () -> Bool
    ) {
        let deadline = Date().addingTimeInterval(timeout)

        while Date() < deadline {
            if condition() {
                return
            }
            RunLoop.current.run(until: Date().addingTimeInterval(interval))
        }

        XCTFail("Condition was not met within \(timeout) seconds", file: file, line: line)
    }

    /// Asserts a value eventually equals expected
    func assertEventuallyEqual<T: Equatable>(
        _ expression: @autoclosure @escaping () -> T,
        equals expected: T,
        timeout: TimeInterval = 3.0,
        file: StaticString = #file,
        line: UInt = #line
    ) {
        assertEventually(timeout: timeout, file: file, line: line) {
            expression() == expected
        }
    }
}
```

---

## UI Testing Infrastructure

```swift
// MARK: - XCUIApplication+Extensions.swift

import XCTest

extension XCUIApplication {

    // MARK: - Launch Configuration

    func launchWithMocks(
        authState: AuthState = .loggedIn,
        featureFlags: [String: Bool] = [:],
        mockResponses: [String: String] = [:]
    ) {
        launchArguments = ["--uitesting"]

        // Auth state
        launchEnvironment["AUTH_STATE"] = authState.rawValue

        // Feature flags
        for (key, value) in featureFlags {
            launchEnvironment["FF_\(key)"] = value ? "1" : "0"
        }

        // Mock responses
        for (endpoint, response) in mockResponses {
            launchEnvironment["MOCK_\(endpoint)"] = response
        }

        launch()
    }

    enum AuthState: String {
        case loggedIn = "logged_in"
        case loggedOut = "logged_out"
        case sessionExpired = "session_expired"
    }

    // MARK: - Element Queries

    func button(_ identifier: String) -> XCUIElement {
        buttons[identifier]
    }

    func textField(_ identifier: String) -> XCUIElement {
        textFields[identifier]
    }

    func secureTextField(_ identifier: String) -> XCUIElement {
        secureTextFields[identifier]
    }

    func staticText(_ identifier: String) -> XCUIElement {
        staticTexts[identifier]
    }

    func cell(_ identifier: String) -> XCUIElement {
        cells[identifier]
    }

    // MARK: - Convenience Actions

    func tapButton(_ identifier: String) {
        button(identifier).tap()
    }

    func typeInTextField(_ identifier: String, text: String) {
        let field = textField(identifier)
        field.tap()
        field.typeText(text)
    }

    func typeInSecureField(_ identifier: String, text: String) {
        let field = secureTextField(identifier)
        field.tap()
        field.typeText(text)
    }

    func scrollTo(_ identifier: String, in scrollView: XCUIElement? = nil) {
        let element = staticTexts[identifier].firstMatch
        let container = scrollView ?? scrollViews.firstMatch

        while !element.isHittable {
            container.swipeUp()
        }
    }
}

// MARK: - XCUIElement+Extensions.swift

extension XCUIElement {

    /// Waits for element to exist with timeout
    @discardableResult
    func waitForExistence(timeout: TimeInterval = 5.0) -> Bool {
        waitForExistence(timeout: timeout)
    }

    /// Waits for element to be hittable
    func waitForHittable(timeout: TimeInterval = 5.0) -> Bool {
        let predicate = NSPredicate(format: "isHittable == true")
        let expectation = XCTNSPredicateExpectation(predicate: predicate, object: self)
        let result = XCTWaiter().wait(for: [expectation], timeout: timeout)
        return result == .completed
    }

    /// Waits for element to not exist
    func waitForNonExistence(timeout: TimeInterval = 5.0) -> Bool {
        let predicate = NSPredicate(format: "exists == false")
        let expectation = XCTNSPredicateExpectation(predicate: predicate, object: self)
        let result = XCTWaiter().wait(for: [expectation], timeout: timeout)
        return result == .completed
    }

    /// Clears text field and types new text
    func clearAndType(_ text: String) {
        guard let currentValue = value as? String, !currentValue.isEmpty else {
            tap()
            typeText(text)
            return
        }

        tap()
        let deleteString = String(repeating: XCUIKeyboardKey.delete.rawValue, count: currentValue.count)
        typeText(deleteString)
        typeText(text)
    }
}
```

---

## Memory Leak Testing

```swift
// MARK: - MemoryLeakTracking.swift

import XCTest

extension XCTestCase {

    /// Tracks object for memory leaks - fails test if object is not deallocated
    func trackForMemoryLeaks(
        _ instance: AnyObject,
        file: StaticString = #file,
        line: UInt = #line
    ) {
        addTeardownBlock { [weak instance] in
            XCTAssertNil(
                instance,
                "Instance should have been deallocated. Potential memory leak.",
                file: file,
                line: line
            )
        }
    }

    /// Creates a ViewModel and tracks it for memory leaks
    func makeViewModel<T: AnyObject>(
        _ factory: () -> T,
        file: StaticString = #file,
        line: UInt = #line
    ) -> T {
        let instance = factory()
        trackForMemoryLeaks(instance, file: file, line: line)
        return instance
    }
}

// MARK: - Usage Example

final class ViewModelMemoryTests: XCTestCase {

    func testViewModelDoesNotLeak() {
        // Arrange
        let mockService = MockUserService()
        let sut = makeViewModel {
            UserViewModel(userService: mockService)
        }

        // Act
        Task { await sut.loadUser(id: "123") }

        // Assert (memory leak check happens in teardown)
    }

    func testClosureDoesNotRetainViewModel() async {
        var viewModel: UserViewModel? = UserViewModel(userService: MockUserService())
        weak var weakViewModel = viewModel

        // Setup closure that should NOT retain
        let task = Task { [weak viewModel] in
            await viewModel?.loadUser(id: "123")
        }

        await task.value
        viewModel = nil

        XCTAssertNil(weakViewModel, "ViewModel should be deallocated")
    }
}
```
