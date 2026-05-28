# Navigation Patterns

> Các pattern navigation trong MVVM: Intent-based, Navigator, Coordinator.

---

## 🎯 Recommended Approach

| Pattern | Khi nào dùng |
|---------|--------------|
| **Intent-based** (default) | Hầu hết cases |
| **Navigator injection** | Cần mock trong tests |
| **Coordinator** | Complex multi-flow apps |

---

## 1️⃣ Intent-Based Navigation (Default)

ViewModel publish intent, View executes navigation.

### ViewModel

```swift
class LoginViewModel: ObservableObject {
    @Published var navigationIntent: NavigationIntent?
    
    enum NavigationIntent: Equatable {
        case home
        case forgotPassword
        case signup
    }
    
    func loginSuccess(user: User) {
        navigationIntent = .home
    }
    
    func forgotPasswordTapped() {
        navigationIntent = .forgotPassword
    }
}
```

### View

```swift
struct LoginView: View {
    @StateObject var viewModel: LoginViewModel
    @State private var navigationPath = NavigationPath()
    @State private var showForgotPassword = false
    
    var body: some View {
        NavigationStack(path: $navigationPath) {
            // content
        }
        .onChange(of: viewModel.navigationIntent) { intent in
            guard let intent = intent else { return }
            
            switch intent {
            case .home:
                navigationPath.append(Route.home)
            case .forgotPassword:
                showForgotPassword = true
            case .signup:
                navigationPath.append(Route.signup)
            }
            
            viewModel.navigationIntent = nil  // Consume intent
        }
        .sheet(isPresented: $showForgotPassword) {
            ForgotPasswordView()
        }
    }
}
```

### Pros/Cons

| ✅ Pros | ❌ Cons |
|---------|---------|
| Clear separation | Glue code trong View |
| Easy to test intent | Repetitive với nhiều màn hình |
| View controls transitions | |

---

## 2️⃣ Navigator Injection (Use Sparingly)

ViewModel inject Navigator protocol.

### Protocol

```swift
protocol Navigator: AnyObject {
    func push(_ route: Route)
    func present(_ route: Route)
    func pop()
    func dismiss()
}

enum Route: Equatable {
    case home
    case detail(id: String)
    case settings
}
```

### ViewModel

```swift
class LoginViewModel: ObservableObject {
    private weak var navigator: Navigator?  // ⚠️ Weak reference
    
    init(navigator: Navigator?) {
        self.navigator = navigator
    }
    
    func loginSuccess() {
        navigator?.push(.home)
    }
}
```

### SwiftUI Implementation

```swift
class AppNavigator: Navigator, ObservableObject {
    @Published var path = NavigationPath()
    @Published var presentedRoute: Route?
    
    func push(_ route: Route) {
        path.append(route)
    }
    
    func present(_ route: Route) {
        presentedRoute = route
    }
    
    func pop() {
        if !path.isEmpty {
            path.removeLast()
        }
    }
    
    func dismiss() {
        presentedRoute = nil
    }
}

// App
struct ContentView: View {
    @StateObject var navigator = AppNavigator()
    
    var body: some View {
        NavigationStack(path: $navigator.path) {
            RootView()
                .navigationDestination(for: Route.self) { route in
                    destinationView(for: route)
                }
        }
        .sheet(item: $navigator.presentedRoute) { route in
            destinationView(for: route)
        }
        .environmentObject(navigator)
    }
}
```

### Testing

```swift
class MockNavigator: Navigator {
    var pushedRoutes: [Route] = []
    var presentedRoutes: [Route] = []
    
    func push(_ route: Route) {
        pushedRoutes.append(route)
    }
    
    func present(_ route: Route) {
        presentedRoutes.append(route)
    }
    
    func pop() {}
    func dismiss() {}
}

// Test
func testLoginSuccess_NavigatesToHome() async {
    let mockNavigator = MockNavigator()
    let viewModel = LoginViewModel(
        loginUseCase: MockLoginUseCase(),
        navigator: mockNavigator
    )
    
    await viewModel.login()
    
    XCTAssertEqual(mockNavigator.pushedRoutes, [.home])
}
```

---

## 3️⃣ Coordinator Pattern (Complex Flows)

Cho apps với nhiều flows (auth, onboarding, main).

### Coordinator Protocol

```swift
protocol Coordinator: AnyObject {
    var childCoordinators: [Coordinator] { get set }
    func start()
}
```

### Auth Coordinator

```swift
class AuthCoordinator: Coordinator {
    var childCoordinators: [Coordinator] = []
    private let navigator: Navigator
    var onLoginComplete: ((User) -> Void)?
    
    init(navigator: Navigator) {
        self.navigator = navigator
    }
    
    func start() {
        showLogin()
    }
    
    func showLogin() {
        let viewModel = LoginViewModel(
            loginUseCase: Resolver.resolve()
        )
        viewModel.onLoginSuccess = { [weak self] user in
            self?.onLoginComplete?(user)
        }
        viewModel.onSignupTapped = { [weak self] in
            self?.showSignup()
        }
        
        navigator.push(.login(viewModel: viewModel))
    }
    
    func showSignup() {
        let viewModel = SignupViewModel()
        viewModel.onSignupSuccess = { [weak self] user in
            self?.onLoginComplete?(user)
        }
        
        navigator.push(.signup(viewModel: viewModel))
    }
}
```

### App Coordinator

```swift
class AppCoordinator: Coordinator {
    var childCoordinators: [Coordinator] = []
    private let navigator: Navigator
    
    init(navigator: Navigator) {
        self.navigator = navigator
    }
    
    func start() {
        if UserSession.shared.isLoggedIn {
            showMain()
        } else {
            showAuth()
        }
    }
    
    private func showAuth() {
        let authCoordinator = AuthCoordinator(navigator: navigator)
        authCoordinator.onLoginComplete = { [weak self] user in
            self?.removeChild(authCoordinator)
            self?.showMain()
        }
        addChild(authCoordinator)
        authCoordinator.start()
    }
    
    private func showMain() {
        let mainCoordinator = MainCoordinator(navigator: navigator)
        addChild(mainCoordinator)
        mainCoordinator.start()
    }
}
```

---

## 📊 Comparison

| Aspect | Intent-based | Navigator | Coordinator |
|--------|--------------|-----------|-------------|
| Complexity | Low | Medium | High |
| Testability | Medium | High | High |
| Reusability | Low | Medium | High |
| Boilerplate | Low | Medium | High |
| Best for | Simple apps | Medium apps | Large apps |

---

## ✅ Guidelines

1. **Start with Intent-based** cho hầu hết cases
2. **Add Navigator** khi cần test navigation logic
3. **Use Coordinator** cho apps với >10 screens hoặc multiple flows
4. **Always consume intent** sau khi handle (set to nil)
5. **Weak reference** cho Navigator trong ViewModel

