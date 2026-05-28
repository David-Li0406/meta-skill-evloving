# Clean Architecture iOS — Complete Layer Implementations

> **Loading Trigger**: Load when implementing Clean Architecture layers from scratch or refactoring to Clean Architecture.

---

## Domain Layer (No Framework Dependencies)

```swift
// MARK: - Domain/Entities/User.swift

import Foundation

struct User: Identifiable, Equatable {
    let id: String
    let email: String
    let name: String
    let avatarURL: URL?
    let createdAt: Date
    let role: Role

    enum Role: String {
        case user
        case admin
        case moderator
    }
}

// MARK: - Domain/Entities/Order.swift

struct Order: Identifiable, Equatable {
    let id: String
    let userId: String
    let items: [OrderItem]
    let status: Status
    let createdAt: Date
    let shippingAddress: Address

    enum Status: String {
        case pending
        case processing
        case shipped
        case delivered
        case cancelled
    }

    var total: Decimal {
        items.reduce(0) { $0 + $1.subtotal }
    }
}

struct OrderItem: Equatable {
    let productId: String
    let productName: String
    let quantity: Int
    let unitPrice: Decimal

    var subtotal: Decimal {
        unitPrice * Decimal(quantity)
    }
}

struct Address: Equatable {
    let street: String
    let city: String
    let state: String
    let zipCode: String
    let country: String
}

// MARK: - Domain/Errors/DomainError.swift

enum DomainError: Error, Equatable {
    case validation(String)
    case businessRule(String)
    case notFound(String)
    case unauthorized
    case unknown
}

// MARK: - Domain/Repositories/UserRepositoryProtocol.swift

protocol UserRepositoryProtocol {
    func getUser(id: String) async throws -> User
    func getCurrentUser() async throws -> User
    func updateUser(_ user: User) async throws -> User
}

protocol OrderRepositoryProtocol {
    func getOrders(userId: String) async throws -> [Order]
    func getOrder(id: String) async throws -> Order
    func createOrder(_ order: Order) async throws -> Order
    func updateOrderStatus(id: String, status: Order.Status) async throws -> Order
}

protocol ProductRepositoryProtocol {
    func getProducts(categoryId: String?) async throws -> [Product]
    func getProduct(id: String) async throws -> Product
    func searchProducts(query: String) async throws -> [Product]
}

// MARK: - Domain/UseCases/PlaceOrderUseCase.swift

protocol PlaceOrderUseCaseProtocol {
    func execute(cart: Cart, shippingAddress: Address) async throws -> Order
}

final class PlaceOrderUseCase: PlaceOrderUseCaseProtocol {
    private let orderRepository: OrderRepositoryProtocol
    private let productRepository: ProductRepositoryProtocol
    private let userRepository: UserRepositoryProtocol

    init(
        orderRepository: OrderRepositoryProtocol,
        productRepository: ProductRepositoryProtocol,
        userRepository: UserRepositoryProtocol
    ) {
        self.orderRepository = orderRepository
        self.productRepository = productRepository
        self.userRepository = userRepository
    }

    func execute(cart: Cart, shippingAddress: Address) async throws -> Order {
        // Business Rule: Cart must not be empty
        guard !cart.items.isEmpty else {
            throw DomainError.businessRule("Cart is empty")
        }

        // Business Rule: Validate stock for all items
        for item in cart.items {
            let product = try await productRepository.getProduct(id: item.productId)
            guard product.stockQuantity >= item.quantity else {
                throw DomainError.businessRule("\(product.name) has insufficient stock")
            }
        }

        // Get current user
        let user = try await userRepository.getCurrentUser()

        // Create order
        let orderItems = cart.items.map { item in
            OrderItem(
                productId: item.productId,
                productName: item.productName,
                quantity: item.quantity,
                unitPrice: item.unitPrice
            )
        }

        let order = Order(
            id: UUID().uuidString,
            userId: user.id,
            items: orderItems,
            status: .pending,
            createdAt: Date(),
            shippingAddress: shippingAddress
        )

        return try await orderRepository.createOrder(order)
    }
}

// MARK: - Domain/UseCases/GetUserOrdersUseCase.swift

protocol GetUserOrdersUseCaseProtocol {
    func execute() async throws -> [Order]
}

final class GetUserOrdersUseCase: GetUserOrdersUseCaseProtocol {
    private let orderRepository: OrderRepositoryProtocol
    private let userRepository: UserRepositoryProtocol

    init(
        orderRepository: OrderRepositoryProtocol,
        userRepository: UserRepositoryProtocol
    ) {
        self.orderRepository = orderRepository
        self.userRepository = userRepository
    }

    func execute() async throws -> [Order] {
        let user = try await userRepository.getCurrentUser()
        return try await orderRepository.getOrders(userId: user.id)
    }
}
```

---

## Data Layer (Framework Dependencies OK)

```swift
// MARK: - Data/DTOs/UserDTO.swift

struct UserDTO: Codable {
    let id: String
    let email: String
    let name: String
    let avatar_url: String?
    let created_at: String
    let role: String
}

struct OrderDTO: Codable {
    let id: String
    let user_id: String
    let items: [OrderItemDTO]
    let status: String
    let created_at: String
    let shipping_address: AddressDTO
}

struct OrderItemDTO: Codable {
    let product_id: String
    let product_name: String
    let quantity: Int
    let unit_price: String
}

struct AddressDTO: Codable {
    let street: String
    let city: String
    let state: String
    let zip_code: String
    let country: String
}

// MARK: - Data/Mappers/UserMapper.swift

enum UserMapper {
    static func toDomain(_ dto: UserDTO) throws -> User {
        guard let role = User.Role(rawValue: dto.role) else {
            throw MappingError.invalidField("role", value: dto.role)
        }

        guard let createdAt = ISO8601DateFormatter().date(from: dto.created_at) else {
            throw MappingError.invalidField("created_at", value: dto.created_at)
        }

        return User(
            id: dto.id,
            email: dto.email,
            name: dto.name,
            avatarURL: dto.avatar_url.flatMap { URL(string: $0) },
            createdAt: createdAt,
            role: role
        )
    }

    static func toDTO(_ domain: User) -> UserDTO {
        UserDTO(
            id: domain.id,
            email: domain.email,
            name: domain.name,
            avatar_url: domain.avatarURL?.absoluteString,
            created_at: ISO8601DateFormatter().string(from: domain.createdAt),
            role: domain.role.rawValue
        )
    }
}

enum OrderMapper {
    static func toDomain(_ dto: OrderDTO) throws -> Order {
        guard let status = Order.Status(rawValue: dto.status) else {
            throw MappingError.invalidField("status", value: dto.status)
        }

        guard let createdAt = ISO8601DateFormatter().date(from: dto.created_at) else {
            throw MappingError.invalidField("created_at", value: dto.created_at)
        }

        let items = try dto.items.map { try OrderItemMapper.toDomain($0) }
        let address = AddressMapper.toDomain(dto.shipping_address)

        return Order(
            id: dto.id,
            userId: dto.user_id,
            items: items,
            status: status,
            createdAt: createdAt,
            shippingAddress: address
        )
    }
}

enum OrderItemMapper {
    static func toDomain(_ dto: OrderItemDTO) throws -> OrderItem {
        guard let unitPrice = Decimal(string: dto.unit_price) else {
            throw MappingError.invalidField("unit_price", value: dto.unit_price)
        }

        return OrderItem(
            productId: dto.product_id,
            productName: dto.product_name,
            quantity: dto.quantity,
            unitPrice: unitPrice
        )
    }
}

enum AddressMapper {
    static func toDomain(_ dto: AddressDTO) -> Address {
        Address(
            street: dto.street,
            city: dto.city,
            state: dto.state,
            zipCode: dto.zip_code,
            country: dto.country
        )
    }

    static func toDTO(_ domain: Address) -> AddressDTO {
        AddressDTO(
            street: domain.street,
            city: domain.city,
            state: domain.state,
            zip_code: domain.zipCode,
            country: domain.country
        )
    }
}

enum MappingError: Error {
    case invalidField(String, value: String)
}

// MARK: - Data/DataSources/UserRemoteDataSource.swift

protocol UserRemoteDataSourceProtocol {
    func fetchUser(id: String) async throws -> UserDTO
    func fetchCurrentUser() async throws -> UserDTO
    func updateUser(_ user: UserDTO) async throws -> UserDTO
}

final class UserRemoteDataSource: UserRemoteDataSourceProtocol {
    private let networkClient: NetworkClient

    init(networkClient: NetworkClient) {
        self.networkClient = networkClient
    }

    func fetchUser(id: String) async throws -> UserDTO {
        try await networkClient.request(.user(id: id))
    }

    func fetchCurrentUser() async throws -> UserDTO {
        try await networkClient.request(.currentUser)
    }

    func updateUser(_ user: UserDTO) async throws -> UserDTO {
        try await networkClient.request(.updateUser(user))
    }
}

// MARK: - Data/DataSources/UserLocalDataSource.swift

protocol UserLocalDataSourceProtocol {
    func getUser(id: String) async throws -> UserDTO?
    func saveUser(_ user: UserDTO) async throws
    func deleteUser(id: String) async throws
}

final class UserLocalDataSource: UserLocalDataSourceProtocol {
    private let database: DatabaseManager

    init(database: DatabaseManager) {
        self.database = database
    }

    func getUser(id: String) async throws -> UserDTO? {
        try await database.fetch(UserDTO.self, id: id)
    }

    func saveUser(_ user: UserDTO) async throws {
        try await database.save(user, id: user.id)
    }

    func deleteUser(id: String) async throws {
        try await database.delete(UserDTO.self, id: id)
    }
}

// MARK: - Data/Repositories/UserRepository.swift

final class UserRepository: UserRepositoryProtocol {
    private let remoteDataSource: UserRemoteDataSourceProtocol
    private let localDataSource: UserLocalDataSourceProtocol

    init(
        remoteDataSource: UserRemoteDataSourceProtocol,
        localDataSource: UserLocalDataSourceProtocol
    ) {
        self.remoteDataSource = remoteDataSource
        self.localDataSource = localDataSource
    }

    func getUser(id: String) async throws -> User {
        // Try cache first
        if let cached = try? await localDataSource.getUser(id: id) {
            return try UserMapper.toDomain(cached)
        }

        // Fetch from remote
        let dto = try await remoteDataSource.fetchUser(id: id)

        // Cache for next time
        try? await localDataSource.saveUser(dto)

        return try UserMapper.toDomain(dto)
    }

    func getCurrentUser() async throws -> User {
        let dto = try await remoteDataSource.fetchCurrentUser()
        try? await localDataSource.saveUser(dto)
        return try UserMapper.toDomain(dto)
    }

    func updateUser(_ user: User) async throws -> User {
        let dto = UserMapper.toDTO(user)
        let updatedDTO = try await remoteDataSource.updateUser(dto)
        try? await localDataSource.saveUser(updatedDTO)
        return try UserMapper.toDomain(updatedDTO)
    }
}
```

---

## Presentation Layer

```swift
// MARK: - Presentation/ViewModels/OrderHistoryViewModel.swift

import SwiftUI

@MainActor
final class OrderHistoryViewModel: ObservableObject {
    enum State: Equatable {
        case idle
        case loading
        case loaded([Order])
        case error(String)
    }

    @Published private(set) var state: State = .idle

    private let getUserOrdersUseCase: GetUserOrdersUseCaseProtocol

    init(getUserOrdersUseCase: GetUserOrdersUseCaseProtocol) {
        self.getUserOrdersUseCase = getUserOrdersUseCase
    }

    func loadOrders() async {
        state = .loading

        do {
            let orders = try await getUserOrdersUseCase.execute()
            state = .loaded(orders)
        } catch {
            state = .error(error.localizedDescription)
        }
    }
}

// MARK: - Presentation/Views/OrderHistoryView.swift

struct OrderHistoryView: View {
    @StateObject private var viewModel: OrderHistoryViewModel

    init(viewModel: OrderHistoryViewModel) {
        _viewModel = StateObject(wrappedValue: viewModel)
    }

    var body: some View {
        Group {
            switch viewModel.state {
            case .idle, .loading:
                ProgressView()
            case .loaded(let orders):
                if orders.isEmpty {
                    ContentUnavailableView(
                        "No Orders",
                        systemImage: "bag",
                        description: Text("You haven't placed any orders yet.")
                    )
                } else {
                    List(orders) { order in
                        OrderRowView(order: order)
                    }
                }
            case .error(let message):
                ContentUnavailableView(
                    "Error",
                    systemImage: "exclamationmark.triangle",
                    description: Text(message)
                )
            }
        }
        .navigationTitle("Orders")
        .task {
            await viewModel.loadOrders()
        }
    }
}

struct OrderRowView: View {
    let order: Order

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text("Order #\(order.id.prefix(8))")
                    .font(.headline)
                Spacer()
                StatusBadge(status: order.status)
            }

            Text("\(order.items.count) items")
                .foregroundColor(.secondary)

            Text(order.total, format: .currency(code: "USD"))
                .font(.subheadline.bold())
        }
        .padding(.vertical, 4)
    }
}

struct StatusBadge: View {
    let status: Order.Status

    var body: some View {
        Text(status.rawValue.capitalized)
            .font(.caption)
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .background(backgroundColor)
            .foregroundColor(.white)
            .cornerRadius(4)
    }

    private var backgroundColor: Color {
        switch status {
        case .pending: return .orange
        case .processing: return .blue
        case .shipped: return .purple
        case .delivered: return .green
        case .cancelled: return .red
        }
    }
}
```

---

## Dependency Container

```swift
// MARK: - Container/DependencyContainer.swift

@MainActor
final class DependencyContainer {
    static let shared = DependencyContainer()

    // MARK: - Infrastructure

    private lazy var networkClient: NetworkClient = {
        NetworkClient(baseURL: Environment.apiBaseURL)
    }()

    private lazy var database: DatabaseManager = {
        CoreDataManager(modelName: "AppModel")
    }()

    // MARK: - Data Sources

    private lazy var userRemoteDataSource: UserRemoteDataSourceProtocol = {
        UserRemoteDataSource(networkClient: networkClient)
    }()

    private lazy var userLocalDataSource: UserLocalDataSourceProtocol = {
        UserLocalDataSource(database: database)
    }()

    // MARK: - Repositories

    lazy var userRepository: UserRepositoryProtocol = {
        UserRepository(
            remoteDataSource: userRemoteDataSource,
            localDataSource: userLocalDataSource
        )
    }()

    lazy var orderRepository: OrderRepositoryProtocol = {
        OrderRepository(
            remoteDataSource: OrderRemoteDataSource(networkClient: networkClient),
            localDataSource: OrderLocalDataSource(database: database)
        )
    }()

    lazy var productRepository: ProductRepositoryProtocol = {
        ProductRepository(
            remoteDataSource: ProductRemoteDataSource(networkClient: networkClient)
        )
    }()

    // MARK: - Use Cases

    func makePlaceOrderUseCase() -> PlaceOrderUseCaseProtocol {
        PlaceOrderUseCase(
            orderRepository: orderRepository,
            productRepository: productRepository,
            userRepository: userRepository
        )
    }

    func makeGetUserOrdersUseCase() -> GetUserOrdersUseCaseProtocol {
        GetUserOrdersUseCase(
            orderRepository: orderRepository,
            userRepository: userRepository
        )
    }

    // MARK: - ViewModels

    func makeOrderHistoryViewModel() -> OrderHistoryViewModel {
        OrderHistoryViewModel(getUserOrdersUseCase: makeGetUserOrdersUseCase())
    }

    func makeCheckoutViewModel(cart: Cart) -> CheckoutViewModel {
        CheckoutViewModel(
            cart: cart,
            placeOrderUseCase: makePlaceOrderUseCase()
        )
    }
}
```
