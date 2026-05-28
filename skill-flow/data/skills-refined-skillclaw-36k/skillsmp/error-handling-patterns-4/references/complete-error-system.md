# Error Handling — Complete Error System

> **Loading Trigger**: Load when designing app-wide error handling architecture or implementing error recovery strategies.

---

## Complete Error Type Hierarchy

```swift
import Foundation

// MARK: - Base App Error

/// Base error type for the entire application
/// All feature-specific errors should conform to this
protocol AppError: LocalizedError {
    var errorCode: String { get }
    var isRetryable: Bool { get }
    var underlyingError: Error? { get }
    var analyticsProperties: [String: Any] { get }
}

extension AppError {
    var underlyingError: Error? { nil }

    var analyticsProperties: [String: Any] {
        [
            "error_code": errorCode,
            "error_description": errorDescription ?? "Unknown",
            "is_retryable": isRetryable
        ]
    }
}

// MARK: - Network Errors

enum NetworkError: AppError {
    case noConnection
    case timeout
    case serverError(statusCode: Int, message: String?)
    case unauthorized
    case forbidden
    case notFound
    case rateLimited(retryAfter: TimeInterval?)
    case invalidResponse
    case decodingFailed(type: String, underlying: Error)
    case encodingFailed(type: String, underlying: Error)
    case cancelled
    case unknown(underlying: Error)

    var errorCode: String {
        switch self {
        case .noConnection: return "NET_001"
        case .timeout: return "NET_002"
        case .serverError(let code, _): return "NET_5\(code)"
        case .unauthorized: return "NET_401"
        case .forbidden: return "NET_403"
        case .notFound: return "NET_404"
        case .rateLimited: return "NET_429"
        case .invalidResponse: return "NET_003"
        case .decodingFailed: return "NET_004"
        case .encodingFailed: return "NET_005"
        case .cancelled: return "NET_006"
        case .unknown: return "NET_000"
        }
    }

    var errorDescription: String? {
        switch self {
        case .noConnection:
            return "No internet connection"
        case .timeout:
            return "Request timed out"
        case .serverError(_, let message):
            return message ?? "Server error occurred"
        case .unauthorized:
            return "Session expired"
        case .forbidden:
            return "Access denied"
        case .notFound:
            return "Resource not found"
        case .rateLimited:
            return "Too many requests"
        case .invalidResponse:
            return "Invalid server response"
        case .decodingFailed:
            return "Failed to process server response"
        case .encodingFailed:
            return "Failed to send request"
        case .cancelled:
            return nil // Cancellation shouldn't show error
        case .unknown:
            return "An unexpected error occurred"
        }
    }

    var recoverySuggestion: String? {
        switch self {
        case .noConnection:
            return "Please check your network settings and try again"
        case .timeout:
            return "Please try again"
        case .serverError:
            return "Please try again later"
        case .unauthorized:
            return "Please log in again"
        case .forbidden:
            return "Contact support if you believe this is an error"
        case .notFound:
            return "The item may have been removed"
        case .rateLimited(let retryAfter):
            if let seconds = retryAfter {
                return "Please wait \(Int(seconds)) seconds before trying again"
            }
            return "Please wait a moment before trying again"
        case .invalidResponse, .decodingFailed, .encodingFailed:
            return "Please try again or contact support"
        case .cancelled:
            return nil
        case .unknown:
            return "Please try again"
        }
    }

    var isRetryable: Bool {
        switch self {
        case .noConnection, .timeout, .serverError, .rateLimited:
            return true
        case .unauthorized, .forbidden, .notFound,
             .invalidResponse, .decodingFailed, .encodingFailed,
             .cancelled, .unknown:
            return false
        }
    }

    var underlyingError: Error? {
        switch self {
        case .decodingFailed(_, let error),
             .encodingFailed(_, let error),
             .unknown(let error):
            return error
        default:
            return nil
        }
    }
}

// MARK: - Authentication Errors

enum AuthError: AppError {
    case invalidCredentials
    case accountLocked(unlockTime: Date?)
    case accountDisabled
    case emailNotVerified
    case passwordExpired
    case twoFactorRequired(methods: [TwoFactorMethod])
    case twoFactorFailed
    case sessionExpired
    case tokenRefreshFailed
    case biometricFailed(reason: String)
    case socialLoginFailed(provider: String, reason: String)

    enum TwoFactorMethod: String, Codable {
        case sms, email, authenticator, backup
    }

    var errorCode: String {
        switch self {
        case .invalidCredentials: return "AUTH_001"
        case .accountLocked: return "AUTH_002"
        case .accountDisabled: return "AUTH_003"
        case .emailNotVerified: return "AUTH_004"
        case .passwordExpired: return "AUTH_005"
        case .twoFactorRequired: return "AUTH_006"
        case .twoFactorFailed: return "AUTH_007"
        case .sessionExpired: return "AUTH_008"
        case .tokenRefreshFailed: return "AUTH_009"
        case .biometricFailed: return "AUTH_010"
        case .socialLoginFailed: return "AUTH_011"
        }
    }

    var errorDescription: String? {
        switch self {
        case .invalidCredentials:
            return "Invalid email or password"
        case .accountLocked(let unlockTime):
            if let time = unlockTime {
                let formatter = RelativeDateTimeFormatter()
                return "Account locked. Try again \(formatter.localizedString(for: time, relativeTo: Date()))"
            }
            return "Account locked"
        case .accountDisabled:
            return "Account has been disabled"
        case .emailNotVerified:
            return "Please verify your email address"
        case .passwordExpired:
            return "Your password has expired"
        case .twoFactorRequired:
            return "Two-factor authentication required"
        case .twoFactorFailed:
            return "Invalid verification code"
        case .sessionExpired:
            return "Your session has expired"
        case .tokenRefreshFailed:
            return "Unable to refresh session"
        case .biometricFailed(let reason):
            return "Biometric authentication failed: \(reason)"
        case .socialLoginFailed(let provider, _):
            return "\(provider) login failed"
        }
    }

    var recoverySuggestion: String? {
        switch self {
        case .invalidCredentials:
            return "Please check your credentials and try again"
        case .accountLocked:
            return "Contact support if you need immediate access"
        case .accountDisabled:
            return "Contact support for assistance"
        case .emailNotVerified:
            return "Check your email for the verification link"
        case .passwordExpired:
            return "Please reset your password"
        case .twoFactorRequired:
            return "Enter the code from your authenticator app"
        case .twoFactorFailed:
            return "Please check the code and try again"
        case .sessionExpired, .tokenRefreshFailed:
            return "Please log in again"
        case .biometricFailed:
            return "Try again or use your password"
        case .socialLoginFailed:
            return "Please try again or use a different login method"
        }
    }

    var isRetryable: Bool {
        switch self {
        case .invalidCredentials, .twoFactorFailed, .biometricFailed, .socialLoginFailed:
            return true
        case .accountLocked, .accountDisabled, .emailNotVerified, .passwordExpired,
             .twoFactorRequired, .sessionExpired, .tokenRefreshFailed:
            return false
        }
    }
}

// MARK: - Validation Errors

struct ValidationError: AppError {
    let field: String
    let rule: ValidationRule
    let value: String?

    enum ValidationRule: String {
        case required
        case email
        case minLength
        case maxLength
        case pattern
        case mismatch
        case invalid
    }

    var errorCode: String {
        "VAL_\(field.uppercased())_\(rule.rawValue.uppercased())"
    }

    var errorDescription: String? {
        switch rule {
        case .required:
            return "\(field.capitalized) is required"
        case .email:
            return "Please enter a valid email address"
        case .minLength:
            return "\(field.capitalized) is too short"
        case .maxLength:
            return "\(field.capitalized) is too long"
        case .pattern:
            return "\(field.capitalized) format is invalid"
        case .mismatch:
            return "\(field.capitalized) does not match"
        case .invalid:
            return "\(field.capitalized) is invalid"
        }
    }

    var isRetryable: Bool { true }
}

// MARK: - Business Logic Errors

enum BusinessError: AppError {
    case insufficientFunds(available: Decimal, required: Decimal)
    case outOfStock(productName: String)
    case cartEmpty
    case orderNotFound(id: String)
    case paymentDeclined(reason: String)
    case couponExpired
    case couponInvalid
    case addressNotServiceable
    case minimumOrderNotMet(minimum: Decimal, current: Decimal)

    var errorCode: String {
        switch self {
        case .insufficientFunds: return "BIZ_001"
        case .outOfStock: return "BIZ_002"
        case .cartEmpty: return "BIZ_003"
        case .orderNotFound: return "BIZ_004"
        case .paymentDeclined: return "BIZ_005"
        case .couponExpired: return "BIZ_006"
        case .couponInvalid: return "BIZ_007"
        case .addressNotServiceable: return "BIZ_008"
        case .minimumOrderNotMet: return "BIZ_009"
        }
    }

    var errorDescription: String? {
        switch self {
        case .insufficientFunds(let available, let required):
            return "Insufficient funds. Available: $\(available), Required: $\(required)"
        case .outOfStock(let name):
            return "\(name) is out of stock"
        case .cartEmpty:
            return "Your cart is empty"
        case .orderNotFound:
            return "Order not found"
        case .paymentDeclined(let reason):
            return "Payment declined: \(reason)"
        case .couponExpired:
            return "This coupon has expired"
        case .couponInvalid:
            return "Invalid coupon code"
        case .addressNotServiceable:
            return "We don't deliver to this address"
        case .minimumOrderNotMet(let minimum, let current):
            return "Minimum order is $\(minimum). Current: $\(current)"
        }
    }

    var isRetryable: Bool {
        switch self {
        case .paymentDeclined:
            return true
        default:
            return false
        }
    }
}
```

---

## Error Handler Service

```swift
// MARK: - Error Handler Protocol

@MainActor
protocol ErrorHandling {
    func handle(_ error: Error, context: ErrorContext)
    func shouldShowToUser(_ error: Error) -> Bool
    func userFacingMessage(for error: Error) -> String
}

struct ErrorContext {
    let source: String
    let action: String
    let userId: String?
    let additionalInfo: [String: Any]

    init(
        source: String,
        action: String,
        userId: String? = nil,
        additionalInfo: [String: Any] = [:]
    ) {
        self.source = source
        self.action = action
        self.userId = userId
        self.additionalInfo = additionalInfo
    }
}

// MARK: - Error Handler Implementation

@MainActor
final class ErrorHandler: ErrorHandling, ObservableObject {
    @Published private(set) var currentError: PresentableError?

    private let analyticsService: AnalyticsServiceProtocol
    private let crashReporter: CrashReporting
    private let logger: Logger

    struct PresentableError: Identifiable {
        let id = UUID()
        let title: String
        let message: String
        let isRetryable: Bool
        let retryAction: (() -> Void)?
        let dismissAction: (() -> Void)?
    }

    init(
        analyticsService: AnalyticsServiceProtocol,
        crashReporter: CrashReporting,
        logger: Logger = Logger(subsystem: "com.app", category: "errors")
    ) {
        self.analyticsService = analyticsService
        self.crashReporter = crashReporter
        self.logger = logger
    }

    func handle(_ error: Error, context: ErrorContext) {
        // Log
        logError(error, context: context)

        // Track analytics
        trackError(error, context: context)

        // Report to crash service (non-fatal)
        reportError(error, context: context)

        // Present to user if needed
        if shouldShowToUser(error) {
            presentError(error, context: context)
        }
    }

    func shouldShowToUser(_ error: Error) -> Bool {
        // Never show cancellation errors
        if error is CancellationError { return false }

        // Check for network cancellation
        if let networkError = error as? NetworkError,
           case .cancelled = networkError {
            return false
        }

        return true
    }

    func userFacingMessage(for error: Error) -> String {
        if let appError = error as? AppError {
            return appError.errorDescription ?? "An unexpected error occurred"
        }

        // Map common system errors
        let nsError = error as NSError
        switch (nsError.domain, nsError.code) {
        case (NSURLErrorDomain, NSURLErrorNotConnectedToInternet):
            return "No internet connection"
        case (NSURLErrorDomain, NSURLErrorTimedOut):
            return "Request timed out"
        case (NSURLErrorDomain, NSURLErrorCancelled):
            return "" // Don't show
        default:
            return "An unexpected error occurred"
        }
    }

    // MARK: - Private

    private func logError(_ error: Error, context: ErrorContext) {
        let errorInfo: [String: Any] = [
            "source": context.source,
            "action": context.action,
            "error": String(describing: error),
            "userId": context.userId ?? "anonymous"
        ]

        logger.error("Error: \(error.localizedDescription) - Context: \(errorInfo)")
    }

    private func trackError(_ error: Error, context: ErrorContext) {
        var properties: [String: Any] = [
            "source": context.source,
            "action": context.action
        ]

        if let appError = error as? AppError {
            properties.merge(appError.analyticsProperties) { _, new in new }
        }

        analyticsService.track(event: .error(properties: properties))
    }

    private func reportError(_ error: Error, context: ErrorContext) {
        var userInfo: [String: Any] = [
            "source": context.source,
            "action": context.action
        ]
        userInfo.merge(context.additionalInfo) { _, new in new }

        crashReporter.recordNonFatal(error, userInfo: userInfo)
    }

    private func presentError(_ error: Error, context: ErrorContext) {
        let message = userFacingMessage(for: error)
        guard !message.isEmpty else { return }

        let isRetryable = (error as? AppError)?.isRetryable ?? false

        currentError = PresentableError(
            title: "Error",
            message: message,
            isRetryable: isRetryable,
            retryAction: nil,
            dismissAction: { [weak self] in
                self?.currentError = nil
            }
        )
    }

    func dismiss() {
        currentError = nil
    }
}
```

---

## Retry Logic Implementation

```swift
// MARK: - Retry Configuration

struct RetryConfiguration {
    let maxAttempts: Int
    let initialDelay: Duration
    let maxDelay: Duration
    let multiplier: Double
    let jitter: Bool

    static let `default` = RetryConfiguration(
        maxAttempts: 3,
        initialDelay: .seconds(1),
        maxDelay: .seconds(30),
        multiplier: 2.0,
        jitter: true
    )

    static let aggressive = RetryConfiguration(
        maxAttempts: 5,
        initialDelay: .milliseconds(500),
        maxDelay: .seconds(60),
        multiplier: 2.0,
        jitter: true
    )

    static let conservative = RetryConfiguration(
        maxAttempts: 2,
        initialDelay: .seconds(2),
        maxDelay: .seconds(10),
        multiplier: 1.5,
        jitter: false
    )
}

// MARK: - Retry with Backoff

func withRetry<T>(
    configuration: RetryConfiguration = .default,
    shouldRetry: @escaping (Error) -> Bool = { ($0 as? AppError)?.isRetryable ?? false },
    operation: () async throws -> T
) async throws -> T {
    var currentDelay = configuration.initialDelay
    var lastError: Error?

    for attempt in 1...configuration.maxAttempts {
        do {
            return try await operation()
        } catch {
            lastError = error

            // Check if this is the last attempt
            guard attempt < configuration.maxAttempts else { break }

            // Check if error is retryable
            guard shouldRetry(error) else { throw error }

            // Check for task cancellation
            try Task.checkCancellation()

            // Calculate delay with optional jitter
            var delay = currentDelay
            if configuration.jitter {
                let jitterRange = Double(delay.components.seconds) * 0.2
                let jitter = Duration.milliseconds(Int.random(in: 0...Int(jitterRange * 1000)))
                delay += jitter
            }

            // Wait before retry
            try await Task.sleep(for: delay)

            // Increase delay for next attempt (with cap)
            let nextDelay = Duration.seconds(
                Double(currentDelay.components.seconds) * configuration.multiplier
            )
            currentDelay = min(nextDelay, configuration.maxDelay)
        }
    }

    throw lastError ?? RetryError.maxAttemptsExceeded
}

enum RetryError: Error {
    case maxAttemptsExceeded
}

// MARK: - Usage Example

class DataService {
    func fetchWithRetry() async throws -> Data {
        try await withRetry(configuration: .default) {
            try await networkManager.request(endpoint)
        }
    }

    func fetchWithCustomRetry() async throws -> Data {
        try await withRetry(
            configuration: .aggressive,
            shouldRetry: { error in
                // Custom retry logic
                if let networkError = error as? NetworkError {
                    switch networkError {
                    case .timeout, .noConnection, .serverError:
                        return true
                    default:
                        return false
                    }
                }
                return false
            }
        ) {
            try await networkManager.request(endpoint)
        }
    }
}
```

---

## SwiftUI Error Presentation

```swift
// MARK: - Error Alert Modifier

struct ErrorAlertModifier: ViewModifier {
    @Binding var error: Error?
    let onRetry: (() -> Void)?

    func body(content: Content) -> some View {
        content
            .alert(
                "Error",
                isPresented: Binding(
                    get: { error != nil },
                    set: { if !$0 { error = nil } }
                )
            ) {
                if let retryable = (error as? AppError)?.isRetryable, retryable,
                   let retry = onRetry {
                    Button("Retry", action: retry)
                }
                Button("OK", role: .cancel) { error = nil }
            } message: {
                if let error = error {
                    Text(errorMessage(for: error))
                }
            }
    }

    private func errorMessage(for error: Error) -> String {
        (error as? AppError)?.errorDescription ?? error.localizedDescription
    }
}

extension View {
    func errorAlert(_ error: Binding<Error?>, onRetry: (() -> Void)? = nil) -> some View {
        modifier(ErrorAlertModifier(error: error, onRetry: onRetry))
    }
}

// MARK: - Error Banner View

struct ErrorBannerView: View {
    let error: AppError
    let onDismiss: () -> Void
    let onRetry: (() -> Void)?

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: "exclamationmark.triangle.fill")
                .foregroundColor(.white)

            VStack(alignment: .leading, spacing: 2) {
                Text(error.errorDescription ?? "Error")
                    .font(.subheadline.weight(.semibold))
                    .foregroundColor(.white)

                if let suggestion = error.recoverySuggestion {
                    Text(suggestion)
                        .font(.caption)
                        .foregroundColor(.white.opacity(0.8))
                }
            }

            Spacer()

            if error.isRetryable, let retry = onRetry {
                Button("Retry") {
                    retry()
                }
                .buttonStyle(.bordered)
                .tint(.white)
            }

            Button {
                onDismiss()
            } label: {
                Image(systemName: "xmark")
                    .foregroundColor(.white)
            }
        }
        .padding()
        .background(Color.red)
        .cornerRadius(12)
        .shadow(radius: 4)
        .padding()
    }
}

// MARK: - Full Screen Error View

struct FullScreenErrorView: View {
    let error: AppError
    let onRetry: (() -> Void)?
    let onDismiss: (() -> Void)?

    var body: some View {
        VStack(spacing: 24) {
            Spacer()

            Image(systemName: "exclamationmark.triangle")
                .font(.system(size: 64))
                .foregroundColor(.red)

            Text(error.errorDescription ?? "Something went wrong")
                .font(.title2.weight(.semibold))
                .multilineTextAlignment(.center)

            if let suggestion = error.recoverySuggestion {
                Text(suggestion)
                    .font(.body)
                    .foregroundColor(.secondary)
                    .multilineTextAlignment(.center)
            }

            VStack(spacing: 12) {
                if error.isRetryable, let retry = onRetry {
                    Button("Try Again") {
                        retry()
                    }
                    .buttonStyle(.borderedProminent)
                }

                if let dismiss = onDismiss {
                    Button("Go Back") {
                        dismiss()
                    }
                    .buttonStyle(.bordered)
                }
            }

            Spacer()
        }
        .padding()
    }
}
```
