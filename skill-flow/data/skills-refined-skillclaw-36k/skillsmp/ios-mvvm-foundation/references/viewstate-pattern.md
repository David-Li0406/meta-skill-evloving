# ViewState Pattern

> Optional pattern cho màn hình phức tạp với nhiều formatting logic.

---

## 🎯 Khi Nào Dùng?

| Dùng ViewState | Không cần |
|----------------|-----------|
| Nhiều formatting/mapping logic | Màn hình đơn giản |
| Nhiều `@Published` cần group | Ít state properties |
| Muốn test rendering logic | Direct binding đủ |
| Optimize SwiftUI updates | Performance OK |

---

## 📦 Implementation

### ViewModel với ViewState

```swift
class LoginViewModel: ObservableObject {
    // MARK: - Public ViewState (single source for View)
    @Published private(set) var viewState: ViewState = .idle
    
    // MARK: - Private Business State
    @Published private var email: String = ""
    @Published private var password: String = ""
    @Published private var status: Status = .idle
    
    // MARK: - ViewState Definition
    struct ViewState: Equatable {
        let emailText: String
        let passwordText: String
        let buttonTitle: String
        let isButtonEnabled: Bool
        let showsLoading: Bool
        let errorMessage: String?
        
        static let idle = ViewState(
            emailText: "",
            passwordText: "",
            buttonTitle: "Đăng nhập",
            isButtonEnabled: false,
            showsLoading: false,
            errorMessage: nil
        )
    }
    
    private enum Status: Equatable {
        case idle, loading, success, error(String)
    }
    
    // MARK: - User Actions
    func emailChanged(_ newEmail: String) {
        email = newEmail
        updateViewState()
    }
    
    func passwordChanged(_ newPassword: String) {
        password = newPassword
        updateViewState()
    }
    
    func login() async {
        status = .loading
        updateViewState()
        
        do {
            try await loginUseCase.execute(email: email, password: password)
            status = .success
        } catch {
            status = .error(error.localizedDescription)
        }
        updateViewState()
    }
    
    // MARK: - ViewState Update
    private func updateViewState() {
        let isLoading = status == .loading
        let errorMessage: String? = {
            if case .error(let message) = status {
                return message
            }
            return nil
        }()
        
        viewState = ViewState(
            emailText: email,
            passwordText: password,
            buttonTitle: isLoading ? "Đang xử lý..." : "Đăng nhập",
            isButtonEnabled: !email.isEmpty && !password.isEmpty && !isLoading,
            showsLoading: isLoading,
            errorMessage: errorMessage
        )
    }
}
```

### View đọc ViewState

```swift
struct LoginView: View {
    @StateObject var viewModel: LoginViewModel
    
    // Animation vẫn ở @State
    @State private var buttonScale: CGFloat = 1.0
    
    var body: some View {
        VStack(spacing: 20) {
            TextField("Email", text: Binding(
                get: { viewModel.viewState.emailText },
                set: { viewModel.emailChanged($0) }
            ))
            .textFieldStyle(.roundedBorder)
            
            SecureField("Password", text: Binding(
                get: { viewModel.viewState.passwordText },
                set: { viewModel.passwordChanged($0) }
            ))
            .textFieldStyle(.roundedBorder)
            
            Button(viewModel.viewState.buttonTitle) {
                Task { await viewModel.login() }
            }
            .disabled(!viewModel.viewState.isButtonEnabled)
            .scaleEffect(buttonScale)
            
            if viewModel.viewState.showsLoading {
                ProgressView()
            }
            
            if let error = viewModel.viewState.errorMessage {
                Text(error)
                    .foregroundColor(.red)
                    .font(.caption)
            }
        }
        .padding()
        .onChange(of: viewModel.viewState.showsLoading) { loading in
            withAnimation(.easeInOut(duration: 0.15)) {
                buttonScale = loading ? 0.95 : 1.0
            }
        }
    }
}
```

---

## 🔄 Combine Auto-Update (Alternative)

```swift
class LoginViewModel: ObservableObject {
    @Published private(set) var viewState: ViewState = .idle
    @Published private var email: String = ""
    @Published private var password: String = ""
    @Published private var status: Status = .idle
    
    private var cancellables = Set<AnyCancellable>()
    
    init() {
        setupBindings()
    }
    
    private func setupBindings() {
        Publishers.CombineLatest3($email, $password, $status)
            .map { email, password, status in
                let isLoading = status == .loading
                return ViewState(
                    emailText: email,
                    passwordText: password,
                    buttonTitle: isLoading ? "Đang xử lý..." : "Đăng nhập",
                    isButtonEnabled: !email.isEmpty && !password.isEmpty && !isLoading,
                    showsLoading: isLoading,
                    errorMessage: nil
                )
            }
            .assign(to: &$viewState)
    }
}
```

---

## ✅ Rules

| ✅ Do | ❌ Don't |
|-------|---------|
| ViewState là `struct Equatable` | Class hoặc non-Equatable |
| Chỉ chứa View-ready data | Raw business entities |
| Nested trong ViewModel | File riêng |
| Animation vẫn ở View `@State` | Animation trong ViewState |
| `private(set)` cho viewState | Public mutable |

---

## 🧪 Testing

```swift
func testViewState_WhenLoading() async {
    let viewModel = LoginViewModel.mock()
    viewModel.emailChanged("test@test.com")
    viewModel.passwordChanged("password123")
    
    // Trigger loading
    Task { await viewModel.login() }
    
    // Wait a bit for loading state
    try? await Task.sleep(nanoseconds: 100_000_000)
    
    XCTAssertTrue(viewModel.viewState.showsLoading)
    XCTAssertEqual(viewModel.viewState.buttonTitle, "Đang xử lý...")
    XCTAssertFalse(viewModel.viewState.isButtonEnabled)
}

func testViewState_ButtonEnabled() {
    let viewModel = LoginViewModel.mock()
    
    // Initially disabled
    XCTAssertFalse(viewModel.viewState.isButtonEnabled)
    
    // After email only - still disabled
    viewModel.emailChanged("test@test.com")
    XCTAssertFalse(viewModel.viewState.isButtonEnabled)
    
    // After password - enabled
    viewModel.passwordChanged("password123")
    XCTAssertTrue(viewModel.viewState.isButtonEnabled)
}
```

---

## 🔗 Related

- [presentation-patterns.md](presentation-patterns.md) - MVVM patterns
- [animation-guidelines.md](animation-guidelines.md) - Animation rules

