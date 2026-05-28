# Swift Performance Review Guide

Performance-focused review points for Swift code.

## Collection Operations

### Array Performance

```swift
// INEFFICIENT: Appending in loop without capacity
var items: [Item] = []
for i in 0..<1000 {
    items.append(Item(id: i))  // Multiple reallocations
}

// EFFICIENT: Reserve capacity
var items: [Item] = []
items.reserveCapacity(1000)
for i in 0..<1000 {
    items.append(Item(id: i))
}

// BEST: Use map
let items = (0..<1000).map { Item(id: $0) }
```

### Dictionary Performance

```swift
// INEFFICIENT: Checking existence then accessing
if dictionary.keys.contains(key) {
    let value = dictionary[key]!
}

// EFFICIENT: Use optional binding
if let value = dictionary[key] {
    // use value
}

// For default values
let value = dictionary[key, default: defaultValue]
```

### Set vs Array for Lookups

```swift
// INEFFICIENT: O(n) lookup
let userIds = [1, 2, 3, 4, 5]
if userIds.contains(targetId) { }  // Searches entire array

// EFFICIENT: O(1) lookup
let userIdSet: Set<Int> = [1, 2, 3, 4, 5]
if userIdSet.contains(targetId) { }  // Hash lookup
```

## String Operations

### String Concatenation

```swift
// INEFFICIENT: String concatenation in loop
var result = ""
for item in items {
    result += item.name + ", "  // Creates new string each time
}

// EFFICIENT: Use joined
let result = items.map(\.name).joined(separator: ", ")
```

### String Comparison

```swift
// INEFFICIENT: Case-insensitive comparison
if string1.lowercased() == string2.lowercased() { }  // Creates new strings

// EFFICIENT: Use comparison option
if string1.caseInsensitiveCompare(string2) == .orderedSame { }

// Or for equality
if string1.localizedCaseInsensitiveCompare(string2) == .orderedSame { }
```

## Object Creation

### Expensive Object Caching

```swift
// INEFFICIENT: Creating formatter each call
func formatDate(_ date: Date) -> String {
    let formatter = DateFormatter()  // Expensive
    formatter.dateStyle = .medium
    return formatter.string(from: date)
}

// EFFICIENT: Cache formatter
private static let dateFormatter: DateFormatter = {
    let formatter = DateFormatter()
    formatter.dateStyle = .medium
    return formatter
}()

func formatDate(_ date: Date) -> String {
    Self.dateFormatter.string(from: date)
}
```

### Regex Caching

```swift
// INEFFICIENT: Compiling regex each call
func isValidEmail(_ email: String) -> Bool {
    let pattern = "[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}"
    return email.range(of: pattern, options: .regularExpression) != nil
}

// EFFICIENT: Compile once
private static let emailRegex = try? Regex("[A-Z0-9a-z._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}")

func isValidEmail(_ email: String) -> Bool {
    guard let regex = Self.emailRegex else { return false }
    return email.contains(regex)
}
```

## SwiftUI Performance

### Avoiding Unnecessary Recomputation

```swift
// INEFFICIENT: Computed in body
struct ItemList: View {
    let items: [Item]

    var body: some View {
        // Sorted on every render
        List(items.sorted(by: { $0.date > $1.date })) { item in
            ItemRow(item: item)
        }
    }
}

// EFFICIENT: Compute only when needed
struct ItemList: View {
    let items: [Item]

    private var sortedItems: [Item] {
        items.sorted(by: { $0.date > $1.date })
    }

    var body: some View {
        List(sortedItems) { item in
            ItemRow(item: item)
        }
    }
}

// BEST: Sort at data layer
```

### View Identity

```swift
// INEFFICIENT: Missing stable ID
ForEach(items.indices, id: \.self) { index in
    ItemRow(item: items[index])  // Entire list re-renders on change
}

// EFFICIENT: Stable identifiers
ForEach(items) { item in  // Assumes Item: Identifiable
    ItemRow(item: item)
}
```

### Object Creation in Views

```swift
// INEFFICIENT: New object every render
struct BadView: View {
    var body: some View {
        ChildView(config: Config(size: .large))  // New Config each render
    }
}

// EFFICIENT: Constant or memoized
private let config = Config(size: .large)

struct GoodView: View {
    var body: some View {
        ChildView(config: config)
    }
}
```

## Memory Performance

### Lazy Initialization

```swift
// EAGER: Computed even if never used
class ViewModel {
    let expensiveData = loadExpensiveData()  // Always computed
}

// LAZY: Computed only when accessed
class ViewModel {
    lazy var expensiveData = loadExpensiveData()  // Computed on first access
}
```

### Value Types vs Reference Types

```swift
// Consider value type for small, frequently copied data
struct Point {  // Copied on assignment
    var x: Double
    var y: Double
}

// Use reference type for:
// - Identity matters (same instance)
// - Expensive to copy
// - Shared mutable state
class DataManager {
    var cache: [String: Data] = [:]
}
```

### Copy-on-Write

```swift
// Swift collections use CoW
var array1 = [1, 2, 3]
var array2 = array1  // No copy yet (shared storage)
array2.append(4)  // Now copied (separate storage)

// Custom CoW for reference types
struct OptimizedData {
    private var storage: Storage

    mutating func modify() {
        if !isKnownUniquelyReferenced(&storage) {
            storage = storage.copy()
        }
        // Now safe to modify
    }
}
```

## Async/Await Performance

### Parallel Execution

```swift
// SEQUENTIAL: Slow
func loadData() async throws -> DashboardData {
    let user = try await fetchUser()
    let posts = try await fetchPosts()  // Waits for user
    let comments = try await fetchComments()  // Waits for posts
    return DashboardData(user: user, posts: posts, comments: comments)
}

// PARALLEL: Fast
func loadData() async throws -> DashboardData {
    async let user = fetchUser()
    async let posts = fetchPosts()
    async let comments = fetchComments()

    return try await DashboardData(
        user: user,
        posts: posts,
        comments: comments
    )
}
```

### Task Group for Dynamic Work

```swift
// Process many items in parallel
func processAll(ids: [String]) async throws -> [Result] {
    try await withThrowingTaskGroup(of: Result.self) { group in
        for id in ids {
            group.addTask {
                try await process(id: id)
            }
        }

        var results: [Result] = []
        results.reserveCapacity(ids.count)

        for try await result in group {
            results.append(result)
        }

        return results
    }
}
```

## Performance Review Checklist

- [ ] Collection operations are efficient (no unnecessary iterations)
- [ ] Expensive objects (formatters, regex) are cached
- [ ] SwiftUI views have stable identifiers
- [ ] Objects aren't created unnecessarily in view body
- [ ] Lazy initialization for expensive computed properties
- [ ] Parallel async execution where independent
- [ ] Capacity reserved for collections with known size
- [ ] Set used for frequent lookups instead of Array
- [ ] String concatenation uses efficient methods
