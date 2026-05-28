# Coordinator Pattern — Complete Implementations

> **Loading Trigger**: Load when implementing coordinator infrastructure or debugging coordinator lifecycle issues.

---

## Full App Coordinator Implementation

```swift
import SwiftUI

// MARK: - Coordinator Protocol

@MainActor
protocol Coordinator: AnyObject, ObservableObject {
    associatedtype Route: Hashable
    var path: NavigationPath { get set }
    var childCoordinators: [any Coordinator] { get set }

    func start() -> AnyView
    func navigate(to route: Route)
    func pop()
    func popToRoot()
}

extension Coordinator {
    func pop() {
        guard !path.isEmpty else { return }
        path.removeLast()
    }

    func popToRoot() {
        path = NavigationPath()
    }

    func addChild(_ coordinator: any Coordinator) {
        childCoordinators.append(coordinator)
    }

    func removeChild(_ coordinator: any Coordinator) {
        childCoordinators.removeAll { $0 === coordinator as AnyObject }
    }
}

// MARK: - App Coordinator

@MainActor
final class AppCoordinator: ObservableObject {
    @Published var isAuthenticated = false
    @Published var showOnboarding = false

    private(set) var authCoordinator: AuthCoordinator?
    private(set) var mainCoordinator: MainTabCoordinator?

    private let container: DependencyContainer

    init(container: DependencyContainer) {
        self.container = container
        checkAuthenticationState()
    }

    @ViewBuilder
    func start() -> some View {
        Group {
            if showOnboarding {
                OnboardingCoordinatorView(
                    coordinator: makeOnboardingCoordinator()
                )
            } else if isAuthenticated {
                MainTabCoordinatorView(
                    coordinator: makeMainCoordinator()
                )
            } else {
                AuthCoordinatorView(
                    coordinator: makeAuthCoordinator()
                )
            }
        }
    }

    // MARK: - Factory Methods

    private func makeAuthCoordinator() -> AuthCoordinator {
        let coordinator = AuthCoordinator(
            container: container,
            onAuthenticated: { [weak self] user in
                self?.handleAuthentication(user: user)
            }
        )
        authCoordinator = coordinator
        return coordinator
    }

    private func makeMainCoordinator() -> MainTabCoordinator {
        let coordinator = MainTabCoordinator(
            container: container,
            onLogout: { [weak self] in
                self?.handleLogout()
            }
        )
        mainCoordinator = coordinator
        return coordinator
    }

    private func makeOnboardingCoordinator() -> OnboardingCoordinator {
        OnboardingCoordinator(
            onComplete: { [weak self] in
                self?.showOnboarding = false
                UserDefaults.standard.set(true, forKey: "hasCompletedOnboarding")
            }
        )
    }

    // MARK: - State Management

    private func checkAuthenticationState() {
        showOnboarding = !UserDefaults.standard.bool(forKey: "hasCompletedOnboarding")
        isAuthenticated = container.authService.isAuthenticated
    }

    private func handleAuthentication(user: User) {
        authCoordinator = nil
        isAuthenticated = true
    }

    private func handleLogout() {
        mainCoordinator = nil
        isAuthenticated = false
    }
}

// MARK: - Auth Coordinator

@MainActor
final class AuthCoordinator: Coordinator, ObservableObject {
    enum Route: Hashable {
        case login
        case register
        case forgotPassword
        case twoFactor(email: String)
        case resetPassword(token: String)
    }

    @Published var path = NavigationPath()
    var childCoordinators: [any Coordinator] = []

    private let container: DependencyContainer
    private let onAuthenticated: (User) -> Void

    init(container: DependencyContainer, onAuthenticated: @escaping (User) -> Void) {
        self.container = container
        self.onAuthenticated = onAuthenticated
    }

    func start() -> AnyView {
        AnyView(
            NavigationStack(path: $path) {
                LoginView(viewModel: makeLoginViewModel())
                    .navigationDestination(for: Route.self) { route in
                        self.destination(for: route)
                    }
            }
        )
    }

    func navigate(to route: Route) {
        path.append(route)
    }

    @ViewBuilder
    private func destination(for route: Route) -> some View {
        switch route {
        case .login:
            LoginView(viewModel: makeLoginViewModel())
        case .register:
            RegisterView(viewModel: makeRegisterViewModel())
        case .forgotPassword:
            ForgotPasswordView(viewModel: makeForgotPasswordViewModel())
        case .twoFactor(let email):
            TwoFactorView(viewModel: makeTwoFactorViewModel(email: email))
        case .resetPassword(let token):
            ResetPasswordView(viewModel: makeResetPasswordViewModel(token: token))
        }
    }

    // MARK: - ViewModel Factories

    private func makeLoginViewModel() -> LoginViewModel {
        LoginViewModel(
            authService: container.authService,
            onSuccess: { [weak self] user in
                self?.onAuthenticated(user)
            },
            onNeedsTwoFactor: { [weak self] email in
                self?.navigate(to: .twoFactor(email: email))
            },
            onRegister: { [weak self] in
                self?.navigate(to: .register)
            },
            onForgotPassword: { [weak self] in
                self?.navigate(to: .forgotPassword)
            }
        )
    }

    private func makeRegisterViewModel() -> RegisterViewModel {
        RegisterViewModel(
            authService: container.authService,
            onSuccess: { [weak self] user in
                self?.onAuthenticated(user)
            },
            onBack: { [weak self] in
                self?.pop()
            }
        )
    }

    private func makeForgotPasswordViewModel() -> ForgotPasswordViewModel {
        ForgotPasswordViewModel(
            authService: container.authService,
            onBack: { [weak self] in
                self?.pop()
            }
        )
    }

    private func makeTwoFactorViewModel(email: String) -> TwoFactorViewModel {
        TwoFactorViewModel(
            email: email,
            authService: container.authService,
            onSuccess: { [weak self] user in
                self?.onAuthenticated(user)
            }
        )
    }

    private func makeResetPasswordViewModel(token: String) -> ResetPasswordViewModel {
        ResetPasswordViewModel(
            token: token,
            authService: container.authService,
            onSuccess: { [weak self] in
                self?.popToRoot()
            }
        )
    }
}

// MARK: - Main Tab Coordinator

@MainActor
final class MainTabCoordinator: ObservableObject {
    enum Tab: Hashable {
        case home
        case search
        case cart
        case profile
    }

    @Published var selectedTab: Tab = .home

    private(set) var homeCoordinator: HomeCoordinator
    private(set) var searchCoordinator: SearchCoordinator
    private(set) var cartCoordinator: CartCoordinator
    private(set) var profileCoordinator: ProfileCoordinator

    private let container: DependencyContainer
    private let onLogout: () -> Void

    init(container: DependencyContainer, onLogout: @escaping () -> Void) {
        self.container = container
        self.onLogout = onLogout

        self.homeCoordinator = HomeCoordinator(container: container)
        self.searchCoordinator = SearchCoordinator(container: container)
        self.cartCoordinator = CartCoordinator(container: container)
        self.profileCoordinator = ProfileCoordinator(
            container: container,
            onLogout: onLogout
        )
    }

    @ViewBuilder
    func start() -> some View {
        TabView(selection: $selectedTab) {
            homeCoordinator.start()
                .tabItem { Label("Home", systemImage: "house") }
                .tag(Tab.home)

            searchCoordinator.start()
                .tabItem { Label("Search", systemImage: "magnifyingglass") }
                .tag(Tab.search)

            cartCoordinator.start()
                .tabItem { Label("Cart", systemImage: "cart") }
                .tag(Tab.cart)

            profileCoordinator.start()
                .tabItem { Label("Profile", systemImage: "person") }
                .tag(Tab.profile)
        }
        .onChange(of: selectedTab) { oldValue, newValue in
            handleTabSelection(oldValue: oldValue, newValue: newValue)
        }
    }

    private func handleTabSelection(oldValue: Tab, newValue: Tab) {
        // Pop to root on re-selecting same tab
        if oldValue == newValue {
            switch newValue {
            case .home: homeCoordinator.popToRoot()
            case .search: searchCoordinator.popToRoot()
            case .cart: cartCoordinator.popToRoot()
            case .profile: profileCoordinator.popToRoot()
            }
        }
    }

    // MARK: - Cross-Tab Navigation

    func navigateToProduct(id: String) {
        selectedTab = .home
        homeCoordinator.navigate(to: .productDetail(id: id))
    }

    func navigateToCart() {
        selectedTab = .cart
    }

    func navigateToCheckout() {
        selectedTab = .cart
        cartCoordinator.navigate(to: .checkout)
    }
}

// MARK: - Home Coordinator

@MainActor
final class HomeCoordinator: Coordinator, ObservableObject {
    enum Route: Hashable {
        case productList(categoryId: String)
        case productDetail(id: String)
        case reviews(productId: String)
        case seller(id: String)
    }

    @Published var path = NavigationPath()
    var childCoordinators: [any Coordinator] = []

    private let container: DependencyContainer

    init(container: DependencyContainer) {
        self.container = container
    }

    func start() -> AnyView {
        AnyView(
            NavigationStack(path: $path) {
                HomeView(viewModel: makeHomeViewModel())
                    .navigationDestination(for: Route.self) { route in
                        self.destination(for: route)
                    }
            }
        )
    }

    func navigate(to route: Route) {
        path.append(route)
    }

    @ViewBuilder
    private func destination(for route: Route) -> some View {
        switch route {
        case .productList(let categoryId):
            ProductListView(
                viewModel: makeProductListViewModel(categoryId: categoryId)
            )
        case .productDetail(let id):
            ProductDetailView(
                viewModel: makeProductDetailViewModel(id: id)
            )
        case .reviews(let productId):
            ReviewsView(
                viewModel: makeReviewsViewModel(productId: productId)
            )
        case .seller(let id):
            SellerView(
                viewModel: makeSellerViewModel(id: id)
            )
        }
    }

    // MARK: - ViewModel Factories

    private func makeHomeViewModel() -> HomeViewModel {
        HomeViewModel(
            productService: container.productService,
            onCategorySelected: { [weak self] categoryId in
                self?.navigate(to: .productList(categoryId: categoryId))
            },
            onProductSelected: { [weak self] productId in
                self?.navigate(to: .productDetail(id: productId))
            }
        )
    }

    private func makeProductListViewModel(categoryId: String) -> ProductListViewModel {
        ProductListViewModel(
            categoryId: categoryId,
            productService: container.productService,
            onProductSelected: { [weak self] productId in
                self?.navigate(to: .productDetail(id: productId))
            }
        )
    }

    private func makeProductDetailViewModel(id: String) -> ProductDetailViewModel {
        ProductDetailViewModel(
            productId: id,
            productService: container.productService,
            cartService: container.cartService,
            onReviews: { [weak self] in
                self?.navigate(to: .reviews(productId: id))
            },
            onSeller: { [weak self] sellerId in
                self?.navigate(to: .seller(id: sellerId))
            }
        )
    }

    private func makeReviewsViewModel(productId: String) -> ReviewsViewModel {
        ReviewsViewModel(
            productId: productId,
            reviewService: container.reviewService
        )
    }

    private func makeSellerViewModel(id: String) -> SellerViewModel {
        SellerViewModel(
            sellerId: id,
            sellerService: container.sellerService,
            onProductSelected: { [weak self] productId in
                self?.navigate(to: .productDetail(id: productId))
            }
        )
    }
}
```

---

## Deep Link Handling Complete Implementation

```swift
import Foundation

// MARK: - Deep Link Types

enum DeepLink: Equatable {
    case product(id: String)
    case category(id: String)
    case user(id: String)
    case order(id: String)
    case checkout
    case settings(section: SettingsSection?)
    case resetPassword(token: String)
    case emailVerification(token: String)
    case promotion(code: String)

    enum SettingsSection: String {
        case account
        case notifications
        case privacy
        case payment
    }
}

// MARK: - Deep Link Parser

struct DeepLinkParser {

    /// Parse URL into DeepLink
    /// Supports both custom scheme (myapp://) and universal links (https://myapp.com/)
    static func parse(url: URL) -> DeepLink? {
        // Handle both custom scheme and universal links
        guard let scheme = url.scheme,
              ["myapp", "https", "http"].contains(scheme) else {
            return nil
        }

        // For universal links, verify host
        if scheme == "https" || scheme == "http" {
            guard let host = url.host,
                  ["myapp.com", "www.myapp.com"].contains(host) else {
                return nil
            }
        }

        let pathComponents = url.pathComponents.filter { $0 != "/" }
        let queryItems = URLComponents(url: url, resolvingAgainstBaseURL: false)?
            .queryItems?
            .reduce(into: [String: String]()) { $0[$1.name] = $1.value } ?? [:]

        return parsePathComponents(pathComponents, queryItems: queryItems)
    }

    private static func parsePathComponents(
        _ components: [String],
        queryItems: [String: String]
    ) -> DeepLink? {
        guard let first = components.first else { return nil }

        switch first {
        case "product", "products":
            guard components.count > 1 else { return nil }
            return .product(id: components[1])

        case "category", "categories":
            guard components.count > 1 else { return nil }
            return .category(id: components[1])

        case "user", "users", "profile":
            guard components.count > 1 else { return nil }
            return .user(id: components[1])

        case "order", "orders":
            guard components.count > 1 else { return nil }
            return .order(id: components[1])

        case "checkout":
            return .checkout

        case "settings":
            let section = components.count > 1
                ? DeepLink.SettingsSection(rawValue: components[1])
                : nil
            return .settings(section: section)

        case "reset-password":
            guard let token = queryItems["token"] else { return nil }
            return .resetPassword(token: token)

        case "verify-email":
            guard let token = queryItems["token"] else { return nil }
            return .emailVerification(token: token)

        case "promo", "promotion":
            guard let code = queryItems["code"] ?? (components.count > 1 ? components[1] : nil) else {
                return nil
            }
            return .promotion(code: code)

        default:
            return nil
        }
    }
}

// MARK: - Deep Link Handler

@MainActor
final class DeepLinkHandler: ObservableObject {
    @Published private(set) var pendingDeepLink: DeepLink?

    private weak var appCoordinator: AppCoordinator?

    init(appCoordinator: AppCoordinator? = nil) {
        self.appCoordinator = appCoordinator
    }

    func setAppCoordinator(_ coordinator: AppCoordinator) {
        self.appCoordinator = coordinator
        processPendingDeepLink()
    }

    func handle(url: URL) {
        guard let deepLink = DeepLinkParser.parse(url: url) else {
            print("Failed to parse deep link: \(url)")
            return
        }
        handle(deepLink: deepLink)
    }

    func handle(deepLink: DeepLink) {
        // If app coordinator isn't ready, queue the deep link
        guard let appCoordinator = appCoordinator,
              appCoordinator.isAuthenticated || isPublicDeepLink(deepLink) else {
            pendingDeepLink = deepLink
            return
        }

        route(deepLink: deepLink)
    }

    private func processPendingDeepLink() {
        guard let deepLink = pendingDeepLink else { return }
        pendingDeepLink = nil
        handle(deepLink: deepLink)
    }

    private func isPublicDeepLink(_ deepLink: DeepLink) -> Bool {
        switch deepLink {
        case .resetPassword, .emailVerification, .product, .category:
            return true
        default:
            return false
        }
    }

    private func route(deepLink: DeepLink) {
        guard let mainCoordinator = appCoordinator?.mainCoordinator else {
            // Handle auth-flow deep links
            routeAuthDeepLink(deepLink)
            return
        }

        switch deepLink {
        case .product(let id):
            mainCoordinator.navigateToProduct(id: id)

        case .category(let id):
            mainCoordinator.selectedTab = .home
            mainCoordinator.homeCoordinator.popToRoot()
            mainCoordinator.homeCoordinator.navigate(to: .productList(categoryId: id))

        case .user(let id):
            mainCoordinator.selectedTab = .profile
            // Navigate to user profile

        case .order(let id):
            mainCoordinator.selectedTab = .profile
            mainCoordinator.profileCoordinator.navigate(to: .orderDetail(id: id))

        case .checkout:
            mainCoordinator.navigateToCheckout()

        case .settings(let section):
            mainCoordinator.selectedTab = .profile
            mainCoordinator.profileCoordinator.navigate(to: .settings)
            if let section = section {
                mainCoordinator.profileCoordinator.navigate(
                    to: .settingsSection(section)
                )
            }

        case .promotion(let code):
            mainCoordinator.selectedTab = .cart
            mainCoordinator.cartCoordinator.applyPromoCode(code)

        case .resetPassword, .emailVerification:
            routeAuthDeepLink(deepLink)
        }
    }

    private func routeAuthDeepLink(_ deepLink: DeepLink) {
        guard let authCoordinator = appCoordinator?.authCoordinator else { return }

        switch deepLink {
        case .resetPassword(let token):
            authCoordinator.navigate(to: .resetPassword(token: token))
        case .emailVerification(let token):
            authCoordinator.handleEmailVerification(token: token)
        default:
            break
        }
    }
}

// MARK: - App Integration

@main
struct MyApp: App {
    @StateObject private var appCoordinator: AppCoordinator
    @StateObject private var deepLinkHandler: DeepLinkHandler

    init() {
        let container = DependencyContainer()
        let coordinator = AppCoordinator(container: container)
        let handler = DeepLinkHandler()

        _appCoordinator = StateObject(wrappedValue: coordinator)
        _deepLinkHandler = StateObject(wrappedValue: handler)
    }

    var body: some Scene {
        WindowGroup {
            appCoordinator.start()
                .environmentObject(appCoordinator)
                .environmentObject(deepLinkHandler)
                .onAppear {
                    deepLinkHandler.setAppCoordinator(appCoordinator)
                }
                .onOpenURL { url in
                    deepLinkHandler.handle(url: url)
                }
        }
    }
}
```

---

## UIKit Coordinator (Legacy/Hybrid Apps)

```swift
import UIKit

// MARK: - UIKit Coordinator Protocol

protocol UIKitCoordinator: AnyObject {
    var navigationController: UINavigationController { get }
    var childCoordinators: [UIKitCoordinator] { get set }
    var parentCoordinator: UIKitCoordinator? { get set }

    func start()
    func finish()
}

extension UIKitCoordinator {
    func addChild(_ coordinator: UIKitCoordinator) {
        coordinator.parentCoordinator = self
        childCoordinators.append(coordinator)
    }

    func removeChild(_ coordinator: UIKitCoordinator) {
        childCoordinators.removeAll { $0 === coordinator }
    }

    func finish() {
        parentCoordinator?.removeChild(self)
    }
}

// MARK: - Main UIKit Coordinator

final class MainUIKitCoordinator: UIKitCoordinator {
    let navigationController: UINavigationController
    var childCoordinators: [UIKitCoordinator] = []
    weak var parentCoordinator: UIKitCoordinator?

    private let container: DependencyContainer

    init(navigationController: UINavigationController, container: DependencyContainer) {
        self.navigationController = navigationController
        self.container = container
    }

    func start() {
        let homeVC = HomeViewController()
        homeVC.delegate = self
        navigationController.pushViewController(homeVC, animated: false)
    }

    private func startProductFlow(productId: String) {
        let productCoordinator = ProductCoordinator(
            navigationController: navigationController,
            container: container,
            productId: productId
        )
        productCoordinator.delegate = self
        addChild(productCoordinator)
        productCoordinator.start()
    }
}

extension MainUIKitCoordinator: HomeViewControllerDelegate {
    func homeViewController(_ vc: HomeViewController, didSelectProduct productId: String) {
        startProductFlow(productId: productId)
    }
}

extension MainUIKitCoordinator: ProductCoordinatorDelegate {
    func productCoordinatorDidFinish(_ coordinator: ProductCoordinator) {
        removeChild(coordinator)
    }

    func productCoordinator(
        _ coordinator: ProductCoordinator,
        didAddToCart productId: String
    ) {
        // Handle cart addition
        removeChild(coordinator)
        navigationController.popToRootViewController(animated: true)
    }
}

// MARK: - Product Coordinator

protocol ProductCoordinatorDelegate: AnyObject {
    func productCoordinatorDidFinish(_ coordinator: ProductCoordinator)
    func productCoordinator(_ coordinator: ProductCoordinator, didAddToCart productId: String)
}

final class ProductCoordinator: UIKitCoordinator {
    let navigationController: UINavigationController
    var childCoordinators: [UIKitCoordinator] = []
    weak var parentCoordinator: UIKitCoordinator?
    weak var delegate: ProductCoordinatorDelegate?

    private let container: DependencyContainer
    private let productId: String

    init(
        navigationController: UINavigationController,
        container: DependencyContainer,
        productId: String
    ) {
        self.navigationController = navigationController
        self.container = container
        self.productId = productId
    }

    func start() {
        let productDetailVC = ProductDetailViewController(productId: productId)
        productDetailVC.delegate = self
        navigationController.pushViewController(productDetailVC, animated: true)
    }
}

extension ProductCoordinator: ProductDetailViewControllerDelegate {
    func productDetailViewControllerDidTapBack(_ vc: ProductDetailViewController) {
        navigationController.popViewController(animated: true)
        delegate?.productCoordinatorDidFinish(self)
    }

    func productDetailViewController(
        _ vc: ProductDetailViewController,
        didAddToCart productId: String
    ) {
        delegate?.productCoordinator(self, didAddToCart: productId)
    }

    func productDetailViewController(
        _ vc: ProductDetailViewController,
        didTapReviews productId: String
    ) {
        let reviewsVC = ReviewsViewController(productId: productId)
        navigationController.pushViewController(reviewsVC, animated: true)
    }
}
```
