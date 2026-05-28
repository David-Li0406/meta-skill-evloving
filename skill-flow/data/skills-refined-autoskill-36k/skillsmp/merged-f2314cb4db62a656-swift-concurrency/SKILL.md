---
name: swift-concurrency
description: Expert guidance on Swift Concurrency best practices, patterns, and implementation. Use this skill when developers mention Swift Concurrency, async/await, actors, tasks, or related performance and safety issues.
---

# Swift Concurrency

## Overview

This skill provides expert guidance on Swift Concurrency, covering modern async/await patterns, actors, tasks, Sendable conformance, and migration to Swift 6. Use this skill to help developers write safe, performant concurrent code and navigate the complexities of Swift's structured concurrency model.

## Agent Behavior Contract (Follow These Rules)

1. Analyze the project/package file to determine the Swift language mode (Swift 5.x vs Swift 6) and the Xcode/Swift toolchain used.
2. Identify the isolation boundary: `@MainActor`, custom actor, actor instance isolation, or nonisolated before proposing fixes.
3. Do not recommend `@MainActor` as a blanket fix; justify its use based on the code context.
4. Prefer structured concurrency (child tasks, task groups) over unstructured tasks. Use `Task.detached` only with a clear reason.
5. If recommending `@preconcurrency`, `@unchecked Sendable`, or `nonisolated(unsafe)`, require:
   - A documented safety invariant.
   - A follow-up ticket to remove or migrate it.
6. For migration work, optimize for minimal blast radius (small, reviewable changes) and add verification steps.
7. Use course references sparingly and only when they clearly help answer the developer’s question.

## Project Settings Intake (Evaluate Before Advising)

Concurrency behavior depends on build settings. Always try to determine:

- Default actor isolation (is the module default `@MainActor` or `nonisolated`?)
- Strict concurrency checking level (minimal/targeted/complete)
- Whether upcoming features are enabled (especially `NonisolatedNonsendingByDefault`)
- Swift language mode (Swift 5.x vs Swift 6) and SwiftPM tools version

### Manual checks (no scripts)

- **SwiftPM**:
  - Check `Package.swift` for `.defaultIsolation(MainActor.self)`.
  - Check for strict concurrency flags: `.enableExperimentalFeature("StrictConcurrency=targeted")` (or similar).
  - Check tools version at the top: `// swift-tools-version: ...`
- **Xcode projects**:
  - Search `project.pbxproj` for:
    - `SWIFT_DEFAULT_ACTOR_ISOLATION`
    - `SWIFT_STRICT_CONCURRENCY`
    - `SWIFT_UPCOMING_FEATURE_` (and/or `SWIFT_ENABLE_EXPERIMENTAL_FEATURES`)

If any of these are unknown, ask the developer to confirm them before giving migration-sensitive guidance.

## Quick Decision Tree

When a developer needs concurrency guidance, follow this decision tree:

1. **Starting fresh with async code?**
   - Read `references/async-await-basics.md` for foundational patterns.
   - For parallel operations → `references/tasks.md` (async let, task groups).

2. **Protecting shared mutable state?**
   - Need to protect class-based state → `references/actors.md` (actors, @MainActor).
   - Need thread-safe value passing → `references/sendable.md` (Sendable conformance).

3. **Managing async operations?**
   - Structured async work → `references/tasks.md` (Task, child tasks, cancellation).
   - Streaming data → `references/async-sequences.md` (AsyncSequence, AsyncStream).

4. **Working with legacy frameworks?**
   - Core Data integration → `references/core-data.md`.
   - General migration → `references/migration.md`.

5. **Performance or debugging issues?**
   - Slow async code → `references/performance.md` (profiling, suspension points).
   - Testing concerns → `references/testing.md` (XCTest, Swift Testing).

6. **Understanding threading behavior?**
   - Read `references/threading.md` for thread/task relationship and isolation.

7. **Memory issues with tasks?**
   - Read `references/memory-management.md` for retain cycle prevention.

## Triage-First Playbook (Common Errors -> Next Best Move)

- **SwiftLint concurrency-related warnings**:
  - Use `references/linting.md` for rule intent and preferred fixes; avoid dummy awaits as “fixes”.
- **SwiftLint `async_without_await` warning**:
  - Remove `async` if not required; if required by protocol/override/@concurrent, prefer narrow suppression over adding fake awaits.
- **"Sending value of non-Sendable type ... risks causing data races"**:
  - Identify where the value crosses an isolation boundary and use `references/sendable.md` and `references/threading.md`.
- **"Main actor-isolated ... cannot be used from a nonisolated context"**:
  - Decide if it truly belongs on `@MainActor` and use `references/actors.md` and `references/threading.md`.
- **"Class property 'current' is unavailable from asynchronous contexts"**:
  - Use `references/threading.md` to avoid thread-centric debugging and rely on isolation + Instruments.
- **XCTest async errors like "wait(...) is unavailable from asynchronous contexts"**:
  - Use `references/testing.md` for proper async test methods.
- **Core Data concurrency warnings/errors**:
  - Use `references/core-data.md` for handling NSManagedObject sendability and isolation conflicts.

## Core Patterns Reference

### When to Use Each Concurrency Tool

**async/await** - Making existing synchronous code asynchronous
```swift
// Use for: Single asynchronous operations
func fetchUser() async throws -> User {
    try await networkClient.get("/user")
}
```

**async let** - Running multiple independent async operations in parallel
```swift
// Use for: Fixed number of parallel operations known at compile time
async let user = fetchUser()
async let posts = fetchPosts()
let profile = try await (user, posts)
```

**Task** - Starting unstructured asynchronous work
```swift
// Use for: Fire-and-forget operations, bridging sync to async contexts
Task {
    await updateUI()
}
```

**Task Group** - Dynamic parallel operations with structured concurrency
```swift
// Use for: Unknown number of parallel operations at compile time
await withTaskGroup(of: Result.self) { group in
    for item in items {
        group.addTask { await process(item) }
    }
}
```

**Actor** - Protecting mutable state from data races
```swift
// Use for: Shared mutable state accessed from multiple contexts
actor DataCache {
    private var cache: [String: Data] = [:]
    func get(_ key: String) -> Data? { cache[key] }
}
```

**@MainActor** - Ensuring UI updates on main thread
```swift
// Use for: View models, UI-related classes
@MainActor
class ViewModel: ObservableObject {
    @Published var data: String = ""
}
```

### Common Scenarios

**Scenario: Network request with UI update**
```swift
Task { @concurrent in
    let data = try await fetchData() // Background
    await MainActor.run {
        self.updateUI(with: data) // Main thread
    }
}
```

**Scenario: Multiple parallel network requests**
```swift
async let users = fetchUsers()
async let posts = fetchPosts()
async let comments = fetchComments()
let (u, p, c) = try await (users, posts, comments)
```

**Scenario: Processing array items in parallel**
```swift
await withTaskGroup(of: ProcessedItem.self) { group in
    for item in items {
        group.addTask { await process(item) }
    }
    for await result in group {
        results.append(result)
    }
}
```

## Swift 6 Migration Quick Guide

Key changes in Swift 6:
- **Strict concurrency checking** enabled by default.
- **Complete data-race safety** at compile time.
- **Sendable requirements** enforced on boundaries.
- **Isolation checking** for all async boundaries.

For detailed migration steps, see `references/migration.md`.

## Reference Files

Load these files as needed for specific topics:

- **`async-await-basics.md`** - async/await syntax, execution order, async let, URLSession patterns.
- **`tasks.md`** - Task lifecycle, cancellation, priorities, task groups, structured vs unstructured.
- **`threading.md`** - Thread/task relationship, suspension points, isolation domains, nonisolated.
- **`memory-management.md`** - Retain cycles in tasks, memory safety patterns.
- **`actors.md`** - Actor isolation, @MainActor, global actors, reentrancy, custom executors, Mutex.
- **`sendable.md`** - Sendable conformance, value/reference types, @unchecked, region isolation.
- **`linting.md`** - Concurrency-focused lint rules and SwiftLint `async_without_await`.
- **`async-sequences.md`** - AsyncSequence, AsyncStream, when to use vs regular async methods.
- **`core-data.md`** - NSManagedObject sendability, custom executors, isolation conflicts.
- **`performance.md`** - Profiling with Instruments, reducing suspension points, execution strategies.
- **`testing.md`** - XCTest async patterns, Swift Testing, concurrency testing utilities.
- **`migration.md`** - Swift 6 migration strategy, closure-to-async conversion, @preconcurrency, FRP migration.

## Best Practices Summary

1. **Prefer structured concurrency** - Use task groups over unstructured tasks when possible.
2. **Minimize suspension points** - Keep actor-isolated sections small to reduce context switches.
3. **Use @MainActor judiciously** - Only for truly UI-related code.
4. **Make types Sendable** - Enable safe concurrent access by conforming to Sendable.
5. **Handle cancellation** - Check Task.isCancelled in long-running operations.
6. **Avoid blocking** - Never use semaphores or locks in async contexts.
7. **Test concurrent code** - Use proper async test methods and consider timing issues.

## Verification Checklist (When You Change Concurrency Code)

- Confirm build settings (default isolation, strict concurrency, upcoming features) before interpreting diagnostics.
- After refactors:
  - Run tests, especially concurrency-sensitive ones.
  - If performance-related, verify with Instruments.
  - If lifetime-related, verify deinit/cancellation behavior.

## Glossary

See `references/glossary.md` for quick definitions of core concurrency terms used across this skill.

---

**Note**: This skill is based on the comprehensive [Swift Concurrency Course](https://www.swiftconcurrencycourse.com?utm_source=github&utm_medium=agent-skill&utm_campaign=skill-footer) by Antoine van der Lee.