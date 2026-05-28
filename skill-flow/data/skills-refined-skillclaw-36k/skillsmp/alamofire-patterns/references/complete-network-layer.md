# Alamofire Patterns — Complete Network Layer

> **Loading Trigger**: Load when implementing production network layer with Alamofire, including authentication, retry logic, and certificate pinning.

---

## Complete Session Configuration

```swift
// MARK: - NetworkConfiguration.swift

import Alamofire
import Foundation

enum NetworkConfiguration {

    // MARK: - Environment

    enum Environment {
        case development
        case staging
        case production

        var baseURL: URL {
            switch self {
            case .development:
                return URL(string: "https://dev-api.yourapp.com")!
            case .staging:
                return URL(string: "https://staging-api.yourapp.com")!
            case .production:
                return URL(string: "https://api.yourapp.com")!
            }
        }

        static var current: Environment {
            #if DEBUG
            return .development
            #elseif STAGING
            return .staging
            #else
            return .production
            #endif
        }
    }

    // MARK: - Session Factory

    static func makeSession(
        tokenStore: TokenStoreProtocol,
        environment: Environment = .current
    ) -> Session {
        let configuration = URLSessionConfiguration.af.default
        configuration.timeoutIntervalForRequest = 30
        configuration.timeoutIntervalForResource = 60
        configuration.waitsForConnectivity = true

        // Interceptor chain
        let interceptor = makeInterceptor(tokenStore: tokenStore)

        // Server trust
        let serverTrustManager = makeServerTrustManager(for: environment)

        // Event monitors
        let monitors: [EventMonitor] = [
            NetworkLogger(),
            NetworkMetrics()
        ]

        return Session(
            configuration: configuration,
            interceptor: interceptor,
            serverTrustManager: serverTrustManager,
            eventMonitors: monitors
        )
    }

    // MARK: - Interceptor

    private static func makeInterceptor(tokenStore: TokenStoreProtocol) -> Interceptor {
        let authenticator = OAuthAuthenticator(tokenStore: tokenStore)
        let credential = tokenStore.currentCredential

        let authInterceptor = AuthenticationInterceptor(
            authenticator: authenticator,
            credential: credential
        )

        return Interceptor(
            adapters: [
                BaseHeadersAdapter(),
                authInterceptor
            ],
            retriers: [
                authInterceptor,
                NetworkRetryPolicy()
            ]
        )
    }

    // MARK: - Server Trust

    private static func makeServerTrustManager(for environment: Environment) -> ServerTrustManager {
        let evaluators: [String: ServerTrustEvaluating]

        switch environment {
        case .development:
            // Allow self-signed certs in development
            evaluators = [
                "dev-api.yourapp.com": DisabledTrustEvaluator()
            ]
        case .staging, .production:
            // Certificate pinning for staging/production
            evaluators = [
                "api.yourapp.com": PinnedCertificatesTrustEvaluator(
                    certificates: Bundle.main.af.certificates,
                    acceptSelfSignedCertificates: false,
                    performDefaultValidation: true,
                    validateHost: true
                ),
                "staging-api.yourapp.com": PinnedCertificatesTrustEvaluator(
                    certificates: Bundle.main.af.certificates,
                    acceptSelfSignedCertificates: false,
                    performDefaultValidation: true,
                    validateHost: true
                )
            ]
        }

        return ServerTrustManager(evaluators: evaluators)
    }
}
```

---

## Complete OAuth Authenticator

```swift
// MARK: - OAuthCredential.swift

import Alamofire
import Foundation

struct OAuthCredential: AuthenticationCredential {
    let accessToken: String
    let refreshToken: String
    let expiration: Date

    var requiresRefresh: Bool {
        // Refresh 5 minutes before expiration
        Date().addingTimeInterval(5 * 60) >= expiration
    }
}

// MARK: - OAuthAuthenticator.swift

final class OAuthAuthenticator: Authenticator {
    typealias Credential = OAuthCredential

    private let tokenStore: TokenStoreProtocol
    private let refreshService: TokenRefreshServiceProtocol
    private let lock = NSLock()
    private var isRefreshing = false
    private var refreshCompletions: [(Result<OAuthCredential, Error>) -> Void] = []

    init(
        tokenStore: TokenStoreProtocol,
        refreshService: TokenRefreshServiceProtocol = TokenRefreshService()
    ) {
        self.tokenStore = tokenStore
        self.refreshService = refreshService
    }

    // MARK: - Apply Credential

    func apply(_ credential: OAuthCredential, to urlRequest: inout URLRequest) {
        urlRequest.headers.add(.authorization(bearerToken: credential.accessToken))
    }

    // MARK: - Refresh

    func refresh(
        _ credential: OAuthCredential,
        for session: Session,
        completion: @escaping (Result<OAuthCredential, Error>) -> Void
    ) {
        lock.lock()

        // If already refreshing, queue the completion
        if isRefreshing {
            refreshCompletions.append(completion)
            lock.unlock()
            return
        }

        isRefreshing = true
        refreshCompletions.append(completion)
        lock.unlock()

        // Perform refresh
        Task {
            do {
                let tokens = try await refreshService.refreshToken(
                    refreshToken: credential.refreshToken
                )

                let newCredential = OAuthCredential(
                    accessToken: tokens.accessToken,
                    refreshToken: tokens.refreshToken,
                    expiration: tokens.expiresAt
                )

                // Save new credential
                tokenStore.save(newCredential)

                // Complete all waiting requests
                completeRefresh(with: .success(newCredential))

            } catch {
                // Clear invalid tokens
                tokenStore.clear()

                // Notify all waiting requests
                completeRefresh(with: .failure(error))

                // Post logout notification
                NotificationCenter.default.post(
                    name: .authSessionExpired,
                    object: nil
                )
            }
        }
    }

    private func completeRefresh(with result: Result<OAuthCredential, Error>) {
        lock.lock()
        let completions = refreshCompletions
        refreshCompletions = []
        isRefreshing = false
        lock.unlock()

        completions.forEach { $0(result) }
    }

    // MARK: - Failure Detection

    func didRequest(
        _ urlRequest: URLRequest,
        with response: HTTPURLResponse,
        failDueToAuthenticationError error: Error
    ) -> Bool {
        response.statusCode == 401
    }

    func isRequest(
        _ urlRequest: URLRequest,
        authenticatedWith credential: OAuthCredential
    ) -> Bool {
        let bearerToken = HTTPHeader.authorization(bearerToken: credential.accessToken).value
        return urlRequest.headers["Authorization"] == bearerToken
    }
}
```

---

## Request Adapters

```swift
// MARK: - BaseHeadersAdapter.swift

import Alamofire
import Foundation

final class BaseHeadersAdapter: RequestAdapter {

    func adapt(
        _ urlRequest: URLRequest,
        for session: Session,
        completion: @escaping (Result<URLRequest, Error>) -> Void
    ) {
        var request = urlRequest

        // Common headers
        request.headers.add(.contentType("application/json"))
        request.headers.add(.accept("application/json"))

        // App version
        if let version = Bundle.main.infoDictionary?["CFBundleShortVersionString"] as? String,
           let build = Bundle.main.infoDictionary?["CFBundleVersion"] as? String {
            request.headers.add(name: "X-App-Version", value: "\(version)+\(build)")
        }

        // Platform
        request.headers.add(name: "X-Platform", value: "iOS")

        // Device ID (non-PII)
        if let deviceId = UIDevice.current.identifierForVendor?.uuidString {
            request.headers.add(name: "X-Device-Id", value: deviceId)
        }

        // Locale
        request.headers.add(name: "Accept-Language", value: Locale.current.identifier)

        completion(.success(request))
    }
}

// MARK: - IdempotencyKeyAdapter.swift

/// Adds idempotency key for POST/PUT/PATCH requests
final class IdempotencyKeyAdapter: RequestAdapter {

    func adapt(
        _ urlRequest: URLRequest,
        for session: Session,
        completion: @escaping (Result<URLRequest, Error>) -> Void
    ) {
        var request = urlRequest

        // Only add for mutating requests
        let mutatingMethods: Set<HTTPMethod> = [.post, .put, .patch]
        if let method = request.method, mutatingMethods.contains(method) {
            // Check if not already set
            if request.headers["Idempotency-Key"] == nil {
                request.headers.add(name: "Idempotency-Key", value: UUID().uuidString)
            }
        }

        completion(.success(request))
    }
}
```

---

## Retry Policy

```swift
// MARK: - NetworkRetryPolicy.swift

import Alamofire
import Foundation

final class NetworkRetryPolicy: RequestRetrier {
    private let maxRetries: Int
    private let exponentialBackoffBase: Double
    private let exponentialBackoffScale: Double

    init(
        maxRetries: Int = 3,
        exponentialBackoffBase: Double = 2.0,
        exponentialBackoffScale: Double = 0.5
    ) {
        self.maxRetries = maxRetries
        self.exponentialBackoffBase = exponentialBackoffBase
        self.exponentialBackoffScale = exponentialBackoffScale
    }

    func retry(
        _ request: Request,
        for session: Session,
        dueTo error: Error,
        completion: @escaping (RetryResult) -> Void
    ) {
        let retryCount = request.retryCount

        // Check retry limit
        guard retryCount < maxRetries else {
            completion(.doNotRetry)
            return
        }

        // Only retry for retryable errors
        guard shouldRetry(error: error, request: request) else {
            completion(.doNotRetry)
            return
        }

        // Calculate delay with exponential backoff
        let delay = pow(exponentialBackoffBase, Double(retryCount)) * exponentialBackoffScale

        completion(.retryWithDelay(delay))
    }

    private func shouldRetry(error: Error, request: Request) -> Bool {
        // Check if request is idempotent (safe to retry)
        guard isIdempotent(request: request) else {
            return false
        }

        // Retry for network errors
        if let urlError = error as? URLError {
            let retryableCodes: Set<URLError.Code> = [
                .timedOut,
                .cannotFindHost,
                .cannotConnectToHost,
                .networkConnectionLost,
                .dnsLookupFailed,
                .notConnectedToInternet
            ]
            return retryableCodes.contains(urlError.code)
        }

        // Retry for specific HTTP status codes
        if let response = request.response {
            let retryableStatusCodes: Set<Int> = [408, 429, 503, 504]
            return retryableStatusCodes.contains(response.statusCode)
        }

        return false
    }

    private func isIdempotent(request: Request) -> Bool {
        guard let httpMethod = request.request?.method else {
            return false
        }

        // GET, HEAD, OPTIONS, PUT, DELETE are idempotent
        // POST is NOT idempotent unless it has an idempotency key
        let idempotentMethods: Set<HTTPMethod> = [.get, .head, .options, .put, .delete]

        if idempotentMethods.contains(httpMethod) {
            return true
        }

        // POST with idempotency key is safe to retry
        if httpMethod == .post,
           request.request?.headers["Idempotency-Key"] != nil {
            return true
        }

        return false
    }
}
```

---

## Event Monitors

```swift
// MARK: - NetworkLogger.swift

import Alamofire
import os.log

final class NetworkLogger: EventMonitor {
    private let logger = Logger(subsystem: Bundle.main.bundleIdentifier ?? "App", category: "Network")

    let queue = DispatchQueue(label: "com.app.networklogger")

    func requestDidResume(_ request: Request) {
        let method = request.request?.method?.rawValue ?? "?"
        let url = request.request?.url?.absoluteString ?? "?"

        logger.info("➡️ \(method) \(url)")

        #if DEBUG
        if let headers = request.request?.headers {
            logger.debug("Headers: \(headers.dictionary)")
        }
        if let body = request.request?.httpBody,
           let bodyString = String(data: body, encoding: .utf8) {
            logger.debug("Body: \(bodyString)")
        }
        #endif
    }

    func request<Value>(_ request: DataRequest, didParseResponse response: DataResponse<Value, AFError>) {
        let method = request.request?.method?.rawValue ?? "?"
        let url = request.request?.url?.absoluteString ?? "?"
        let statusCode = response.response?.statusCode ?? 0
        let duration = response.metrics?.taskInterval.duration ?? 0

        switch response.result {
        case .success:
            logger.info("✅ \(method) \(url) [\(statusCode)] (\(String(format: "%.2f", duration))s)")
        case .failure(let error):
            logger.error("❌ \(method) \(url) [\(statusCode)] - \(error.localizedDescription)")
        }
    }
}

// MARK: - NetworkMetrics.swift

import Alamofire
import os.signpost

final class NetworkMetrics: EventMonitor {
    private let signpostLog = OSLog(subsystem: Bundle.main.bundleIdentifier ?? "App", category: .pointsOfInterest)
    private var signpostIDs: [Request: OSSignpostID] = [:]

    let queue = DispatchQueue(label: "com.app.networkmetrics")

    func requestDidResume(_ request: Request) {
        let signpostID = OSSignpostID(log: signpostLog)
        signpostIDs[request] = signpostID

        let name = request.request?.url?.path ?? "request"
        os_signpost(.begin, log: signpostLog, name: "Network Request", signpostID: signpostID, "%{public}s", name)
    }

    func requestDidFinish(_ request: Request) {
        guard let signpostID = signpostIDs.removeValue(forKey: request) else { return }

        let statusCode = request.response?.statusCode ?? 0
        os_signpost(.end, log: signpostLog, name: "Network Request", signpostID: signpostID, "status: %d", statusCode)
    }
}
```

---

## API Router

```swift
// MARK: - APIRouter.swift

import Alamofire
import Foundation

enum APIRouter: URLRequestConvertible {
    // MARK: - Auth
    case login(email: String, password: String)
    case refreshToken(refreshToken: String)
    case logout

    // MARK: - Users
    case getCurrentUser
    case getUser(id: String)
    case updateUser(id: String, name: String?, email: String?)
    case deleteUser(id: String)

    // MARK: - Products
    case getProducts(page: Int, limit: Int)
    case getProduct(id: String)
    case searchProducts(query: String, page: Int)

    // MARK: - Orders
    case getOrders(page: Int, limit: Int)
    case getOrder(id: String)
    case createOrder(items: [OrderItemRequest], idempotencyKey: String)
    case cancelOrder(id: String)

    // MARK: - URL Request Convertible

    func asURLRequest() throws -> URLRequest {
        let url = NetworkConfiguration.Environment.current.baseURL.appendingPathComponent(path)
        var request = try URLRequest(url: url, method: method)

        // Body encoding
        if let parameters = parameters {
            request = try JSONParameterEncoder.default.encode(parameters, into: request)
        }

        // Custom headers
        for (key, value) in headers {
            request.headers.add(name: key, value: value)
        }

        return request
    }

    // MARK: - Components

    private var path: String {
        switch self {
        case .login: return "/auth/login"
        case .refreshToken: return "/auth/refresh"
        case .logout: return "/auth/logout"

        case .getCurrentUser: return "/users/me"
        case .getUser(let id): return "/users/\(id)"
        case .updateUser(let id, _, _): return "/users/\(id)"
        case .deleteUser(let id): return "/users/\(id)"

        case .getProducts: return "/products"
        case .getProduct(let id): return "/products/\(id)"
        case .searchProducts: return "/products/search"

        case .getOrders: return "/orders"
        case .getOrder(let id): return "/orders/\(id)"
        case .createOrder: return "/orders"
        case .cancelOrder(let id): return "/orders/\(id)/cancel"
        }
    }

    private var method: HTTPMethod {
        switch self {
        case .login, .refreshToken, .createOrder, .cancelOrder:
            return .post
        case .updateUser:
            return .patch
        case .deleteUser:
            return .delete
        case .logout, .getCurrentUser, .getUser, .getProducts, .getProduct, .searchProducts, .getOrders, .getOrder:
            return .get
        }
    }

    private var parameters: Encodable? {
        switch self {
        case .login(let email, let password):
            return ["email": email, "password": password]
        case .refreshToken(let refreshToken):
            return ["refresh_token": refreshToken]
        case .updateUser(_, let name, let email):
            var params: [String: String] = [:]
            if let name = name { params["name"] = name }
            if let email = email { params["email"] = email }
            return params.isEmpty ? nil : params
        case .getProducts(let page, let limit):
            return ["page": page, "limit": limit]
        case .searchProducts(let query, let page):
            return ["q": query, "page": page]
        case .getOrders(let page, let limit):
            return ["page": page, "limit": limit]
        case .createOrder(let items, _):
            return ["items": items]
        default:
            return nil
        }
    }

    private var headers: [String: String] {
        switch self {
        case .createOrder(_, let idempotencyKey):
            return ["Idempotency-Key": idempotencyKey]
        default:
            return [:]
        }
    }

    // MARK: - Auth Requirements

    var requiresAuthentication: Bool {
        switch self {
        case .login, .refreshToken:
            return false
        default:
            return true
        }
    }
}
```

---

## Network Manager

```swift
// MARK: - NetworkManager.swift

import Alamofire
import Foundation

protocol NetworkManagerProtocol {
    func request<T: Decodable>(_ router: APIRouter) async throws -> T
    func request(_ router: APIRouter) async throws
}

final class NetworkManager: NetworkManagerProtocol {
    static let shared = NetworkManager()

    private let session: Session
    private let decoder: JSONDecoder

    init(
        session: Session? = nil,
        tokenStore: TokenStoreProtocol = TokenStore.shared
    ) {
        self.session = session ?? NetworkConfiguration.makeSession(tokenStore: tokenStore)

        self.decoder = JSONDecoder()
        self.decoder.keyDecodingStrategy = .convertFromSnakeCase
        self.decoder.dateDecodingStrategy = .iso8601
    }

    // MARK: - Request with Response

    func request<T: Decodable>(_ router: APIRouter) async throws -> T {
        try await session.request(router)
            .validate(statusCode: 200..<300)
            .serializingDecodable(T.self, decoder: decoder)
            .value
    }

    // MARK: - Request without Response

    func request(_ router: APIRouter) async throws {
        _ = try await session.request(router)
            .validate(statusCode: 200..<300)
            .serializingData()
            .value
    }
}
```
