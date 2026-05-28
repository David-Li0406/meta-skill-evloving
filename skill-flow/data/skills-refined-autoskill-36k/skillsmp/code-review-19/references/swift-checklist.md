# Swift Code Review Checklist

Complete checklist for Swift (iOS 17+) code review.

## Quick Reference

| Priority | Category | Check |
|----------|----------|-------|
| Critical | Memory | No retain cycles in closures |
| Critical | Concurrency | @MainActor for UI updates |
| Critical | Safety | No unhandled force unwraps |
| High | Error Handling | Proper try/catch usage |
| High | Types | No implicit any/AnyObject |
| Medium | Performance | Efficient collection operations |
| Medium | Style | Consistent naming conventions |
| Low | Documentation | Public API has comments |

## Detailed Checklist

### 1. Memory Management

- [ ] **Closures use `[weak self]` where appropriate**
  ```swift
  // Check for potential retain cycles
  onComplete = { [weak self] in
      self?.handleCompletion()
  }
  ```

- [ ] **Delegates are declared as `weak`**
  ```swift
  weak var delegate: SomeDelegate?
  ```

- [ ] **Timers are properly invalidated**
  ```swift
  deinit {
      timer?.invalidate()
  }
  ```

- [ ] **NotificationCenter observers are removed**
  ```swift
  deinit {
      NotificationCenter.default.removeObserver(self)
  }
  ```

- [ ] **Tasks are cancelled when no longer needed**
  ```swift
  private var task: Task<Void, Never>?

  func cleanup() {
      task?.cancel()
  }
  ```

### 2. Concurrency & Thread Safety

- [ ] **UI updates use @MainActor**
  ```swift
  @Observable
  @MainActor
  class ViewModel {
      var items: [Item] = []  // Safe to update
  }
  ```

- [ ] **Async functions handle cancellation**
  ```swift
  func loadData() async throws {
      try Task.checkCancellation()
      // ... load data
  }
  ```

- [ ] **Actors are used for shared mutable state**
  ```swift
  actor DataStore {
      private var cache: [String: Data] = [:]
  }
  ```

- [ ] **No data races in concurrent code**
  - Review all mutable state accessed from multiple tasks
  - Use actors or locks for synchronization

### 3. Optional Handling

- [ ] **No force unwrapping without safety checks**
  ```swift
  // BAD
  let value = optional!

  // GOOD
  guard let value = optional else { return }
  ```

- [ ] **Implicitly unwrapped optionals are justified**
  - Only use for IBOutlets or late-initialized properties
  - Document why it's safe

- [ ] **Optional chaining is not excessive**
  - Break long chains into meaningful steps
  - Consider guard let for complex unwrapping

### 4. Error Handling

- [ ] **Errors are not silently swallowed**
  ```swift
  // BAD
  do {
      try operation()
  } catch { }  // Silent failure

  // GOOD
  do {
      try operation()
  } catch {
      logger.error("Operation failed: \(error)")
      throw error
  }
  ```

- [ ] **Custom errors implement LocalizedError**
  ```swift
  enum AppError: Error, LocalizedError {
      case networkError

      var errorDescription: String? {
          switch self {
          case .networkError: return "Network connection failed"
          }
      }
  }
  ```

- [ ] **Async errors are properly propagated**

### 5. SwiftUI Specifics

- [ ] **@State is used correctly**
  - Only for value types owned by the view
  - Not for complex reference types

- [ ] **@Observable is used (iOS 17+)**
  - Instead of ObservableObject for new code
  - Use @State private var viewModel = ViewModel()

- [ ] **Views are appropriately decomposed**
  - Extract reusable components
  - Keep body relatively simple

- [ ] **Navigation uses NavigationStack**
  - Type-safe navigation with NavigationPath
  - Avoid deprecated NavigationView

### 6. Performance

- [ ] **Expensive operations are cached**
  ```swift
  // Cache formatters, regex, etc.
  private static let dateFormatter: DateFormatter = {
      let formatter = DateFormatter()
      formatter.dateStyle = .medium
      return formatter
  }()
  ```

- [ ] **Collections reserve capacity when size is known**
  ```swift
  var items: [Item] = []
  items.reserveCapacity(expectedCount)
  ```

- [ ] **Lazy properties are used appropriately**
  ```swift
  lazy var expensiveValue: Value = computeExpensiveValue()
  ```

- [ ] **View updates are minimized**
  - Avoid unnecessary @State changes
  - Use equatable conformance where helpful

### 7. Code Style

- [ ] **Naming follows Swift conventions**
  - Types: PascalCase
  - Properties/Methods: camelCase
  - Constants: camelCase (not SCREAMING_CASE)

- [ ] **Access control is appropriate**
  - Default to private, expose only what's needed
  - Use internal for cross-file access within module

- [ ] **Types are explicit where helpful**
  - Complex return types
  - Closures with multiple parameters

### 8. Testing Considerations

- [ ] **Dependencies are injectable**
  ```swift
  class ViewModel {
      private let repository: RepositoryProtocol

      init(repository: RepositoryProtocol = Repository()) {
          self.repository = repository
      }
  }
  ```

- [ ] **Date/Time is injectable for testing**
  ```swift
  init(now: @escaping () -> Date = Date.init) {
      self.now = now
  }
  ```

- [ ] **Side effects are isolated**
  - Network calls through protocols
  - File operations through protocols

## Review Output Format

When reporting issues, use this format:

```
## Issue: [Brief Title]

- **File**: path/to/file.swift:line_number
- **Severity**: Critical | High | Medium | Low
- **Category**: Memory | Concurrency | Safety | Performance | Style

### Problem
[Description of the issue]

### Current Code
```swift
// problematic code
```

### Suggested Fix
```swift
// corrected code
```
```
