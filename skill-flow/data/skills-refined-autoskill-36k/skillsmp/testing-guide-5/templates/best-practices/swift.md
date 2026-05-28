# XCTest 最佳实践

Swift / iOS 测试框架的配置和最佳实践指南。

## 目录

- [项目配置](#项目配置)
- [测试结构](#测试结构)
- [断言最佳实践](#断言最佳实践)
- [参数化测试](#参数化测试)
- [Mock 策略](#mock-策略)
- [异步测试](#异步测试)
- [UI 测试](#ui-测试)
- [覆盖率配置](#覆盖率配置)

---

## 项目配置

### Swift Package Manager

```swift
// Package.swift
// swift-tools-version:5.9
import PackageDescription

let package = Package(
    name: "MyProject",
    platforms: [
        .iOS(.v15),
        .macOS(.v12)
    ],
    products: [
        .library(name: "MyProject", targets: ["MyProject"]),
    ],
    dependencies: [
        // Mock 框架
        .package(url: "https://github.com/Codeido/SwiftyMock.git", from: "1.0.0"),
        // 更好的断言
        .package(url: "https://github.com/pointfreeco/swift-custom-dump.git", from: "1.0.0"),
    ],
    targets: [
        .target(
            name: "MyProject",
            dependencies: []
        ),
        .testTarget(
            name: "MyProjectTests",
            dependencies: [
                "MyProject",
                .product(name: "CustomDump", package: "swift-custom-dump"),
            ]
        ),
    ]
)
```

### Xcode 项目配置

```
MyProject/
├── MyProject/
│   ├── Sources/
│   │   ├── User/
│   │   │   ├── UserService.swift
│   │   │   └── UserRepository.swift
│   │   └── ...
│   └── MyProject.swift
├── MyProjectTests/
│   ├── User/
│   │   ├── UserServiceTests.swift
│   │   └── UserRepositoryTests.swift
│   ├── Mocks/
│   │   └── MockUserRepository.swift
│   ├── Helpers/
│   │   └── TestHelpers.swift
│   └── MyProjectTests.swift
└── MyProjectUITests/
    └── UserFlowUITests.swift
```

---

## 测试结构

### 基本结构

```swift
import XCTest
@testable import MyProject

final class UserServiceTests: XCTestCase {

    // MARK: - Properties

    private var sut: UserService!  // System Under Test
    private var mockRepository: MockUserRepository!

    // MARK: - Setup & Teardown

    override func setUp() {
        super.setUp()
        mockRepository = MockUserRepository()
        sut = UserService(repository: mockRepository)
    }

    override func tearDown() {
        sut = nil
        mockRepository = nil
        super.tearDown()
    }

    // MARK: - Create User Tests

    func test_createUser_shouldCreateUser_whenInputIsValid() {
        // Arrange
        let request = CreateUserRequest(email: "test@example.com", name: "Test User")
        mockRepository.existsByEmailResult = false

        // Act
        let result = sut.createUser(request: request)

        // Assert
        switch result {
        case .success(let user):
            XCTAssertFalse(user.id.isEmpty)
            XCTAssertEqual(user.email, "test@example.com")
            XCTAssertEqual(user.name, "Test User")
        case .failure(let error):
            XCTFail("Expected success but got error: \(error)")
        }
    }

    func test_createUser_shouldReturnError_whenEmailExists() {
        // Arrange
        let request = CreateUserRequest(email: "existing@example.com", name: "New User")
        mockRepository.existsByEmailResult = true

        // Act
        let result = sut.createUser(request: request)

        // Assert
        switch result {
        case .success:
            XCTFail("Expected failure but got success")
        case .failure(let error):
            XCTAssertEqual(error, .duplicateEmail)
        }
    }
}
```

### 测试命名规范

```swift
// ❌ 不好的命名
func testCreate() {}
func test1() {}

// ✅ 好的命名 - 方法_场景_预期结果
func test_createUser_whenInputValid_returnsUser() {}
func test_createUser_whenEmailExists_returnsError() {}

// ✅ 好的命名 - should 风格
func test_createUser_shouldCreateUser_whenInputIsValid() {}
func test_createUser_shouldReturnError_whenEmailAlreadyExists() {}
```

### 测试分组

```swift
final class UserServiceTests: XCTestCase {

    // MARK: - Create User

    func test_createUser_shouldCreateUser_whenInputIsValid() {}
    func test_createUser_shouldReturnError_whenEmailExists() {}
    func test_createUser_shouldReturnError_whenNameIsEmpty() {}

    // MARK: - Get User

    func test_getUser_shouldReturnUser_whenUserExists() {}
    func test_getUser_shouldReturnNil_whenUserNotFound() {}

    // MARK: - Update User

    func test_updateUser_shouldUpdateUser_whenUserExists() {}
    func test_updateUser_shouldReturnError_whenUserNotFound() {}
}
```

---

## 断言最佳实践

### 标准 XCTest 断言

```swift
// 相等性
XCTAssertEqual(actual, expected)
XCTAssertNotEqual(actual, unexpected)

// 布尔值
XCTAssertTrue(condition)
XCTAssertFalse(condition)

// Nil 检查
XCTAssertNil(optional)
XCTAssertNotNil(optional)

// 比较
XCTAssertGreaterThan(a, b)
XCTAssertLessThan(a, b)
XCTAssertGreaterThanOrEqual(a, b)
XCTAssertLessThanOrEqual(a, b)

// 异常
XCTAssertThrowsError(try throwingFunction()) { error in
    XCTAssertEqual(error as? MyError, .invalidInput)
}
XCTAssertNoThrow(try nonThrowingFunction())

// 带消息的断言
XCTAssertEqual(actual, expected, "用户邮箱不匹配")
```

### 禁止弱断言

```swift
// ❌ 弱断言 - 几乎不验证任何东西
XCTAssertNotNil(result)
XCTAssertTrue(result != nil)
XCTAssertFalse(list.isEmpty)

// ✅ 强断言 - 验证具体值
XCTAssertEqual(result?.status, .success)
XCTAssertEqual(result?.email, "test@example.com")
XCTAssertEqual(list.count, 3)
XCTAssertTrue(list.contains(expectedItem))
```

### 使用 CustomDump (推荐)

```swift
import CustomDump

func test_createUser_shouldCreateUser_whenInputIsValid() {
    let result = sut.createUser(request: request)

    // 更好的差异对比输出
    XCTAssertNoDifference(
        result,
        .success(User(id: "123", email: "test@example.com", name: "Test"))
    )
}
```

### 解包 Optional

```swift
// ❌ 不好的方式
func test_getUser() {
    let user = sut.getUser(id: "1")
    XCTAssertNotNil(user)
    XCTAssertEqual(user!.name, "Test")  // 强制解包危险
}

// ✅ 使用 XCTUnwrap
func test_getUser_shouldReturnUser_whenUserExists() throws {
    let user = try XCTUnwrap(sut.getUser(id: "1"))
    XCTAssertEqual(user.name, "Test")
    XCTAssertEqual(user.email, "test@example.com")
}

// ✅ 使用 guard
func test_getUser_alternative() {
    guard let user = sut.getUser(id: "1") else {
        XCTFail("User should exist")
        return
    }
    XCTAssertEqual(user.name, "Test")
}
```

### Result 断言

```swift
// 自定义 Result 断言扩展
extension XCTestCase {
    func assertSuccess<T, E: Error>(
        _ result: Result<T, E>,
        file: StaticString = #file,
        line: UInt = #line,
        then: (T) -> Void
    ) {
        switch result {
        case .success(let value):
            then(value)
        case .failure(let error):
            XCTFail("Expected success but got failure: \(error)", file: file, line: line)
        }
    }

    func assertFailure<T, E: Error & Equatable>(
        _ result: Result<T, E>,
        expectedError: E,
        file: StaticString = #file,
        line: UInt = #line
    ) {
        switch result {
        case .success(let value):
            XCTFail("Expected failure but got success: \(value)", file: file, line: line)
        case .failure(let error):
            XCTAssertEqual(error, expectedError, file: file, line: line)
        }
    }
}

// 使用
func test_createUser() {
    let result = sut.createUser(request: request)

    assertSuccess(result) { user in
        XCTAssertEqual(user.email, "test@example.com")
    }
}
```

---

## 参数化测试

### 使用循环

```swift
func test_validateEmail_shouldReturnExpectedResult() {
    let testCases: [(email: String, expected: Bool, description: String)] = [
        ("", false, "empty string"),
        (" ", false, "whitespace"),
        ("invalid", false, "missing @"),
        ("test@", false, "missing domain"),
        ("test@example.com", true, "valid email"),
    ]

    for testCase in testCases {
        let result = sut.validateEmail(testCase.email)
        XCTAssertEqual(
            result,
            testCase.expected,
            "Failed for \(testCase.description): \(testCase.email)"
        )
    }
}
```

### 使用 addTeardownBlock

```swift
func test_calculateDiscount_withVariousInputs() {
    let testCases: [(price: Int, discount: Int, expected: Int)] = [
        (100, 0, 100),
        (100, 10, 90),
        (200, 25, 150),
        (1000, 50, 500),
    ]

    for (index, testCase) in testCases.enumerated() {
        addTeardownBlock {
            // 每个测试用例后的清理
        }

        let result = sut.calculateDiscount(price: testCase.price, discount: testCase.discount)
        XCTAssertEqual(
            result,
            testCase.expected,
            "Test case \(index + 1) failed"
        )
    }
}
```

### 使用子测试

```swift
func test_validateEmail() {
    let testCases: [(email: String, expected: Bool)] = [
        ("", false),
        ("test@example.com", true),
    ]

    for testCase in testCases {
        // 每个用例作为独立的子测试
        XCTContext.runActivity(named: "Email: '\(testCase.email)'") { _ in
            let result = sut.validateEmail(testCase.email)
            XCTAssertEqual(result, testCase.expected)
        }
    }
}
```

---

## Mock 策略

### 手动创建 Mock

```swift
// 协议定义
protocol UserRepositoryProtocol {
    func save(_ user: User) throws
    func findById(_ id: String) -> User?
    func existsByEmail(_ email: String) -> Bool
}

// Mock 实现
final class MockUserRepository: UserRepositoryProtocol {

    // 记录调用
    var saveCallCount = 0
    var savedUsers: [User] = []
    var findByIdCallCount = 0
    var findByIdArguments: [String] = []

    // 配置返回值
    var saveError: Error?
    var findByIdResult: User?
    var existsByEmailResult = false

    func save(_ user: User) throws {
        saveCallCount += 1
        savedUsers.append(user)
        if let error = saveError {
            throw error
        }
    }

    func findById(_ id: String) -> User? {
        findByIdCallCount += 1
        findByIdArguments.append(id)
        return findByIdResult
    }

    func existsByEmail(_ email: String) -> Bool {
        return existsByEmailResult
    }

    // 重置
    func reset() {
        saveCallCount = 0
        savedUsers = []
        findByIdCallCount = 0
        findByIdArguments = []
        saveError = nil
        findByIdResult = nil
        existsByEmailResult = false
    }
}
```

### 使用 Mock

```swift
final class UserServiceTests: XCTestCase {

    private var sut: UserService!
    private var mockRepository: MockUserRepository!

    override func setUp() {
        super.setUp()
        mockRepository = MockUserRepository()
        sut = UserService(repository: mockRepository)
    }

    func test_createUser_shouldSaveToRepository() throws {
        // Arrange
        let request = CreateUserRequest(email: "test@example.com", name: "Test")
        mockRepository.existsByEmailResult = false

        // Act
        _ = sut.createUser(request: request)

        // Assert - 验证调用
        XCTAssertEqual(mockRepository.saveCallCount, 1)
        XCTAssertEqual(mockRepository.savedUsers.first?.email, "test@example.com")
    }

    func test_getUser_shouldCallRepositoryWithCorrectId() {
        // Arrange
        mockRepository.findByIdResult = User(id: "1", email: "test@example.com", name: "Test")

        // Act
        _ = sut.getUser(id: "1")

        // Assert
        XCTAssertEqual(mockRepository.findByIdCallCount, 1)
        XCTAssertEqual(mockRepository.findByIdArguments.first, "1")
    }
}
```

### 使用 Spy 模式

```swift
final class SpyNotificationService: NotificationServiceProtocol {

    struct SendEmailCall {
        let to: String
        let subject: String
        let body: String
    }

    private(set) var sendEmailCalls: [SendEmailCall] = []

    func sendEmail(to: String, subject: String, body: String) {
        sendEmailCalls.append(SendEmailCall(to: to, subject: subject, body: body))
    }
}

// 测试中使用
func test_registerUser_shouldSendWelcomeEmail() {
    // Arrange
    let spy = SpyNotificationService()
    let sut = UserService(repository: mockRepository, notificationService: spy)

    // Act
    sut.registerUser(request: CreateUserRequest(email: "test@example.com", name: "Test"))

    // Assert
    XCTAssertEqual(spy.sendEmailCalls.count, 1)
    XCTAssertEqual(spy.sendEmailCalls.first?.to, "test@example.com")
    XCTAssertTrue(spy.sendEmailCalls.first?.subject.contains("Welcome") ?? false)
}
```

---

## 异步测试

### 使用 async/await

```swift
func test_fetchUser_shouldReturnUser() async throws {
    // Arrange
    mockRepository.findByIdResult = User(id: "1", email: "test@example.com", name: "Test")

    // Act
    let user = try await sut.fetchUser(id: "1")

    // Assert
    XCTAssertEqual(user.email, "test@example.com")
}

func test_fetchUser_shouldThrow_whenNotFound() async {
    // Arrange
    mockRepository.findByIdResult = nil

    // Act & Assert
    do {
        _ = try await sut.fetchUser(id: "999")
        XCTFail("Expected error to be thrown")
    } catch {
        XCTAssertEqual(error as? UserError, .notFound)
    }
}
```

### 使用 XCTestExpectation

```swift
func test_fetchData_withCompletion() {
    // Arrange
    let expectation = expectation(description: "Fetch data")
    var receivedResult: Result<Data, Error>?

    // Act
    sut.fetchData { result in
        receivedResult = result
        expectation.fulfill()
    }

    // Assert
    wait(for: [expectation], timeout: 5.0)
    XCTAssertNotNil(receivedResult)
    if case .success(let data) = receivedResult {
        XCTAssertFalse(data.isEmpty)
    } else {
        XCTFail("Expected success")
    }
}

func test_multipleAsyncOperations() {
    let expectation1 = expectation(description: "First operation")
    let expectation2 = expectation(description: "Second operation")

    sut.firstOperation { _ in expectation1.fulfill() }
    sut.secondOperation { _ in expectation2.fulfill() }

    wait(for: [expectation1, expectation2], timeout: 10.0)
}
```

### 测试 Combine Publishers

```swift
import Combine

func test_userPublisher_shouldEmitUser() {
    // Arrange
    let expectation = expectation(description: "Publisher emits")
    var receivedUser: User?
    var cancellables = Set<AnyCancellable>()

    // Act
    sut.userPublisher
        .sink(
            receiveCompletion: { _ in },
            receiveValue: { user in
                receivedUser = user
                expectation.fulfill()
            }
        )
        .store(in: &cancellables)

    sut.loadUser(id: "1")

    // Assert
    wait(for: [expectation], timeout: 5.0)
    XCTAssertEqual(receivedUser?.id, "1")
}
```

---

## UI 测试

### 基本 UI 测试

```swift
import XCTest

final class LoginUITests: XCTestCase {

    private var app: XCUIApplication!

    override func setUp() {
        super.setUp()
        continueAfterFailure = false
        app = XCUIApplication()
        app.launch()
    }

    override func tearDown() {
        app = nil
        super.tearDown()
    }

    func test_login_shouldShowDashboard_whenCredentialsValid() {
        // Arrange
        let emailTextField = app.textFields["emailTextField"]
        let passwordTextField = app.secureTextFields["passwordTextField"]
        let loginButton = app.buttons["loginButton"]

        // Act
        emailTextField.tap()
        emailTextField.typeText("test@example.com")

        passwordTextField.tap()
        passwordTextField.typeText("password123")

        loginButton.tap()

        // Assert
        let dashboardTitle = app.staticTexts["dashboardTitle"]
        XCTAssertTrue(dashboardTitle.waitForExistence(timeout: 5))
    }

    func test_login_shouldShowError_whenCredentialsInvalid() {
        // Arrange
        let emailTextField = app.textFields["emailTextField"]
        let passwordTextField = app.secureTextFields["passwordTextField"]
        let loginButton = app.buttons["loginButton"]

        // Act
        emailTextField.tap()
        emailTextField.typeText("invalid@example.com")

        passwordTextField.tap()
        passwordTextField.typeText("wrongpassword")

        loginButton.tap()

        // Assert
        let errorAlert = app.alerts["errorAlert"]
        XCTAssertTrue(errorAlert.waitForExistence(timeout: 5))
        XCTAssertTrue(errorAlert.staticTexts["Invalid credentials"].exists)
    }
}
```

### Page Object 模式

```swift
// Page Objects
struct LoginPage {
    private let app: XCUIApplication

    init(app: XCUIApplication) {
        self.app = app
    }

    var emailTextField: XCUIElement {
        app.textFields["emailTextField"]
    }

    var passwordTextField: XCUIElement {
        app.secureTextFields["passwordTextField"]
    }

    var loginButton: XCUIElement {
        app.buttons["loginButton"]
    }

    func login(email: String, password: String) -> DashboardPage {
        emailTextField.tap()
        emailTextField.typeText(email)
        passwordTextField.tap()
        passwordTextField.typeText(password)
        loginButton.tap()
        return DashboardPage(app: app)
    }
}

struct DashboardPage {
    private let app: XCUIApplication

    init(app: XCUIApplication) {
        self.app = app
    }

    var title: XCUIElement {
        app.staticTexts["dashboardTitle"]
    }

    var isDisplayed: Bool {
        title.waitForExistence(timeout: 5)
    }
}

// 使用 Page Objects
func test_login_withPageObjects() {
    let loginPage = LoginPage(app: app)
    let dashboardPage = loginPage.login(email: "test@example.com", password: "password123")

    XCTAssertTrue(dashboardPage.isDisplayed)
}
```

---

## 覆盖率配置

### Xcode 配置

1. Edit Scheme → Test → Options → Code Coverage
2. 勾选 "Gather coverage for" 并选择目标

### 命令行

```bash
# 运行测试并生成覆盖率
xcodebuild test \
    -scheme MyProject \
    -destination 'platform=iOS Simulator,name=iPhone 15' \
    -enableCodeCoverage YES

# 查看覆盖率
xcrun xccov view --report Build/Logs/Test/*.xcresult
```

### CI 配置

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: macos-14
    steps:
      - uses: actions/checkout@v4

      - name: Select Xcode
        run: sudo xcode-select -s /Applications/Xcode_15.0.app

      - name: Run tests
        run: |
          xcodebuild test \
            -scheme MyProject \
            -destination 'platform=iOS Simulator,name=iPhone 15' \
            -enableCodeCoverage YES \
            -resultBundlePath TestResults.xcresult

      - name: Generate coverage report
        run: xcrun xccov view --report TestResults.xcresult --json > coverage.json

      - name: Check coverage threshold
        run: |
          COVERAGE=$(cat coverage.json | jq '.lineCoverage')
          if (( $(echo "$COVERAGE < 0.80" | bc -l) )); then
            echo "Coverage $COVERAGE is below 80%"
            exit 1
          fi
```

---

## 常用命令

```bash
# Xcode 命令行测试
xcodebuild test -scheme MyProject -destination 'platform=iOS Simulator,name=iPhone 15'

# 运行特定测试
xcodebuild test -scheme MyProject -only-testing:MyProjectTests/UserServiceTests

# Swift Package Manager 测试
swift test

# 运行特定测试
swift test --filter UserServiceTests

# 并行测试
swift test --parallel

# 生成覆盖率
swift test --enable-code-coverage

# 查看覆盖率
llvm-cov report .build/debug/MyProjectPackageTests.xctest/Contents/MacOS/MyProjectPackageTests \
    -instr-profile .build/debug/codecov/default.profdata
```

---

## 参考资源

- [XCTest Documentation](https://developer.apple.com/documentation/xctest)
- [Testing Your Apps in Xcode](https://developer.apple.com/documentation/xcode/testing-your-apps-in-xcode)
- [UI Testing in Xcode](https://developer.apple.com/library/archive/documentation/DeveloperTools/Conceptual/testing_with_xcode/chapters/09-ui_testing.html)
- [swift-custom-dump](https://github.com/pointfreeco/swift-custom-dump)
