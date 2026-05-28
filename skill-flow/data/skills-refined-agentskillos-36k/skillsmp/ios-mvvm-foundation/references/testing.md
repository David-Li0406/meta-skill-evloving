# Testing

> Unit testing cho MVVM với XCTest và mock dependencies.

---

## 🎯 Testing Strategy

| Layer | Test | Framework |
|-------|------|-----------|
| ViewModel | Unit tests với mocks | XCTest |
| UseCase | Unit tests | XCTest |
| View | UI tests | XCUITest |

**Coverage target**: >80%

---

## 📦 ViewModel Tests

### Basic Structure

```swift
import XCTest
import Combine
@testable import YourApp

class LoginViewModelTests: XCTestCase {
    var viewModel: LoginViewModel!
    var mockUseCase: MockLoginUseCase!
    var cancellables: Set<AnyCancellable>!
    
    override func setUp() {
        super.setUp()
        mockUseCase = MockLoginUseCase()
        viewModel = LoginViewModel(loginUseCase: mockUseCase)
        cancellables = []
    }
    
    override func tearDown() {
        cancellables = nil
        viewModel = nil
        mockUseCase = nil
        super.tearDown()
    }
}
```

### Test Async Methods

```swift
func testLoginSuccess() async {
    // Given
    mockUseCase.result = .success(User.mock)
    viewModel.updateEmail("test@test.com")
    viewModel.updatePassword("password123")
    
    // When
    await viewModel.login()
    
    // Then
    XCTAssertEqual(viewModel.status, .success)
    XCTAssertTrue(mockUseCase.executeCalled)
    XCTAssertEqual(mockUseCase.lastEmail, "test@test.com")
}

func testLoginFailure() async {
    // Given
    mockUseCase.result = .failure(APIError.unauthorized)
    
    // When
    await viewModel.login()
    
    // Then
    XCTAssertEqual(viewModel.status, .error)
    XCTAssertNotNil(viewModel.errorMessage)
}
```

### Test @Published Changes

```swift
func testStatusChangesToLoading() {
    let expectation = XCTestExpectation(description: "Status loading")
    
    viewModel.$status
        .dropFirst()  // Skip initial value
        .sink { status in
            if status == .loading {
                expectation.fulfill()
            }
        }
        .store(in: &cancellables)
    
    Task { await viewModel.login() }
    
    wait(for: [expectation], timeout: 1.0)
}
```

### Test Navigation Intent

```swift
func testLoginSuccess_SetsNavigationIntent() async {
    // Given
    mockUseCase.result = .success(User.mock)
    
    // When
    await viewModel.login()
    
    // Then
    XCTAssertEqual(viewModel.navigationIntent, .home)
}
```

---

## 🎭 Mock Dependencies

### Mock UseCase

```swift
class MockLoginUseCase: LoginUseCaseProtocol {
    var result: Result<User, Error>!
    var executeCalled = false
    var callCount = 0
    var lastEmail: String?
    var lastPassword: String?
    
    func execute(email: String, password: String) async throws -> User {
        executeCalled = true
        callCount += 1
        lastEmail = email
        lastPassword = password
        
        switch result! {
        case .success(let user): return user
        case .failure(let error): throw error
        }
    }
}
```

### Mock Service

```swift
class MockAnalyticsService: AnalyticsServiceProtocol {
    var trackedEvents: [AnalyticsEvent] = []
    
    func track(event: AnalyticsEvent) async {
        trackedEvents.append(event)
    }
}
```

### Mock Navigator

```swift
class MockNavigator: Navigator {
    var pushedRoutes: [Route] = []
    var presentedRoutes: [Route] = []
    var popCalled = false
    var dismissCalled = false
    
    func push(_ route: Route) {
        pushedRoutes.append(route)
    }
    
    func present(_ route: Route) {
        presentedRoutes.append(route)
    }
    
    func pop() {
        popCalled = true
    }
    
    func dismiss() {
        dismissCalled = true
    }
}
```

---

## 📊 Test Data

### Mock Models

```swift
extension User {
    static var mock: User {
        User(
            id: "user-123",
            email: "test@test.com",
            name: "Test User"
        )
    }
}

extension Item {
    static var mockList: [Item] {
        [
            Item(id: "1", title: "Item 1"),
            Item(id: "2", title: "Item 2"),
            Item(id: "3", title: "Item 3")
        ]
    }
}
```

---

## 🧪 UseCase Tests

```swift
class LoginUseCaseTests: XCTestCase {
    var useCase: LoginUseCase!
    var mockRepository: MockAuthRepository!
    
    override func setUp() {
        mockRepository = MockAuthRepository()
        useCase = LoginUseCase(authRepository: mockRepository)
    }
    
    func testExecute_CallsRepository() async throws {
        // Given
        mockRepository.loginResult = .success(User.mock)
        
        // When
        let user = try await useCase.execute(
            email: "test@test.com",
            password: "password"
        )
        
        // Then
        XCTAssertEqual(user.email, "test@test.com")
        XCTAssertTrue(mockRepository.loginCalled)
    }
}
```

---

## ✅ Testing Checklist

### ViewModel Tests
- [ ] Test initial state
- [ ] Test user actions (methods)
- [ ] Test @Published state changes
- [ ] Test error handling
- [ ] Test navigation intents
- [ ] Test computed properties

### UseCase Tests
- [ ] Test success path
- [ ] Test error path
- [ ] Test input validation

### Mock Requirements
- [ ] All dependencies have mock versions
- [ ] Mocks track method calls
- [ ] Mocks can return configurable results

---

## 🔗 Related

- [presentation-patterns.md](presentation-patterns.md) - ViewModel structure
- [di.md](di.md) - Dependency injection for testing

