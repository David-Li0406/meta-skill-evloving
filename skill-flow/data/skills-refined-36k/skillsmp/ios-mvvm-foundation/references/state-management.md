# State Management

> ObservableObject ViewModels với @Published properties cho MVVM state management.

---

## 🎯 Overview

| Aspect | Description |
|--------|-------------|
| **Framework** | MVVM (Model-View-ViewModel) |
| **Async Pattern** | async/await + Combine Publishers |
| **State Container** | ObservableObject class |

---

## 📦 State Ownership

### Business State → ViewModel (@Published)

```swift
final class LoginViewModel: ObservableObject {
    @Published var isLoading: Bool = false
    @Published var userData: User?
    @Published var errorMessage: String?
}
```

- **Location**: ViewModel `@Published` properties
- **Mechanism**: ObservableObject class, updated via methods
- **Examples**: `loginStatus`, `userData`, `errorMessage`, `isLoading`

### UI Animation State → View (@State)

```swift
struct LoginView: View {
    @State private var buttonScale: CGFloat = 1.0
    @State private var shakeOffset: CGFloat = 0
}
```

- **Location**: View `@State` properties
- **Mechanism**: SwiftUI @State
- **Examples**: `animationProgress`, `dragOffset`, `rotation`, `buttonScale`
- **Performance**: Optimized for 60fps, bypasses ViewModel overhead

> ⚠️ **CRITICAL**: NEVER put animation values in ViewModel @Published

### Navigation State → ViewModel (@Published enum)

```swift
@Published var navigationIntent: NavigationIntent?

enum NavigationIntent: Equatable {
    case home
    case login
}
```

---

## 🏗️ ViewModel Pattern

### Basic Structure

```swift
final class LoginViewModel: ObservableObject {
    // MARK: - Published State
    @Published private(set) var email = ""
    @Published private(set) var isLoading = false
    
    // MARK: - Dependencies
    private let loginUseCase: LoginUseCaseProtocol
    
    init(loginUseCase: LoginUseCaseProtocol) {
        self.loginUseCase = loginUseCase
    }
    
    // MARK: - Actions
    func login() async {
        isLoading = true
        defer { isLoading = false }
        
        do {
            let user = try await loginUseCase.execute(email: email, password: password)
            await MainActor.run {
                self.user = user
                navigationIntent = .home
            }
        } catch {
            await MainActor.run {
                self.error = error
            }
        }
    }
}
```

### View Integration

```swift
struct LoginView: View {
    @StateObject private var viewModel: LoginViewModel
    
    var body: some View {
        Text(viewModel.email)
    }
}
```

---

## 🎨 Property Wrappers

| Wrapper | Usage | Scope |
|---------|-------|-------|
| `@State` | Animation, UI-local state | Private to View |
| `@StateObject` | View owns ViewModel | View lifetime |
| `@ObservedObject` | View receives ViewModel | External lifetime |
| `@FocusState` | TextField focus | View-local |
| `@GestureState` | Gesture animations | Gesture-local |

### @State với Animation

```swift
@State private var buttonScale: CGFloat = 1.0

.onChange(of: viewModel.isLoading) { loading in
    withAnimation {
        buttonScale = loading ? 0.95 : 1.0
    }
}
```

---

## 📊 State Patterns

### Enum State Machine (Preferred)

```swift
final class LoginViewModel: ObservableObject {
    @Published private(set) var status: Status = .idle
    
    enum Status: Equatable {
        case idle
        case loading
        case success(User)
        case error(String)
    }
}
```

**Benefits:**
- No invalid states
- Clear transitions
- Type safety

### Navigation Intent

```swift
@Published var navigationIntent: NavigationIntent?

enum NavigationIntent: Equatable {
    case home
    case login
}

// In View
.onChange(of: viewModel.navigationIntent) { intent in
    handleNavigation(intent)
    viewModel.navigationIntent = nil  // Consume
}
```

---

## 🧵 Threading Rules

### ViewModel Threading

| Context | Rule |
|---------|------|
| Method calls | Can be from any thread |
| State updates | Must be on MainActor |
| Async methods | Background threads OK |

### MainActor Usage

```swift
func fetchData() async {
    let data = await apiClient.fetch()  // Background
    await MainActor.run {
        self.items = data  // Main thread
    }
}
```

---

## 🎬 Animation State Management

### ✅ Correct Pattern

```swift
// ViewModel - Business state only
final class TaskViewModel: ObservableObject {
    @Published var status: Status = .idle
    
    enum Status { case idle, active, paused }
}

// View - Animation state
struct TaskView: View {
    @StateObject private var viewModel = TaskViewModel()
    @State private var pulseScale: CGFloat = 1.0
    
    var body: some View {
        Circle()
            .scaleEffect(pulseScale)
            .onChange(of: viewModel.status) { status in
                if status == .active {
                    withAnimation(.easeInOut.repeatForever()) {
                        pulseScale = 1.2
                    }
                }
            }
    }
}
```

### ❌ Wrong Pattern

```swift
// DON'T DO THIS
final class TaskViewModel: ObservableObject {
    @Published var pulseScale: CGFloat = 1.0  // ❌ Animation in ViewModel
}
```

### Why Separate?

| Reason | Explanation |
|--------|-------------|
| **Performance** | ViewModel updates expensive, animations need 60fps |
| **Architecture** | Animations are UI concerns, not business logic |
| **Testability** | Business tests don't need to know about animations |

---

## 📋 Quick Reference

### Do's ✅

- Use `@Published` for business state
- Use `@State` for animations
- Use enum for mutually exclusive states
- Use `MainActor.run` for UI updates from background
- Consume navigation intent after handling

### Don'ts ❌

- Put CGFloat/Double/Angle in ViewModel
- Update @Published from background thread
- Forget to consume navigation intent
- Mix business logic with animation logic
