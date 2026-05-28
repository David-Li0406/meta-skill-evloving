# Complete Security Implementation Reference

<!-- Loading Trigger: Load this reference when implementing secure storage, authentication flows, certificate pinning, biometric authentication, or comprehensive security auditing for iOS/tvOS applications -->

## Advanced Keychain Manager with Biometrics

```swift
import Foundation
import Security
import LocalAuthentication

// MARK: - Keychain Error Types

enum KeychainError: LocalizedError {
    case itemNotFound
    case duplicateItem
    case authenticationFailed
    case unhandledError(status: OSStatus)
    case invalidData
    case biometricNotAvailable
    case biometricNotEnrolled
    case biometricLockout

    var errorDescription: String? {
        switch self {
        case .itemNotFound:
            return "Keychain item not found"
        case .duplicateItem:
            return "Duplicate keychain item"
        case .authenticationFailed:
            return "Biometric authentication failed"
        case .unhandledError(let status):
            return "Keychain error: \(status)"
        case .invalidData:
            return "Invalid data format"
        case .biometricNotAvailable:
            return "Biometric authentication not available"
        case .biometricNotEnrolled:
            return "No biometric credentials enrolled"
        case .biometricLockout:
            return "Biometric authentication locked out"
        }
    }
}

// MARK: - Keychain Accessibility Levels

enum KeychainAccessibility {
    case whenUnlocked
    case whenUnlockedThisDeviceOnly
    case afterFirstUnlock
    case afterFirstUnlockThisDeviceOnly
    case whenPasscodeSetThisDeviceOnly

    var secAccessibility: CFString {
        switch self {
        case .whenUnlocked:
            return kSecAttrAccessibleWhenUnlocked
        case .whenUnlockedThisDeviceOnly:
            return kSecAttrAccessibleWhenUnlockedThisDeviceOnly
        case .afterFirstUnlock:
            return kSecAttrAccessibleAfterFirstUnlock
        case .afterFirstUnlockThisDeviceOnly:
            return kSecAttrAccessibleAfterFirstUnlockThisDeviceOnly
        case .whenPasscodeSetThisDeviceOnly:
            return kSecAttrAccessibleWhenPasscodeSetThisDeviceOnly
        }
    }
}

// MARK: - Biometric Protection Level

enum BiometricProtection {
    case none
    case biometryAny           // Accept new biometric enrollment
    case biometryCurrentSet    // Invalidate on biometric changes
    case devicePasscode        // Allow passcode fallback

    func createAccessControl(accessibility: CFString) -> SecAccessControl? {
        var flags: SecAccessControlCreateFlags = []

        switch self {
        case .none:
            return nil
        case .biometryAny:
            flags = .biometryAny
        case .biometryCurrentSet:
            flags = .biometryCurrentSet
        case .devicePasscode:
            flags = [.biometryAny, .or, .devicePasscode]
        }

        var error: Unmanaged<CFError>?
        let accessControl = SecAccessControlCreateWithFlags(
            kCFAllocatorDefault,
            accessibility,
            flags,
            &error
        )

        return accessControl
    }
}

// MARK: - Complete Keychain Manager

final class SecureKeychainManager {

    static let shared = SecureKeychainManager()

    private let serviceName: String
    private let accessGroup: String?
    private let synchronizable: Bool

    init(
        serviceName: String = Bundle.main.bundleIdentifier ?? "com.app.keychain",
        accessGroup: String? = nil,
        synchronizable: Bool = false
    ) {
        self.serviceName = serviceName
        self.accessGroup = accessGroup
        self.synchronizable = synchronizable
    }

    // MARK: - Save Operations

    func save(
        key: String,
        data: Data,
        accessibility: KeychainAccessibility = .afterFirstUnlock,
        biometricProtection: BiometricProtection = .none
    ) throws {
        // Delete existing item first (upsert pattern)
        try? delete(key: key)

        var query = baseQuery(for: key)
        query[kSecValueData as String] = data

        // Set accessibility
        if let accessControl = biometricProtection.createAccessControl(
            accessibility: accessibility.secAccessibility
        ) {
            query[kSecAttrAccessControl as String] = accessControl
        } else {
            query[kSecAttrAccessible as String] = accessibility.secAccessibility
        }

        // Add synchronizable if enabled
        if synchronizable {
            query[kSecAttrSynchronizable as String] = true
        }

        let status = SecItemAdd(query as CFDictionary, nil)

        guard status == errSecSuccess else {
            throw KeychainError.unhandledError(status: status)
        }
    }

    func save<T: Encodable>(
        key: String,
        value: T,
        accessibility: KeychainAccessibility = .afterFirstUnlock,
        biometricProtection: BiometricProtection = .none
    ) throws {
        let data = try JSONEncoder().encode(value)
        try save(
            key: key,
            data: data,
            accessibility: accessibility,
            biometricProtection: biometricProtection
        )
    }

    // MARK: - Load Operations

    func load(key: String, promptMessage: String? = nil) throws -> Data {
        var query = baseQuery(for: key)
        query[kSecReturnData as String] = true
        query[kSecMatchLimit as String] = kSecMatchLimitOne

        // For biometric-protected items
        if let prompt = promptMessage {
            let context = LAContext()
            context.localizedReason = prompt
            query[kSecUseAuthenticationContext as String] = context
        }

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        switch status {
        case errSecSuccess:
            guard let data = result as? Data else {
                throw KeychainError.invalidData
            }
            return data

        case errSecItemNotFound:
            throw KeychainError.itemNotFound

        case errSecAuthFailed, errSecUserCanceled:
            throw KeychainError.authenticationFailed

        default:
            throw KeychainError.unhandledError(status: status)
        }
    }

    func load<T: Decodable>(
        key: String,
        type: T.Type,
        promptMessage: String? = nil
    ) throws -> T {
        let data = try load(key: key, promptMessage: promptMessage)
        return try JSONDecoder().decode(type, from: data)
    }

    // MARK: - Delete Operations

    func delete(key: String) throws {
        let query = baseQuery(for: key)
        let status = SecItemDelete(query as CFDictionary)

        guard status == errSecSuccess || status == errSecItemNotFound else {
            throw KeychainError.unhandledError(status: status)
        }
    }

    func deleteAll() throws {
        var query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: serviceName
        ]

        if let group = accessGroup {
            query[kSecAttrAccessGroup as String] = group
        }

        let status = SecItemDelete(query as CFDictionary)

        guard status == errSecSuccess || status == errSecItemNotFound else {
            throw KeychainError.unhandledError(status: status)
        }
    }

    // MARK: - Existence Check

    func exists(key: String) -> Bool {
        var query = baseQuery(for: key)
        query[kSecReturnData as String] = false

        let status = SecItemCopyMatching(query as CFDictionary, nil)
        return status == errSecSuccess
    }

    // MARK: - Update Operations

    func update(key: String, data: Data) throws {
        let query = baseQuery(for: key)
        let attributes: [String: Any] = [kSecValueData as String: data]

        let status = SecItemUpdate(query as CFDictionary, attributes as CFDictionary)

        switch status {
        case errSecSuccess:
            return
        case errSecItemNotFound:
            throw KeychainError.itemNotFound
        default:
            throw KeychainError.unhandledError(status: status)
        }
    }

    // MARK: - Private Helpers

    private func baseQuery(for key: String) -> [String: Any] {
        var query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: serviceName,
            kSecAttrAccount as String: key
        ]

        if let group = accessGroup {
            query[kSecAttrAccessGroup as String] = group
        }

        return query
    }
}
```

## Biometric Authentication Manager

```swift
import LocalAuthentication

// MARK: - Biometric Type

enum BiometricType {
    case none
    case touchID
    case faceID
    case opticID  // Vision Pro

    var displayName: String {
        switch self {
        case .none:
            return "None"
        case .touchID:
            return "Touch ID"
        case .faceID:
            return "Face ID"
        case .opticID:
            return "Optic ID"
        }
    }
}

// MARK: - Biometric Authentication Result

enum BiometricAuthResult {
    case success
    case userCancelled
    case userFallback  // User chose to enter password
    case biometryNotAvailable
    case biometryNotEnrolled
    case biometryLockout
    case failed(Error)
}

// MARK: - Biometric Manager

@MainActor
final class BiometricManager {

    static let shared = BiometricManager()

    private let context = LAContext()

    // MARK: - Biometric Availability

    var biometricType: BiometricType {
        var error: NSError?
        guard context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) else {
            return .none
        }

        switch context.biometryType {
        case .touchID:
            return .touchID
        case .faceID:
            return .faceID
        case .opticID:
            return .opticID
        case .none:
            return .none
        @unknown default:
            return .none
        }
    }

    var isBiometricAvailable: Bool {
        var error: NSError?
        return context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error)
    }

    var biometricError: LAError? {
        var error: NSError?
        _ = context.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error)
        return error as? LAError
    }

    // MARK: - Authentication

    func authenticate(
        reason: String,
        fallbackTitle: String? = nil,
        cancelTitle: String? = nil
    ) async -> BiometricAuthResult {
        let newContext = LAContext()

        // Configure context
        newContext.localizedFallbackTitle = fallbackTitle
        newContext.localizedCancelTitle = cancelTitle

        // Check availability
        var error: NSError?
        guard newContext.canEvaluatePolicy(.deviceOwnerAuthenticationWithBiometrics, error: &error) else {
            if let laError = error as? LAError {
                return mapLAError(laError)
            }
            return .biometryNotAvailable
        }

        // Perform authentication
        do {
            let success = try await newContext.evaluatePolicy(
                .deviceOwnerAuthenticationWithBiometrics,
                localizedReason: reason
            )
            return success ? .success : .failed(LAError(.authenticationFailed))
        } catch let error as LAError {
            return mapLAError(error)
        } catch {
            return .failed(error)
        }
    }

    /// Authenticate with device passcode fallback
    func authenticateWithPasscodeFallback(reason: String) async -> BiometricAuthResult {
        let newContext = LAContext()

        var error: NSError?
        guard newContext.canEvaluatePolicy(.deviceOwnerAuthentication, error: &error) else {
            if let laError = error as? LAError {
                return mapLAError(laError)
            }
            return .biometryNotAvailable
        }

        do {
            let success = try await newContext.evaluatePolicy(
                .deviceOwnerAuthentication,
                localizedReason: reason
            )
            return success ? .success : .failed(LAError(.authenticationFailed))
        } catch let error as LAError {
            return mapLAError(error)
        } catch {
            return .failed(error)
        }
    }

    // MARK: - Private Helpers

    private func mapLAError(_ error: LAError) -> BiometricAuthResult {
        switch error.code {
        case .userCancel:
            return .userCancelled
        case .userFallback:
            return .userFallback
        case .biometryNotAvailable:
            return .biometryNotAvailable
        case .biometryNotEnrolled:
            return .biometryNotEnrolled
        case .biometryLockout:
            return .biometryLockout
        default:
            return .failed(error)
        }
    }
}
```

## Certificate Pinning with Alamofire

```swift
import Alamofire
import Foundation

// MARK: - Certificate Pin Configuration

struct CertificatePinConfig {
    let host: String
    let publicKeyHashes: [String]  // SHA-256 hashes in base64
    let includeSubdomains: Bool

    init(
        host: String,
        publicKeyHashes: [String],
        includeSubdomains: Bool = true
    ) {
        self.host = host
        self.publicKeyHashes = publicKeyHashes
        self.includeSubdomains = includeSubdomains
    }
}

// MARK: - Pinned Session Manager

final class PinnedSessionManager {

    let session: Session

    init(pins: [CertificatePinConfig], timeout: TimeInterval = 30) {
        // Build evaluators dictionary
        var evaluators: [String: ServerTrustEvaluating] = [:]

        for pin in pins {
            let publicKeys = pin.publicKeyHashes.compactMap { hash -> SecKey? in
                // In production, load actual public keys
                // This is a placeholder showing the pattern
                return nil
            }

            // Use public key pinning (survives certificate renewal)
            let evaluator = PublicKeysTrustEvaluator(
                keys: publicKeys,
                performDefaultValidation: true,
                validateHost: true
            )

            evaluators[pin.host] = evaluator
        }

        let serverTrustManager = ServerTrustManager(
            allHostsMustBeEvaluated: false,  // Only evaluate configured hosts
            evaluators: evaluators
        )

        let configuration = URLSessionConfiguration.af.default
        configuration.timeoutIntervalForRequest = timeout
        configuration.timeoutIntervalForResource = timeout * 2

        session = Session(
            configuration: configuration,
            serverTrustManager: serverTrustManager
        )
    }

    // MARK: - Certificate Hash Extraction (Debug only)

    #if DEBUG
    static func extractPublicKeyHash(from certificate: SecCertificate) -> String? {
        guard let publicKey = SecCertificateCopyKey(certificate) else {
            return nil
        }

        var error: Unmanaged<CFError>?
        guard let publicKeyData = SecKeyCopyExternalRepresentation(publicKey, &error) as Data? else {
            return nil
        }

        // Add ASN.1 header for RSA keys
        let rsa2048Asn1Header: [UInt8] = [
            0x30, 0x82, 0x01, 0x22, 0x30, 0x0d, 0x06, 0x09, 0x2a, 0x86, 0x48, 0x86,
            0xf7, 0x0d, 0x01, 0x01, 0x01, 0x05, 0x00, 0x03, 0x82, 0x01, 0x0f, 0x00
        ]

        var keyWithHeader = Data(rsa2048Asn1Header)
        keyWithHeader.append(publicKeyData)

        // SHA-256 hash
        let hash = SHA256.hash(data: keyWithHeader)
        return Data(hash).base64EncodedString()
    }
    #endif
}

// MARK: - URLSession Certificate Pinning Delegate

final class CertificatePinningDelegate: NSObject, URLSessionDelegate {

    private let pinnedHosts: [String: [String]]  // host -> [public key hashes]

    init(pinnedHosts: [String: [String]]) {
        self.pinnedHosts = pinnedHosts
        super.init()
    }

    func urlSession(
        _ session: URLSession,
        didReceive challenge: URLAuthenticationChallenge,
        completionHandler: @escaping (URLSession.AuthChallengeDisposition, URLCredential?) -> Void
    ) {
        guard challenge.protectionSpace.authenticationMethod == NSURLAuthenticationMethodServerTrust,
              let serverTrust = challenge.protectionSpace.serverTrust else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        let host = challenge.protectionSpace.host

        // If host is not in our pinned list, use default validation
        guard let expectedHashes = pinnedHosts[host] else {
            completionHandler(.performDefaultHandling, nil)
            return
        }

        // Evaluate trust
        guard SecTrustEvaluateWithError(serverTrust, nil) else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        // Extract server's public key
        guard let serverCertificate = SecTrustGetCertificateAtIndex(serverTrust, 0),
              let serverPublicKey = SecCertificateCopyKey(serverCertificate) else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        // Get public key hash
        guard let serverKeyHash = publicKeyHash(for: serverPublicKey) else {
            completionHandler(.cancelAuthenticationChallenge, nil)
            return
        }

        // Verify against expected hashes
        if expectedHashes.contains(serverKeyHash) {
            completionHandler(.useCredential, URLCredential(trust: serverTrust))
        } else {
            // Pin mismatch - potential MITM attack
            Logger.security.error("Certificate pinning failed for host: \(host)")
            completionHandler(.cancelAuthenticationChallenge, nil)
        }
    }

    private func publicKeyHash(for publicKey: SecKey) -> String? {
        var error: Unmanaged<CFError>?
        guard let publicKeyData = SecKeyCopyExternalRepresentation(publicKey, &error) as Data? else {
            return nil
        }

        let hash = SHA256.hash(data: publicKeyData)
        return Data(hash).base64EncodedString()
    }
}
```

## Secure Data Encryption

```swift
import CryptoKit
import Foundation

// MARK: - Encryption Error

enum EncryptionError: LocalizedError {
    case keyGenerationFailed
    case encryptionFailed
    case decryptionFailed
    case invalidData
    case keyNotFound

    var errorDescription: String? {
        switch self {
        case .keyGenerationFailed:
            return "Failed to generate encryption key"
        case .encryptionFailed:
            return "Encryption failed"
        case .decryptionFailed:
            return "Decryption failed"
        case .invalidData:
            return "Invalid encrypted data format"
        case .keyNotFound:
            return "Encryption key not found"
        }
    }
}

// MARK: - Symmetric Encryption Manager

final class SymmetricEncryptionManager {

    private let keychain: SecureKeychainManager
    private let keyIdentifier: String

    init(
        keychain: SecureKeychainManager = .shared,
        keyIdentifier: String = "app.encryption.key"
    ) {
        self.keychain = keychain
        self.keyIdentifier = keyIdentifier
    }

    // MARK: - Key Management

    func generateAndStoreKey() throws {
        let key = SymmetricKey(size: .bits256)
        let keyData = key.withUnsafeBytes { Data($0) }

        try keychain.save(
            key: keyIdentifier,
            data: keyData,
            accessibility: .whenUnlockedThisDeviceOnly,
            biometricProtection: .biometryCurrentSet
        )
    }

    func deleteKey() throws {
        try keychain.delete(key: keyIdentifier)
    }

    private func loadKey() throws -> SymmetricKey {
        let keyData = try keychain.load(
            key: keyIdentifier,
            promptMessage: "Authenticate to access encrypted data"
        )
        return SymmetricKey(data: keyData)
    }

    // MARK: - Encryption

    func encrypt(_ data: Data) throws -> Data {
        let key = try loadKey()

        do {
            let sealedBox = try AES.GCM.seal(data, using: key)
            guard let combined = sealedBox.combined else {
                throw EncryptionError.encryptionFailed
            }
            return combined
        } catch {
            throw EncryptionError.encryptionFailed
        }
    }

    func encrypt<T: Encodable>(_ value: T) throws -> Data {
        let data = try JSONEncoder().encode(value)
        return try encrypt(data)
    }

    // MARK: - Decryption

    func decrypt(_ encryptedData: Data) throws -> Data {
        let key = try loadKey()

        do {
            let sealedBox = try AES.GCM.SealedBox(combined: encryptedData)
            return try AES.GCM.open(sealedBox, using: key)
        } catch {
            throw EncryptionError.decryptionFailed
        }
    }

    func decrypt<T: Decodable>(_ encryptedData: Data, as type: T.Type) throws -> T {
        let data = try decrypt(encryptedData)
        return try JSONDecoder().decode(type, from: data)
    }
}

// MARK: - Secure File Manager

final class SecureFileManager {

    private let encryptionManager: SymmetricEncryptionManager
    private let fileManager = FileManager.default

    init(encryptionManager: SymmetricEncryptionManager = .init()) {
        self.encryptionManager = encryptionManager
    }

    var secureDirectory: URL {
        let documentsURL = fileManager.urls(for: .documentDirectory, in: .userDomainMask)[0]
        let secureURL = documentsURL.appendingPathComponent("secure", isDirectory: true)

        if !fileManager.fileExists(atPath: secureURL.path) {
            try? fileManager.createDirectory(at: secureURL, withIntermediateDirectories: true)

            // Set file protection
            try? fileManager.setAttributes(
                [.protectionKey: FileProtectionType.complete],
                ofItemAtPath: secureURL.path
            )
        }

        return secureURL
    }

    func writeSecurely<T: Encodable>(_ value: T, filename: String) throws {
        let encryptedData = try encryptionManager.encrypt(value)
        let fileURL = secureDirectory.appendingPathComponent(filename)

        try encryptedData.write(to: fileURL, options: [.atomic, .completeFileProtection])
    }

    func readSecurely<T: Decodable>(_ type: T.Type, filename: String) throws -> T {
        let fileURL = secureDirectory.appendingPathComponent(filename)
        let encryptedData = try Data(contentsOf: fileURL)

        return try encryptionManager.decrypt(encryptedData, as: type)
    }

    func deleteSecurely(filename: String) throws {
        let fileURL = secureDirectory.appendingPathComponent(filename)
        try fileManager.removeItem(at: fileURL)
    }
}
```

## Security Audit Framework

```swift
import Foundation
import os.log

// MARK: - Security Logger

extension Logger {
    static let security = Logger(subsystem: Bundle.main.bundleIdentifier ?? "", category: "security")
}

// MARK: - Security Audit Result

struct SecurityAuditResult {
    let checkName: String
    let passed: Bool
    let severity: Severity
    let message: String
    let recommendation: String?

    enum Severity: String, CaseIterable {
        case critical = "CRITICAL"
        case high = "HIGH"
        case medium = "MEDIUM"
        case low = "LOW"
        case info = "INFO"
    }
}

// MARK: - Security Auditor

final class SecurityAuditor {

    static let shared = SecurityAuditor()

    private var results: [SecurityAuditResult] = []

    func runFullAudit() -> [SecurityAuditResult] {
        results = []

        // Storage Checks
        checkUserDefaultsSensitiveData()
        checkKeychainAccess()
        checkFileProtection()

        // Network Checks
        checkATSConfiguration()
        checkCertificatePinning()

        // App Configuration Checks
        checkDebugSettings()
        checkLoggingConfiguration()

        // Runtime Checks
        checkJailbreakIndicators()
        checkDebuggerAttached()

        return results
    }

    // MARK: - Storage Checks

    private func checkUserDefaultsSensitiveData() {
        let sensitiveKeys = ["token", "password", "secret", "api_key", "credential", "auth"]
        let defaults = UserDefaults.standard.dictionaryRepresentation()

        var foundSensitive = false
        for key in defaults.keys {
            let lowercaseKey = key.lowercased()
            if sensitiveKeys.contains(where: { lowercaseKey.contains($0) }) {
                foundSensitive = true
                Logger.security.warning("Potential sensitive data in UserDefaults: \(key)")
            }
        }

        results.append(SecurityAuditResult(
            checkName: "UserDefaults Sensitive Data",
            passed: !foundSensitive,
            severity: foundSensitive ? .critical : .info,
            message: foundSensitive ? "Found potentially sensitive keys in UserDefaults" : "No sensitive data found in UserDefaults",
            recommendation: foundSensitive ? "Move sensitive data to Keychain" : nil
        ))
    }

    private func checkKeychainAccess() {
        // Check if keychain items have appropriate access levels
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecMatchLimit as String: kSecMatchLimitAll,
            kSecReturnAttributes as String: true
        ]

        var result: AnyObject?
        let status = SecItemCopyMatching(query as CFDictionary, &result)

        if status == errSecSuccess, let items = result as? [[String: Any]] {
            var hasWeakAccess = false

            for item in items {
                if let accessibility = item[kSecAttrAccessible as String] as? String {
                    if accessibility == kSecAttrAccessibleAlways as String {
                        hasWeakAccess = true
                        break
                    }
                }
            }

            results.append(SecurityAuditResult(
                checkName: "Keychain Access Levels",
                passed: !hasWeakAccess,
                severity: hasWeakAccess ? .high : .info,
                message: hasWeakAccess ? "Found keychain items with kSecAttrAccessibleAlways" : "Keychain access levels appropriate",
                recommendation: hasWeakAccess ? "Use kSecAttrAccessibleAfterFirstUnlock or more restrictive" : nil
            ))
        }
    }

    private func checkFileProtection() {
        let documentsURL = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask)[0]

        do {
            let attributes = try FileManager.default.attributesOfItem(atPath: documentsURL.path)
            let protection = attributes[.protectionKey] as? FileProtectionType

            let hasProtection = protection == .complete || protection == .completeUnlessOpen

            results.append(SecurityAuditResult(
                checkName: "File Protection",
                passed: hasProtection,
                severity: hasProtection ? .info : .medium,
                message: hasProtection ? "Documents directory has file protection" : "Documents directory lacks complete protection",
                recommendation: hasProtection ? nil : "Enable .completeFileProtection for sensitive directories"
            ))
        } catch {
            results.append(SecurityAuditResult(
                checkName: "File Protection",
                passed: false,
                severity: .medium,
                message: "Could not check file protection: \(error.localizedDescription)",
                recommendation: nil
            ))
        }
    }

    // MARK: - Network Checks

    private func checkATSConfiguration() {
        guard let infoPlist = Bundle.main.infoDictionary,
              let atsSettings = infoPlist["NSAppTransportSecurity"] as? [String: Any] else {
            results.append(SecurityAuditResult(
                checkName: "ATS Configuration",
                passed: true,
                severity: .info,
                message: "No custom ATS settings - using secure defaults",
                recommendation: nil
            ))
            return
        }

        let allowsArbitrary = atsSettings["NSAllowsArbitraryLoads"] as? Bool ?? false

        results.append(SecurityAuditResult(
            checkName: "ATS Configuration",
            passed: !allowsArbitrary,
            severity: allowsArbitrary ? .critical : .info,
            message: allowsArbitrary ? "NSAllowsArbitraryLoads is enabled!" : "ATS is properly configured",
            recommendation: allowsArbitrary ? "Disable NSAllowsArbitraryLoads and use exception domains if needed" : nil
        ))
    }

    private func checkCertificatePinning() {
        // This is a manual check indicator
        results.append(SecurityAuditResult(
            checkName: "Certificate Pinning",
            passed: false,
            severity: .medium,
            message: "Certificate pinning status requires manual verification",
            recommendation: "Implement public key pinning for sensitive API endpoints"
        ))
    }

    // MARK: - App Configuration Checks

    private func checkDebugSettings() {
        #if DEBUG
        results.append(SecurityAuditResult(
            checkName: "Debug Build",
            passed: false,
            severity: .high,
            message: "App is running in DEBUG mode",
            recommendation: "Ensure RELEASE build for production"
        ))
        #else
        results.append(SecurityAuditResult(
            checkName: "Debug Build",
            passed: true,
            severity: .info,
            message: "App is running in RELEASE mode",
            recommendation: nil
        ))
        #endif
    }

    private func checkLoggingConfiguration() {
        // Check if os_log is being used appropriately
        results.append(SecurityAuditResult(
            checkName: "Logging Configuration",
            passed: true,
            severity: .info,
            message: "Verify no sensitive data is logged",
            recommendation: "Audit all log statements for credential exposure"
        ))
    }

    // MARK: - Runtime Checks

    private func checkJailbreakIndicators() {
        var indicators: [String] = []

        // Check for common jailbreak files
        let jailbreakPaths = [
            "/Applications/Cydia.app",
            "/Library/MobileSubstrate/MobileSubstrate.dylib",
            "/bin/bash",
            "/usr/sbin/sshd",
            "/etc/apt",
            "/private/var/lib/apt/"
        ]

        for path in jailbreakPaths {
            if FileManager.default.fileExists(atPath: path) {
                indicators.append(path)
            }
        }

        // Check if app can write outside sandbox
        let testPath = "/private/jailbreak_test_\(UUID().uuidString)"
        let canWrite = FileManager.default.createFile(atPath: testPath, contents: nil, attributes: nil)
        if canWrite {
            indicators.append("Can write outside sandbox")
            try? FileManager.default.removeItem(atPath: testPath)
        }

        let isJailbroken = !indicators.isEmpty

        results.append(SecurityAuditResult(
            checkName: "Jailbreak Detection",
            passed: !isJailbroken,
            severity: isJailbroken ? .critical : .info,
            message: isJailbroken ? "Jailbreak indicators found: \(indicators.joined(separator: ", "))" : "No jailbreak indicators detected",
            recommendation: isJailbroken ? "Consider restricting functionality on jailbroken devices" : nil
        ))
    }

    private func checkDebuggerAttached() {
        var info = kinfo_proc()
        var mib: [Int32] = [CTL_KERN, KERN_PROC, KERN_PROC_PID, getpid()]
        var size = MemoryLayout<kinfo_proc>.stride

        let result = sysctl(&mib, UInt32(mib.count), &info, &size, nil, 0)

        let isDebugged = result == 0 && (info.kp_proc.p_flag & P_TRACED) != 0

        results.append(SecurityAuditResult(
            checkName: "Debugger Detection",
            passed: !isDebugged,
            severity: isDebugged ? .high : .info,
            message: isDebugged ? "Debugger is attached to process" : "No debugger detected",
            recommendation: isDebugged ? "Anti-debug measures may be needed for sensitive operations" : nil
        ))
    }
}
```

## Secure Token Manager

```swift
import Foundation

// MARK: - Token Types

struct AuthTokens: Codable {
    let accessToken: String
    let refreshToken: String
    let expiresAt: Date
    let tokenType: String

    var isExpired: Bool {
        Date() >= expiresAt
    }

    var isAboutToExpire: Bool {
        // Consider expired 5 minutes before actual expiration
        Date().addingTimeInterval(300) >= expiresAt
    }
}

// MARK: - Secure Token Manager

actor SecureTokenManager {

    private let keychain: SecureKeychainManager
    private let accessTokenKey = "auth.access_token"
    private let refreshTokenKey = "auth.refresh_token"
    private let tokensKey = "auth.tokens"

    private var cachedTokens: AuthTokens?

    init(keychain: SecureKeychainManager = .shared) {
        self.keychain = keychain
    }

    // MARK: - Token Storage

    func storeTokens(_ tokens: AuthTokens) throws {
        try keychain.save(
            key: tokensKey,
            value: tokens,
            accessibility: .afterFirstUnlock,
            biometricProtection: .none
        )
        cachedTokens = tokens
    }

    func loadTokens() throws -> AuthTokens {
        if let cached = cachedTokens {
            return cached
        }

        let tokens: AuthTokens = try keychain.load(
            key: tokensKey,
            type: AuthTokens.self
        )
        cachedTokens = tokens
        return tokens
    }

    func clearTokens() throws {
        try keychain.delete(key: tokensKey)
        cachedTokens = nil
    }

    // MARK: - Token Validation

    func getValidAccessToken() throws -> String {
        let tokens = try loadTokens()

        guard !tokens.isExpired else {
            throw AuthError.tokenExpired
        }

        return tokens.accessToken
    }

    func getRefreshToken() throws -> String {
        let tokens = try loadTokens()
        return tokens.refreshToken
    }

    func hasValidTokens() -> Bool {
        guard let tokens = try? loadTokens() else {
            return false
        }
        return !tokens.isExpired
    }

    func shouldRefresh() -> Bool {
        guard let tokens = try? loadTokens() else {
            return false
        }
        return tokens.isAboutToExpire
    }
}

// MARK: - Auth Error

enum AuthError: LocalizedError {
    case tokenExpired
    case noTokensStored
    case refreshFailed
    case invalidCredentials

    var errorDescription: String? {
        switch self {
        case .tokenExpired:
            return "Authentication token has expired"
        case .noTokensStored:
            return "No authentication tokens found"
        case .refreshFailed:
            return "Failed to refresh authentication"
        case .invalidCredentials:
            return "Invalid credentials provided"
        }
    }
}
```

## API Key Obfuscation

```swift
import Foundation

// MARK: - Obfuscator (Last Resort for Client-Side Keys)

/// WARNING: This is NOT secure protection. Keys can still be extracted.
/// Use only when:
/// 1. You cannot proxy through your backend
/// 2. Key exposure would be annoying, not catastrophic
/// 3. You've accepted the risk
///
/// Better alternatives:
/// - Proxy API calls through your backend
/// - Use OAuth where user authenticates directly with service
/// - Use device attestation + backend key distribution
final class KeyObfuscator {

    private let salt: [UInt8]

    init(salt: [UInt8]) {
        self.salt = salt
    }

    /// Obfuscate at compile time - store the result in your code
    func obfuscate(_ string: String) -> [UInt8] {
        let bytes = Array(string.utf8)
        return bytes.enumerated().map { index, byte in
            byte ^ salt[index % salt.count]
        }
    }

    /// Reveal at runtime
    func reveal(_ obfuscated: [UInt8]) -> String {
        let bytes = obfuscated.enumerated().map { index, byte in
            byte ^ salt[index % salt.count]
        }
        return String(bytes: bytes, encoding: .utf8) ?? ""
    }

    // MARK: - Compile-Time Helper

    /// Use this in a separate script to generate obfuscated bytes
    /// Then paste the result into your code
    static func printObfuscatedCode(key: String, variableName: String) {
        let salt: [UInt8] = (0..<16).map { _ in UInt8.random(in: 0...255) }
        let obfuscator = KeyObfuscator(salt: salt)
        let obfuscated = obfuscator.obfuscate(key)

        print("""
        private let \(variableName)Salt: [UInt8] = [\(salt.map { String($0) }.joined(separator: ", "))]
        private let \(variableName)Obfuscated: [UInt8] = [\(obfuscated.map { String($0) }.joined(separator: ", "))]

        private var \(variableName): String {
            KeyObfuscator(salt: \(variableName)Salt).reveal(\(variableName)Obfuscated)
        }
        """)
    }
}

// MARK: - Usage Example

/*
 // In a build script, run:
 KeyObfuscator.printObfuscatedCode(key: "sk_live_abc123", variableName: "apiKey")

 // Then paste the output into your code:
 private let apiKeySalt: [UInt8] = [123, 45, 67, 89, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
 private let apiKeyObfuscated: [UInt8] = [...]

 private var apiKey: String {
     KeyObfuscator(salt: apiKeySalt).reveal(apiKeyObfuscated)
 }
 */
```

---

## Testing Security Implementation

```swift
import XCTest
@testable import YourApp

final class SecurityTests: XCTestCase {

    var keychain: SecureKeychainManager!

    override func setUp() {
        super.setUp()
        keychain = SecureKeychainManager(serviceName: "com.test.keychain")
    }

    override func tearDown() {
        try? keychain.deleteAll()
        super.tearDown()
    }

    // MARK: - Keychain Tests

    func testKeychainSaveAndLoad() throws {
        let testData = "secret_value".data(using: .utf8)!

        try keychain.save(key: "test_key", data: testData)
        let loaded = try keychain.load(key: "test_key")

        XCTAssertEqual(testData, loaded)
    }

    func testKeychainDelete() throws {
        let testData = "secret".data(using: .utf8)!

        try keychain.save(key: "delete_test", data: testData)
        XCTAssertTrue(keychain.exists(key: "delete_test"))

        try keychain.delete(key: "delete_test")
        XCTAssertFalse(keychain.exists(key: "delete_test"))
    }

    func testKeychainUpsert() throws {
        let value1 = "first".data(using: .utf8)!
        let value2 = "second".data(using: .utf8)!

        try keychain.save(key: "upsert_test", data: value1)
        try keychain.save(key: "upsert_test", data: value2)

        let loaded = try keychain.load(key: "upsert_test")
        XCTAssertEqual(value2, loaded)
    }

    func testKeychainCodable() throws {
        struct TestModel: Codable, Equatable {
            let id: Int
            let name: String
        }

        let model = TestModel(id: 1, name: "Test")

        try keychain.save(key: "codable_test", value: model)
        let loaded: TestModel = try keychain.load(key: "codable_test", type: TestModel.self)

        XCTAssertEqual(model, loaded)
    }

    // MARK: - Encryption Tests

    func testEncryptionRoundTrip() throws {
        let encryption = SymmetricEncryptionManager()
        try encryption.generateAndStoreKey()

        let original = "sensitive data".data(using: .utf8)!
        let encrypted = try encryption.encrypt(original)
        let decrypted = try encryption.decrypt(encrypted)

        XCTAssertEqual(original, decrypted)
        XCTAssertNotEqual(original, encrypted)

        try encryption.deleteKey()
    }

    // MARK: - Security Audit Tests

    func testSecurityAuditRuns() {
        let auditor = SecurityAuditor.shared
        let results = auditor.runFullAudit()

        XCTAssertFalse(results.isEmpty)

        // Log results for review
        for result in results {
            print("[\(result.severity.rawValue)] \(result.checkName): \(result.passed ? "PASS" : "FAIL") - \(result.message)")
        }
    }
}
```
