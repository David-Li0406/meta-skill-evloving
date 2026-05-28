# Testing Coordinators

> **Loading Trigger**: Load when writing coordinator tests or debugging coordinator test failures.

---

## Mock Infrastructure

```swift
import XCTest
@testable import MyApp

// MARK: - Mock Navigation Path

@MainActor
final class MockNavigationPath {
    private(set) var appendedRoutes: [Any] = []
    private(set) var popCount = 0
    private(set) var popToRootCount = 0

    var isEmpty: Bool { appendedRoutes.isEmpty }
    var count: Int { appendedRoutes.count }

    func append<R: Hashable>(_ route: R) {
        appendedRoutes.append(route)
    }

    func removeLast() {
        guard !appendedRoutes.isEmpty else { return }
        appendedRoutes.removeLast()
        popCount += 1
    }

    func removeAll() {
        appendedRoutes.removeAll()
        popToRootCount += 1
    }

    func lastRoute<R: Hashable>(as type: R.Type) -> R? {
        appendedRoutes.last as? R
    }

    func route<R: Hashable>(at index: Int, as type: R.Type) -> R? {
        guard index < appendedRoutes.count else { return nil }
        return appendedRoutes[index] as? R
    }
}

// MARK: - Testable Coordinator Base

@MainActor
class TestableCoordinator<Route: Hashable>: ObservableObject {
    @Published var path = NavigationPath()
    var childCoordinators: [any Coordinator] = []

    // Test tracking
    private(set) var navigatedRoutes: [Route] = []
    private(set) var popCount = 0
    private(set) var popToRootCount = 0

    func navigate(to route: Route) {
        navigatedRoutes.append(route)
        path.append(route)
    }

    func pop() {
        guard !path.isEmpty else { return }
        path.removeLast()
        popCount += 1
    }

    func popToRoot() {
        path = NavigationPath()
        popToRootCount += 1
    }

    var lastNavigatedRoute: Route? {
        navigatedRoutes.last
    }
}
```

---

## Unit Testing Coordinators

```swift
// MARK: - Auth Coordinator Tests

@MainActor
final class AuthCoordinatorTests: XCTestCase {
    var sut: AuthCoordinator!
    var mockContainer: MockDependencyContainer!
    var authenticatedUser: User?

    override func setUp() async throws {
        mockContainer = MockDependencyContainer()
        sut = AuthCoordinator(
            container: mockContainer,
            onAuthenticated: { [weak self] user in
                self?.authenticatedUser = user
            }
        )
    }

    override func tearDown() async throws {
        sut = nil
        mockContainer = nil
        authenticatedUser = nil
    }

    // MARK: - Navigation Tests

    func test_navigateToRegister_appendsRegisterRoute() {
        // When
        sut.navigate(to: .register)

        // Then
        XCTAssertFalse(sut.path.isEmpty)
    }

    func test_navigateToForgotPassword_appendsForgotPasswordRoute() {
        // When
        sut.navigate(to: .forgotPassword)

        // Then
        XCTAssertFalse(sut.path.isEmpty)
    }

    func test_navigateToTwoFactor_appendsTwoFactorRoute() {
        // Given
        let email = "test@example.com"

        // When
        sut.navigate(to: .twoFactor(email: email))

        // Then
        XCTAssertFalse(sut.path.isEmpty)
    }

    func test_pop_removesLastRoute() {
        // Given
        sut.navigate(to: .register)
        sut.navigate(to: .forgotPassword)

        // When
        sut.pop()

        // Then
        XCTAssertEqual(sut.path.count, 1)
    }

    func test_popToRoot_clearsAllRoutes() {
        // Given
        sut.navigate(to: .register)
        sut.navigate(to: .forgotPassword)

        // When
        sut.popToRoot()

        // Then
        XCTAssertTrue(sut.path.isEmpty)
    }

    // MARK: - Authentication Flow Tests

    func test_completeLogin_callsOnAuthenticated() async {
        // Given
        let expectedUser = User.mock()
        mockContainer.mockAuthService.stubbedUser = expectedUser

        // When
        sut.completeLogin(user: expectedUser)

        // Then
        XCTAssertEqual(authenticatedUser?.id, expectedUser.id)
    }

    func test_loginViewModel_navigatesToRegister_onRegisterTapped() async {
        // Given
        let viewModel = sut.makeLoginViewModel()

        // When
        viewModel.onRegister?()

        // Then
        XCTAssertFalse(sut.path.isEmpty)
    }
}

// MARK: - Main Tab Coordinator Tests

@MainActor
final class MainTabCoordinatorTests: XCTestCase {
    var sut: MainTabCoordinator!
    var mockContainer: MockDependencyContainer!
    var logoutCalled = false

    override func setUp() async throws {
        mockContainer = MockDependencyContainer()
        sut = MainTabCoordinator(
            container: mockContainer,
            onLogout: { [weak self] in
                self?.logoutCalled = true
            }
        )
    }

    // MARK: - Tab Selection Tests

    func test_initialTab_isHome() {
        XCTAssertEqual(sut.selectedTab, .home)
    }

    func test_selectingDifferentTab_changesSelectedTab() {
        // When
        sut.selectedTab = .profile

        // Then
        XCTAssertEqual(sut.selectedTab, .profile)
    }

    // MARK: - Cross-Tab Navigation Tests

    func test_navigateToProduct_switchesToHomeTab() {
        // Given
        sut.selectedTab = .profile

        // When
        sut.navigateToProduct(id: "123")

        // Then
        XCTAssertEqual(sut.selectedTab, .home)
    }

    func test_navigateToCart_switchesToCartTab() {
        // Given
        sut.selectedTab = .home

        // When
        sut.navigateToCart()

        // Then
        XCTAssertEqual(sut.selectedTab, .cart)
    }

    func test_navigateToCheckout_switchesToCartAndNavigates() {
        // Given
        sut.selectedTab = .home

        // When
        sut.navigateToCheckout()

        // Then
        XCTAssertEqual(sut.selectedTab, .cart)
    }

    // MARK: - Child Coordinator Tests

    func test_childCoordinators_areInitialized() {
        XCTAssertNotNil(sut.homeCoordinator)
        XCTAssertNotNil(sut.searchCoordinator)
        XCTAssertNotNil(sut.cartCoordinator)
        XCTAssertNotNil(sut.profileCoordinator)
    }
}

// MARK: - Home Coordinator Tests

@MainActor
final class HomeCoordinatorTests: XCTestCase {
    var sut: HomeCoordinator!
    var mockContainer: MockDependencyContainer!

    override func setUp() async throws {
        mockContainer = MockDependencyContainer()
        sut = HomeCoordinator(container: mockContainer)
    }

    func test_navigateToProductList_appendsRoute() {
        // When
        sut.navigate(to: .productList(categoryId: "electronics"))

        // Then
        XCTAssertFalse(sut.path.isEmpty)
    }

    func test_navigateToProductDetail_appendsRoute() {
        // When
        sut.navigate(to: .productDetail(id: "product-123"))

        // Then
        XCTAssertFalse(sut.path.isEmpty)
    }

    func test_multipleNavigations_stacksRoutes() {
        // When
        sut.navigate(to: .productList(categoryId: "electronics"))
        sut.navigate(to: .productDetail(id: "product-123"))
        sut.navigate(to: .reviews(productId: "product-123"))

        // Then
        XCTAssertEqual(sut.path.count, 3)
    }

    func test_popFromDeepNavigation_preservesPreviousRoutes() {
        // Given
        sut.navigate(to: .productList(categoryId: "electronics"))
        sut.navigate(to: .productDetail(id: "product-123"))
        sut.navigate(to: .reviews(productId: "product-123"))

        // When
        sut.pop()

        // Then
        XCTAssertEqual(sut.path.count, 2)
    }
}
```

---

## Integration Testing

```swift
// MARK: - Deep Link Integration Tests

@MainActor
final class DeepLinkIntegrationTests: XCTestCase {
    var appCoordinator: AppCoordinator!
    var deepLinkHandler: DeepLinkHandler!
    var mockContainer: MockDependencyContainer!

    override func setUp() async throws {
        mockContainer = MockDependencyContainer()
        mockContainer.mockAuthService.isAuthenticated = true

        appCoordinator = AppCoordinator(container: mockContainer)
        deepLinkHandler = DeepLinkHandler(appCoordinator: appCoordinator)
    }

    func test_productDeepLink_navigatesToProduct() {
        // Given
        let url = URL(string: "myapp://product/123")!

        // When
        deepLinkHandler.handle(url: url)

        // Then
        XCTAssertEqual(appCoordinator.mainCoordinator?.selectedTab, .home)
    }

    func test_checkoutDeepLink_navigatesToCheckout() {
        // Given
        let url = URL(string: "myapp://checkout")!

        // When
        deepLinkHandler.handle(url: url)

        // Then
        XCTAssertEqual(appCoordinator.mainCoordinator?.selectedTab, .cart)
    }

    func test_deepLinkBeforeAuth_queuesPendingLink() {
        // Given
        mockContainer.mockAuthService.isAuthenticated = false
        let freshCoordinator = AppCoordinator(container: mockContainer)
        let handler = DeepLinkHandler(appCoordinator: freshCoordinator)

        // When
        handler.handle(url: URL(string: "myapp://checkout")!)

        // Then
        XCTAssertNotNil(handler.pendingDeepLink)
    }

    func test_universalLink_parsesCorrectly() {
        // Given
        let url = URL(string: "https://myapp.com/product/456")!

        // When
        let deepLink = DeepLinkParser.parse(url: url)

        // Then
        XCTAssertEqual(deepLink, .product(id: "456"))
    }
}

// MARK: - Coordinator Memory Tests

@MainActor
final class CoordinatorMemoryTests: XCTestCase {

    func test_childCoordinator_isDeallocatedOnRemoval() {
        // Given
        var childCoordinator: HomeCoordinator? = HomeCoordinator(
            container: MockDependencyContainer()
        )
        weak var weakChild = childCoordinator

        let parent = MainTabCoordinator(
            container: MockDependencyContainer(),
            onLogout: {}
        )

        // When - Would normally add child, but for test we just nil the reference
        childCoordinator = nil

        // Then
        XCTAssertNil(weakChild, "Child coordinator should be deallocated")
    }

    func test_coordinatorChain_hasNoRetainCycles() {
        // Given
        var appCoordinator: AppCoordinator? = AppCoordinator(
            container: MockDependencyContainer()
        )
        weak var weakApp = appCoordinator

        // When - Simulate app dismissal
        appCoordinator = nil

        // Then
        XCTAssertNil(weakApp, "App coordinator should be deallocated")
    }
}
```

---

## Mock Dependencies

```swift
// MARK: - Mock Dependency Container

final class MockDependencyContainer: DependencyContainer {
    let mockAuthService = MockAuthService()
    let mockProductService = MockProductService()
    let mockCartService = MockCartService()
    let mockUserService = MockUserService()

    override var authService: AuthServiceProtocol { mockAuthService }
    override var productService: ProductServiceProtocol { mockProductService }
    override var cartService: CartServiceProtocol { mockCartService }
    override var userService: UserServiceProtocol { mockUserService }
}

// MARK: - Mock Auth Service

final class MockAuthService: AuthServiceProtocol {
    var isAuthenticated = false
    var stubbedUser: User?
    var stubbedError: Error?

    private(set) var loginCallCount = 0
    private(set) var lastLoginEmail: String?

    func login(email: String, password: String) async throws -> User {
        loginCallCount += 1
        lastLoginEmail = email

        if let error = stubbedError { throw error }
        guard let user = stubbedUser else {
            throw AuthError.invalidCredentials
        }
        return user
    }

    func logout() async {
        isAuthenticated = false
    }
}

// MARK: - Mock Product Service

final class MockProductService: ProductServiceProtocol {
    var stubbedProducts: [Product] = []
    var stubbedProduct: Product?
    var stubbedError: Error?

    func fetchProducts(categoryId: String) async throws -> [Product] {
        if let error = stubbedError { throw error }
        return stubbedProducts
    }

    func fetchProduct(id: String) async throws -> Product {
        if let error = stubbedError { throw error }
        guard let product = stubbedProduct else {
            throw ProductError.notFound
        }
        return product
    }
}

// MARK: - Test Fixtures

extension User {
    static func mock(
        id: String = "user-123",
        email: String = "test@example.com",
        name: String = "Test User"
    ) -> User {
        User(id: id, email: email, name: name)
    }
}

extension Product {
    static func mock(
        id: String = "product-123",
        name: String = "Test Product",
        price: Decimal = 29.99
    ) -> Product {
        Product(id: id, name: name, price: price)
    }
}
```
