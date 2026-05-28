---
name: dependency-injection
description: "Expert DI decisions for iOS/tvOS: when DI containers add value vs overkill, choosing between injection patterns, protocol design for testability, and SwiftUI-specific injection strategies. Use when designing service layers, setting up testing infrastructure, or deciding how to wire dependencies. Trigger keywords: dependency injection, DI, constructor injection, protocol, mock, testability, container, factory, @EnvironmentObject, service locator"
version: "3.0.0"
---

# Dependency Injection — Expert Decisions

Expert decision frameworks for dependency injection choices. Claude knows DI basics — this skill provides judgment calls for when and how to apply DI patterns.

---

## Decision Trees

### Do You Need DI?

```
Is the dependency tested independently?
├─ NO → Is it a pure function or value type?
│  ├─ YES → No DI needed (just call it)
│  └─ NO → Consider DI for future testability
│
└─ YES → How many classes use this dependency?
   ├─ 1 class → Simple constructor injection
   ├─ 2-5 classes → Protocol + constructor injection
   └─ Many classes → Consider lightweight container
```

**The trap**: DI everything. If a helper function has no side effects and doesn't need mocking, don't wrap it in a protocol.

### Which Injection Pattern?

```
Who creates the object?
├─ Caller provides dependency
│  └─ Constructor Injection (most common)
│     init(service: ServiceProtocol)
│
├─ Object creates dependency but needs flexibility
│  └─ Default Parameter Injection
│     init(service: ServiceProtocol = Service())
│
├─ Dependency changes during lifetime
│  └─ Property Injection (rare, avoid if possible)
│     var service: ServiceProtocol?
│
└─ Factory creates object with dependencies
   └─ Factory Pattern
      container.makeUserViewModel()
```

### Protocol vs Concrete Type

```
Will this dependency be mocked in tests?
├─ YES → Protocol
│
└─ NO → Is it from external module?
   ├─ YES → Protocol (wrap for decoupling)
   └─ NO → Is interface likely to change?
      ├─ YES → Protocol
      └─ NO → Concrete type is fine
```

**Rule of thumb**: Network, database, analytics, external APIs → Protocol. Date formatters, math utilities → Concrete.

### DI Container Complexity

```
Team size?
├─ Solo/Small (1-3)
│  └─ Default parameters + simple factory
│
├─ Medium (4-10)
│  └─ Simple manual container
│     final class Container {
│         lazy var userService = UserService()
│     }
│
└─ Large (10+)
   └─ Consider Swinject or similar
      (only if manual wiring becomes painful)
```

---

## NEVER Do

### Protocol Design

**NEVER** create protocols with only one implementation:
```swift
// ❌ Protocol just for the sake of it
protocol DateFormatterProtocol {
    func format(_ date: Date) -> String
}

class DateFormatterImpl: DateFormatterProtocol {
    func format(_ date: Date) -> String { ... }
}

// ✅ Just use the type directly
let formatter = DateFormatter()
formatter.dateStyle = .medium
```

**Exception**: When wrapping external dependencies for decoupling or testing.

**NEVER** mirror the entire class interface in a protocol:
```swift
// ❌ 1:1 mapping is a code smell
protocol UserServiceProtocol {
    var users: [User] { get }
    var isLoading: Bool { get }
    func fetchUser(id: String) async throws -> User
    func updateUser(_ user: User) async throws
    func deleteUser(id: String) async throws
    // ...20 more methods
}

// ✅ Minimal interface for what's actually needed
protocol UserFetching {
    func fetchUser(id: String) async throws -> User
}
```

**NEVER** put mutable state requirements in protocols:
```swift
// ❌ Forces implementation details
protocol CacheProtocol {
    var storage: [String: Any] { get set }  // Leaks implementation
}

// ✅ Behavior-focused
protocol CacheProtocol {
    func get(key: String) -> Any?
    func set(key: String, value: Any)
}
```

### Constructor Injection

**NEVER** use property injection when constructor injection works:
```swift
// ❌ Object can be in invalid state
class UserViewModel {
    var userService: UserServiceProtocol!  // Can be nil!

    func loadUser() async {
        let user = try? await userService.fetchUser(id: "1")  // Crash if not set!
    }
}

// ✅ Guaranteed valid state
class UserViewModel {
    private let userService: UserServiceProtocol

    init(userService: UserServiceProtocol) {
        self.userService = userService  // Never nil
    }
}
```

**NEVER** create objects with many dependencies (> 5):
```swift
// ❌ Too many dependencies — class does too much
init(
    userService: UserServiceProtocol,
    authService: AuthServiceProtocol,
    analyticsService: AnalyticsProtocol,
    networkManager: NetworkManagerProtocol,
    cacheManager: CacheProtocol,
    configService: ConfigServiceProtocol,
    featureFlagService: FeatureFlagProtocol
) { ... }

// ✅ Split into smaller, focused classes
// Or create a composite service
```

### Service Locator (Anti-Pattern)

**NEVER** use Service Locator pattern:
```swift
// ❌ Hidden dependencies, runtime errors, untestable
class UserViewModel {
    func loadUser() async {
        let service = ServiceLocator.shared.resolve(UserServiceProtocol.self)!
        // Crashes if not registered
        // Dependency is hidden
        // Can't see what this class needs
    }
}

// ✅ Explicit constructor injection
class UserViewModel {
    private let userService: UserServiceProtocol  // Visible dependency

    init(userService: UserServiceProtocol) {
        self.userService = userService
    }
}
```

### Testing

**NEVER** create mocks with real side effects:
```swift
// ❌ Mock does real work
class MockNetworkManager: NetworkManagerProtocol {
    func request<T>(_ endpoint: Endpoint) async throws -> T {
        // Actually makes network call!
        return try await URLSession.shared.data(from: endpoint.url)
    }
}

// ✅ Mocks return stubbed data
class MockNetworkManager: NetworkManagerProtocol {
    var stubbedResult: Any?
    var stubbedError: Error?

    func request<T>(_ endpoint: Endpoint) async throws -> T {
        if let error = stubbedError { throw error }
        return stubbedResult as! T
    }
}
```

**NEVER** test mocks instead of real code:
```swift
// ❌ Testing the mock, not the system
func testMockReturnsUser() {
    let mock = MockUserService()
    mock.stubbedUser = User(name: "John")
    XCTAssertEqual(mock.fetchUser().name, "John")  // Tests mock, not app
}

// ✅ Test the system under test
func testViewModelLoadsUser() async {
    let mock = MockUserService()
    mock.stubbedUser = User(name: "John")

    let viewModel = UserViewModel(userService: mock)  // SUT
    await viewModel.loadUser(id: "1")

    XCTAssertEqual(viewModel.user?.name, "John")  // Tests ViewModel
}
```

---

## Essential Patterns

### Default Parameter Injection

```swift
// Production uses real, tests inject mock
@MainActor
final class UserViewModel: ObservableObject {
    private let userService: UserServiceProtocol

    init(userService: UserServiceProtocol = UserService()) {
        self.userService = userService
    }
}

// Production
let viewModel = UserViewModel()

// Test
let viewModel = UserViewModel(userService: MockUserService())
```

### Simple Manual Container

```swift
@MainActor
final class Container {
    static let shared = Container()

    // Singletons (lazy initialized)
    lazy var networkManager: NetworkManagerProtocol = NetworkManager()
    lazy var authService: AuthServiceProtocol = AuthService(network: networkManager)
    lazy var userService: UserServiceProtocol = UserService(network: networkManager)

    // Factory methods (new instance each time)
    func makeUserViewModel() -> UserViewModel {
        UserViewModel(userService: userService)
    }

    func makeLoginViewModel() -> LoginViewModel {
        LoginViewModel(authService: authService)
    }
}
```

### SwiftUI Environment Injection

```swift
// Custom environment key
private struct UserServiceKey: EnvironmentKey {
    static let defaultValue: UserServiceProtocol = UserService()
}

extension EnvironmentValues {
    var userService: UserServiceProtocol {
        get { self[UserServiceKey.self] }
        set { self[UserServiceKey.self] = newValue }
    }
}

// Inject at app level
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.userService, Container.shared.userService)
        }
    }
}

// Consume in any view
struct UserView: View {
    @Environment(\.userService) var userService

    var body: some View {
        // Use userService
    }
}
```

### Mock with Verification

```swift
final class MockUserService: UserServiceProtocol {
    // Stubbed returns
    var stubbedUser: User?
    var stubbedError: Error?

    // Call tracking
    private(set) var fetchUserCallCount = 0
    private(set) var fetchUserLastId: String?

    func fetchUser(id: String) async throws -> User {
        fetchUserCallCount += 1
        fetchUserLastId = id

        if let error = stubbedError { throw error }
        guard let user = stubbedUser else {
            throw MockError.notStubbed
        }
        return user
    }
}

// Test with verification
func testFetchesCorrectUser() async {
    let mock = MockUserService()
    mock.stubbedUser = User(id: "123", name: "John")

    let viewModel = UserViewModel(userService: mock)
    await viewModel.loadUser(id: "123")

    XCTAssertEqual(mock.fetchUserCallCount, 1)
    XCTAssertEqual(mock.fetchUserLastId, "123")
}
```

---

## Quick Reference

### When to Use Each Pattern

| Pattern | Use When | Avoid When |
|---------|----------|------------|
| Constructor injection | Default choice | Never avoid |
| Default parameters | Convenience with testability | Dependency changes at runtime |
| Property injection | Framework requires it (rare) | You have control over init |
| Factory | Object needs runtime parameters | Simple object creation |
| Container | Many cross-cutting dependencies | Small app, few dependencies |

### Protocol Checklist

- [ ] Will it be mocked? If no, skip protocol
- [ ] Interface is minimal (only needed methods)
- [ ] No mutable state requirements
- [ ] No implementation details leaked
- [ ] Single responsibility

### DI Red Flags

| Smell | Problem | Fix |
|-------|---------|-----|
| Protocol for every class | Over-engineering | Only where needed |
| Service Locator | Hidden dependencies | Constructor injection |
| > 5 constructor params | Class does too much | Split responsibilities |
| Property injection | Object can be invalid | Constructor injection |
| Mock does real work | Tests are slow/flaky | Return stubbed data |
| 1:1 protocol:class ratio | Unnecessary abstraction | Remove unused protocols |

### SwiftUI DI Comparison

| Pattern | Scope | Use For |
|---------|-------|---------|
| `@Environment` | View hierarchy | System/app services |
| `@EnvironmentObject` | View hierarchy | Observable shared state |
| `@StateObject` init injection | Single view | View-specific ViewModel |
| Container factory | App-wide | Complex dependency graphs |
