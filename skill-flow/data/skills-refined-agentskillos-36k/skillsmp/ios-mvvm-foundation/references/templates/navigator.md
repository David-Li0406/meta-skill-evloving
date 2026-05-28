# Navigator Template

> Navigation patterns cho MVVM.

---

## 🎯 Navigation Options

| Pattern | When to Use | Complexity |
|---------|-------------|------------|
| **Intent-based** | Default, simple flows | Low |
| **Navigator Protocol** | Need to mock, imperative nav | Medium |
| **Coordinator** | Complex multi-screen flows | High |

---

## 📋 Intent-Based Navigation (Recommended)

### ViewModel

```swift
class ExampleViewModel: ObservableObject {
    @Published var navigationIntent: NavigationIntent?
    
    enum NavigationIntent: Equatable {
        case home
        case detail(id: String)
        case settings
    }
    
    func onSuccess() {
        navigationIntent = .home
    }
    
    func viewDetail(id: String) {
        navigationIntent = .detail(id: id)
    }
}
```

### View

```swift
struct ExampleView: View {
    @StateObject private var viewModel = ExampleViewModel()
    @State private var navigationPath = NavigationPath()
    
    var body: some View {
        NavigationStack(path: $navigationPath) {
            // Content
        }
        .onChange(of: viewModel.navigationIntent) { intent in
            guard let intent = intent else { return }
            
            switch intent {
            case .home:
                navigationPath.append(Route.home)
            case .detail(let id):
                navigationPath.append(Route.detail(id))
            case .settings:
                navigationPath.append(Route.settings)
            }
            
            viewModel.navigationIntent = nil  // Consume
        }
    }
}
```

---

## 🏗️ Navigator Protocol (Use Sparingly)

### Protocol

```swift
import Foundation
import UIKit

protocol Navigator: AnyObject {
    func push(_ route: Route)
    func present(_ route: Route, style: PresentationStyle)
    func pop()
    func popToRoot()
    func dismiss()
}

enum PresentationStyle {
    case sheet
    case fullScreen
}
```

### Route Enum

```swift
enum Route: Equatable {
    case home
    case login
    case profile(userId: String)
    case settings
}
```

### Implementation

```swift
class AppNavigator: Navigator {
    private weak var navigationController: UINavigationController?
    
    init(navigationController: UINavigationController) {
        self.navigationController = navigationController
    }
    
    func push(_ route: Route) {
        guard let viewController = makeViewController(for: route) else { return }
        navigationController?.pushViewController(viewController, animated: true)
    }
    
    func present(_ route: Route, style: PresentationStyle = .sheet) {
        guard let viewController = makeViewController(for: route) else { return }
        
        switch style {
        case .sheet:
            viewController.modalPresentationStyle = .pageSheet
        case .fullScreen:
            viewController.modalPresentationStyle = .fullScreen
        }
        
        navigationController?.present(viewController, animated: true)
    }
    
    func pop() {
        navigationController?.popViewController(animated: true)
    }
    
    func popToRoot() {
        navigationController?.popToRootViewController(animated: true)
    }
    
    func dismiss() {
        navigationController?.dismiss(animated: true)
    }
    
    // MARK: - Factory
    
    private func makeViewController(for route: Route) -> UIViewController? {
        switch route {
        case .home:
            let viewModel = HomeViewModel()
            return UIHostingController(rootView: HomeView(viewModel: viewModel))
            
        case .login:
            let viewModel = LoginViewModel()
            return UIHostingController(rootView: LoginView(viewModel: viewModel))
            
        case .profile(let userId):
            let viewModel = ProfileViewModel(userId: userId)
            return UIHostingController(rootView: ProfileView(viewModel: viewModel))
            
        case .settings:
            let viewModel = SettingsViewModel()
            return UIHostingController(rootView: SettingsView(viewModel: viewModel))
        }
    }
}
```

---

## 🧪 Mock Navigator (Testing)

```swift
class MockNavigator: Navigator {
    var pushedRoutes: [Route] = []
    var presentedRoutes: [(route: Route, style: PresentationStyle)] = []
    var didPop = false
    var didPopToRoot = false
    var didDismiss = false
    
    func push(_ route: Route) {
        pushedRoutes.append(route)
    }
    
    func present(_ route: Route, style: PresentationStyle = .sheet) {
        presentedRoutes.append((route, style))
    }
    
    func pop() {
        didPop = true
    }
    
    func popToRoot() {
        didPopToRoot = true
    }
    
    func dismiss() {
        didDismiss = true
    }
}
```

### Test Example

```swift
func testOnSuccess_NavigatesToHome() {
    let mockNavigator = MockNavigator()
    let viewModel = MyViewModel(
        useCase: mockUseCase,
        navigator: mockNavigator
    )
    
    viewModel.onSuccess()
    
    XCTAssertEqual(mockNavigator.pushedRoutes, [.home])
}
```

---

## ✅ Best Practices

- [ ] Keep Navigator protocol small (push/pop/present/dismiss)
- [ ] Use **weak** reference for Navigator in ViewModel
- [ ] **Prefer intent-based** navigation by default
- [ ] Use Navigator injection sparingly
- [ ] Never put business logic in Navigator
- [ ] Navigator is presentation-layer only
- [ ] Use MockNavigator for testing

---

## ❌ Anti-Patterns

| Anti-Pattern | Why Bad |
|--------------|---------|
| Navigator as God object | Too many responsibilities |
| Navigator in Domain layer | Violates clean architecture |
| Strong reference to Navigator | Causes retain cycles |
| Overusing Navigator injection | Unnecessary complexity |
| No MockNavigator for tests | Can't test navigation |
