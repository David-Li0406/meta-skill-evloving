# Repository Template

> Repository protocol (Domain) và implementation (Data).

---

## 📁 Files Generated

| File | Path |
|------|------|
| `{ENTITY}RepositoryProtocol.swift` | `Domain/Repositories/{ENTITY}RepositoryProtocol.swift` |
| `{ENTITY}Repository.swift` | `Data/Repositories/{ENTITY}Repository.swift` |

---

## 📋 Protocol Template (Domain Layer)

```swift
import Foundation

/// Repository protocol for {ENTITY} data access
/// - Note: This is the Domain layer contract
protocol {ENTITY}RepositoryProtocol {
    /// Fetches {ENTITY} by ID
    func get(id: String) async throws -> {ENTITY}
    
    /// Fetches all {ENTITY}s
    func getAll() async throws -> [{ENTITY}]
    
    /// Creates new {ENTITY}
    func create(_ entity: {ENTITY}) async throws -> {ENTITY}
    
    /// Updates existing {ENTITY}
    func update(_ entity: {ENTITY}) async throws -> {ENTITY}
    
    /// Deletes {ENTITY} by ID
    func delete(id: String) async throws
}
```

---

## 🏗️ Implementation Template (Data Layer)

```swift
import Foundation

/// Concrete implementation of {ENTITY}Repository
class {ENTITY}Repository: {ENTITY}RepositoryProtocol {
    // MARK: - Dependencies
    
    private let remoteDataSource: {ENTITY}RemoteDataSource
    private let localDataSource: {ENTITY}LocalDataSource
    private let cachePolicy: CachePolicy
    
    // MARK: - Init
    
    init(
        remoteDataSource: {ENTITY}RemoteDataSource,
        localDataSource: {ENTITY}LocalDataSource,
        cachePolicy: CachePolicy = .cacheFirst(ttl: 300)
    ) {
        self.remoteDataSource = remoteDataSource
        self.localDataSource = localDataSource
        self.cachePolicy = cachePolicy
    }
    
    // MARK: - Repository Methods
    
    func get(id: String) async throws -> {ENTITY} {
        // Try cache first
        if case .cacheFirst(let ttl) = cachePolicy,
           let cached = try? await localDataSource.get(id: id),
           !cached.isExpired(ttl: ttl) {
            return cached.toDomain()
        }
        
        // Fetch from remote
        let dto = try await remoteDataSource.fetch(id: id)
        let entity = dto.toDomain()
        
        // Update cache
        try? await localDataSource.save(entity)
        
        return entity
    }
    
    func getAll() async throws -> [{ENTITY}] {
        let dtos = try await remoteDataSource.fetchAll()
        return dtos.map { $0.toDomain() }
    }
    
    func create(_ entity: {ENTITY}) async throws -> {ENTITY} {
        let dto = {ENTITY}DTO(from: entity)
        let createdDTO = try await remoteDataSource.create(dto)
        let created = createdDTO.toDomain()
        
        // Save to local
        try? await localDataSource.save(created)
        
        return created
    }
    
    func update(_ entity: {ENTITY}) async throws -> {ENTITY} {
        let dto = {ENTITY}DTO(from: entity)
        let updatedDTO = try await remoteDataSource.update(id: entity.id, dto: dto)
        let updated = updatedDTO.toDomain()
        
        // Update local
        try? await localDataSource.save(updated)
        
        return updated
    }
    
    func delete(id: String) async throws {
        try await remoteDataSource.delete(id: id)
        try? await localDataSource.delete(id: id)
    }
}
```

---

## 🔄 Cache Policy

```swift
enum CachePolicy {
    case networkOnly
    case cacheOnly
    case cacheFirst(ttl: TimeInterval)
    case networkFirst
}
```

---

## 📊 Data Flow

```
ViewModel → UseCase → Repository (Protocol)
                            ↓
                      Repository (Impl)
                       ↙        ↘
              RemoteDataSource  LocalDataSource
                     ↓               ↓
                   API            Realm/CoreData
```

---

## ✅ Best Practices

- [ ] Protocol định nghĩa trong Domain layer
- [ ] Implementation trong Data layer
- [ ] Inject data sources via init
- [ ] Use cache policy for offline support
- [ ] Convert DTO ↔ Domain entities
- [ ] Handle cache invalidation
