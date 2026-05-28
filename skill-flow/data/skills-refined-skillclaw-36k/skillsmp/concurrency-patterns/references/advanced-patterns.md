# Concurrency Patterns — Advanced Patterns

> **Loading Trigger**: Load when implementing complex async patterns, debugging data races, or designing actor-based systems.

---

## Complete Actor Implementation

```swift
import Foundation

// MARK: - Cache Actor

actor Cache<Key: Hashable, Value> {
    private var storage: [Key: CacheEntry<Value>] = [:]
    private let maxAge: TimeInterval
    private let maxSize: Int

    struct CacheEntry<T> {
        let value: T
        let timestamp: Date
        var isExpired: Bool {
            Date().timeIntervalSince(timestamp) > maxAge
        }
        private let maxAge: TimeInterval

        init(value: T, maxAge: TimeInterval) {
            self.value = value
            self.timestamp = Date()
            self.maxAge = maxAge
        }
    }

    init(maxAge: TimeInterval = 300, maxSize: Int = 100) {
        self.maxAge = maxAge
        self.maxSize = maxSize
    }

    func get(_ key: Key) -> Value? {
        guard let entry = storage[key], !entry.isExpired else {
            storage.removeValue(forKey: key)
            return nil
        }
        return entry.value
    }

    func set(_ key: Key, value: Value) {
        // Evict if at capacity
        if storage.count >= maxSize {
            evictOldest()
        }
        storage[key] = CacheEntry(value: value, maxAge: maxAge)
    }

    func remove(_ key: Key) {
        storage.removeValue(forKey: key)
    }

    func clear() {
        storage.removeAll()
    }

    func getOrFetch(_ key: Key, fetch: () async throws -> Value) async throws -> Value {
        if let cached = get(key) {
            return cached
        }
        let value = try await fetch()
        set(key, value: value)
        return value
    }

    private func evictOldest() {
        // Remove expired entries first
        storage = storage.filter { !$0.value.isExpired }

        // If still over capacity, remove oldest
        if storage.count >= maxSize {
            let oldest = storage.min { $0.value.timestamp < $1.value.timestamp }
            if let key = oldest?.key {
                storage.removeValue(forKey: key)
            }
        }
    }

    // MARK: - Bulk Operations

    func getAll() -> [Key: Value] {
        storage.compactMapValues { entry in
            entry.isExpired ? nil : entry.value
        }
    }

    func setAll(_ items: [Key: Value]) {
        for (key, value) in items {
            set(key, value: value)
        }
    }
}

// MARK: - Rate Limiter Actor

actor RateLimiter {
    private let maxRequests: Int
    private let window: TimeInterval
    private var requests: [Date] = []

    init(maxRequests: Int, perWindow window: TimeInterval) {
        self.maxRequests = maxRequests
        self.window = window
    }

    func acquire() async throws {
        cleanupExpiredRequests()

        if requests.count >= maxRequests {
            let oldestRequest = requests.first!
            let waitTime = window - Date().timeIntervalSince(oldestRequest)

            if waitTime > 0 {
                try await Task.sleep(for: .seconds(waitTime))
                try await acquire() // Recursive retry
                return
            }
        }

        requests.append(Date())
    }

    func tryAcquire() -> Bool {
        cleanupExpiredRequests()

        if requests.count < maxRequests {
            requests.append(Date())
            return true
        }
        return false
    }

    private func cleanupExpiredRequests() {
        let cutoff = Date().addingTimeInterval(-window)
        requests.removeAll { $0 < cutoff }
    }

    var availableTokens: Int {
        cleanupExpiredRequests()
        return max(0, maxRequests - requests.count)
    }
}

// MARK: - Semaphore Actor

actor AsyncSemaphore {
    private var permits: Int
    private var waiters: [CheckedContinuation<Void, Never>] = []

    init(permits: Int) {
        self.permits = permits
    }

    func acquire() async {
        if permits > 0 {
            permits -= 1
            return
        }

        await withCheckedContinuation { continuation in
            waiters.append(continuation)
        }
    }

    func release() {
        if let waiter = waiters.first {
            waiters.removeFirst()
            waiter.resume()
        } else {
            permits += 1
        }
    }

    func withPermit<T>(_ operation: () async throws -> T) async rethrows -> T {
        await acquire()
        defer { Task { await release() } }
        return try await operation()
    }
}
```

---

## TaskGroup Patterns

```swift
// MARK: - Parallel Map

extension Sequence {
    func asyncMap<T>(
        _ transform: @escaping (Element) async throws -> T
    ) async throws -> [T] {
        try await withThrowingTaskGroup(of: (Int, T).self) { group in
            for (index, element) in self.enumerated() {
                group.addTask {
                    let result = try await transform(element)
                    return (index, result)
                }
            }

            var results: [(Int, T)] = []
            for try await result in group {
                results.append(result)
            }

            return results.sorted { $0.0 < $1.0 }.map { $0.1 }
        }
    }

    func asyncCompactMap<T>(
        _ transform: @escaping (Element) async throws -> T?
    ) async throws -> [T] {
        try await withThrowingTaskGroup(of: (Int, T?).self) { group in
            for (index, element) in self.enumerated() {
                group.addTask {
                    let result = try await transform(element)
                    return (index, result)
                }
            }

            var results: [(Int, T?)] = []
            for try await result in group {
                results.append(result)
            }

            return results
                .sorted { $0.0 < $1.0 }
                .compactMap { $0.1 }
        }
    }

    func asyncForEach(
        _ operation: @escaping (Element) async throws -> Void
    ) async throws {
        try await withThrowingTaskGroup(of: Void.self) { group in
            for element in self {
                group.addTask {
                    try await operation(element)
                }
            }
            try await group.waitForAll()
        }
    }
}

// MARK: - Throttled TaskGroup

func throttledTaskGroup<T, R>(
    items: [T],
    maxConcurrency: Int,
    operation: @escaping (T) async throws -> R
) async throws -> [R] {
    let semaphore = AsyncSemaphore(permits: maxConcurrency)

    return try await withThrowingTaskGroup(of: (Int, R).self) { group in
        for (index, item) in items.enumerated() {
            group.addTask {
                await semaphore.acquire()
                defer { Task { await semaphore.release() } }

                let result = try await operation(item)
                return (index, result)
            }
        }

        var results: [(Int, R)] = []
        for try await result in group {
            results.append(result)
        }

        return results.sorted { $0.0 < $1.0 }.map { $0.1 }
    }
}

// MARK: - First Success Pattern

func firstSuccess<T>(
    operations: [() async throws -> T]
) async throws -> T {
    try await withThrowingTaskGroup(of: T.self) { group in
        for operation in operations {
            group.addTask {
                try await operation()
            }
        }

        // Return first successful result
        if let result = try await group.next() {
            group.cancelAll()
            return result
        }

        throw ConcurrencyError.allOperationsFailed
    }
}

enum ConcurrencyError: Error {
    case allOperationsFailed
    case timeout
}

// MARK: - Race Pattern

func race<T>(
    _ operations: (() async throws -> T)...
) async throws -> T {
    try await withThrowingTaskGroup(of: T.self) { group in
        for operation in operations {
            group.addTask {
                try await operation()
            }
        }

        guard let result = try await group.next() else {
            throw ConcurrencyError.allOperationsFailed
        }

        group.cancelAll()
        return result
    }
}

// MARK: - Timeout Pattern

func withTimeout<T>(
    _ duration: Duration,
    operation: @escaping () async throws -> T
) async throws -> T {
    try await withThrowingTaskGroup(of: T.self) { group in
        group.addTask {
            try await operation()
        }

        group.addTask {
            try await Task.sleep(for: duration)
            throw ConcurrencyError.timeout
        }

        guard let result = try await group.next() else {
            throw ConcurrencyError.allOperationsFailed
        }

        group.cancelAll()
        return result
    }
}
```

---

## AsyncSequence Patterns

```swift
// MARK: - Debounced AsyncSequence

struct DebouncedAsyncSequence<Base: AsyncSequence>: AsyncSequence {
    typealias Element = Base.Element

    let base: Base
    let interval: Duration

    struct AsyncIterator: AsyncIteratorProtocol {
        var baseIterator: Base.AsyncIterator
        let interval: Duration
        var lastEmission: ContinuousClock.Instant?

        mutating func next() async throws -> Element? {
            while true {
                guard let element = try await baseIterator.next() else {
                    return nil
                }

                let now = ContinuousClock.now
                if let last = lastEmission,
                   now - last < interval {
                    // Skip this element, continue to next
                    continue
                }

                lastEmission = now
                return element
            }
        }
    }

    func makeAsyncIterator() -> AsyncIterator {
        AsyncIterator(
            baseIterator: base.makeAsyncIterator(),
            interval: interval
        )
    }
}

extension AsyncSequence {
    func debounced(for interval: Duration) -> DebouncedAsyncSequence<Self> {
        DebouncedAsyncSequence(base: self, interval: interval)
    }
}

// MARK: - Chunked AsyncSequence

struct ChunkedAsyncSequence<Base: AsyncSequence>: AsyncSequence {
    typealias Element = [Base.Element]

    let base: Base
    let size: Int

    struct AsyncIterator: AsyncIteratorProtocol {
        var baseIterator: Base.AsyncIterator
        let size: Int

        mutating func next() async throws -> [Base.Element]? {
            var chunk: [Base.Element] = []
            chunk.reserveCapacity(size)

            while chunk.count < size {
                guard let element = try await baseIterator.next() else {
                    return chunk.isEmpty ? nil : chunk
                }
                chunk.append(element)
            }

            return chunk
        }
    }

    func makeAsyncIterator() -> AsyncIterator {
        AsyncIterator(baseIterator: base.makeAsyncIterator(), size: size)
    }
}

extension AsyncSequence {
    func chunked(by size: Int) -> ChunkedAsyncSequence<Self> {
        ChunkedAsyncSequence(base: self, size: size)
    }
}

// MARK: - AsyncStream Builders

extension AsyncStream {
    static func from<S: Sequence>(_ sequence: S) -> AsyncStream<Element> where S.Element == Element {
        AsyncStream { continuation in
            for element in sequence {
                continuation.yield(element)
            }
            continuation.finish()
        }
    }

    static func timer(
        interval: Duration,
        clock: ContinuousClock = .continuous
    ) -> AsyncStream<ContinuousClock.Instant> {
        AsyncStream { continuation in
            let task = Task {
                while !Task.isCancelled {
                    try? await Task.sleep(for: interval)
                    if Task.isCancelled { break }
                    continuation.yield(clock.now)
                }
                continuation.finish()
            }

            continuation.onTermination = { _ in
                task.cancel()
            }
        }
    }
}
```

---

## Continuation Bridges

```swift
// MARK: - Callback to Async

func withCallback<T>(
    _ operation: (@escaping (Result<T, Error>) -> Void) -> Void
) async throws -> T {
    try await withCheckedThrowingContinuation { continuation in
        operation { result in
            continuation.resume(with: result)
        }
    }
}

// MARK: - Delegate to AsyncStream

protocol LocationDelegate: AnyObject {
    func didUpdateLocation(_ location: CLLocation)
    func didFailWithError(_ error: Error)
}

class LocationManager {
    private var continuation: AsyncThrowingStream<CLLocation, Error>.Continuation?

    func startUpdating() -> AsyncThrowingStream<CLLocation, Error> {
        AsyncThrowingStream { continuation in
            self.continuation = continuation

            continuation.onTermination = { @Sendable [weak self] _ in
                self?.stopUpdating()
            }

            // Start location updates...
        }
    }

    func stopUpdating() {
        continuation?.finish()
        continuation = nil
    }

    // Called by CLLocationManager delegate
    func locationManager(
        _ manager: CLLocationManager,
        didUpdateLocations locations: [CLLocation]
    ) {
        for location in locations {
            continuation?.yield(location)
        }
    }

    func locationManager(
        _ manager: CLLocationManager,
        didFailWithError error: Error
    ) {
        continuation?.finish(throwing: error)
    }
}

// MARK: - NotificationCenter to AsyncSequence

extension NotificationCenter {
    func notifications(
        named name: Notification.Name,
        object: AnyObject? = nil
    ) -> AsyncStream<Notification> {
        AsyncStream { continuation in
            let observer = addObserver(
                forName: name,
                object: object,
                queue: nil
            ) { notification in
                continuation.yield(notification)
            }

            continuation.onTermination = { @Sendable [weak self] _ in
                self?.removeObserver(observer)
            }
        }
    }
}

// Usage
func observeKeyboardNotifications() async {
    for await notification in NotificationCenter.default.notifications(
        named: UIResponder.keyboardWillShowNotification
    ) {
        let frame = notification.userInfo?[UIResponder.keyboardFrameEndUserInfoKey] as? CGRect
        // Handle keyboard frame
    }
}
```

---

## MainActor Patterns

```swift
// MARK: - MainActor ViewModel Base

@MainActor
class BaseViewModel: ObservableObject {
    @Published private(set) var isLoading = false
    @Published private(set) var error: Error?

    private var currentTask: Task<Void, Never>?

    func load<T>(
        _ operation: @escaping () async throws -> T,
        onSuccess: @escaping (T) -> Void
    ) {
        currentTask?.cancel()

        currentTask = Task {
            isLoading = true
            error = nil

            do {
                let result = try await operation()
                if !Task.isCancelled {
                    onSuccess(result)
                }
            } catch is CancellationError {
                // Ignore cancellation
            } catch {
                self.error = error
            }

            isLoading = false
        }
    }

    func cancel() {
        currentTask?.cancel()
        currentTask = nil
    }

    deinit {
        currentTask?.cancel()
    }
}

// MARK: - Sendable View Model Data

// Data that needs to cross actor boundaries should be Sendable
struct ViewModelData: Sendable {
    let items: [Item]
    let totalCount: Int
    let lastUpdated: Date
}

// Use nonisolated for Sendable computed properties
@MainActor
final class ItemsViewModel: ObservableObject {
    @Published private(set) var data: ViewModelData?

    nonisolated var itemCount: Int {
        // Safe because ViewModelData is Sendable
        // But we need to access it on MainActor
        MainActor.assumeIsolated {
            data?.totalCount ?? 0
        }
    }
}

// MARK: - Background Processing with MainActor Results

@MainActor
final class ImageProcessingViewModel: ObservableObject {
    @Published private(set) var processedImage: UIImage?
    @Published private(set) var isProcessing = false

    func processImage(_ image: UIImage) async {
        isProcessing = true

        // Offload heavy work to background
        let result = await Task.detached(priority: .userInitiated) {
            // Heavy image processing
            self.applyFilters(to: image)
        }.value

        // Back on MainActor
        processedImage = result
        isProcessing = false
    }

    nonisolated private func applyFilters(to image: UIImage) -> UIImage {
        // CPU-intensive work here
        // This runs off the MainActor
        return image
    }
}
```
