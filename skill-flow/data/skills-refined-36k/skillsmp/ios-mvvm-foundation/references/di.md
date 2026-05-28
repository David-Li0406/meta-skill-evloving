# Dependency Injection

> DI patterns với Resolver cho MVVM architecture.

---

## 🎯 Primary Pattern

| Pattern | Sử dụng cho |
|---------|-------------|
| **ViewModel init** | Feature dependencies |
| **Resolver** | Global services |

---

## 📦 ViewModel Init Pattern

```swift
class LoginViewModel: ObservableObject {
    // MARK: - Dependencies
    private let loginUseCase: LoginUseCaseProtocol
    private let analyticsService: AnalyticsServiceProtocol
    
    // MARK: - Full init (for testing)
    init(
        loginUseCase: LoginUseCaseProtocol,
        analyticsService: AnalyticsServiceProtocol
    ) {
        self.loginUseCase = loginUseCase
        self.analyticsService = analyticsService
    }
}

// MARK: - Factory Methods
extension LoginViewModel {
    /// Production instance
    static func live() -> LoginViewModel {
        LoginViewModel(
            loginUseCase: Resolver.resolve(),
            analyticsService: Resolver.resolve()
        )
    }
    
    /// Mock instance for testing/previews
    static func mock() -> LoginViewModel {
        LoginViewModel(
            loginUseCase: MockLoginUseCase(),
            analyticsService: MockAnalyticsService()
        )
    }
}
```

### View Usage

```swift
struct LoginView: View {
    @StateObject private var viewModel: LoginViewModel
    
    init(viewModel: LoginViewModel = .live()) {
        _viewModel = StateObject(wrappedValue: viewModel)
    }
}

// Preview
struct LoginView_Previews: PreviewProvider {
    static var previews: some View {
        LoginView(viewModel: .mock())
    }
}
```

---

## ⚙️ Resolver Setup

### Registration

```swift
// Core/DI/DependencyContainer.swift

import Resolver

extension Resolver: ResolverRegistering {
    public static func registerAllServices() {
        // MARK: - Core Services (Singleton)
        register { APIClient() }
            .scope(.application)
        
        register { KeychainService() }
            .scope(.application)
        
        register { AnalyticsService() as AnalyticsServiceProtocol }
            .scope(.application)
        
        // MARK: - Repositories (Singleton)
        register { AuthRepository(
            apiClient: resolve()
        ) as AuthRepositoryProtocol }
            .scope(.application)
        
        register { UserRepository(
            apiClient: resolve(),
            storage: resolve()
        ) as UserRepositoryProtocol }
            .scope(.application)
        
        // MARK: - UseCases (Factory - new instance)
        register { LoginUseCase(
            authRepository: resolve()
        ) as LoginUseCaseProtocol }
        
        register { FetchUserUseCase(
            userRepository: resolve()
        ) as FetchUserUseCaseProtocol }
    }
}
```

### App Launch

```swift
// App.swift
@main
struct MyApp: App {
    init() {
        Resolver.registerAllServices()
    }
    
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
    }
}
```

---

## 🔄 Scopes

| Scope | Lifecycle | Use For |
|-------|-----------|---------|
| `.application` | Singleton (app lifetime) | Services, Repositories |
| `.cached` | Lazy, cleared on memory warning | Heavy objects |
| `.shared` (default) | New instance per resolve | UseCases |
| `.unique` | Always new instance | Stateful objects |

```swift
// Singleton
register { APIClient() }
    .scope(.application)

// New instance each time
register { LoginUseCase() }
    // No scope = .shared = factory
```

---

## 📊 Dependency Flow

```
View
└─> ViewModel (via factory method)
     └─> UseCases (from Resolver)
          └─> Repositories (from Resolver)
               └─> Services (from Resolver)
```

### Example Flow

```
LoginView
└─> LoginViewModel.live()
     └─> LoginUseCase: LoginUseCaseProtocol
          └─> AuthRepository: AuthRepositoryProtocol
               └─> APIClient (singleton)
               └─> KeychainService (singleton)
```

---

## 🧪 Testing

```swift
class LoginViewModelTests: XCTestCase {
    var viewModel: LoginViewModel!
    var mockUseCase: MockLoginUseCase!
    var mockAnalytics: MockAnalyticsService!
    
    override func setUp() {
        mockUseCase = MockLoginUseCase()
        mockAnalytics = MockAnalyticsService()
        
        // Use full init - no Resolver
        viewModel = LoginViewModel(
            loginUseCase: mockUseCase,
            analyticsService: mockAnalytics
        )
    }
    
    func testLoginSuccess() async {
        mockUseCase.result = .success(User.mock)
        
        await viewModel.login()
        
        XCTAssertEqual(viewModel.status, .success)
        XCTAssertTrue(mockAnalytics.trackedEvents.contains(.loginSuccess))
    }
}
```

---

## ⚠️ Rules

| ✅ Do | ❌ Don't |
|-------|---------|
| Inject UseCases vào ViewModel | Inject Repository trực tiếp |
| Protocol types cho dependencies | Concrete types |
| Factory methods (`live()`, `mock()`) | Direct Resolver.resolve() trong View |
| Singleton cho Services/Repos | Singleton cho UseCases |
| Full init cho testing | Chỉ có convenience init |

---

## 🔗 Related

- [testing.md](testing.md) - Testing với mocks
- [presentation-patterns.md](presentation-patterns.md) - ViewModel structure

