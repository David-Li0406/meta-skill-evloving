# API Integration — Complete Service Layer

> **Loading Trigger**: Load when implementing service layer with caching, offline support, and proper error mapping.

---

## Complete Service Layer Architecture

```swift
// MARK: - ServiceResult.swift

enum ServiceResult<T> {
    case success(T)
    case failure(ServiceError)
    case cached(T, isStale: Bool)

    var value: T? {
        switch self {
        case .success(let value), .cached(let value, _):
            return value
        case .failure:
            return nil
        }
    }

    var error: ServiceError? {
        guard case .failure(let error) = self else { return nil }
        return error
    }

    var isStale: Bool {
        guard case .cached(_, let stale) = self else { return false }
        return stale
    }
}

// MARK: - ServiceError.swift

enum ServiceError: LocalizedError {
    case network(NetworkError)
    case validation([ValidationFailure])
    case notFound(resource: String)
    case unauthorized
    case serverError(message: String)
    case decodingFailed
    case unknown(Error)

    var errorDescription: String? {
        switch self {
        case .network(let error):
            return error.userMessage
        case .validation(let failures):
            return failures.map(\.message).joined(separator: ", ")
        case .notFound(let resource):
            return "\(resource) not found"
        case .unauthorized:
            return "Please log in to continue"
        case .serverError(let message):
            return message
        case .decodingFailed:
            return "Unable to process server response"
        case .unknown:
            return "An unexpected error occurred"
        }
    }

    var isRetryable: Bool {
        switch self {
        case .network(let error):
            return error.isRetryable
        case .serverError:
            return true
        default:
            return false
        }
    }
}

struct ValidationFailure {
    let field: String
    let message: String
}
```

---

## Base Service Protocol

```swift
// MARK: - BaseService.swift

protocol BaseServiceProtocol {
    var networkManager: NetworkManagerProtocol { get }
    var cache: CacheProtocol { get }
}

extension BaseServiceProtocol {

    // MARK: - Fetch with Cache Strategy

    func fetch<T: Codable>(
        cacheKey: String,
        ttl: CacheTTL = .short,
        forceRefresh: Bool = false,
        networkRequest: () async throws -> T
    ) async -> ServiceResult<T> {

        // Return cached if valid and not forcing refresh
        if !forceRefresh {
            if let cached: CacheEntry<T> = cache.get(cacheKey) {
                if !cached.isExpired {
                    return .success(cached.value)
                } else {
                    // Return stale and refresh in background
                    Task { await refreshInBackground(cacheKey: cacheKey, ttl: ttl, request: networkRequest) }
                    return .cached(cached.value, isStale: true)
                }
            }
        }

        // Fetch from network
        do {
            let result = try await networkRequest()
            cache.set(cacheKey, value: result, ttl: ttl)
            return .success(result)
        } catch let error as NetworkError {
            // On network failure, try to return stale cache
            if let cached: CacheEntry<T> = cache.get(cacheKey) {
                return .cached(cached.value, isStale: true)
            }
            return .failure(.network(error))
        } catch {
            return .failure(.unknown(error))
        }
    }

    private func refreshInBackground<T: Codable>(
        cacheKey: String,
        ttl: CacheTTL,
        request: () async throws -> T
    ) async {
        do {
            let result = try await request()
            cache.set(cacheKey, value: result, ttl: ttl)
        } catch {
            // Silent failure for background refresh
        }
    }

    // MARK: - Error Mapping

    func mapError(_ error: Error) -> ServiceError {
        switch error {
        case let networkError as NetworkError:
            switch networkError {
            case .unauthorized:
                return .unauthorized
            case .notFound:
                return .notFound(resource: "Resource")
            default:
                return .network(networkError)
            }
        case is DecodingError:
            return .decodingFailed
        case let serviceError as ServiceError:
            return serviceError
        default:
            return .unknown(error)
        }
    }
}
```

---

## User Service Implementation

```swift
// MARK: - UserServiceProtocol.swift

protocol UserServiceProtocol {
    func getCurrentUser(forceRefresh: Bool) async -> ServiceResult<User>
    func getUser(id: String, forceRefresh: Bool) async -> ServiceResult<User>
    func updateUser(_ update: UserUpdate) async -> ServiceResult<User>
    func searchUsers(query: String, page: Int) async -> ServiceResult<PaginatedResult<User>>
}

// MARK: - UserService.swift

final class UserService: BaseServiceProtocol, UserServiceProtocol {
    let networkManager: NetworkManagerProtocol
    let cache: CacheProtocol

    init(
        networkManager: NetworkManagerProtocol = NetworkManager.shared,
        cache: CacheProtocol = CacheManager.shared
    ) {
        self.networkManager = networkManager
        self.cache = cache
    }

    // MARK: - Get Current User

    func getCurrentUser(forceRefresh: Bool = false) async -> ServiceResult<User> {
        await fetch(
            cacheKey: CacheKeys.currentUser,
            ttl: .medium,
            forceRefresh: forceRefresh
        ) { [networkManager] in
            let dto: UserDTO = try await networkManager.request(.getCurrentUser)
            return try User(from: dto)
        }
    }

    // MARK: - Get User by ID

    func getUser(id: String, forceRefresh: Bool = false) async -> ServiceResult<User> {
        await fetch(
            cacheKey: CacheKeys.user(id: id),
            ttl: .short,
            forceRefresh: forceRefresh
        ) { [networkManager] in
            let dto: UserDTO = try await networkManager.request(.getUser(id: id))
            return try User(from: dto)
        }
    }

    // MARK: - Update User

    func updateUser(_ update: UserUpdate) async -> ServiceResult<User> {
        do {
            let dto: UserDTO = try await networkManager.request(
                .updateUser(id: update.id, name: update.name, email: update.email)
            )
            let user = try User(from: dto)

            // Invalidate related caches
            cache.remove(CacheKeys.user(id: update.id))
            cache.remove(CacheKeys.currentUser)

            return .success(user)
        } catch let error as NetworkError where error.validationErrors != nil {
            return .failure(.validation(error.validationErrors!))
        } catch {
            return .failure(mapError(error))
        }
    }

    // MARK: - Search Users

    func searchUsers(query: String, page: Int) async -> ServiceResult<PaginatedResult<User>> {
        // Don't cache search results
        do {
            let response: PaginatedResponse<UserDTO> = try await networkManager.request(
                .searchUsers(query: query, page: page)
            )
            let users = try response.data.map { try User(from: $0) }
            let result = PaginatedResult(
                items: users,
                page: response.page,
                totalPages: response.totalPages,
                totalItems: response.totalItems
            )
            return .success(result)
        } catch {
            return .failure(mapError(error))
        }
    }
}

// MARK: - Cache Keys

private enum CacheKeys {
    static let currentUser = "user_current"
    static func user(id: String) -> String { "user_\(id)" }
}
```

---

## Cache System

```swift
// MARK: - CacheProtocol.swift

protocol CacheProtocol {
    func get<T: Codable>(_ key: String) -> CacheEntry<T>?
    func set<T: Codable>(_ key: String, value: T, ttl: CacheTTL)
    func remove(_ key: String)
    func removeAll()
}

// MARK: - CacheEntry.swift

struct CacheEntry<T: Codable>: Codable {
    let value: T
    let createdAt: Date
    let expiresAt: Date

    var isExpired: Bool {
        Date() >= expiresAt
    }

    var age: TimeInterval {
        Date().timeIntervalSince(createdAt)
    }
}

// MARK: - CacheTTL.swift

enum CacheTTL {
    case short      // 5 minutes
    case medium     // 15 minutes
    case long       // 1 hour
    case veryLong   // 24 hours
    case custom(TimeInterval)

    var interval: TimeInterval {
        switch self {
        case .short: return 5 * 60
        case .medium: return 15 * 60
        case .long: return 60 * 60
        case .veryLong: return 24 * 60 * 60
        case .custom(let interval): return interval
        }
    }
}

// MARK: - CacheManager.swift

final class CacheManager: CacheProtocol {
    static let shared = CacheManager()

    private let memoryCache = NSCache<NSString, CacheEntryWrapper>()
    private let fileManager = FileManager.default
    private let cacheDirectory: URL
    private let encoder = JSONEncoder()
    private let decoder = JSONDecoder()
    private let queue = DispatchQueue(label: "com.app.cache", attributes: .concurrent)

    init() {
        let paths = fileManager.urls(for: .cachesDirectory, in: .userDomainMask)
        cacheDirectory = paths[0].appendingPathComponent("AppCache")

        try? fileManager.createDirectory(at: cacheDirectory, withIntermediateDirectories: true)
    }

    // MARK: - Get

    func get<T: Codable>(_ key: String) -> CacheEntry<T>? {
        // Try memory cache first
        if let wrapper = memoryCache.object(forKey: key as NSString),
           let entry = wrapper.entry as? CacheEntry<T> {
            return entry
        }

        // Try disk cache
        return queue.sync {
            let fileURL = cacheDirectory.appendingPathComponent(key.sha256)

            guard let data = try? Data(contentsOf: fileURL),
                  let entry = try? decoder.decode(CacheEntry<T>.self, from: data) else {
                return nil
            }

            // Populate memory cache
            let wrapper = CacheEntryWrapper(entry: entry)
            memoryCache.setObject(wrapper, forKey: key as NSString)

            return entry
        }
    }

    // MARK: - Set

    func set<T: Codable>(_ key: String, value: T, ttl: CacheTTL) {
        let entry = CacheEntry(
            value: value,
            createdAt: Date(),
            expiresAt: Date().addingTimeInterval(ttl.interval)
        )

        // Memory cache
        let wrapper = CacheEntryWrapper(entry: entry)
        memoryCache.setObject(wrapper, forKey: key as NSString)

        // Disk cache (background)
        queue.async(flags: .barrier) { [weak self] in
            guard let self = self,
                  let data = try? self.encoder.encode(entry) else { return }

            let fileURL = self.cacheDirectory.appendingPathComponent(key.sha256)
            try? data.write(to: fileURL)
        }
    }

    // MARK: - Remove

    func remove(_ key: String) {
        memoryCache.removeObject(forKey: key as NSString)

        queue.async(flags: .barrier) { [weak self] in
            guard let self = self else { return }
            let fileURL = self.cacheDirectory.appendingPathComponent(key.sha256)
            try? self.fileManager.removeItem(at: fileURL)
        }
    }

    func removeAll() {
        memoryCache.removeAllObjects()

        queue.async(flags: .barrier) { [weak self] in
            guard let self = self else { return }
            try? self.fileManager.removeItem(at: self.cacheDirectory)
            try? self.fileManager.createDirectory(at: self.cacheDirectory, withIntermediateDirectories: true)
        }
    }
}

// MARK: - Wrapper for NSCache

private class CacheEntryWrapper {
    let entry: Any

    init<T: Codable>(entry: CacheEntry<T>) {
        self.entry = entry
    }
}

// MARK: - String Extension

private extension String {
    var sha256: String {
        let data = Data(utf8)
        var hash = [UInt8](repeating: 0, count: Int(CC_SHA256_DIGEST_LENGTH))
        data.withUnsafeBytes {
            _ = CC_SHA256($0.baseAddress, CC_LONG(data.count), &hash)
        }
        return hash.map { String(format: "%02x", $0) }.joined()
    }
}
```

---

## Offline Sync System

```swift
// MARK: - SyncQueue.swift

actor SyncQueue {
    static let shared = SyncQueue()

    private var pendingOperations: [PendingOperation] = []
    private let storage: SyncQueueStorage
    private var isProcessing = false

    init(storage: SyncQueueStorage = .shared) {
        self.storage = storage
        Task { await loadPendingOperations() }
    }

    // MARK: - Enqueue

    func enqueue(_ operation: PendingOperation) {
        pendingOperations.append(operation)
        Task { await storage.save(pendingOperations) }
    }

    // MARK: - Process Queue

    func processQueue() async {
        guard !isProcessing, !pendingOperations.isEmpty else { return }

        isProcessing = true
        defer { isProcessing = false }

        var failed: [PendingOperation] = []

        for operation in pendingOperations {
            do {
                try await executeOperation(operation)
            } catch {
                var updatedOp = operation
                updatedOp.retryCount += 1

                if updatedOp.retryCount < updatedOp.maxRetries {
                    failed.append(updatedOp)
                } else {
                    // Max retries reached - notify user or log
                    await handleFailedOperation(updatedOp, error: error)
                }
            }
        }

        pendingOperations = failed
        await storage.save(pendingOperations)
    }

    // MARK: - Private

    private func loadPendingOperations() async {
        pendingOperations = await storage.load()
    }

    private func executeOperation(_ operation: PendingOperation) async throws {
        switch operation.type {
        case .createOrder(let request):
            _ = try await OrderService.shared.createOrder(request)
        case .updateUser(let update):
            _ = try await UserService.shared.updateUser(update)
        case .deleteItem(let id):
            try await ItemService.shared.deleteItem(id: id)
        }
    }

    private func handleFailedOperation(_ operation: PendingOperation, error: Error) async {
        NotificationCenter.default.post(
            name: .syncOperationFailed,
            object: nil,
            userInfo: [
                "operation": operation,
                "error": error
            ]
        )
    }
}

// MARK: - PendingOperation.swift

struct PendingOperation: Codable, Identifiable {
    let id: UUID
    let type: OperationType
    let createdAt: Date
    var retryCount: Int
    let maxRetries: Int

    init(type: OperationType, maxRetries: Int = 3) {
        self.id = UUID()
        self.type = type
        self.createdAt = Date()
        self.retryCount = 0
        self.maxRetries = maxRetries
    }

    enum OperationType: Codable {
        case createOrder(CreateOrderRequest)
        case updateUser(UserUpdate)
        case deleteItem(id: String)
    }
}

// MARK: - NetworkMonitor.swift

import Network

@MainActor
final class NetworkMonitor: ObservableObject {
    static let shared = NetworkMonitor()

    @Published private(set) var isConnected = true
    @Published private(set) var connectionType: ConnectionType = .unknown

    private let monitor = NWPathMonitor()
    private let queue = DispatchQueue(label: "com.app.networkmonitor")

    enum ConnectionType {
        case wifi
        case cellular
        case wired
        case unknown
    }

    init() {
        startMonitoring()
    }

    private func startMonitoring() {
        monitor.pathUpdateHandler = { [weak self] path in
            Task { @MainActor in
                self?.isConnected = path.status == .satisfied

                if path.usesInterfaceType(.wifi) {
                    self?.connectionType = .wifi
                } else if path.usesInterfaceType(.cellular) {
                    self?.connectionType = .cellular
                } else if path.usesInterfaceType(.wiredEthernet) {
                    self?.connectionType = .wired
                } else {
                    self?.connectionType = .unknown
                }

                // Process sync queue when connection restored
                if path.status == .satisfied {
                    await SyncQueue.shared.processQueue()
                }
            }
        }

        monitor.start(queue: queue)
    }
}
```

---

## Pagination Support

```swift
// MARK: - PaginatedResult.swift

struct PaginatedResult<T> {
    let items: [T]
    let page: Int
    let totalPages: Int
    let totalItems: Int

    var hasMore: Bool {
        page < totalPages
    }

    var nextPage: Int? {
        hasMore ? page + 1 : nil
    }
}

// MARK: - PaginationState.swift

@MainActor
final class PaginationState<T: Identifiable>: ObservableObject {
    @Published private(set) var items: [T] = []
    @Published private(set) var isLoading = false
    @Published private(set) var isLoadingMore = false
    @Published private(set) var error: ServiceError?
    @Published private(set) var hasMore = true

    private var currentPage = 0
    private let pageSize: Int
    private let fetch: (Int, Int) async -> ServiceResult<PaginatedResult<T>>

    init(
        pageSize: Int = 20,
        fetch: @escaping (Int, Int) async -> ServiceResult<PaginatedResult<T>>
    ) {
        self.pageSize = pageSize
        self.fetch = fetch
    }

    func loadInitial() async {
        guard !isLoading else { return }

        isLoading = true
        error = nil
        currentPage = 1

        let result = await fetch(1, pageSize)

        switch result {
        case .success(let paginated), .cached(let paginated, _):
            items = paginated.items
            hasMore = paginated.hasMore
        case .failure(let err):
            error = err
        }

        isLoading = false
    }

    func loadMore() async {
        guard !isLoading, !isLoadingMore, hasMore else { return }

        isLoadingMore = true
        let nextPage = currentPage + 1

        let result = await fetch(nextPage, pageSize)

        switch result {
        case .success(let paginated), .cached(let paginated, _):
            items.append(contentsOf: paginated.items)
            currentPage = nextPage
            hasMore = paginated.hasMore
        case .failure:
            // Silent failure for pagination
            break
        }

        isLoadingMore = false
    }

    func refresh() async {
        await loadInitial()
    }
}
```
