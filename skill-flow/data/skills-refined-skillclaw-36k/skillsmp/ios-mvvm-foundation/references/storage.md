# Storage

> Data persistence patterns cho iOS applications.

---

## 🎯 Decision Matrix

| Storage | Use Case | Security | Size Limit |
|---------|----------|----------|------------|
| **Keychain** | Credentials, tokens | Hardware encryption | < 4KB/item |
| **UserDefaults** | Settings, preferences | ⚠️ Plaintext | < 1MB total |
| **Realm** | Offline data, complex queries | Encrypted optional | Unlimited |
| **CoreData** | Legacy, iCloud sync | Encrypted optional | Unlimited |
| **FileManager** | Large files, documents | File protection | Unlimited |

---

## 🔐 Keychain

### When to Use
- JWT tokens
- API keys
- User passwords
- Encryption keys

### Implementation

```swift
import KeychainAccess

enum KeychainKey: String {
    case accessToken
    case refreshToken
    case encryptionKey
}

class KeychainService {
    private let keychain: Keychain
    
    init(service: String = "com.app.keychain") {
        self.keychain = Keychain(service: service)
    }
    
    func save(token: String, for key: KeychainKey) throws {
        try keychain.set(token, key: key.rawValue)
    }
    
    func get(key: KeychainKey) -> String? {
        try? keychain.get(key.rawValue)
    }
    
    func delete(key: KeychainKey) throws {
        try keychain.remove(key.rawValue)
    }
}
```

---

## ⚙️ UserDefaults

### When to Use
- App theme (light/dark)
- Language preference
- Onboarding completed flag
- Feature flags cache

### ❌ Never Store
- Passwords
- Tokens
- PII (email, name)
- Financial data

### Implementation

```swift
enum UserDefaultsKey: String {
    case theme
    case language
    case hasCompletedOnboarding
}

class UserDefaultsService {
    private let defaults = UserDefaults.standard
    
    func set<T>(_ value: T, for key: UserDefaultsKey) {
        defaults.set(value, forKey: key.rawValue)
    }
    
    func get<T>(for key: UserDefaultsKey) -> T? {
        defaults.object(forKey: key.rawValue) as? T
    }
    
    func remove(key: UserDefaultsKey) {
        defaults.removeObject(forKey: key.rawValue)
    }
}
```

---

## 📦 Realm Swift

### When to Use
- Offline-first data
- Complex queries
- Real-time sync
- Large datasets

### Benefits
- Fast queries with indexes
- Live objects (auto-updates)
- Cross-platform (iOS + Android)
- ACID transactions
- Easy migrations

### Model Definition

```swift
import RealmSwift

class Portfolio: Object {
    @Persisted(primaryKey: true) var id: String
    @Persisted var userId: String
    @Persisted var totalValue: Double
    @Persisted var holdings: List<Holding>
    @Persisted var lastUpdated: Date
    
    convenience init(id: String, userId: String) {
        self.init()
        self.id = id
        self.userId = userId
        self.lastUpdated = Date()
    }
}
```

### Service Implementation

```swift
class RealmService {
    private let realm: Realm
    
    init() throws {
        var config = Realm.Configuration.defaultConfiguration
        config.schemaVersion = 1
        config.encryptionKey = try KeychainService().getEncryptionKey()
        realm = try Realm(configuration: config)
    }
    
    func save<T: Object>(_ object: T) throws {
        try realm.write {
            realm.add(object, update: .modified)
        }
    }
    
    func fetch<T: Object>(_ type: T.Type, filter: String? = nil) -> Results<T> {
        if let filter = filter {
            return realm.objects(type).filter(filter)
        }
        return realm.objects(type)
    }
    
    func delete<T: Object>(_ object: T) throws {
        try realm.write {
            realm.delete(object)
        }
    }
}
```

---

## 📁 FileManager

### Directories

| Directory | Purpose | Backed Up |
|-----------|---------|-----------|
| `Documents` | User-generated content | ✅ iCloud |
| `Caches` | Temporary data | ❌ |
| `tmp` | Very temporary | ❌ |

### When to Use
- Downloaded PDFs
- Cached images
- Exported CSV files

---

## 🚦 Recommendation Flowchart

```
Is it a credential?
    ├── YES → Keychain
    └── NO
        Is it a large file?
            ├── YES → FileManager
            └── NO
                Is it a simple setting?
                    ├── YES → UserDefaults
                    └── NO
                        Is it relational data?
                            ├── YES → Realm
                            └── NO
                                Needs complex queries?
                                    ├── YES → Realm
                                    └── NO → UserDefaults
```

---

## 🔒 Security Best Practices

### Realm Encryption

```swift
let encryptionKey = try KeychainService().getRealmEncryptionKey()
var config = Realm.Configuration.defaultConfiguration
config.encryptionKey = encryptionKey
```

### Data Classification

| Level | Storage | Examples |
|-------|---------|----------|
| **Critical** | Keychain only | Tokens, passwords |
| **Sensitive** | Encrypted Realm | Financial data, PII |
| **Public** | UserDefaults | UI preferences |

---

## 📋 Quick Reference

### Example App Usage

| Storage | Data |
|---------|------|
| **Keychain** | JWT access token, Refresh token, API keys |
| **UserDefaults** | Theme, Language, Onboarding status |
| **Realm** | User profiles, Transaction history, Cache |
| **FileManager** | Exported reports, Chart snapshots |
