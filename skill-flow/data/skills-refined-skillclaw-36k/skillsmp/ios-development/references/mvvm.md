# MVVM Architecture Reference

Comprehensive MVVM implementation guide for iOS 17+ with SwiftUI.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
├─────────────────────────────────────────────────────────┤
│  View (SwiftUI)  ←──────────→  ViewModel (@Observable)  │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                      Domain Layer                        │
├─────────────────────────────────────────────────────────┤
│           Model (Entities)  ←───→  UseCase              │
└─────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────┐
│                       Data Layer                         │
├─────────────────────────────────────────────────────────┤
│  Repository Protocol  ←───→  DataSource (API/DB)        │
└─────────────────────────────────────────────────────────┘
```

## ViewModel Design

### Basic ViewModel Structure

```swift
import Observation

@Observable
@MainActor
class UserListViewModel {
    // MARK: - Published State
    private(set) var users: [User] = []
    private(set) var isLoading = false
    private(set) var error: UserListError?

    // MARK: - Dependencies
    private let repository: UserRepositoryProtocol

    // MARK: - Initialization
    init(repository: UserRepositoryProtocol) {
        self.repository = repository
    }

    // MARK: - Actions
    func loadUsers() async {
        isLoading = true
        error = nil
        defer { isLoading = false }

        do {
            users = try await repository.fetchUsers()
        } catch {
            self.error = .fetchFailed(error)
        }
    }

    func deleteUser(_ user: User) async {
        do {
            try await repository.deleteUser(user.id)
            users.removeAll { $0.id == user.id }
        } catch {
            self.error = .deleteFailed(error)
        }
    }
}
```

### Error Handling in ViewModel

```swift
enum UserListError: LocalizedError {
    case fetchFailed(Error)
    case deleteFailed(Error)
    case networkUnavailable

    var errorDescription: String? {
        switch self {
        case .fetchFailed:
            return "Failed to load users"
        case .deleteFailed:
            return "Failed to delete user"
        case .networkUnavailable:
            return "Network is unavailable"
        }
    }

    var recoverySuggestion: String? {
        switch self {
        case .fetchFailed, .deleteFailed:
            return "Please try again later"
        case .networkUnavailable:
            return "Check your internet connection"
        }
    }
}
```

## Repository Pattern

### Repository Protocol

```swift
protocol UserRepositoryProtocol: Sendable {
    func fetchUsers() async throws -> [User]
    func fetchUser(id: Int) async throws -> User
    func createUser(_ user: User) async throws -> User
    func updateUser(_ user: User) async throws -> User
    func deleteUser(_ id: Int) async throws
}
```

### Repository Implementation

```swift
actor UserRepository: UserRepositoryProtocol {
    private let apiClient: APIClientProtocol
    private let cache: CacheProtocol

    init(apiClient: APIClientProtocol, cache: CacheProtocol) {
        self.apiClient = apiClient
        self.cache = cache
    }

    func fetchUsers() async throws -> [User] {
        // Try cache first
        if let cached: [User] = await cache.get(forKey: "users") {
            return cached
        }

        // Fetch from API
        let users: [User] = try await apiClient.request(.getUsers)

        // Update cache
        await cache.set(users, forKey: "users")

        return users
    }

    func fetchUser(id: Int) async throws -> User {
        try await apiClient.request(.getUser(id: id))
    }

    func createUser(_ user: User) async throws -> User {
        let created: User = try await apiClient.request(.createUser(user))
        await cache.invalidate(forKey: "users")
        return created
    }

    func updateUser(_ user: User) async throws -> User {
        let updated: User = try await apiClient.request(.updateUser(user))
        await cache.invalidate(forKey: "users")
        return updated
    }

    func deleteUser(_ id: Int) async throws {
        try await apiClient.request(.deleteUser(id: id))
        await cache.invalidate(forKey: "users")
    }
}
```

## Dependency Injection

### Container Pattern

```swift
@Observable
class DependencyContainer {
    // MARK: - Shared Services
    private(set) lazy var apiClient: APIClientProtocol = APIClient(
        baseURL: URL(string: "https://api.example.com")!
    )

    private(set) lazy var cache: CacheProtocol = InMemoryCache()

    // MARK: - Repositories
    private(set) lazy var userRepository: UserRepositoryProtocol = UserRepository(
        apiClient: apiClient,
        cache: cache
    )

    // MARK: - ViewModels
    @MainActor
    func makeUserListViewModel() -> UserListViewModel {
        UserListViewModel(repository: userRepository)
    }

    @MainActor
    func makeUserDetailViewModel(userId: Int) -> UserDetailViewModel {
        UserDetailViewModel(
            userId: userId,
            repository: userRepository
        )
    }
}
```

### Environment-based Injection

```swift
@main
struct MyApp: App {
    @State private var container = DependencyContainer()

    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(container)
        }
    }
}

struct UserListView: View {
    @Environment(DependencyContainer.self) private var container
    @State private var viewModel: UserListViewModel?

    var body: some View {
        Group {
            if let viewModel {
                UserListContent(viewModel: viewModel)
            } else {
                ProgressView()
            }
        }
        .task {
            viewModel = container.makeUserListViewModel()
        }
    }
}
```

### Protocol-based Injection (for Testing)

```swift
// Mock for testing
class MockUserRepository: UserRepositoryProtocol {
    var usersToReturn: [User] = []
    var errorToThrow: Error?
    var fetchUsersCalled = false

    func fetchUsers() async throws -> [User] {
        fetchUsersCalled = true
        if let error = errorToThrow {
            throw error
        }
        return usersToReturn
    }

    // ... other methods
}

// In tests
@MainActor
func test_loadUsers_success() async {
    let mockRepository = MockUserRepository()
    mockRepository.usersToReturn = [User(id: 1, name: "Test")]

    let viewModel = UserListViewModel(repository: mockRepository)
    await viewModel.loadUsers()

    XCTAssertTrue(mockRepository.fetchUsersCalled)
    XCTAssertEqual(viewModel.users.count, 1)
}
```

## View-ViewModel Binding

### Basic Binding

```swift
struct UserListView: View {
    @State private var viewModel: UserListViewModel

    init(repository: UserRepositoryProtocol) {
        _viewModel = State(initialValue: UserListViewModel(repository: repository))
    }

    var body: some View {
        List(viewModel.users) { user in
            UserRow(user: user)
        }
        .overlay {
            if viewModel.isLoading {
                ProgressView()
            }
        }
        .alert(item: $viewModel.error) { error in
            Alert(
                title: Text("Error"),
                message: Text(error.localizedDescription)
            )
        }
        .task {
            await viewModel.loadUsers()
        }
    }
}
```

### Form Binding with @Bindable

```swift
@Observable
class ProfileEditViewModel {
    var name: String = ""
    var email: String = ""
    var bio: String = ""

    private(set) var isSaving = false
    private(set) var error: Error?

    private let repository: UserRepositoryProtocol
    private let userId: Int

    init(user: User, repository: UserRepositoryProtocol) {
        self.userId = user.id
        self.name = user.name
        self.email = user.email
        self.bio = user.bio ?? ""
        self.repository = repository
    }

    func save() async -> Bool {
        isSaving = true
        defer { isSaving = false }

        do {
            let updatedUser = User(
                id: userId,
                name: name,
                email: email,
                bio: bio
            )
            _ = try await repository.updateUser(updatedUser)
            return true
        } catch {
            self.error = error
            return false
        }
    }
}

struct ProfileEditView: View {
    @Bindable var viewModel: ProfileEditViewModel
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        Form {
            TextField("Name", text: $viewModel.name)
            TextField("Email", text: $viewModel.email)
            TextEditor(text: $viewModel.bio)
        }
        .navigationTitle("Edit Profile")
        .toolbar {
            ToolbarItem(placement: .confirmationAction) {
                Button("Save") {
                    Task {
                        if await viewModel.save() {
                            dismiss()
                        }
                    }
                }
                .disabled(viewModel.isSaving)
            }
        }
    }
}
```

## UseCase Pattern

For complex business logic, extract to UseCase classes:

```swift
protocol FetchUserListUseCaseProtocol {
    func execute(filter: UserFilter?) async throws -> [User]
}

struct FetchUserListUseCase: FetchUserListUseCaseProtocol {
    private let repository: UserRepositoryProtocol

    init(repository: UserRepositoryProtocol) {
        self.repository = repository
    }

    func execute(filter: UserFilter?) async throws -> [User] {
        var users = try await repository.fetchUsers()

        if let filter {
            users = apply(filter: filter, to: users)
        }

        return users.sorted { $0.name < $1.name }
    }

    private func apply(filter: UserFilter, to users: [User]) -> [User] {
        users.filter { user in
            if let searchText = filter.searchText, !searchText.isEmpty {
                guard user.name.localizedCaseInsensitiveContains(searchText) else {
                    return false
                }
            }
            if let status = filter.status {
                guard user.status == status else {
                    return false
                }
            }
            return true
        }
    }
}
```

## Best Practices

### ViewModel Guidelines

1. **Single Responsibility**: One ViewModel per screen/feature
2. **@MainActor**: Mark ViewModels with `@MainActor` for UI updates
3. **Immutable Published State**: Use `private(set)` for state properties
4. **Clear Actions**: Define explicit action methods
5. **Error Handling**: Use typed errors for better UI feedback

### Repository Guidelines

1. **Protocol-first**: Always define protocol for testability
2. **Actor for Thread Safety**: Use `actor` for mutable state
3. **Cache Strategy**: Implement appropriate caching
4. **Single Source of Truth**: Repository owns the data

### Dependency Injection Guidelines

1. **Constructor Injection**: Prefer constructor over property injection
2. **Protocol Dependencies**: Depend on protocols, not implementations
3. **Container Pattern**: Use container for complex dependency graphs
4. **Environment for SwiftUI**: Use `@Environment` for view-level injection

### Testing Guidelines

1. **Mock Repositories**: Create mock implementations for testing
2. **Test Actions**: Test each ViewModel action independently
3. **Test State Changes**: Verify state transitions
4. **Test Error Handling**: Verify error states are handled correctly
