# MVVM Architecture — Complete ViewModel Patterns

> **Loading Trigger**: Load when building ViewModels for complex screens or implementing advanced state management patterns.

---

## Complete Feature ViewModel Template

```swift
import Foundation
import Combine

// MARK: - Feature ViewModel with All Patterns

@MainActor
final class ProductDetailViewModel: ObservableObject {
    // MARK: - State

    enum State: Equatable {
        case idle
        case loading
        case loaded(Product)
        case error(ErrorInfo)

        struct ErrorInfo: Equatable {
            let message: String
            let isRetryable: Bool
        }

        var product: Product? {
            guard case .loaded(let product) = self else { return nil }
            return product
        }

        var isLoading: Bool {
            guard case .loading = self else { return false }
            return true
        }
    }

    @Published private(set) var state: State = .idle
    @Published private(set) var isFavorite = false
    @Published private(set) var isAddingToCart = false
    @Published var showAddToCartSuccess = false
    @Published var quantity = 1

    // MARK: - Dependencies

    private let productId: String
    private let productService: ProductServiceProtocol
    private let cartService: CartServiceProtocol
    private let favoritesService: FavoritesServiceProtocol
    private let analyticsService: AnalyticsServiceProtocol

    // MARK: - Task Management

    private var loadTask: Task<Void, Never>?
    private var cancellables = Set<AnyCancellable>()

    // MARK: - Callbacks

    private let onAddToCart: () -> Void
    private let onError: (Error) -> Void

    // MARK: - Initialization

    init(
        productId: String,
        productService: ProductServiceProtocol = ProductService(),
        cartService: CartServiceProtocol = CartService(),
        favoritesService: FavoritesServiceProtocol = FavoritesService(),
        analyticsService: AnalyticsServiceProtocol = AnalyticsService(),
        onAddToCart: @escaping () -> Void = {},
        onError: @escaping (Error) -> Void = { _ in }
    ) {
        self.productId = productId
        self.productService = productService
        self.cartService = cartService
        self.favoritesService = favoritesService
        self.analyticsService = analyticsService
        self.onAddToCart = onAddToCart
        self.onError = onError

        setupBindings()
    }

    // MARK: - Setup

    private func setupBindings() {
        // React to quantity changes
        $quantity
            .dropFirst()
            .sink { [weak self] quantity in
                self?.analyticsService.track(.quantityChanged(quantity: quantity))
            }
            .store(in: &cancellables)
    }

    // MARK: - Actions

    func loadProduct() async {
        loadTask?.cancel()

        loadTask = Task {
            state = .loading

            do {
                async let product = productService.fetchProduct(id: productId)
                async let isFav = favoritesService.isFavorite(productId: productId)

                let (loadedProduct, favorite) = try await (product, isFav)

                try Task.checkCancellation()

                state = .loaded(loadedProduct)
                isFavorite = favorite

                analyticsService.track(.productViewed(productId: productId))

            } catch is CancellationError {
                // Ignore cancellation
            } catch {
                state = .error(State.ErrorInfo(
                    message: error.localizedDescription,
                    isRetryable: (error as? NetworkError)?.isRetryable ?? true
                ))
                onError(error)
            }
        }
    }

    func toggleFavorite() async {
        guard case .loaded(let product) = state else { return }

        let newFavorite = !isFavorite
        isFavorite = newFavorite // Optimistic update

        do {
            if newFavorite {
                try await favoritesService.add(productId: product.id)
                analyticsService.track(.favoriteAdded(productId: product.id))
            } else {
                try await favoritesService.remove(productId: product.id)
                analyticsService.track(.favoriteRemoved(productId: product.id))
            }
        } catch {
            isFavorite = !newFavorite // Revert on failure
            onError(error)
        }
    }

    func addToCart() async {
        guard case .loaded(let product) = state else { return }

        isAddingToCart = true

        do {
            try await cartService.add(productId: product.id, quantity: quantity)

            analyticsService.track(.addedToCart(
                productId: product.id,
                quantity: quantity,
                price: product.price
            ))

            showAddToCartSuccess = true
            onAddToCart()

            // Auto-hide success after delay
            try? await Task.sleep(for: .seconds(2))
            showAddToCartSuccess = false

        } catch {
            onError(error)
        }

        isAddingToCart = false
    }

    func incrementQuantity() {
        guard let product = state.product, quantity < product.maxQuantity else { return }
        quantity += 1
    }

    func decrementQuantity() {
        guard quantity > 1 else { return }
        quantity -= 1
    }

    // MARK: - Cleanup

    func cancel() {
        loadTask?.cancel()
    }

    deinit {
        loadTask?.cancel()
    }
}

// MARK: - Computed Properties for View

extension ProductDetailViewModel {
    var formattedPrice: String {
        guard let product = state.product else { return "--" }
        return product.price.formatted(.currency(code: "USD"))
    }

    var totalPrice: Decimal {
        guard let product = state.product else { return 0 }
        return product.price * Decimal(quantity)
    }

    var formattedTotalPrice: String {
        totalPrice.formatted(.currency(code: "USD"))
    }

    var canAddToCart: Bool {
        guard case .loaded(let product) = state else { return false }
        return product.inStock && !isAddingToCart
    }

    var addToCartButtonTitle: String {
        if isAddingToCart { return "Adding..." }
        if let product = state.product, !product.inStock { return "Out of Stock" }
        return "Add to Cart"
    }
}
```

---

## Combine-Based Form ViewModel

```swift
import Combine

@MainActor
final class RegistrationViewModel: ObservableObject {
    // MARK: - Inputs

    @Published var email = ""
    @Published var password = ""
    @Published var confirmPassword = ""
    @Published var acceptedTerms = false

    // MARK: - Outputs

    @Published private(set) var emailError: String?
    @Published private(set) var passwordError: String?
    @Published private(set) var confirmPasswordError: String?
    @Published private(set) var isFormValid = false
    @Published private(set) var isSubmitting = false
    @Published var registrationError: Error?

    // MARK: - Private

    private var cancellables = Set<AnyCancellable>()
    private let authService: AuthServiceProtocol

    // MARK: - Init

    init(authService: AuthServiceProtocol = AuthService()) {
        self.authService = authService
        setupValidation()
    }

    // MARK: - Validation Chains

    private func setupValidation() {
        // Email validation
        $email
            .dropFirst()
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .map { email -> String? in
                if email.isEmpty { return nil }
                if !email.contains("@") { return "Please enter a valid email" }
                return nil
            }
            .assign(to: &$emailError)

        // Password validation
        $password
            .dropFirst()
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .map { password -> String? in
                if password.isEmpty { return nil }
                if password.count < 8 { return "Password must be at least 8 characters" }
                if !password.contains(where: { $0.isNumber }) {
                    return "Password must contain a number"
                }
                return nil
            }
            .assign(to: &$passwordError)

        // Confirm password validation
        Publishers.CombineLatest($password, $confirmPassword)
            .dropFirst()
            .debounce(for: .milliseconds(300), scheduler: DispatchQueue.main)
            .map { password, confirm -> String? in
                if confirm.isEmpty { return nil }
                if password != confirm { return "Passwords don't match" }
                return nil
            }
            .assign(to: &$confirmPasswordError)

        // Form validity
        Publishers.CombineLatest4($email, $password, $confirmPassword, $acceptedTerms)
            .combineLatest($emailError, $passwordError, $confirmPasswordError)
            .map { inputs, errors in
                let (email, password, confirm, accepted) = inputs
                let (emailErr, passErr, confirmErr) = errors

                return !email.isEmpty &&
                       !password.isEmpty &&
                       !confirm.isEmpty &&
                       accepted &&
                       emailErr == nil &&
                       passErr == nil &&
                       confirmErr == nil
            }
            .assign(to: &$isFormValid)
    }

    // MARK: - Actions

    func register() async {
        guard isFormValid else { return }

        isSubmitting = true

        do {
            try await authService.register(email: email, password: password)
        } catch {
            registrationError = error
        }

        isSubmitting = false
    }
}
```

---

## Multi-Section List ViewModel

```swift
@MainActor
final class DashboardViewModel: ObservableObject {
    // MARK: - Section States (Load Independently)

    struct SectionState<T: Equatable>: Equatable {
        var data: T?
        var isLoading = false
        var error: String?

        static func == (lhs: SectionState, rhs: SectionState) -> Bool {
            lhs.isLoading == rhs.isLoading && lhs.error == rhs.error
        }
    }

    @Published private(set) var featuredSection = SectionState<[Product]>()
    @Published private(set) var categoriesSection = SectionState<[Category]>()
    @Published private(set) var recentOrdersSection = SectionState<[Order]>()
    @Published private(set) var recommendedSection = SectionState<[Product]>()

    // MARK: - Dependencies

    private let productService: ProductServiceProtocol
    private let categoryService: CategoryServiceProtocol
    private let orderService: OrderServiceProtocol

    init(
        productService: ProductServiceProtocol = ProductService(),
        categoryService: CategoryServiceProtocol = CategoryService(),
        orderService: OrderServiceProtocol = OrderService()
    ) {
        self.productService = productService
        self.categoryService = categoryService
        self.orderService = orderService
    }

    // MARK: - Load All Sections in Parallel

    func loadAllSections() async {
        await withTaskGroup(of: Void.self) { group in
            group.addTask { await self.loadFeatured() }
            group.addTask { await self.loadCategories() }
            group.addTask { await self.loadRecentOrders() }
            group.addTask { await self.loadRecommended() }
        }
    }

    // MARK: - Individual Section Loaders

    func loadFeatured() async {
        featuredSection.isLoading = true
        featuredSection.error = nil

        do {
            let products = try await productService.fetchFeatured()
            featuredSection.data = products
        } catch {
            featuredSection.error = "Couldn't load featured products"
        }

        featuredSection.isLoading = false
    }

    func loadCategories() async {
        categoriesSection.isLoading = true
        categoriesSection.error = nil

        do {
            let categories = try await categoryService.fetchAll()
            categoriesSection.data = categories
        } catch {
            categoriesSection.error = "Couldn't load categories"
        }

        categoriesSection.isLoading = false
    }

    func loadRecentOrders() async {
        recentOrdersSection.isLoading = true
        recentOrdersSection.error = nil

        do {
            let orders = try await orderService.fetchRecent(limit: 3)
            recentOrdersSection.data = orders
        } catch {
            recentOrdersSection.error = "Couldn't load recent orders"
        }

        recentOrdersSection.isLoading = false
    }

    func loadRecommended() async {
        recommendedSection.isLoading = true
        recommendedSection.error = nil

        do {
            let products = try await productService.fetchRecommended()
            recommendedSection.data = products
        } catch {
            recommendedSection.error = "Couldn't load recommendations"
        }

        recommendedSection.isLoading = false
    }
}
```

---

## Testable ViewModel Pattern

```swift
// MARK: - Protocol for Testing

protocol ProductDetailViewModelProtocol: ObservableObject {
    var state: ProductDetailViewModel.State { get }
    var isFavorite: Bool { get }
    var quantity: Int { get set }

    func loadProduct() async
    func toggleFavorite() async
    func addToCart() async
}

// MARK: - Mock ViewModel for Previews

final class MockProductDetailViewModel: ProductDetailViewModelProtocol, ObservableObject {
    @Published var state: ProductDetailViewModel.State
    @Published var isFavorite: Bool
    @Published var quantity: Int

    init(
        state: ProductDetailViewModel.State = .idle,
        isFavorite: Bool = false,
        quantity: Int = 1
    ) {
        self.state = state
        self.isFavorite = isFavorite
        self.quantity = quantity
    }

    func loadProduct() async {
        // No-op for preview
    }

    func toggleFavorite() async {
        isFavorite.toggle()
    }

    func addToCart() async {
        // No-op for preview
    }
}

// MARK: - Preview with Mock

struct ProductDetailView_Previews: PreviewProvider {
    static var previews: some View {
        Group {
            // Loading state
            ProductDetailView(viewModel: MockProductDetailViewModel(state: .loading))

            // Loaded state
            ProductDetailView(viewModel: MockProductDetailViewModel(
                state: .loaded(Product.preview),
                isFavorite: true
            ))

            // Error state
            ProductDetailView(viewModel: MockProductDetailViewModel(
                state: .error(.init(message: "Network error", isRetryable: true))
            ))
        }
    }
}
```
