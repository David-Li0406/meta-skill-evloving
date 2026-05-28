---
name: ios-development
description: Comprehensive iOS development guidelines covering SwiftUI, UIKit, architecture patterns, and Apple platform best practices. Use when building iOS, iPadOS, watchOS, or macOS applications.
version: 1.0.0
---

# iOS Development Guidelines

This skill provides comprehensive guidance for building high-quality iOS applications using Swift, SwiftUI, and UIKit.

---

## Part 1: Swift Best Practices

### Modern Swift Conventions

```swift
// PREFER: Use guard for early exits
func processUser(_ user: User?) {
    guard let user = user else { return }
    // Process user...
}

// PREFER: Use if-let for optional binding
if let name = user.name {
    print(name)
}

// PREFER: Trailing closure syntax
users.filter { $0.isActive }
     .map { $0.name }

// PREFER: Computed properties over methods for simple getters
var fullName: String {
    "\(firstName) \(lastName)"
}
```

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Types | UpperCamelCase | `UserProfile`, `NetworkManager` |
| Functions/Variables | lowerCamelCase | `fetchUsers()`, `userName` |
| Constants | lowerCamelCase | `let maxRetryCount = 3` |
| Protocols | UpperCamelCase + able/ing/Type | `Equatable`, `Loading`, `ViewModelType` |
| Enums | UpperCamelCase, cases lowerCamelCase | `enum State { case loading }` |

### Error Handling

```swift
// Define custom errors
enum NetworkError: LocalizedError {
    case invalidURL
    case noData
    case decodingFailed(Error)

    var errorDescription: String? {
        switch self {
        case .invalidURL: return "Invalid URL"
        case .noData: return "No data received"
        case .decodingFailed(let error): return "Decoding failed: \(error.localizedDescription)"
        }
    }
}

// Use Result type for async operations
func fetchData() async -> Result<Data, NetworkError> {
    // ...
}

// Or throw errors with async/await
func fetchData() async throws -> Data {
    // ...
}
```

---

## Part 2: SwiftUI Patterns

### View Structure

```swift
struct ContentView: View {
    // MARK: - Properties
    @StateObject private var viewModel = ContentViewModel()
    @State private var isPresented = false

    // MARK: - Body
    var body: some View {
        NavigationStack {
            content
                .navigationTitle("Home")
                .toolbar { toolbarContent }
        }
        .sheet(isPresented: $isPresented) {
            DetailView()
        }
    }

    // MARK: - Subviews
    private var content: some View {
        List(viewModel.items) { item in
            ItemRow(item: item)
        }
    }

    @ToolbarContentBuilder
    private var toolbarContent: some ToolbarContent {
        ToolbarItem(placement: .primaryAction) {
            Button("Add") { isPresented = true }
        }
    }
}
```

### State Management

| Property Wrapper | Use Case |
|------------------|----------|
| `@State` | Simple value types owned by the view |
| `@Binding` | Two-way connection to parent's state |
| `@StateObject` | Reference type owned by the view (create once) |
| `@ObservedObject` | Reference type passed from parent |
| `@EnvironmentObject` | Shared data across view hierarchy |
| `@Environment` | System values (colorScheme, locale, etc.) |

### Extracting Subviews

```swift
// GOOD: Extract complex subviews
struct ProfileView: View {
    let user: User

    var body: some View {
        VStack {
            ProfileHeader(user: user)
            ProfileStats(user: user)
            ProfileActions(user: user)
        }
    }
}

// GOOD: Use ViewBuilder for conditional content
@ViewBuilder
private var statusView: some View {
    if isLoading {
        ProgressView()
    } else if let error = error {
        ErrorView(error: error)
    } else {
        ContentView()
    }
}
```

---

## Part 3: Architecture Patterns

### MVVM (Recommended for SwiftUI)

```swift
// Model
struct User: Identifiable, Codable {
    let id: UUID
    var name: String
    var email: String
}

// ViewModel
@MainActor
class UserViewModel: ObservableObject {
    @Published private(set) var users: [User] = []
    @Published private(set) var isLoading = false
    @Published var error: Error?

    private let repository: UserRepositoryProtocol

    init(repository: UserRepositoryProtocol = UserRepository()) {
        self.repository = repository
    }

    func fetchUsers() async {
        isLoading = true
        defer { isLoading = false }

        do {
            users = try await repository.fetchUsers()
        } catch {
            self.error = error
        }
    }
}

// View
struct UserListView: View {
    @StateObject private var viewModel = UserViewModel()

    var body: some View {
        List(viewModel.users) { user in
            Text(user.name)
        }
        .task { await viewModel.fetchUsers() }
    }
}
```

### Repository Pattern

```swift
protocol UserRepositoryProtocol {
    func fetchUsers() async throws -> [User]
    func saveUser(_ user: User) async throws
}

class UserRepository: UserRepositoryProtocol {
    private let networkService: NetworkServiceProtocol
    private let cacheService: CacheServiceProtocol

    init(
        networkService: NetworkServiceProtocol = NetworkService(),
        cacheService: CacheServiceProtocol = CacheService()
    ) {
        self.networkService = networkService
        self.cacheService = cacheService
    }

    func fetchUsers() async throws -> [User] {
        // Check cache first
        if let cached: [User] = cacheService.get(forKey: "users") {
            return cached
        }

        // Fetch from network
        let users = try await networkService.fetch([User].self, from: .users)
        cacheService.set(users, forKey: "users")
        return users
    }
}
```

---

## Part 4: Networking

### Modern Async/Await Networking

```swift
class NetworkService {
    private let session: URLSession
    private let decoder: JSONDecoder

    init(session: URLSession = .shared) {
        self.session = session
        self.decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        decoder.dateDecodingStrategy = .iso8601
    }

    func fetch<T: Decodable>(_ type: T.Type, from endpoint: Endpoint) async throws -> T {
        let request = try endpoint.urlRequest()
        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }

        guard (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.httpError(httpResponse.statusCode)
        }

        return try decoder.decode(T.self, from: data)
    }
}
```

### Endpoint Configuration

```swift
enum Endpoint {
    case users
    case user(id: UUID)
    case createUser(User)

    var path: String {
        switch self {
        case .users: return "/users"
        case .user(let id): return "/users/\(id)"
        case .createUser: return "/users"
        }
    }

    var method: HTTPMethod {
        switch self {
        case .users, .user: return .get
        case .createUser: return .post
        }
    }

    func urlRequest() throws -> URLRequest {
        guard let url = URL(string: APIConfig.baseURL + path) else {
            throw NetworkError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        if case .createUser(let user) = self {
            request.httpBody = try JSONEncoder().encode(user)
        }

        return request
    }
}
```

---

## Part 5: Data Persistence

### SwiftData (iOS 17+)

```swift
import SwiftData

@Model
class Task {
    var title: String
    var isCompleted: Bool
    var createdAt: Date

    init(title: String, isCompleted: Bool = false) {
        self.title = title
        self.isCompleted = isCompleted
        self.createdAt = Date()
    }
}

// In App
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: Task.self)
    }
}

// In View
struct TaskListView: View {
    @Environment(\.modelContext) private var modelContext
    @Query(sort: \Task.createdAt) private var tasks: [Task]

    var body: some View {
        List(tasks) { task in
            TaskRow(task: task)
        }
    }

    func addTask(title: String) {
        let task = Task(title: title)
        modelContext.insert(task)
    }
}
```

### UserDefaults (Simple Settings)

```swift
@propertyWrapper
struct UserDefault<T> {
    let key: String
    let defaultValue: T

    var wrappedValue: T {
        get { UserDefaults.standard.object(forKey: key) as? T ?? defaultValue }
        set { UserDefaults.standard.set(newValue, forKey: key) }
    }
}

// Usage
enum Settings {
    @UserDefault(key: "hasCompletedOnboarding", defaultValue: false)
    static var hasCompletedOnboarding: Bool

    @UserDefault(key: "preferredTheme", defaultValue: "system")
    static var preferredTheme: String
}
```

---

## Part 6: Testing

### Unit Testing

```swift
import XCTest
@testable import MyApp

final class UserViewModelTests: XCTestCase {
    var sut: UserViewModel!
    var mockRepository: MockUserRepository!

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

    func test_fetchUsers_success_updatesUsers() async {
        // Given
        let expectedUsers = [User(id: UUID(), name: "Test", email: "test@example.com")]
        mockRepository.usersToReturn = expectedUsers

        // When
        await sut.fetchUsers()

        // Then
        XCTAssertEqual(sut.users, expectedUsers)
        XCTAssertFalse(sut.isLoading)
        XCTAssertNil(sut.error)
    }

    func test_fetchUsers_failure_setsError() async {
        // Given
        mockRepository.errorToThrow = NetworkError.noData

        // When
        await sut.fetchUsers()

        // Then
        XCTAssertTrue(sut.users.isEmpty)
        XCTAssertNotNil(sut.error)
    }
}
```

### UI Testing

```swift
import XCTest

final class OnboardingUITests: XCTestCase {
    let app = XCUIApplication()

    override func setUp() {
        continueAfterFailure = false
        app.launchArguments = ["--uitesting"]
        app.launch()
    }

    func test_onboarding_completeFlow() {
        // First screen
        XCTAssertTrue(app.staticTexts["Welcome"].exists)
        app.buttons["Continue"].tap()

        // Second screen
        XCTAssertTrue(app.staticTexts["Features"].exists)
        app.buttons["Get Started"].tap()

        // Main app
        XCTAssertTrue(app.navigationBars["Home"].exists)
    }
}
```

---

## Pre-Implementation Checklist

- [ ] Define clear architecture (MVVM recommended for SwiftUI)
- [ ] Set up dependency injection for testability
- [ ] Plan data models with Codable conformance
- [ ] Consider offline support requirements
- [ ] Plan error handling strategy
- [ ] Set up proper state management (@StateObject vs @ObservedObject)
- [ ] Plan navigation flow (NavigationStack, sheets, fullScreenCover)
- [ ] Consider accessibility (VoiceOver, Dynamic Type)
- [ ] Plan for different device sizes and orientations

---

## Common Pitfalls to Avoid

| Issue | Problem | Solution |
|-------|---------|----------|
| Massive Views | Hard to maintain, poor performance | Extract subviews, use ViewBuilder |
| Wrong property wrapper | Memory leaks, unexpected behavior | Use @StateObject for owned objects |
| Force unwrapping | Crashes | Use guard, if-let, nil coalescing |
| Main thread blocking | UI freezes | Use async/await, move work to background |
| Retain cycles | Memory leaks | Use [weak self] in closures |
| Ignoring errors | Silent failures | Always handle errors appropriately |
