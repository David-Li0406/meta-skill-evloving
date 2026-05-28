# Complete Session Management System

<!-- Loading Trigger: Agent reads this file when implementing authentication flows, token management, Keychain storage, session refresh strategies, or logout cleanup -->

## Complete SessionManager Implementation

```swift
import Foundation
import Combine

// MARK: - Session Manager

@MainActor
final class SessionManager: ObservableObject {

    // MARK: - Singleton

    static let shared = SessionManager()

    // MARK: - Published State

    @Published private(set) var authenticationState: AuthenticationState = .unknown
    @Published private(set) var currentUser: User?

    // MARK: - Private Properties

    private let keychainService = "com.app.session"
    private let tokenRefreshThreshold: TimeInterval = 5 * 60 // 5 minutes before expiry
    private var refreshTask: Task<Void, Never>?
    private var tokenExpirationDate: Date?
    private var cancellables = Set<AnyCancellable>()

    // MARK: - Initialization

    private init() {
        restoreSession()
        setupNotifications()
    }

    // MARK: - Authentication State

    enum AuthenticationState: Equatable {
        case unknown
        case authenticated
        case unauthenticated
        case refreshing
        case sessionExpired
    }

    // MARK: - Public API

    /// Login with credentials
    func login(email: String, password: String) async throws {
        authenticationState = .refreshing

        do {
            let response = try await AuthAPI.login(email: email, password: password)
            try storeTokens(response.tokens)
            currentUser = response.user
            authenticationState = .authenticated
            scheduleTokenRefresh(expiresAt: response.tokens.accessTokenExpiry)
        } catch {
            authenticationState = .unauthenticated
            throw error
        }
    }

    /// Login with OAuth provider
    func loginWithOAuth(provider: OAuthProvider, code: String) async throws {
        authenticationState = .refreshing

        do {
            let response = try await AuthAPI.exchangeOAuthCode(provider: provider, code: code)
            try storeTokens(response.tokens)
            currentUser = response.user
            authenticationState = .authenticated
            scheduleTokenRefresh(expiresAt: response.tokens.accessTokenExpiry)
        } catch {
            authenticationState = .unauthenticated
            throw error
        }
    }

    /// Logout and clean up
    func logout(reason: LogoutReason = .userInitiated) {
        // Cancel any pending refresh
        refreshTask?.cancel()
        refreshTask = nil

        // Clear tokens from Keychain
        KeychainManager.shared.deleteAll(service: keychainService)

        // Clear user state
        currentUser = nil
        tokenExpirationDate = nil

        // Update auth state
        switch reason {
        case .userInitiated, .serverForced:
            authenticationState = .unauthenticated
        case .tokenExpired:
            authenticationState = .sessionExpired
        }

        // Perform cleanup
        performLogoutCleanup()

        // Notify observers
        NotificationCenter.default.post(name: .userDidLogout, object: nil, userInfo: [
            "reason": reason
        ])
    }

    enum LogoutReason {
        case userInitiated
        case tokenExpired
        case serverForced
    }

    /// Get current access token (for API requests)
    func getAccessToken() async throws -> String {
        // Check if we have a valid token
        guard let token = KeychainManager.shared.read(
            service: keychainService,
            account: "accessToken"
        ) else {
            throw SessionError.noToken
        }

        // Check if token needs refresh
        if let expiryDate = tokenExpirationDate,
           expiryDate.timeIntervalSinceNow < tokenRefreshThreshold {
            try await refreshAccessToken()
        }

        return token
    }

    /// Manually refresh token (call before long operations)
    func refreshAccessToken() async throws {
        guard let refreshToken = KeychainManager.shared.read(
            service: keychainService,
            account: "refreshToken"
        ) else {
            logout(reason: .tokenExpired)
            throw SessionError.noRefreshToken
        }

        do {
            let response = try await AuthAPI.refreshToken(refreshToken: refreshToken)
            try storeTokens(response.tokens)
            scheduleTokenRefresh(expiresAt: response.tokens.accessTokenExpiry)
        } catch {
            // Refresh failed - likely token is invalid
            logout(reason: .tokenExpired)
            throw SessionError.refreshFailed(underlying: error)
        }
    }

    // MARK: - Private Methods

    private func restoreSession() {
        // Check for existing tokens
        guard let _ = KeychainManager.shared.read(
            service: keychainService,
            account: "accessToken"
        ) else {
            authenticationState = .unauthenticated
            return
        }

        // Have tokens, attempt to load user profile
        authenticationState = .refreshing

        Task {
            do {
                // Validate token by fetching user profile
                try await refreshAccessToken()
                let user = try await AuthAPI.getCurrentUser()
                currentUser = user
                authenticationState = .authenticated
            } catch {
                // Token invalid, user needs to re-authenticate
                logout(reason: .tokenExpired)
            }
        }
    }

    private func storeTokens(_ tokens: AuthTokens) throws {
        // Store access token
        try KeychainManager.shared.save(
            tokens.accessToken,
            service: keychainService,
            account: "accessToken",
            accessibility: .afterFirstUnlock
        )

        // Store refresh token with higher security
        try KeychainManager.shared.save(
            tokens.refreshToken,
            service: keychainService,
            account: "refreshToken",
            accessibility: .whenUnlockedThisDeviceOnly
        )

        tokenExpirationDate = tokens.accessTokenExpiry
    }

    private func scheduleTokenRefresh(expiresAt: Date) {
        refreshTask?.cancel()

        let refreshInterval = max(
            expiresAt.timeIntervalSinceNow - tokenRefreshThreshold,
            60 // Minimum 1 minute
        )

        refreshTask = Task {
            try? await Task.sleep(nanoseconds: UInt64(refreshInterval * 1_000_000_000))

            guard !Task.isCancelled else { return }

            do {
                try await refreshAccessToken()
            } catch {
                // Refresh failed silently in background
                // Will be handled on next API call
            }
        }
    }

    private func setupNotifications() {
        // Handle app becoming active
        NotificationCenter.default.publisher(for: UIApplication.didBecomeActiveNotification)
            .sink { [weak self] _ in
                Task { @MainActor in
                    self?.checkTokenValidity()
                }
            }
            .store(in: &cancellables)

        // Handle remote logout push
        NotificationCenter.default.publisher(for: .forceLogoutReceived)
            .sink { [weak self] _ in
                Task { @MainActor in
                    self?.logout(reason: .serverForced)
                }
            }
            .store(in: &cancellables)
    }

    private func checkTokenValidity() {
        guard authenticationState == .authenticated else { return }

        // Check if token is about to expire
        if let expiryDate = tokenExpirationDate,
           expiryDate.timeIntervalSinceNow < tokenRefreshThreshold {
            Task {
                try? await refreshAccessToken()
            }
        }
    }

    private func performLogoutCleanup() {
        // Clear URL cache (cached API responses)
        URLCache.shared.removeAllCachedResponses()

        // Clear cookies
        if let cookies = HTTPCookieStorage.shared.cookies {
            for cookie in cookies {
                HTTPCookieStorage.shared.deleteCookie(cookie)
            }
        }

        // Clear user-specific UserDefaults
        let userSpecificKeys = ["userId", "userEmail", "userPreferences", "recentSearches"]
        userSpecificKeys.forEach { UserDefaults.standard.removeObject(forKey: $0) }

        // Clear user-specific files
        clearUserSpecificFiles()

        // Clear image cache
        ImageCache.shared.clearAll()

        // Reset any user-specific singletons
        // NotificationManager.shared.reset()
        // AnalyticsManager.shared.reset()
    }

    private func clearUserSpecificFiles() {
        let fileManager = FileManager.default

        // Clear Documents/UserData
        if let documentsURL = fileManager.urls(for: .documentDirectory, in: .userDomainMask).first {
            let userDataURL = documentsURL.appendingPathComponent("UserData")
            try? fileManager.removeItem(at: userDataURL)
        }

        // Clear Caches/UserContent
        if let cachesURL = fileManager.urls(for: .cachesDirectory, in: .userDomainMask).first {
            let userContentURL = cachesURL.appendingPathComponent("UserContent")
            try? fileManager.removeItem(at: userContentURL)
        }
    }
}

// MARK: - Notification Names

extension Notification.Name {
    static let userDidLogout = Notification.Name("userDidLogout")
    static let forceLogoutReceived = Notification.Name("forceLogoutReceived")
}

// MARK: - Session Errors

enum SessionError: LocalizedError {
    case noToken
    case noRefreshToken
    case refreshFailed(underlying: Error)
    case invalidToken

    var errorDescription: String? {
        switch self {
        case .noToken:
            return "No authentication token available"
        case .noRefreshToken:
            return "No refresh token available"
        case .refreshFailed(let error):
            return "Token refresh failed: \(error.localizedDescription)"
        case .invalidToken:
            return "Authentication token is invalid"
        }
    }
}
```

## Complete Keychain Manager

```swift
import Foundation
import Security

// MARK: - Keychain Manager

final class KeychainManager {

    // MARK: - Singleton

    static let shared = KeychainManager()
    private init() {}

    // MARK: - Accessibility Levels

    enum Accessibility {
        case whenUnlocked
        case afterFirstUnlock
        case whenUnlockedThisDeviceOnly
        case afterFirstUnlockThisDeviceOnly
        case whenPasscodeSetThisDeviceOnly

        var cfValue: CFString {
            switch self {
            case .whenUnlocked:
                return kSecAttrAccessibleWhenUnlocked
            case .afterFirstUnlock:
                return kSecAttrAccessibleAfterFirstUnlock
            case .whenUnlockedThisDeviceOnly:
                return kSecAttrAccessibleWhenUnlockedThisDeviceOnly
            case .afterFirstUnlockThisDeviceOnly:
                return kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly
            case .whenPasscodeSetThisDeviceOnly:
                return kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly
            }
        }
    }

    // MARK: - Save

    func save(
        _ value: String,
        service: String,
        account: String,
        accessibility: Accessibility = .afterFirstUnlock
    ) throws {
        guard let data = value.data(using: .utf8) else {
            throw KeychainError.encodingFailed
        }

        try save(data: data, service: service, account: account, accessibility: accessibility)
    }

    func save<T: Encodable>(
        _ value: T,
        service: String,
        account: String,
        accessibility: Accessibility = .afterFirstUnlock
    ) throws {
        let data = try JSONEncoder().encode(value)
        try save(data: data, service: service, account: account, accessibility: accessibility)
    }

    private func save(
        data: Data,
        service: String,
        account: String,
        accessibility: Accessibility
    ) throws {
        // Build query
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: account
        ]

        // Delete any existing item
        SecItemDelete(query as CFDictionary)

        // Build attributes for new item
        var attributes = query
        attributes[kSecValueData as String] = data
        attributes[kSecAttrAccessible as String] = accessibility.cfValue

        // Add new item
        let status = SecItemAdd(attributes as CFDictionary, nil)

        guard status == errSecSuccess else {
            throw KeychainError.saveFailed(status: status)
        }
    }

    // MARK: - Read

    func read(service: String, account: String) -> String? {
        guard let data = readData(service: service, account: account) else {
            return nil
        }
        return String(data: data, encoding: .utf8)
    }

    func read<T: Decodable>(_ type: T.Type, service: String, account: String) -> T? {
        guard let data = readData(service: service, account: account) else {
            return nil
        }
        return try? JSONDecoder().decode(type, from: data)
    }

    private func readData(service: String, account: String) -> Data? {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: account,
            kSecReturnData as String: true,
            kSecMatchLimit as String: kSecMatchLimitOne
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        guard status == errSecSuccess else {
            return nil
        }

        return result as? Data
    }

    // MARK: - Delete

    func delete(service: String, account: String) {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: account
        ]

        SecItemDelete(query as CFDictionary)
    }

    func deleteAll(service: String) {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service
        ]

        SecItemDelete(query as CFDictionary)
    }

    // MARK: - Exists

    func exists(service: String, account: String) -> Bool {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: account,
            kSecReturnData as String: false
        ]

        let status = SecItemCopyMatching(query as CFDictionary, nil)
        return status == errSecSuccess
    }

    // MARK: - Update

    func update(
        _ value: String,
        service: String,
        account: String
    ) throws {
        guard let data = value.data(using: .utf8) else {
            throw KeychainError.encodingFailed
        }

        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: service,
            kSecAttrAccount as String: account
        ]

        let attributes: [String: Any] = [
            kSecValueData as String: data
        ]

        let status = SecItemUpdate(query as CFDictionary, attributes as CFDictionary)

        guard status == errSecSuccess else {
            throw KeychainError.updateFailed(status: status)
        }
    }
}

// MARK: - Keychain Errors

enum KeychainError: LocalizedError {
    case encodingFailed
    case saveFailed(status: OSStatus)
    case readFailed(status: OSStatus)
    case updateFailed(status: OSStatus)
    case deleteFailed(status: OSStatus)
    case itemNotFound

    var errorDescription: String? {
        switch self {
        case .encodingFailed:
            return "Failed to encode data for Keychain"
        case .saveFailed(let status):
            return "Keychain save failed with status: \(status)"
        case .readFailed(let status):
            return "Keychain read failed with status: \(status)"
        case .updateFailed(let status):
            return "Keychain update failed with status: \(status)"
        case .deleteFailed(let status):
            return "Keychain delete failed with status: \(status)"
        case .itemNotFound:
            return "Keychain item not found"
        }
    }
}
```

## Auto-Refresh Network Client

```swift
import Foundation

// MARK: - Authenticated Network Client

actor AuthenticatedNetworkClient {

    private let sessionManager: SessionManager
    private let baseURL: URL
    private let session: URLSession

    private var isRefreshing = false
    private var pendingRequests: [CheckedContinuation<Data, Error>] = []

    init(
        baseURL: URL,
        sessionManager: SessionManager = .shared,
        session: URLSession = .shared
    ) {
        self.baseURL = baseURL
        self.sessionManager = sessionManager
        self.session = session
    }

    // MARK: - Request Methods

    func request<T: Decodable>(
        _ endpoint: Endpoint,
        responseType: T.Type
    ) async throws -> T {
        let data = try await performRequest(endpoint)
        return try JSONDecoder().decode(T.self, from: data)
    }

    func request(_ endpoint: Endpoint) async throws -> Data {
        return try await performRequest(endpoint)
    }

    // MARK: - Private Implementation

    private func performRequest(_ endpoint: Endpoint) async throws -> Data {
        // Build request
        var request = try endpoint.asURLRequest(baseURL: baseURL)

        // Add authentication header
        let token = try await sessionManager.getAccessToken()
        request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")

        // Execute request
        let (data, response) = try await session.data(for: request)

        guard let httpResponse = response as? HTTPURLResponse else {
            throw NetworkError.invalidResponse
        }

        // Handle 401 Unauthorized
        if httpResponse.statusCode == 401 {
            return try await handleUnauthorized(endpoint: endpoint)
        }

        // Handle other errors
        guard (200...299).contains(httpResponse.statusCode) else {
            throw NetworkError.httpError(statusCode: httpResponse.statusCode, data: data)
        }

        return data
    }

    private func handleUnauthorized(endpoint: Endpoint) async throws -> Data {
        // If already refreshing, wait for it
        if isRefreshing {
            return try await withCheckedThrowingContinuation { continuation in
                pendingRequests.append(continuation)
            }
        }

        // Start refresh
        isRefreshing = true

        do {
            try await sessionManager.refreshAccessToken()
            isRefreshing = false

            // Retry original request
            let data = try await performRequest(endpoint)

            // Resume pending requests
            for continuation in pendingRequests {
                continuation.resume(returning: data)
            }
            pendingRequests.removeAll()

            return data
        } catch {
            isRefreshing = false

            // Fail pending requests
            for continuation in pendingRequests {
                continuation.resume(throwing: error)
            }
            pendingRequests.removeAll()

            throw error
        }
    }
}

// MARK: - Endpoint Protocol

protocol Endpoint {
    var path: String { get }
    var method: HTTPMethod { get }
    var headers: [String: String]? { get }
    var body: Data? { get }
    var queryItems: [URLQueryItem]? { get }
}

extension Endpoint {
    func asURLRequest(baseURL: URL) throws -> URLRequest {
        var components = URLComponents(url: baseURL.appendingPathComponent(path), resolvingAgainstBaseURL: true)
        components?.queryItems = queryItems

        guard let url = components?.url else {
            throw NetworkError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = method.rawValue
        request.httpBody = body

        // Default headers
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.setValue("application/json", forHTTPHeaderField: "Accept")

        // Custom headers
        headers?.forEach { request.setValue($1, forHTTPHeaderField: $0) }

        return request
    }
}

enum HTTPMethod: String {
    case get = "GET"
    case post = "POST"
    case put = "PUT"
    case patch = "PATCH"
    case delete = "DELETE"
}

enum NetworkError: LocalizedError {
    case invalidURL
    case invalidResponse
    case httpError(statusCode: Int, data: Data)

    var errorDescription: String? {
        switch self {
        case .invalidURL:
            return "Invalid URL"
        case .invalidResponse:
            return "Invalid response"
        case .httpError(let statusCode, _):
            return "HTTP error: \(statusCode)"
        }
    }
}
```

## Multi-Account Support

```swift
import Foundation

// MARK: - Multi-Account Session Manager

@MainActor
final class MultiAccountSessionManager: ObservableObject {

    static let shared = MultiAccountSessionManager()

    @Published private(set) var accounts: [StoredAccount] = []
    @Published private(set) var activeAccount: StoredAccount?

    private let keychainService = "com.app.accounts"
    private let accountsKey = "storedAccounts"

    private init() {
        loadAccounts()
    }

    // MARK: - Account Management

    /// Add a new account after successful login
    func addAccount(_ account: StoredAccount, tokens: AuthTokens) throws {
        // Store tokens for this account
        try KeychainManager.shared.save(
            tokens.accessToken,
            service: keychainService,
            account: "\(account.id).accessToken"
        )

        try KeychainManager.shared.save(
            tokens.refreshToken,
            service: keychainService,
            account: "\(account.id).refreshToken"
        )

        // Add to accounts list
        if !accounts.contains(where: { $0.id == account.id }) {
            accounts.append(account)
            saveAccounts()
        }

        // Set as active
        activeAccount = account
        saveActiveAccountId(account.id)
    }

    /// Switch to a different account
    func switchTo(accountId: String) async throws {
        guard let account = accounts.first(where: { $0.id == accountId }) else {
            throw AccountError.accountNotFound
        }

        // Validate tokens exist for this account
        guard KeychainManager.shared.exists(
            service: keychainService,
            account: "\(account.id).accessToken"
        ) else {
            throw AccountError.tokensNotFound
        }

        activeAccount = account
        saveActiveAccountId(account.id)

        // Notify about account switch
        NotificationCenter.default.post(name: .accountDidSwitch, object: nil, userInfo: [
            "accountId": accountId
        ])
    }

    /// Remove an account
    func removeAccount(accountId: String) {
        // Clear tokens
        KeychainManager.shared.delete(service: keychainService, account: "\(accountId).accessToken")
        KeychainManager.shared.delete(service: keychainService, account: "\(accountId).refreshToken")

        // Remove from list
        accounts.removeAll { $0.id == accountId }
        saveAccounts()

        // If removing active account, switch to another
        if activeAccount?.id == accountId {
            activeAccount = accounts.first
            if let newActive = activeAccount {
                saveActiveAccountId(newActive.id)
            } else {
                clearActiveAccountId()
            }
        }
    }

    /// Get access token for active account
    func getAccessToken() -> String? {
        guard let accountId = activeAccount?.id else { return nil }
        return KeychainManager.shared.read(service: keychainService, account: "\(accountId).accessToken")
    }

    // MARK: - Private Methods

    private func loadAccounts() {
        // Load account list from UserDefaults (non-sensitive metadata)
        if let data = UserDefaults.standard.data(forKey: accountsKey),
           let accounts = try? JSONDecoder().decode([StoredAccount].self, from: data) {
            self.accounts = accounts
        }

        // Load active account
        if let activeId = UserDefaults.standard.string(forKey: "activeAccountId"),
           let account = accounts.first(where: { $0.id == activeId }) {
            activeAccount = account
        }
    }

    private func saveAccounts() {
        if let data = try? JSONEncoder().encode(accounts) {
            UserDefaults.standard.set(data, forKey: accountsKey)
        }
    }

    private func saveActiveAccountId(_ id: String) {
        UserDefaults.standard.set(id, forKey: "activeAccountId")
    }

    private func clearActiveAccountId() {
        UserDefaults.standard.removeObject(forKey: "activeAccountId")
    }
}

// MARK: - Stored Account

struct StoredAccount: Codable, Identifiable, Equatable {
    let id: String
    let email: String
    let displayName: String
    let avatarURL: URL?
    let provider: AuthProvider

    enum AuthProvider: String, Codable {
        case email
        case google
        case apple
    }
}

// MARK: - Account Errors

enum AccountError: LocalizedError {
    case accountNotFound
    case tokensNotFound
    case switchFailed

    var errorDescription: String? {
        switch self {
        case .accountNotFound:
            return "Account not found"
        case .tokensNotFound:
            return "Authentication tokens not found for this account"
        case .switchFailed:
            return "Failed to switch accounts"
        }
    }
}

// MARK: - Notifications

extension Notification.Name {
    static let accountDidSwitch = Notification.Name("accountDidSwitch")
}
```

## Supporting Types

```swift
// MARK: - Auth API (Example)

enum AuthAPI {

    static func login(email: String, password: String) async throws -> LoginResponse {
        // API implementation
        fatalError("Implement actual API call")
    }

    static func exchangeOAuthCode(provider: OAuthProvider, code: String) async throws -> LoginResponse {
        // API implementation
        fatalError("Implement actual API call")
    }

    static func refreshToken(refreshToken: String) async throws -> TokenResponse {
        // API implementation
        fatalError("Implement actual API call")
    }

    static func getCurrentUser() async throws -> User {
        // API implementation
        fatalError("Implement actual API call")
    }

    static func logout() async throws {
        // API implementation - notify server of logout
        fatalError("Implement actual API call")
    }
}

// MARK: - Response Types

struct LoginResponse {
    let user: User
    let tokens: AuthTokens
}

struct TokenResponse {
    let tokens: AuthTokens
}

struct AuthTokens {
    let accessToken: String
    let refreshToken: String
    let accessTokenExpiry: Date
}

struct User: Codable, Identifiable {
    let id: String
    let email: String
    let displayName: String
    let avatarURL: URL?
}

enum OAuthProvider: String {
    case google
    case apple
    case facebook
}

// MARK: - Image Cache Placeholder

enum ImageCache {
    static let shared = ImageCacheImpl()
}

class ImageCacheImpl {
    func clearAll() {
        // Clear image cache implementation
    }
}
```
