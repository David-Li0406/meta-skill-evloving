# UseCase Template

> Domain layer UseCase với protocol và implementation.

---

## 📁 Files Generated

| File | Path |
|------|------|
| `{ACTION}{ENTITY}UseCaseProtocol.swift` | `Domain/UseCases/{ACTION}{ENTITY}UseCaseProtocol.swift` |
| `{ACTION}{ENTITY}UseCase.swift` | `Domain/UseCases/{ACTION}{ENTITY}UseCase.swift` |

---

## 📋 Protocol Template

```swift
import Foundation

/// Protocol defining the {ACTION}{ENTITY} use case
protocol {ACTION}{ENTITY}UseCaseProtocol {
    /// Executes the {ACTION} operation
    /// - Parameters:
    ///   - param1: Description of param1
    /// - Returns: {ENTITY} on success
    /// - Throws: ValidationError or RepositoryError
    func execute(param1: String) async throws -> {ENTITY}
}
```

---

## 🏗️ Implementation Template

```swift
import Foundation

/// Use case for {ACTION}ing {ENTITY}
class {ACTION}{ENTITY}UseCase: {ACTION}{ENTITY}UseCaseProtocol {
    // MARK: - Dependencies
    
    private let repository: {ENTITY}RepositoryProtocol
    private let validator: ValidationService
    
    // MARK: - Init
    
    init(
        repository: {ENTITY}RepositoryProtocol,
        validator: ValidationService = ValidationService()
    ) {
        self.repository = repository
        self.validator = validator
    }
    
    // MARK: - Execute
    
    func execute(param1: String) async throws -> {ENTITY} {
        // 1. Validate input (Business Rules)
        guard !param1.isEmpty else {
            throw ValidationError.emptyField("param1")
        }
        
        // 2. Call repository
        let result = try await repository.{ACTION_LOWER}(param1: param1)
        
        // 3. Return domain entity
        return result
    }
}
```

---

## ❌ Validation Error

```swift
enum ValidationError: Error, LocalizedError {
    case emptyField(String)
    case invalidFormat(String)
    
    var errorDescription: String? {
        switch self {
        case .emptyField(let field):
            return "\(field) cannot be empty"
        case .invalidFormat(let field):
            return "\(field) has invalid format"
        }
    }
}
```

---

## 📊 UseCase Responsibilities

| Do | Don't |
|----|-------|
| Validate business rules | Handle UI concerns |
| Coordinate repositories | Store state |
| Transform data | Know about Views |
| Throw domain errors | Handle navigation |

---

## 🔄 Common Patterns

### Fetch UseCase

```swift
class FetchUserUseCase: FetchUserUseCaseProtocol {
    func execute(userId: String) async throws -> User {
        return try await repository.get(id: userId)
    }
}
```

### Create UseCase

```swift
class CreateTaskUseCase: CreateTaskUseCaseProtocol {
    func execute(title: String, dueDate: Date) async throws -> Task {
        // Validate
        guard !title.isEmpty else {
            throw ValidationError.emptyField("title")
        }
        
        // Create entity
        let task = Task(title: title, dueDate: dueDate)
        
        // Persist
        return try await repository.create(task)
    }
}
```

### Update UseCase

```swift
class UpdateProfileUseCase: UpdateProfileUseCaseProtocol {
    func execute(profile: Profile) async throws -> Profile {
        // Validate
        try validator.validate(profile)
        
        // Update
        return try await repository.update(profile)
    }
}
```

---

## ✅ Best Practices

- [ ] Single responsibility - one action per UseCase
- [ ] Validate inputs before repository calls
- [ ] Use domain errors (not generic errors)
- [ ] Inject dependencies via init
- [ ] Keep UseCases thin - delegate to repositories
- [ ] Return domain entities (not DTOs)
