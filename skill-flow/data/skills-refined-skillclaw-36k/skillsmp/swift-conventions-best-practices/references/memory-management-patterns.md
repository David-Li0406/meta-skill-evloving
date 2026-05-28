# Swift Conventions — Memory Management Patterns

> **Loading Trigger**: Load when debugging memory leaks, retain cycles, or implementing complex closure patterns.

---

## Retain Cycle Detection and Prevention

```swift
// MARK: - Common Retain Cycle Patterns

// ❌ Pattern 1: Closure stored as property
class BadExample1 {
    var onComplete: (() -> Void)?

    func setup() {
        onComplete = {
            self.doSomething() // Strong capture → retain cycle
        }
    }
}

// ✅ Fix: Weak capture
class GoodExample1 {
    var onComplete: (() -> Void)?

    func setup() {
        onComplete = { [weak self] in
            self?.doSomething()
        }
    }
}

// ❌ Pattern 2: Delegate without weak
class BadExample2 {
    var delegate: SomeDelegate? // Strong reference to delegate
}

// ✅ Fix: Weak delegate
class GoodExample2 {
    weak var delegate: SomeDelegate?
}

// ❌ Pattern 3: Timer with target
class BadExample3 {
    var timer: Timer?

    func startTimer() {
        timer = Timer.scheduledTimer(
            timeInterval: 1.0,
            target: self, // Strong reference to self
            selector: #selector(tick),
            userInfo: nil,
            repeats: true
        )
    }
}

// ✅ Fix: Block-based timer + invalidation
class GoodExample3 {
    var timer: Timer?

    func startTimer() {
        timer = Timer.scheduledTimer(withTimeInterval: 1.0, repeats: true) { [weak self] _ in
            self?.tick()
        }
    }

    deinit {
        timer?.invalidate()
    }
}

// ❌ Pattern 4: NotificationCenter observer
class BadExample4 {
    init() {
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(handleNotification),
            name: .someNotification,
            object: nil
        )
        // Never removed → object can't deallocate
    }
}

// ✅ Fix: Store observer and remove in deinit
class GoodExample4 {
    private var observer: NSObjectProtocol?

    init() {
        observer = NotificationCenter.default.addObserver(
            forName: .someNotification,
            object: nil,
            queue: .main
        ) { [weak self] notification in
            self?.handleNotification(notification)
        }
    }

    deinit {
        if let observer = observer {
            NotificationCenter.default.removeObserver(observer)
        }
    }
}

// ❌ Pattern 5: Combine publishers
class BadExample5: ObservableObject {
    private var cancellables = Set<AnyCancellable>()

    init() {
        somePublisher
            .sink { value in
                self.handle(value) // Strong capture
            }
            .store(in: &cancellables)
    }
}

// ✅ Fix: Weak capture in sink
class GoodExample5: ObservableObject {
    private var cancellables = Set<AnyCancellable>()

    init() {
        somePublisher
            .sink { [weak self] value in
                self?.handle(value)
            }
            .store(in: &cancellables)
    }
}
```

---

## Capture List Patterns

```swift
// MARK: - Understanding Capture Lists

class ClosureCaptures {

    // MARK: - When to use [weak self]

    // Use weak when: closure is stored, async, or escaping
    func storedClosure() {
        let handler: () -> Void = { [weak self] in
            guard let self else { return }
            self.doWork()
        }
        store(handler)
    }

    // MARK: - When to use [unowned self]

    // Use unowned when: you can PROVE self outlives the closure
    // This is rare - prefer weak unless you have a specific reason
    lazy var description: String = { [unowned self] in
        // Safe: lazy property is accessed on self, so self exists
        "\(self.name) - \(self.id)"
    }()

    // MARK: - When capture is unnecessary

    // No capture needed: non-escaping closures
    func processItems() {
        items.forEach { item in
            self.process(item) // Safe: forEach is synchronous
        }

        items.map { item in
            self.transform(item) // Safe: map is synchronous
        }
    }

    // MARK: - Capturing multiple values

    func complexCapture() {
        let userId = self.user.id  // Capture value, not self
        let handler: () -> Void = { [userId] in
            // Uses captured userId, doesn't retain self
            API.fetch(userId: userId)
        }
    }

    // MARK: - guard let self pattern

    func modernWeakSelf() {
        asyncOperation { [weak self] in
            guard let self else { return }
            // Now use self without optional chaining
            self.updateUI()
            self.saveState()
        }
    }

    // MARK: - Capturing value vs reference

    var count = 0

    func captureValue() {
        let currentCount = count // Capture VALUE
        asyncOperation { [currentCount] in
            print(currentCount) // Prints value at capture time
        }
    }

    func captureReference() {
        asyncOperation { [weak self] in
            print(self?.count ?? 0) // Prints current value
        }
    }
}
```

---

## Task Cancellation and Cleanup

```swift
// MARK: - Proper Task Management

@MainActor
final class ViewModel: ObservableObject {
    @Published private(set) var data: [Item] = []
    @Published private(set) var isLoading = false

    private var loadTask: Task<Void, Never>?

    // MARK: - Task Lifecycle

    func loadData() {
        // Cancel any existing task
        loadTask?.cancel()

        loadTask = Task {
            isLoading = true
            defer { isLoading = false }

            do {
                // Check cancellation at checkpoints
                try Task.checkCancellation()

                let items = try await fetchItems()

                // Check again after async work
                try Task.checkCancellation()

                data = items
            } catch is CancellationError {
                // Don't set error state for cancellation
                return
            } catch {
                // Handle real errors
                self.error = error
            }
        }
    }

    func cancel() {
        loadTask?.cancel()
        loadTask = nil
    }

    deinit {
        loadTask?.cancel()
    }
}

// MARK: - TaskGroup Cleanup

func processWithCleanup() async throws {
    try await withThrowingTaskGroup(of: Void.self) { group in
        for item in items {
            group.addTask {
                try await process(item)
            }
        }

        // If any task fails, cancel all others
        do {
            try await group.waitForAll()
        } catch {
            group.cancelAll() // Explicit cleanup
            throw error
        }
    }
}

// MARK: - Actor-based Resource Management

actor ResourceManager {
    private var resources: [String: Resource] = [:]
    private var acquireCount: [String: Int] = [:]

    func acquire(id: String) async throws -> Resource {
        if let existing = resources[id] {
            acquireCount[id, default: 0] += 1
            return existing
        }

        let resource = try await loadResource(id: id)
        resources[id] = resource
        acquireCount[id] = 1
        return resource
    }

    func release(id: String) {
        guard let count = acquireCount[id] else { return }

        if count > 1 {
            acquireCount[id] = count - 1
        } else {
            acquireCount.removeValue(forKey: id)
            resources.removeValue(forKey: id)
        }
    }

    func releaseAll() {
        resources.removeAll()
        acquireCount.removeAll()
    }
}
```

---

## Memory Leak Detection

```swift
// MARK: - Debug Helpers

#if DEBUG

/// Tracks allocations in debug builds
final class AllocationTracker {
    static var allocations: [String: Int] = [:]
    private static let lock = NSLock()

    static func track(_ type: Any.Type) {
        lock.lock()
        defer { lock.unlock() }

        let name = String(describing: type)
        allocations[name, default: 0] += 1
    }

    static func untrack(_ type: Any.Type) {
        lock.lock()
        defer { lock.unlock() }

        let name = String(describing: type)
        if let count = allocations[name], count > 1 {
            allocations[name] = count - 1
        } else {
            allocations.removeValue(forKey: name)
        }
    }

    static func printLeaks() {
        lock.lock()
        defer { lock.unlock() }

        if allocations.isEmpty {
            print("✅ No tracked allocations remaining")
        } else {
            print("⚠️ Potential leaks:")
            for (type, count) in allocations.sorted(by: { $0.value > $1.value }) {
                print("  \(type): \(count)")
            }
        }
    }
}

/// Add to classes to track allocations
class TrackedObject {
    init() {
        AllocationTracker.track(type(of: self))
    }

    deinit {
        AllocationTracker.untrack(type(of: self))
    }
}

// Usage: Make ViewModels inherit from TrackedObject in debug builds
#endif

// MARK: - Leak Detection in Tests

final class MemoryLeakTests: XCTestCase {

    func testViewModelDoesNotLeak() {
        var viewModel: UserViewModel? = UserViewModel()
        weak var weakVM = viewModel

        // Use the view model
        viewModel?.loadUser()

        // Release strong reference
        viewModel = nil

        // Verify deallocation
        XCTAssertNil(weakVM, "UserViewModel should be deallocated")
    }

    func testClosureDoesNotRetain() async {
        var service: UserService? = UserService()
        weak var weakService = service

        // Create closure that captures service
        let task = Task { [weak service] in
            _ = try? await service?.fetchUser(id: "123")
        }

        // Wait for task
        await task.value

        // Release service
        service = nil

        // Verify deallocation
        XCTAssertNil(weakService, "UserService should be deallocated")
    }
}
```

---

## Value Type Memory Patterns

```swift
// MARK: - Copy-on-Write Understanding

struct COWExample {
    private var storage: COWStorage

    init(data: [Int]) {
        storage = COWStorage(data: data)
    }

    var data: [Int] {
        get { storage.data }
        set {
            // Copy only if shared
            if !isKnownUniquelyReferenced(&storage) {
                storage = COWStorage(data: newValue)
            } else {
                storage.data = newValue
            }
        }
    }
}

private final class COWStorage {
    var data: [Int]
    init(data: [Int]) { self.data = data }
}

// MARK: - When COW Breaks

// ❌ Reference type inside value type breaks COW
struct BrokenCOW {
    var items: NSMutableArray // Reference type!
}

var a = BrokenCOW(items: NSMutableArray())
var b = a  // Both point to same NSMutableArray
b.items.add(1)  // Mutates a.items too!

// ✅ Use Swift array instead
struct CorrectCOW {
    var items: [Any]  // Value type with COW
}

// MARK: - Large Value Types

// For large value types that are copied often, consider indirect storage
struct LargeStruct {
    // Direct storage - copied fully on every copy
    var largeArray: [LargeObject]  // Expensive copies
}

// Better: Use reference semantics internally
struct OptimizedLargeStruct {
    private var storage: Storage

    private final class Storage {
        var largeArray: [LargeObject]
        init(largeArray: [LargeObject]) {
            self.largeArray = largeArray
        }
    }

    init(largeArray: [LargeObject]) {
        storage = Storage(largeArray: largeArray)
    }

    // Implement COW for mutations
    var largeArray: [LargeObject] {
        get { storage.largeArray }
        set {
            if !isKnownUniquelyReferenced(&storage) {
                storage = Storage(largeArray: newValue)
            } else {
                storage.largeArray = newValue
            }
        }
    }
}
```
