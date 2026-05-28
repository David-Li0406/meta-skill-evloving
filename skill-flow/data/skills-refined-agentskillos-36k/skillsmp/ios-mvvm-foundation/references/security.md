# Security

> Security best practices cho iOS applications.

---

## 🔑 API Key Management

### Storage: Secrets.xcconfig (gitignored)

```
// Secrets.xcconfig (GITIGNORED!)
API_KEY = sk_live_abc123
API_BASE_URL = https://api.example.com
```

### Info.plist Reference

```xml
<key>API_KEY</key>
<string>$(API_KEY)</string>
```

### Swift Access

```swift
let apiKey = Bundle.main.object(forInfoDictionaryKey: "API_KEY") as? String
```

> ⚠️ **NEVER** hardcode API keys in source code

---

## 🔒 Certificate Pinning

### TrustKit Configuration

```swift
import TrustKit

TrustKit.initSharedInstance(withConfiguration: [
    kTSKSwizzleNetworkDelegates: false,
    kTSKPinnedDomains: [
        "api.example.com": [
            kTSKPublicKeyHashes: [
                "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA=",
                "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB="
            ]
        ]
    ]
])
```

---

## 🛡️ Data Encryption

| Type | Method |
|------|--------|
| **At Rest** | Realm encryption key in Keychain |
| **In Transit** | TLS 1.3 only |
| **Sensitive Data** | Always encrypt before storing |

---

## 🎫 Token Management

### Access Token

| Aspect | Implementation |
|--------|----------------|
| **Storage** | Keychain |
| **Expiration** | Check before API calls |
| **Refresh** | Automatic via refresh token |

### Refresh Token

| Aspect | Implementation |
|--------|----------------|
| **Storage** | Keychain (separate key) |
| **Rotation** | On each refresh |

### Implementation Example

```swift
class TokenService {
    private let keychain = Keychain(service: "com.app.tokens")
    
    func saveAccessToken(_ token: String) throws {
        try keychain.set(token, key: "access_token")
    }
    
    func saveRefreshToken(_ token: String) throws {
        try keychain.set(token, key: "refresh_token")
    }
    
    func getAccessToken() -> String? {
        try? keychain.get("access_token")
    }
    
    func clearTokens() throws {
        try keychain.remove("access_token")
        try keychain.remove("refresh_token")
    }
}
```

---

## 📋 Security Checklist

### Must Have ✅

- [ ] API keys in xcconfig (gitignored)
- [ ] Tokens stored in Keychain
- [ ] Certificate pinning enabled
- [ ] TLS 1.3 only
- [ ] Sensitive data encrypted at rest

### Never Do ❌

- [ ] Hardcode secrets in source code
- [ ] Store tokens in UserDefaults
- [ ] Skip certificate validation
- [ ] Log sensitive data
- [ ] Store passwords in plaintext

---

## 🔐 Keychain Best Practices

### Accessibility Options

| Option | When to Use |
|--------|-------------|
| `kSecAttrAccessibleAfterFirstUnlock` | Default for most data |
| `kSecAttrAccessibleWhenUnlocked` | Highly sensitive data |
| `kSecAttrAccessibleAlways` | Background refresh tokens |

### Keychain Service Example

```swift
import KeychainAccess

class KeychainService {
    private let keychain: Keychain
    
    init(service: String = "com.app.keychain") {
        self.keychain = Keychain(service: service)
            .accessibility(.afterFirstUnlock)
    }
    
    func save(_ value: String, for key: String) throws {
        try keychain.set(value, key: key)
    }
    
    func get(_ key: String) -> String? {
        try? keychain.get(key)
    }
    
    func delete(_ key: String) throws {
        try keychain.remove(key)
    }
}
```

---

## 🚨 Common Vulnerabilities

| Vulnerability | Prevention |
|---------------|------------|
| **Insecure Storage** | Use Keychain for secrets |
| **Man-in-the-Middle** | Certificate pinning |
| **Reverse Engineering** | Code obfuscation |
| **Jailbreak Detection** | Runtime checks |
| **Debug Logging** | Disable in production |
