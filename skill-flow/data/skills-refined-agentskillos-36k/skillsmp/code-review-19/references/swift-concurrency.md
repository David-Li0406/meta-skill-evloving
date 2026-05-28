# Swift Concurrency Review Guide

Review points for Swift concurrency (async/await, actors, tasks).

## Thread Safety

### MainActor for UI

```swift
// REQUIRED: UI-bound properties must be @MainActor
@Observable
@MainActor
class ViewModel {
    var items: [Item] = []  // Safe to update from SwiftUI
    var isLoading = false

    func loadData() async {
        isLoading = true
        defer { isLoading = false }

        items = await fetchItems()  // Runs on main thread
    }
}
```

### Actor for Shared State

```swift
// Use actors for thread-safe shared mutable state
actor DataStore {
    private var cache: [String: Data] = [:]

    func get(_ key: String) -> Data? {
        cache[key]
    }

    func set(_ key: String, data: Data) {
        cache[key] = data
    }

    func clear() {
        cache.removeAll()
    }
}

// Usage (must await)
let store = DataStore()
await store.set("key", data: data)
let cached = await store.get("key")
```

### Sendable Compliance

```swift
// Value types are automatically Sendable
struct Point: Sendable {
    var x: Double
    var y: Double
}

// Reference types need explicit conformance
final class Config: Sendable {
    let apiKey: String  // Only immutable properties

    init(apiKey: String) {
        self.apiKey = apiKey
    }
}

// Use @unchecked Sendable carefully
final class ThreadSafeCache: @unchecked Sendable {
    private let lock = NSLock()
    private var storage: [String: Any] = [:]

    func get(_ key: String) -> Any? {
        lock.withLock { storage[key] }
    }
}
```

## Task Management

### Task Lifecycle

```swift
@Observable
@MainActor
class SearchViewModel {
    var results: [SearchResult] = []
    private var searchTask: Task<Void, Never>?

    func search(query: String) {
        // Cancel previous search
        searchTask?.cancel()

        searchTask = Task {
            // Debounce
            try? await Task.sleep(for: .milliseconds(300))

            // Check cancellation
            guard !Task.isCancelled else { return }

            do {
                results = try await performSearch(query)
            } catch is CancellationError {
                // Expected, ignore
            } catch {
                // Handle other errors
            }
        }
    }

    func cancelSearch() {
        searchTask?.cancel()
    }
}
```

### Task Hierarchy in Views

```swift
struct ContentView: View {
    @State private var viewModel = ContentViewModel()

    var body: some View {
        List(viewModel.items) { item in
            ItemRow(item: item)
        }
        .task {
            // Automatically cancelled when view disappears
            await viewModel.loadItems()
        }
        .task(id: viewModel.selectedCategory) {
            // Re-runs when selectedCategory changes
            // Previous task automatically cancelled
            await viewModel.loadCategoryItems()
        }
    }
}
```

### Detached Tasks

```swift
// Use sparingly - not cancelled with parent
func logAnalytics(event: AnalyticsEvent) {
    Task.detached(priority: .background) {
        // Runs independently of calling task
        await AnalyticsService.shared.log(event)
    }
}
```

## Error Handling

### Cancellation Handling

```swift
func fetchData() async throws -> Data {
    // Check before expensive operation
    try Task.checkCancellation()

    let data = try await networkRequest()

    // Check after each major step
    try Task.checkCancellation()

    let processed = try await processData(data)

    return processed
}

// Non-throwing version
func fetchDataSafe() async -> Data? {
    guard !Task.isCancelled else { return nil }

    // Continue with operation
    return await performFetch()
}
```

### Error Propagation

```swift
// DO: Propagate errors up
func loadUser() async throws -> User {
    try await api.fetchUser()  // Throws propagate
}

// DON'T: Swallow errors silently
func loadUserBad() async -> User? {
    try? await api.fetchUser()  // Error information lost
}

// If catching, handle meaningfully
func loadUserWithFallback() async -> User {
    do {
        return try await api.fetchUser()
    } catch {
        logger.error("Failed to load user: \(error)")
        return User.guest  // Meaningful fallback
    }
}
```

## Parallel Execution

### async let for Known Work

```swift
// Best for fixed number of independent operations
func loadDashboard() async throws -> Dashboard {
    async let user = fetchUser()
    async let notifications = fetchNotifications()
    async let feed = fetchFeed()

    return try await Dashboard(
        user: user,
        notifications: notifications,
        feed: feed
    )
}
```

### TaskGroup for Dynamic Work

```swift
// Best for variable number of operations
func fetchAllUsers(ids: [String]) async throws -> [User] {
    try await withThrowingTaskGroup(of: User.self) { group in
        for id in ids {
            group.addTask {
                try await fetchUser(id: id)
            }
        }

        return try await group.reduce(into: []) { $0.append($1) }
    }
}
```

### Limiting Concurrency

```swift
// Prevent overwhelming resources
func fetchWithLimit(ids: [String], maxConcurrent: Int = 5) async throws -> [User] {
    try await withThrowingTaskGroup(of: User.self) { group in
        var index = 0
        var results: [User] = []
        results.reserveCapacity(ids.count)

        // Start initial batch
        while index < min(maxConcurrent, ids.count) {
            let id = ids[index]
            group.addTask { try await self.fetchUser(id: id) }
            index += 1
        }

        // Process and add more
        for try await user in group {
            results.append(user)
            if index < ids.count {
                let id = ids[index]
                group.addTask { try await self.fetchUser(id: id) }
                index += 1
            }
        }

        return results
    }
}
```

## Continuation Patterns

### Wrapping Callbacks

```swift
// Convert callback-based API to async
func fetchLegacy() async throws -> Data {
    try await withCheckedThrowingContinuation { continuation in
        legacyAPI.fetch { result in
            switch result {
            case .success(let data):
                continuation.resume(returning: data)
            case .failure(let error):
                continuation.resume(throwing: error)
            }
        }
    }
}
```

### Wrapping Delegates

```swift
class LocationFetcher: NSObject, CLLocationManagerDelegate {
    private var continuation: CheckedContinuation<CLLocation, Error>?
    private let manager = CLLocationManager()

    func getLocation() async throws -> CLLocation {
        try await withCheckedThrowingContinuation { continuation in
            self.continuation = continuation
            manager.delegate = self
            manager.requestLocation()
        }
    }

    func locationManager(_ manager: CLLocationManager,
                        didUpdateLocations locations: [CLLocation]) {
        continuation?.resume(returning: locations[0])
        continuation = nil
    }

    func locationManager(_ manager: CLLocationManager,
                        didFailWithError error: Error) {
        continuation?.resume(throwing: error)
        continuation = nil
    }
}
```

## Review Checklist

### Thread Safety
- [ ] UI-bound ViewModels marked with `@MainActor`
- [ ] Shared mutable state protected by actors
- [ ] Types crossing task boundaries are `Sendable`
- [ ] No direct `DispatchQueue.main.async` in new code

### Task Management
- [ ] Tasks cancelled when no longer needed
- [ ] Previous tasks cancelled before starting new ones
- [ ] `.task` modifier used in SwiftUI views
- [ ] Cancellation checked in long operations

### Error Handling
- [ ] Errors propagated, not silently swallowed
- [ ] `CancellationError` handled appropriately
- [ ] Meaningful error messages logged

### Performance
- [ ] Independent operations run in parallel
- [ ] Task groups used for dynamic work
- [ ] Concurrency limited when appropriate
