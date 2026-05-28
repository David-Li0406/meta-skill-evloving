# Navigation Patterns — Complete Router Implementation

> **Loading Trigger**: Load when implementing router infrastructure from scratch or debugging navigation state issues.

---

## Full Router Implementation with All Features

```swift
import SwiftUI
import Combine

// MARK: - Router Protocol

@MainActor
protocol RouterProtocol: ObservableObject {
    associatedtype Route: Hashable & Codable

    var path: [Route] { get set }

    func navigate(to route: Route)
    func pop()
    func popToRoot()
    func replaceStack(with routes: [Route])
    func destination(for route: Route) -> AnyView
}

// MARK: - Type-Safe Router Implementation

@MainActor
final class Router<Route: Hashable & Codable>: ObservableObject {
    @Published var path: [Route] = []
    @Published var presentedSheet: Route?
    @Published var presentedFullScreenCover: Route?
    @Published var presentedAlert: AlertState?

    // State persistence key
    private let persistenceKey: String?
    private var cancellables = Set<AnyCancellable>()

    struct AlertState: Identifiable {
        let id = UUID()
        let title: String
        let message: String?
        let primaryButton: AlertButton
        let secondaryButton: AlertButton?

        struct AlertButton {
            let title: String
            let role: ButtonRole?
            let action: () -> Void
        }
    }

    init(persistenceKey: String? = nil) {
        self.persistenceKey = persistenceKey

        if let key = persistenceKey {
            restoreState(from: key)
            setupStatePersistence(key: key)
        }
    }

    // MARK: - Navigation

    func navigate(to route: Route) {
        path.append(route)
    }

    func pop() {
        guard !path.isEmpty else { return }
        path.removeLast()
    }

    func pop(count: Int) {
        let removeCount = min(count, path.count)
        path.removeLast(removeCount)
    }

    func popToRoot() {
        path.removeAll()
    }

    func replaceStack(with routes: [Route]) {
        path = routes
    }

    func replaceLast(with route: Route) {
        guard !path.isEmpty else {
            navigate(to: route)
            return
        }
        path[path.count - 1] = route
    }

    // MARK: - Modal Presentation

    func presentSheet(_ route: Route) {
        presentedSheet = route
    }

    func dismissSheet() {
        presentedSheet = nil
    }

    func presentFullScreenCover(_ route: Route) {
        presentedFullScreenCover = route
    }

    func dismissFullScreenCover() {
        presentedFullScreenCover = nil
    }

    // MARK: - Alerts

    func showAlert(
        title: String,
        message: String? = nil,
        primaryButton: AlertState.AlertButton,
        secondaryButton: AlertState.AlertButton? = nil
    ) {
        presentedAlert = AlertState(
            title: title,
            message: message,
            primaryButton: primaryButton,
            secondaryButton: secondaryButton
        )
    }

    func dismissAlert() {
        presentedAlert = nil
    }

    // MARK: - State Persistence

    private func setupStatePersistence(key: String) {
        $path
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .sink { [weak self] routes in
                self?.saveState(routes, to: key)
            }
            .store(in: &cancellables)
    }

    private func saveState(_ routes: [Route], to key: String) {
        guard let data = try? JSONEncoder().encode(routes) else { return }
        UserDefaults.standard.set(data, forKey: key)
    }

    private func restoreState(from key: String) {
        guard let data = UserDefaults.standard.data(forKey: key),
              let routes = try? JSONDecoder().decode([Route].self, from: data) else {
            return
        }
        path = routes
    }

    func clearPersistedState() {
        guard let key = persistenceKey else { return }
        UserDefaults.standard.removeObject(forKey: key)
    }
}

// MARK: - Convenience Extensions

extension Router {
    var currentRoute: Route? {
        path.last
    }

    var isAtRoot: Bool {
        path.isEmpty
    }

    var depth: Int {
        path.count
    }

    func contains(_ route: Route) -> Bool {
        path.contains(route)
    }

    func popTo(_ route: Route) {
        guard let index = path.firstIndex(of: route) else { return }
        path = Array(path.prefix(through: index))
    }
}
```

---

## Complete App Example with Router

```swift
// MARK: - Route Definition

enum AppRoute: Hashable, Codable {
    // Home
    case home
    case productList(categoryId: String)
    case productDetail(productId: String)
    case productReviews(productId: String)
    case writeReview(productId: String)

    // Search
    case search
    case searchResults(query: String)
    case searchFilters

    // Cart
    case cart
    case checkout
    case paymentMethods
    case addPaymentMethod
    case orderConfirmation(orderId: String)

    // Profile
    case profile
    case editProfile
    case orders
    case orderDetail(orderId: String)
    case settings
    case settingsNotifications
    case settingsPrivacy
    case settingsPayment
}

// MARK: - App Router

@MainActor
final class AppRouter: ObservableObject {
    @Published var homeRouter = Router<AppRoute>(persistenceKey: "home_nav_state")
    @Published var searchRouter = Router<AppRoute>(persistenceKey: "search_nav_state")
    @Published var cartRouter = Router<AppRoute>(persistenceKey: "cart_nav_state")
    @Published var profileRouter = Router<AppRoute>(persistenceKey: "profile_nav_state")

    @Published var selectedTab: Tab = .home

    enum Tab: Hashable {
        case home, search, cart, profile
    }

    private let container: DependencyContainer

    init(container: DependencyContainer) {
        self.container = container
    }

    // MARK: - Cross-Tab Navigation

    func navigateToProduct(_ productId: String) {
        selectedTab = .home
        homeRouter.popToRoot()
        homeRouter.navigate(to: .productDetail(productId: productId))
    }

    func navigateToCheckout() {
        selectedTab = .cart
        cartRouter.navigate(to: .checkout)
    }

    func navigateToOrder(_ orderId: String) {
        selectedTab = .profile
        profileRouter.popToRoot()
        profileRouter.navigate(to: .orders)
        profileRouter.navigate(to: .orderDetail(orderId: orderId))
    }

    // MARK: - Pop to Root on Tab Re-selection

    func handleTabSelection(_ tab: Tab) {
        if selectedTab == tab {
            // Re-selected same tab - pop to root
            switch tab {
            case .home: homeRouter.popToRoot()
            case .search: searchRouter.popToRoot()
            case .cart: cartRouter.popToRoot()
            case .profile: profileRouter.popToRoot()
            }
        }
        selectedTab = tab
    }

    // MARK: - Destination Factory

    @ViewBuilder
    func destination(for route: AppRoute) -> some View {
        switch route {
        // Home
        case .home:
            HomeView()
        case .productList(let categoryId):
            ProductListView(categoryId: categoryId)
        case .productDetail(let productId):
            ProductDetailView(productId: productId)
        case .productReviews(let productId):
            ReviewsView(productId: productId)
        case .writeReview(let productId):
            WriteReviewView(productId: productId)

        // Search
        case .search:
            SearchView()
        case .searchResults(let query):
            SearchResultsView(query: query)
        case .searchFilters:
            SearchFiltersView()

        // Cart
        case .cart:
            CartView()
        case .checkout:
            CheckoutView()
        case .paymentMethods:
            PaymentMethodsView()
        case .addPaymentMethod:
            AddPaymentMethodView()
        case .orderConfirmation(let orderId):
            OrderConfirmationView(orderId: orderId)

        // Profile
        case .profile:
            ProfileView()
        case .editProfile:
            EditProfileView()
        case .orders:
            OrdersView()
        case .orderDetail(let orderId):
            OrderDetailView(orderId: orderId)
        case .settings:
            SettingsView()
        case .settingsNotifications:
            NotificationSettingsView()
        case .settingsPrivacy:
            PrivacySettingsView()
        case .settingsPayment:
            PaymentSettingsView()
        }
    }
}

// MARK: - Main App View

struct MainAppView: View {
    @StateObject private var appRouter: AppRouter

    init(container: DependencyContainer) {
        _appRouter = StateObject(wrappedValue: AppRouter(container: container))
    }

    var body: some View {
        TabView(selection: tabSelection) {
            homeTab
            searchTab
            cartTab
            profileTab
        }
        .environmentObject(appRouter)
    }

    private var tabSelection: Binding<AppRouter.Tab> {
        Binding(
            get: { appRouter.selectedTab },
            set: { appRouter.handleTabSelection($0) }
        )
    }

    private var homeTab: some View {
        NavigationStack(path: $appRouter.homeRouter.path) {
            HomeView()
                .navigationDestination(for: AppRoute.self) { route in
                    appRouter.destination(for: route)
                }
        }
        .tabItem { Label("Home", systemImage: "house") }
        .tag(AppRouter.Tab.home)
        .environmentObject(appRouter.homeRouter)
    }

    private var searchTab: some View {
        NavigationStack(path: $appRouter.searchRouter.path) {
            SearchView()
                .navigationDestination(for: AppRoute.self) { route in
                    appRouter.destination(for: route)
                }
        }
        .tabItem { Label("Search", systemImage: "magnifyingglass") }
        .tag(AppRouter.Tab.search)
        .environmentObject(appRouter.searchRouter)
    }

    private var cartTab: some View {
        NavigationStack(path: $appRouter.cartRouter.path) {
            CartView()
                .navigationDestination(for: AppRoute.self) { route in
                    appRouter.destination(for: route)
                }
        }
        .tabItem { Label("Cart", systemImage: "cart") }
        .tag(AppRouter.Tab.cart)
        .environmentObject(appRouter.cartRouter)
    }

    private var profileTab: some View {
        NavigationStack(path: $appRouter.profileRouter.path) {
            ProfileView()
                .navigationDestination(for: AppRoute.self) { route in
                    appRouter.destination(for: route)
                }
        }
        .tabItem { Label("Profile", systemImage: "person") }
        .tag(AppRouter.Tab.profile)
        .environmentObject(appRouter.profileRouter)
    }
}
```

---

## Deep Link Router Integration

```swift
// MARK: - Deep Link Handler

@MainActor
final class DeepLinkRouter {
    private weak var appRouter: AppRouter?

    init(appRouter: AppRouter) {
        self.appRouter = appRouter
    }

    func handle(url: URL) -> Bool {
        guard let deepLink = parse(url: url) else { return false }
        route(deepLink: deepLink)
        return true
    }

    private func parse(url: URL) -> DeepLink? {
        // Parse URL into DeepLink enum
        // See complete implementation in coordinator-pattern references
        DeepLinkParser.parse(url: url)
    }

    private func route(deepLink: DeepLink) {
        guard let router = appRouter else { return }

        switch deepLink {
        case .product(let id):
            router.navigateToProduct(id)

        case .category(let id):
            router.selectedTab = .home
            router.homeRouter.popToRoot()
            router.homeRouter.navigate(to: .productList(categoryId: id))

        case .order(let id):
            router.navigateToOrder(id)

        case .checkout:
            router.navigateToCheckout()

        case .settings(let section):
            router.selectedTab = .profile
            router.profileRouter.popToRoot()
            router.profileRouter.navigate(to: .settings)
            if let section = section {
                router.profileRouter.navigate(to: mapSettingsSection(section))
            }

        case .search(let query):
            router.selectedTab = .search
            router.searchRouter.popToRoot()
            if let query = query {
                router.searchRouter.navigate(to: .searchResults(query: query))
            }

        default:
            break
        }
    }

    private func mapSettingsSection(_ section: DeepLink.SettingsSection) -> AppRoute {
        switch section {
        case .notifications: return .settingsNotifications
        case .privacy: return .settingsPrivacy
        case .payment: return .settingsPayment
        case .account: return .editProfile
        }
    }
}

// MARK: - App Integration

@main
struct MyApp: App {
    @StateObject private var appRouter: AppRouter
    private let deepLinkRouter: DeepLinkRouter

    init() {
        let container = DependencyContainer()
        let router = AppRouter(container: container)
        _appRouter = StateObject(wrappedValue: router)
        deepLinkRouter = DeepLinkRouter(appRouter: router)
    }

    var body: some Scene {
        WindowGroup {
            MainAppView(container: DependencyContainer())
                .onOpenURL { url in
                    _ = deepLinkRouter.handle(url: url)
                }
        }
    }
}
```

---

## Navigation State Persistence (Advanced)

```swift
// MARK: - Codable Navigation State

struct NavigationState<Route: Codable>: Codable {
    let path: [Route]
    let timestamp: Date
    let appVersion: String

    var isValid: Bool {
        // Invalidate state older than 24 hours
        Date().timeIntervalSince(timestamp) < 86400
    }
}

// MARK: - Persistent Router

@MainActor
final class PersistentRouter<Route: Hashable & Codable>: ObservableObject {
    @Published var path: [Route] = []

    private let storage: NavigationStorage
    private let storageKey: String
    private var cancellables = Set<AnyCancellable>()

    init(storageKey: String, storage: NavigationStorage = .userDefaults) {
        self.storageKey = storageKey
        self.storage = storage

        restoreState()
        observeStateChanges()
    }

    private func restoreState() {
        guard let state: NavigationState<Route> = storage.load(key: storageKey),
              state.isValid else {
            return
        }
        path = state.path
    }

    private func observeStateChanges() {
        $path
            .debounce(for: .milliseconds(500), scheduler: DispatchQueue.main)
            .sink { [weak self] routes in
                self?.saveState(routes)
            }
            .store(in: &cancellables)
    }

    private func saveState(_ routes: [Route]) {
        let state = NavigationState(
            path: routes,
            timestamp: Date(),
            appVersion: Bundle.main.appVersion
        )
        storage.save(state, key: storageKey)
    }
}

// MARK: - Navigation Storage

enum NavigationStorage {
    case userDefaults
    case fileSystem(directory: URL)
    case keychain

    func save<T: Encodable>(_ value: T, key: String) {
        guard let data = try? JSONEncoder().encode(value) else { return }

        switch self {
        case .userDefaults:
            UserDefaults.standard.set(data, forKey: key)
        case .fileSystem(let directory):
            let url = directory.appendingPathComponent(key)
            try? data.write(to: url)
        case .keychain:
            // Keychain implementation
            break
        }
    }

    func load<T: Decodable>(key: String) -> T? {
        let data: Data?

        switch self {
        case .userDefaults:
            data = UserDefaults.standard.data(forKey: key)
        case .fileSystem(let directory):
            let url = directory.appendingPathComponent(key)
            data = try? Data(contentsOf: url)
        case .keychain:
            data = nil // Keychain implementation
        }

        guard let data = data else { return nil }
        return try? JSONDecoder().decode(T.self, from: data)
    }

    func remove(key: String) {
        switch self {
        case .userDefaults:
            UserDefaults.standard.removeObject(forKey: key)
        case .fileSystem(let directory):
            let url = directory.appendingPathComponent(key)
            try? FileManager.default.removeItem(at: url)
        case .keychain:
            // Keychain implementation
            break
        }
    }
}

extension Bundle {
    var appVersion: String {
        infoDictionary?["CFBundleShortVersionString"] as? String ?? "1.0"
    }
}
```
