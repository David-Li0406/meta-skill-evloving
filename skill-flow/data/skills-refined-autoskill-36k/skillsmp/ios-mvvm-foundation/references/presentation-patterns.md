# MVVM Presentation Patterns

> Chi tiết về ViewModel, View, ViewState trong MVVM architecture.

---

## ⚠️ CRITICAL RULE

```
Animation state → @State (View)
Business state → @Published (ViewModel)
KHÔNG BAO GIỜ đặt animation values trong ViewModel @Published
```

---

## 📦 ViewModel

### Definition

```swift
final class {Feature}ViewModel: ObservableObject {
    // MARK: - Published State
    @Published private(set) var status: Status = .idle
    @Published private(set) var data: [Item] = []
    @Published private(set) var errorMessage: String?
    @Published var navigationIntent: NavigationIntent?
    
    enum Status: Equatable {
        case idle, loading, success, error
    }
    
    enum NavigationIntent: Equatable {
        case detail(id: String)
        case settings
    }
    
    // MARK: - Dependencies
    private let useCase: UseCaseProtocol
    
    init(useCase: UseCaseProtocol) {
        self.useCase = useCase
    }
    
    // MARK: - User Actions
    func loadData() async {
        status = .loading
        do {
            data = try await useCase.execute()
            status = .success
        } catch {
            status = .error
            errorMessage = error.localizedDescription
        }
    }
    
    // MARK: - Computed Properties
    var isLoading: Bool { status == .loading }
    var isEmpty: Bool { data.isEmpty && status == .success }
}

// MARK: - Factory
extension {Feature}ViewModel {
    static func live() -> {Feature}ViewModel {
        .init(useCase: Resolver.resolve())
    }
    
    static func mock() -> {Feature}ViewModel {
        .init(useCase: MockUseCase())
    }
}
```

### Rules

| ✅ PHẢI | ❌ KHÔNG ĐƯỢC |
|---------|---------------|
| `class` conform `ObservableObject` | `struct` ViewModel |
| `@Published` cho business state | `@Published var buttonScale: CGFloat` |
| Inject UseCases via init | Inject Repository trực tiếp |
| `async` methods cho async ops | Synchronous blocking calls |
| `private(set)` cho read-only state | Public mutable state |
| Factory methods (`live()`, `mock()`) | Direct init trong View |

---

## 📱 View

### Definition

```swift
struct {Feature}View: View {
    // MARK: - ViewModel
    @StateObject private var viewModel: {Feature}ViewModel
    
    // MARK: - Environment
    @Environment(\.theme) var theme
    @EnvironmentObject var router: AppRouter
    
    // MARK: - Animation State (CRITICAL: phải ở @State)
    @State private var buttonScale: CGFloat = 1.0
    @State private var isShaking = false
    
    // MARK: - Init
    init(viewModel: {Feature}ViewModel = .live()) {
        _viewModel = StateObject(wrappedValue: viewModel)
    }
    
    var body: some View {
        VStack {
            content
        }
        .onChange(of: viewModel.status) { status in
            handleStatusChange(status)
        }
        .onChange(of: viewModel.navigationIntent) { intent in
            handleNavigation(intent)
        }
    }
    
    // MARK: - Navigation
    private func handleNavigation(_ intent: NavigationIntent?) {
        guard let intent = intent else { return }
        switch intent {
        case .detail(let id):
            router.push(.detail(id: id))
        case .settings:
            router.push(.settings)
        }
        viewModel.navigationIntent = nil  // Consume
    }
    
    // MARK: - Animations
    private func handleStatusChange(_ status: Status) {
        switch status {
        case .loading:
            withAnimation(.easeInOut(duration: 0.15)) { 
                buttonScale = 0.95 
            }
        case .error:
            triggerShakeAnimation()
        default:
            withAnimation { buttonScale = 1.0 }
        }
    }
    
    private func triggerShakeAnimation() {
        withAnimation(.spring(response: 0.1, dampingFraction: 0.2)) {
            isShaking = true
        }
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.3) {
            isShaking = false
        }
    }
}
```

### Property Wrappers

| Wrapper | Sử dụng cho | Ví dụ |
|---------|-------------|-------|
| `@StateObject` | View **sở hữu** ViewModel | `@StateObject private var viewModel` |
| `@ObservedObject` | View **nhận** ViewModel từ parent | `@ObservedObject var viewModel` |
| `@State` | Animation, transient UI state | `@State private var scale: CGFloat` |
| `@FocusState` | TextField focus | `@FocusState private var isFocused` |
| `@Environment` | Theme, locale, etc. | `@Environment(\.theme) var theme` |

---

## 📊 ViewState Pattern (Optional)

Dùng khi View có nhiều formatting/mapping logic.

### ViewModel với ViewState

```swift
class LoginViewModel: ObservableObject {
    // Public: ViewState cho View
    @Published private(set) var viewState: ViewState = .idle
    
    // Private: Business state
    @Published private var email: String = ""
    @Published private var password: String = ""
    @Published private var status: Status = .idle
    
    struct ViewState: Equatable {
        let buttonTitle: String
        let isButtonEnabled: Bool
        let showsLoading: Bool
        let errorMessage: String?
        
        static let idle = ViewState(
            buttonTitle: "Đăng nhập",
            isButtonEnabled: false,
            showsLoading: false,
            errorMessage: nil
        )
    }
    
    func emailChanged(_ newEmail: String) {
        email = newEmail
        updateViewState()
    }
    
    private func updateViewState() {
        viewState = ViewState(
            buttonTitle: status == .loading ? "Đang xử lý..." : "Đăng nhập",
            isButtonEnabled: !email.isEmpty && !password.isEmpty && status != .loading,
            showsLoading: status == .loading,
            errorMessage: status == .error ? "Đăng nhập thất bại" : nil
        )
    }
}
```

### View đọc ViewState

```swift
var body: some View {
    Button(viewModel.viewState.buttonTitle) {
        Task { await viewModel.login() }
    }
    .disabled(!viewModel.viewState.isButtonEnabled)
}
```

### Khi nào dùng ViewState?

| Dùng ViewState | Không cần ViewState |
|----------------|---------------------|
| Nhiều formatting logic | Màn hình đơn giản |
| Nhiều computed properties | Ít state properties |
| Cần test rendering logic | Direct binding đủ |

---

## 🔗 Related

- [animation-guidelines.md](animation-guidelines.md) - Animation rules
- [navigation-patterns.md](navigation-patterns.md) - Navigation patterns
- [viewstate-pattern.md](viewstate-pattern.md) - ViewState chi tiết

