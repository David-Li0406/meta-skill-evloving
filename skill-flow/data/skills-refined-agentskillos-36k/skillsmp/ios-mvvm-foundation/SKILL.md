---
name: ios-mvvm-foundation
description: 'iOS MVVM + Clean Architecture foundation. Sử dụng skill này khi tạo màn hình mới, implement features, hoặc cần guidelines chi tiết về architecture, navigation, animation, testing.'
---

# iOS MVVM Foundation

> **Skill này cung cấp guidelines đầy đủ cho iOS development với MVVM + Clean Architecture.**

## 🎯 Khi Nào Sử Dụng Skill Này

| User Request | Action |
|--------------|--------|
| Tạo màn hình mới | Đọc [references/presentation-patterns.md](references/presentation-patterns.md) |
| Implement animation | Đọc [references/animation-guidelines.md](references/animation-guidelines.md) |
| Setup navigation | Đọc [references/navigation-patterns.md](references/navigation-patterns.md) |
| Viết unit tests | Đọc [references/testing.md](references/testing.md) |
| Dependency injection | Đọc [references/di.md](references/di.md) |
| ViewState pattern | Đọc [references/viewstate-pattern.md](references/viewstate-pattern.md) |
| Theme system | Đọc [references/theme-system.md](references/theme-system.md) |
| Networking | Đọc [references/networking.md](references/networking.md) |
| State management | Đọc [references/state-management.md](references/state-management.md) |
| Security | Đọc [references/security.md](references/security.md) |
| Storage / Persistence | Đọc [references/storage.md](references/storage.md) |
| Code templates | Đọc [references/templates/index.md](references/templates/index.md) |
| App Store submission | Đọc [references/app-store-submission.md](references/app-store-submission.md) |
| IAP / Paywall | Đọc [references/iap.md](references/iap.md) |
| iOS 26 Liquid Glass | Đọc [references/liquid-glass.md](references/liquid-glass.md) |

---

## 📐 Architecture Overview

### Pattern: Clean Architecture + MVVM

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │    View     │───▶│  ViewModel  │───▶│  ViewState  │      │
│  │  (SwiftUI)  │    │(Observable) │    │ (Optional)  │      │
│  └─────────────┘    └──────┬──────┘    └─────────────┘      │
│                            │                                 │
└────────────────────────────┼─────────────────────────────────┘
                             │ inject
┌────────────────────────────▼─────────────────────────────────┐
│                      DOMAIN LAYER                            │
│  ┌─────────────┐    ┌─────────────┐                         │
│  │  UseCases   │───▶│   Entities  │                         │
│  │ (Protocols) │    │  (Models)   │                         │
│  └──────┬──────┘    └─────────────┘                         │
│         │                                                    │
└─────────┼────────────────────────────────────────────────────┘
          │ inject
┌─────────▼────────────────────────────────────────────────────┐
│                       DATA LAYER                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐      │
│  │ Repositories│───▶│   Network   │    │   Storage   │      │
│  │   (Impl)    │    │  Services   │    │  Services   │      │
│  └─────────────┘    └─────────────┘    └─────────────┘      │
└──────────────────────────────────────────────────────────────┘
```

### Dependency Flow
```
Presentation → Domain ← Data
     │            ▲         │
     │            │         │
     └────────────┴─────────┘
```

---

## 🧩 MVVM Components

### 1. ViewModel (2-4 KB mỗi feature)

```swift
final class LoginViewModel: ObservableObject {
    // MARK: - Published State (Business)
    @Published private(set) var email: String = ""
    @Published private(set) var password: String = ""
    @Published private(set) var isLoading: Bool = false
    @Published private(set) var error: AppError?
    @Published var navigationIntent: NavigationIntent?
    
    enum NavigationIntent: Equatable {
        case home
        case forgotPassword
    }
    
    // MARK: - Dependencies
    private let loginUseCase: LoginUseCaseProtocol
    
    init(loginUseCase: LoginUseCaseProtocol) {
        self.loginUseCase = loginUseCase
    }
    
    // MARK: - User Actions
    func updateEmail(_ email: String) {
        self.email = email
    }
    
    func updatePassword(_ password: String) {
        self.password = password
    }
    
    func login() async {
        isLoading = true
        defer { isLoading = false }
        
        do {
            try await loginUseCase.execute(email: email, password: password)
            await MainActor.run { navigationIntent = .home }
        } catch {
            await MainActor.run { self.error = AppError(error) }
        }
    }
    
    // MARK: - Computed Properties
    var isLoginEnabled: Bool {
        !email.isEmpty && !password.isEmpty && !isLoading
    }
}

// MARK: - Factory (for DI)
extension LoginViewModel {
    static func live() -> LoginViewModel {
        LoginViewModel(loginUseCase: Resolver.resolve())
    }
    
    static func mock() -> LoginViewModel {
        LoginViewModel(loginUseCase: MockLoginUseCase())
    }
}
```

### 2. View (SwiftUI)

```swift
struct LoginView: View {
    // MARK: - ViewModel
    @StateObject private var viewModel: LoginViewModel
    
    // MARK: - Animation State (CRITICAL: phải ở @State)
    @State private var buttonScale: CGFloat = 1.0
    @State private var shakeOffset: CGFloat = 0
    
    // MARK: - Navigation
    @EnvironmentObject private var router: AppRouter
    
    init(viewModel: LoginViewModel = .live()) {
        _viewModel = StateObject(wrappedValue: viewModel)
    }
    
    var body: some View {
        VStack(spacing: 20) {
            emailField
            passwordField
            loginButton
        }
        .padding()
        .onChange(of: viewModel.navigationIntent) { intent in
            handleNavigation(intent)
        }
        .onChange(of: viewModel.error) { error in
            if error != nil { triggerShakeAnimation() }
        }
    }
    
    // MARK: - Subviews
    private var emailField: some View {
        TextField("Email", text: Binding(
            get: { viewModel.email },
            set: { viewModel.updateEmail($0) }
        ))
        .textFieldStyle(.roundedBorder)
    }
    
    private var passwordField: some View {
        SecureField("Password", text: Binding(
            get: { viewModel.password },
            set: { viewModel.updatePassword($0) }
        ))
        .textFieldStyle(.roundedBorder)
    }
    
    private var loginButton: some View {
        Button("Đăng nhập") {
            Task { await viewModel.login() }
        }
        .disabled(!viewModel.isLoginEnabled)
        .scaleEffect(buttonScale)
        .offset(x: shakeOffset)
        .onChange(of: viewModel.isLoading) { loading in
            withAnimation(.spring()) {
                buttonScale = loading ? 0.95 : 1.0
            }
        }
    }
    
    // MARK: - Navigation
    private func handleNavigation(_ intent: NavigationIntent?) {
        guard let intent = intent else { return }
        switch intent {
        case .home:
            router.push(.home)
        case .forgotPassword:
            router.push(.forgotPassword)
        }
        viewModel.navigationIntent = nil
    }
    
    // MARK: - Animations
    private func triggerShakeAnimation() {
        withAnimation(.spring(response: 0.1, dampingFraction: 0.2)) {
            shakeOffset = 10
        }
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.1) {
            withAnimation(.spring()) { shakeOffset = 0 }
        }
    }
}
```

---

## ⚡ Quick Reference

### Animation Values

| Type | Đặt ở đâu | Ví dụ |
|------|-----------|-------|
| Scale, Opacity, Offset | `@State` (View) | `@State private var scale: CGFloat = 1.0` |
| Rotation, Color | `@State` (View) | `@State private var rotation: Angle = .zero` |
| Business state | `@Published` (ViewModel) | `@Published var isLoading: Bool` |

### Property Wrappers

| Wrapper | Khi nào dùng |
|---------|--------------|
| `@StateObject` | View SỞ HỮU ViewModel |
| `@ObservedObject` | View NHẬN ViewModel từ parent |
| `@State` | Animation, transient UI state |
| `@Published` | Business state trong ViewModel |
| `@Environment` | Theme, locale, system values |

### Dependency Injection

| Layer | Inject gì |
|-------|-----------|
| ViewModel | UseCases (protocols) |
| UseCase | Repositories (protocols) |
| Repository | Network/Storage services |

---

## 📁 Reference Files

| File | Nội dung | Khi nào đọc |
|------|----------|-------------|
| [presentation-patterns.md](references/presentation-patterns.md) | MVVM chi tiết | Tạo màn hình mới |
| [animation-guidelines.md](references/animation-guidelines.md) | Animation rules | Có animation |
| [navigation-patterns.md](references/navigation-patterns.md) | Navigation patterns | Setup navigation |
| [viewstate-pattern.md](references/viewstate-pattern.md) | ViewState pattern | Complex formatting |
| [state-management.md](references/state-management.md) | State patterns | @Published, @State |
| [testing.md](references/testing.md) | Unit testing | Viết tests |
| [di.md](references/di.md) | Dependency Injection | DI setup |
| [theme-system.md](references/theme-system.md) | Theme system | Styling |
| [networking.md](references/networking.md) | API calls | Network requests |
| [security.md](references/security.md) | Security best practices | Tokens, encryption |
| [storage.md](references/storage.md) | Data persistence | Keychain, Realm |
| [app-store-submission.md](references/app-store-submission.md) | App Store | Submit app |
| [liquid-glass.md](references/liquid-glass.md) | iOS 26+ | Liquid Glass UI |
| [iap.md](references/iap.md) | In-App Purchase | Paywall, subscriptions |
| [templates/](references/templates/index.md) | Code templates | Generate code |

---

## ✅ Code Generation Checklist

Trước khi generate code, validate:

### ViewModel
- [ ] Là `class` conform `ObservableObject`
- [ ] `@Published` chỉ cho business state
- [ ] KHÔNG có `CGFloat`, `Angle` cho animation
- [ ] Inject UseCases (KHÔNG Repository)
- [ ] Có `static func mock()` và `live()`

### View
- [ ] `@StateObject` khi sở hữu ViewModel
- [ ] `@State` cho animation values
- [ ] `.onChange()` để trigger animation từ business state
- [ ] KHÔNG có business logic

### Navigation
- [ ] Intent-based (default) hoặc Navigator protocol
- [ ] Consume intent sau khi handle

