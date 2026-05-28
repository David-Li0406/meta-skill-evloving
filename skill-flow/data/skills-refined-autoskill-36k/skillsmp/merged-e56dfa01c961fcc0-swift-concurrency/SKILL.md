---
name: swift-concurrency
description: Use this skill for expert guidance on Swift 6 concurrency concepts, including async/await, actors, MainActor, Sendable, and thread safety. Ideal for addressing data races, migrating from GCD, or implementing modern concurrency patterns.
---

# Swift Concurrency

This skill provides comprehensive guidance on Swift's concurrency system, covering async/await patterns, actors, Sendable conformance, and migration to Swift 6. Use this skill to help developers write safe, performant concurrent code and navigate the complexities of Swift's structured concurrency model.

## Core Concepts

### Isolation Domains

- **MainActor**: Handles all UI interactions; only one exists.
- **Actors**: Protect their own mutable state with exclusive access.
- **Nonisolated**: Code that opts out of actor isolation, allowing shared access.
- **Sendable**: Types that can safely cross isolation boundaries.

### Async/Await Basics

An `async` function can pause. Use `await` to suspend until work finishes:

```swift
func fetchUser(id: Int) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}
```

For parallel work, use `async let`:

```swift
async let avatar = fetchImage("avatar.jpg")
async let banner = fetchImage("banner.jpg")
return Profile(avatar: try await avatar, banner: try await banner)
```

### Task Management

A `Task` is a unit of async work you can manage:

```swift
let task = Task {
    await performWork()
}

// Task with cancellation
func performWork() async throws {
    for item in items {
        try Task.checkCancellation()  // Throws if cancelled
        await process(item)
    }
}
```

### Task Groups

Use task groups for structured concurrency:

```swift
func fetchAllUsers(ids: [Int]) async throws -> [User] {
    try await withThrowingTaskGroup(of: User.self) { group in
        for id in ids {
            group.addTask {
                try await fetchUser(id: id)
            }
        }

        var users: [User] = []
        for try await user in group {
            users.append(user)
        }
        return users
    }
}
```

### Actors

Actors protect their own mutable state:

```swift
actor BankAccount {
    private var balance: Decimal = 0

    func deposit(_ amount: Decimal) {
        balance += amount
    }

    func getBalance() -> Decimal {
        balance
    }
}

// Usage
let account = BankAccount()
await account.deposit(100)
let balance = await account.getBalance()
```

### Sendable Protocol

Sendable types can be safely passed across isolation boundaries:

```swift
struct User: Sendable {
    let id: Int
    let name: String
}

// Non-Sendable example
class Counter {
    var count = 0
}
```

### @MainActor

Use `@MainActor` for UI-related code:

```swift
@MainActor
class ViewModel: ObservableObject {
    @Published var items: [Item] = []
    @Published var isLoading = false

    func loadItems() async {
        isLoading = true
        defer { isLoading = false }
        items = await fetchItems()
    }
}
```

## Common Pitfalls

1. **Blocking the main thread**: Avoid using DispatchQueue in async code; use MainActor instead.
2. **Creating too many actors**: Only create actors when you have shared mutable state that can't be on MainActor.
3. **Making everything Sendable**: Not all data needs to cross isolation boundaries.

## Best Practices

1. **Prefer structured concurrency**: Use task groups over unstructured tasks.
2. **Make types Sendable**: Design for thread safety from the start.
3. **Use actors for shared mutable state**: Avoid locks in Swift 6.
4. **Isolate UI code to MainActor**: Use @MainActor for ViewModels.
5. **Handle cancellation**: Check `Task.isCancelled` in long operations.
6. **Test concurrent code**: Use proper async test methods and consider timing issues.

## Further Reading

- [Swift Concurrency Documentation](https://docs.swift.org/swift-book/documentation/the-swift-programming-language/concurrency/)
- [Migrating to Swift 6](https://www.swift.org/migration/documentation/migrationguide/)
- [WWDC21: Meet async/await](https://developer.apple.com/videos/play/wwdc2021/10132/)
- [WWDC21: Protect mutable state with actors](https://developer.apple.com/videos/play/wwdc2021/10133/)