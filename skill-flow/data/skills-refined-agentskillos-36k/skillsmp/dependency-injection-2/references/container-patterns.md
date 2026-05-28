# Dependency Injection — Container Patterns

> **Loading Trigger**: Load when designing DI container architecture or implementing complex dependency graphs.

---

## Simple Manual Container (Recommended Start)

```swift
// MARK: - Protocol Definitions

protocol AuthServiceProtocol {
    var isAuthenticated: Bool { get }
    var currentUser: User? { get }
    func login(email: String, password: String) async throws -> User
    func logout() async
}

protocol UserServiceProtocol {
    func fetchUser(id: String) async throws -> User
    func updateUser(_ user: User) async throws -> User
}

protocol ProductServiceProtocol {
    func fetchProducts(categoryId: String?) async throws -> [Product]
    func fetchProduct(id: String) async throws -> Product
}

protocol CartServiceProtocol {
    var items: [CartItem] { get }
    func addItem(_ item: CartItem) async throws
    func removeItem(id: String) async throws
    func checkout() async throws -> Order
}

protocol AnalyticsServiceProtocol {
    func track(event: AnalyticsEvent)
    func setUser(id: String?)
}

// MARK: - Simple Container

@MainActor
final class DependencyContainer {
    // MARK: - Shared Instance (optional)
    static let shared = DependencyContainer()

    // MARK: - Configuration
    private let environment: Environment
    private let baseURL: URL

    init(environment: Environment = .current) {
        self.environment = environment
        self.baseURL = environment.apiBaseURL
    }

    // MARK: - Infrastructure (Singletons)

    lazy var networkManager: NetworkManager = {
        NetworkManager(baseURL: baseURL, session: URLSession.shared)
    }()

    lazy var tokenStorage: TokenStorage = {
        KeychainTokenStorage()
    }()

    lazy var database: DatabaseManager = {
        CoreDataManager(modelName: "AppModel")
    }()

    // MARK: - Services (Singletons with dependencies)

    lazy var authService: AuthServiceProtocol = {
        AuthService(
            networkManager: networkManager,
            tokenStorage: tokenStorage
        )
    }()

    lazy var userService: UserServiceProtocol = {
        UserService(
            networkManager: networkManager,
            cache: userCache
        )
    }()

    lazy var productService: ProductServiceProtocol = {
        ProductService(
            networkManager: networkManager,
            cache: productCache
        )
    }()

    lazy var cartService: CartServiceProtocol = {
        CartService(
            networkManager: networkManager,
            database: database
        )
    }()

    lazy var analyticsService: AnalyticsServiceProtocol = {
        switch environment {
        case .production:
            return MixpanelAnalyticsService(token: Secrets.mixpanelToken)
        case .staging, .development:
            return ConsoleAnalyticsService()
        }
    }()

    // MARK: - Caches

    private lazy var userCache: Cache<String, User> = {
        Cache(maxAge: 300) // 5 minutes
    }()

    private lazy var productCache: Cache<String, Product> = {
        Cache(maxAge: 600) // 10 minutes
    }()

    // MARK: - ViewModel Factories

    func makeLoginViewModel(
        onSuccess: @escaping (User) -> Void
    ) -> LoginViewModel {
        LoginViewModel(
            authService: authService,
            analyticsService: analyticsService,
            onSuccess: onSuccess
        )
    }

    func makeHomeViewModel(
        onProductSelected: @escaping (String) -> Void
    ) -> HomeViewModel {
        HomeViewModel(
            productService: productService,
            analyticsService: analyticsService,
            onProductSelected: onProductSelected
        )
    }

    func makeProductDetailViewModel(
        productId: String,
        onAddToCart: @escaping () -> Void
    ) -> ProductDetailViewModel {
        ProductDetailViewModel(
            productId: productId,
            productService: productService,
            cartService: cartService,
            analyticsService: analyticsService,
            onAddToCart: onAddToCart
        )
    }

    func makeCartViewModel(
        onCheckout: @escaping () -> Void
    ) -> CartViewModel {
        CartViewModel(
            cartService: cartService,
            analyticsService: analyticsService,
            onCheckout: onCheckout
        )
    }

    func makeProfileViewModel(
        onLogout: @escaping () -> Void
    ) -> ProfileViewModel {
        ProfileViewModel(
            userService: userService,
            authService: authService,
            analyticsService: analyticsService,
            onLogout: onLogout
        )
    }
}

// MARK: - Environment

enum Environment {
    case development
    case staging
    case production

    static var current: Environment {
        #if DEBUG
        return .development
        #else
        if Bundle.main.appStoreReceiptURL?.lastPathComponent == "sandboxReceipt" {
            return .staging
        }
        return .production
        #endif
    }

    var apiBaseURL: URL {
        switch self {
        case .development:
            return URL(string: "http://localhost:3000/api/v1")!
        case .staging:
            return URL(string: "https://staging-api.myapp.com/v1")!
        case .production:
            return URL(string: "https://api.myapp.com/v1")!
        }
    }
}
```

---

## Scoped Container Pattern

```swift
// MARK: - Root Container (App-wide singletons)

@MainActor
final class RootContainer {
    static let shared = RootContainer()

    // App-wide singletons
    lazy var networkManager = NetworkManager()
    lazy var analyticsService: AnalyticsServiceProtocol = MixpanelAnalyticsService()
    lazy var featureFlagService = FeatureFlagService()
    lazy var crashReporter = CrashReporter()

    private init() {}
}

// MARK: - Session Container (User session scope)

@MainActor
final class SessionContainer {
    private let root: RootContainer
    let user: User

    init(root: RootContainer = .shared, user: User) {
        self.root = root
        self.user = user
    }

    // Session-scoped services
    lazy var userService: UserServiceProtocol = {
        UserService(
            networkManager: root.networkManager,
            userId: user.id
        )
    }()

    lazy var cartService: CartServiceProtocol = {
        CartService(
            networkManager: root.networkManager,
            userId: user.id
        )
    }()

    lazy var notificationService: NotificationServiceProtocol = {
        NotificationService(userId: user.id)
    }()

    // Factory for feature-scoped containers
    func makeCheckoutContainer() -> CheckoutContainer {
        CheckoutContainer(session: self)
    }

    func makeOrderHistoryContainer() -> OrderHistoryContainer {
        OrderHistoryContainer(session: self)
    }
}

// MARK: - Feature Container (Flow-specific scope)

@MainActor
final class CheckoutContainer {
    private let session: SessionContainer

    init(session: SessionContainer) {
        self.session = session
    }

    // Checkout-specific state
    private(set) var selectedPaymentMethod: PaymentMethod?
    private(set) var selectedShippingAddress: Address?
    private(set) var appliedPromoCode: String?

    // Flow-scoped services
    lazy var paymentService: PaymentServiceProtocol = {
        StripePaymentService(userId: session.user.id)
    }()

    lazy var shippingService: ShippingServiceProtocol = {
        ShippingService(networkManager: RootContainer.shared.networkManager)
    }()

    // ViewModel factories
    func makeCartReviewViewModel() -> CartReviewViewModel {
        CartReviewViewModel(
            cartService: session.cartService,
            onProceed: { [weak self] in
                // Navigate to shipping
            }
        )
    }

    func makeShippingViewModel() -> ShippingViewModel {
        ShippingViewModel(
            shippingService: shippingService,
            user: session.user,
            onAddressSelected: { [weak self] address in
                self?.selectedShippingAddress = address
            }
        )
    }

    func makePaymentViewModel() -> PaymentViewModel {
        PaymentViewModel(
            paymentService: paymentService,
            user: session.user,
            onMethodSelected: { [weak self] method in
                self?.selectedPaymentMethod = method
            }
        )
    }

    func makeOrderConfirmationViewModel() -> OrderConfirmationViewModel {
        OrderConfirmationViewModel(
            cartService: session.cartService,
            paymentService: paymentService,
            shippingAddress: selectedShippingAddress!,
            paymentMethod: selectedPaymentMethod!,
            promoCode: appliedPromoCode
        )
    }
}
```

---

## Protocol-Based Container (Testable)

```swift
// MARK: - Container Protocol

@MainActor
protocol DependencyContainerProtocol {
    var networkManager: NetworkManagerProtocol { get }
    var authService: AuthServiceProtocol { get }
    var userService: UserServiceProtocol { get }
    var productService: ProductServiceProtocol { get }
    var cartService: CartServiceProtocol { get }
    var analyticsService: AnalyticsServiceProtocol { get }

    func makeLoginViewModel(onSuccess: @escaping (User) -> Void) -> LoginViewModel
    func makeHomeViewModel(onProductSelected: @escaping (String) -> Void) -> HomeViewModel
}

// MARK: - Production Container

@MainActor
final class ProductionContainer: DependencyContainerProtocol {
    lazy var networkManager: NetworkManagerProtocol = NetworkManager()

    lazy var authService: AuthServiceProtocol = {
        AuthService(networkManager: networkManager)
    }()

    lazy var userService: UserServiceProtocol = {
        UserService(networkManager: networkManager)
    }()

    lazy var productService: ProductServiceProtocol = {
        ProductService(networkManager: networkManager)
    }()

    lazy var cartService: CartServiceProtocol = {
        CartService(networkManager: networkManager)
    }()

    lazy var analyticsService: AnalyticsServiceProtocol = {
        MixpanelAnalyticsService()
    }()

    func makeLoginViewModel(onSuccess: @escaping (User) -> Void) -> LoginViewModel {
        LoginViewModel(authService: authService, onSuccess: onSuccess)
    }

    func makeHomeViewModel(onProductSelected: @escaping (String) -> Void) -> HomeViewModel {
        HomeViewModel(productService: productService, onProductSelected: onProductSelected)
    }
}

// MARK: - Test Container

@MainActor
final class TestContainer: DependencyContainerProtocol {
    // Expose mocks for test configuration
    let mockNetworkManager = MockNetworkManager()
    let mockAuthService = MockAuthService()
    let mockUserService = MockUserService()
    let mockProductService = MockProductService()
    let mockCartService = MockCartService()
    let mockAnalyticsService = MockAnalyticsService()

    var networkManager: NetworkManagerProtocol { mockNetworkManager }
    var authService: AuthServiceProtocol { mockAuthService }
    var userService: UserServiceProtocol { mockUserService }
    var productService: ProductServiceProtocol { mockProductService }
    var cartService: CartServiceProtocol { mockCartService }
    var analyticsService: AnalyticsServiceProtocol { mockAnalyticsService }

    func makeLoginViewModel(onSuccess: @escaping (User) -> Void) -> LoginViewModel {
        LoginViewModel(authService: authService, onSuccess: onSuccess)
    }

    func makeHomeViewModel(onProductSelected: @escaping (String) -> Void) -> HomeViewModel {
        HomeViewModel(productService: productService, onProductSelected: onProductSelected)
    }
}

// MARK: - Preview Container

@MainActor
final class PreviewContainer: DependencyContainerProtocol {
    lazy var networkManager: NetworkManagerProtocol = {
        MockNetworkManager()
    }()

    lazy var authService: AuthServiceProtocol = {
        let mock = MockAuthService()
        mock.stubbedUser = .preview
        return mock
    }()

    lazy var userService: UserServiceProtocol = {
        let mock = MockUserService()
        mock.stubbedUser = .preview
        return mock
    }()

    lazy var productService: ProductServiceProtocol = {
        let mock = MockProductService()
        mock.stubbedProducts = Product.previewList
        return mock
    }()

    lazy var cartService: CartServiceProtocol = {
        let mock = MockCartService()
        mock.items = CartItem.previewList
        return mock
    }()

    lazy var analyticsService: AnalyticsServiceProtocol = {
        MockAnalyticsService()
    }()

    func makeLoginViewModel(onSuccess: @escaping (User) -> Void) -> LoginViewModel {
        LoginViewModel(authService: authService, onSuccess: onSuccess)
    }

    func makeHomeViewModel(onProductSelected: @escaping (String) -> Void) -> HomeViewModel {
        HomeViewModel(productService: productService, onProductSelected: onProductSelected)
    }
}
```

---

## SwiftUI Environment Integration

```swift
// MARK: - Environment Keys

private struct ContainerKey: EnvironmentKey {
    static let defaultValue: DependencyContainerProtocol = ProductionContainer()
}

extension EnvironmentValues {
    var container: DependencyContainerProtocol {
        get { self[ContainerKey.self] }
        set { self[ContainerKey.self] = newValue }
    }
}

// MARK: - View Extension

extension View {
    func withContainer(_ container: DependencyContainerProtocol) -> some View {
        environment(\.container, container)
    }
}

// MARK: - Usage in Views

struct ContentView: View {
    @Environment(\.container) private var container

    var body: some View {
        HomeView(
            viewModel: container.makeHomeViewModel(
                onProductSelected: { productId in
                    // Handle navigation
                }
            )
        )
    }
}

// MARK: - App Setup

@main
struct MyApp: App {
    private let container: DependencyContainerProtocol

    init() {
        #if DEBUG
        if ProcessInfo.processInfo.environment["XCODE_RUNNING_FOR_PREVIEWS"] == "1" {
            container = PreviewContainer()
        } else if CommandLine.arguments.contains("--uitesting") {
            container = TestContainer()
        } else {
            container = ProductionContainer()
        }
        #else
        container = ProductionContainer()
        #endif
    }

    var body: some Scene {
        WindowGroup {
            RootView()
                .withContainer(container)
        }
    }
}

// MARK: - Preview Support

struct HomeView_Previews: PreviewProvider {
    static var previews: some View {
        HomeView(
            viewModel: PreviewContainer().makeHomeViewModel(
                onProductSelected: { _ in }
            )
        )
        .withContainer(PreviewContainer())
    }
}
```

---

## Factory Pattern with Container

```swift
// MARK: - View Model Factory Protocol

@MainActor
protocol ViewModelFactory {
    associatedtype ViewModel
    func make() -> ViewModel
}

// MARK: - Generic Factory

@MainActor
struct Factory<T>: ViewModelFactory {
    private let builder: () -> T

    init(_ builder: @escaping () -> T) {
        self.builder = builder
    }

    func make() -> T {
        builder()
    }
}

// MARK: - Container with Factories

@MainActor
final class FactoryContainer {
    private let services: ServiceContainer

    init(services: ServiceContainer = ServiceContainer()) {
        self.services = services
    }

    // MARK: - Factories

    func loginViewModelFactory(
        onSuccess: @escaping (User) -> Void
    ) -> Factory<LoginViewModel> {
        Factory {
            LoginViewModel(
                authService: self.services.authService,
                onSuccess: onSuccess
            )
        }
    }

    func productDetailViewModelFactory(
        productId: String
    ) -> Factory<ProductDetailViewModel> {
        Factory {
            ProductDetailViewModel(
                productId: productId,
                productService: self.services.productService,
                cartService: self.services.cartService
            )
        }
    }
}

// MARK: - Usage with Factory

struct ProductDetailView: View {
    @StateObject private var viewModel: ProductDetailViewModel

    init(factory: Factory<ProductDetailViewModel>) {
        _viewModel = StateObject(wrappedValue: factory.make())
    }

    var body: some View {
        // View implementation
    }
}
```
