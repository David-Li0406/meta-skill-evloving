// MARK: - @unchecked Sendable
// 内部で同期処理を行う場合の @unchecked Sendable の使用例

import Foundation

// MARK: - ロックを使った Thread-Safe Cache

/// @unchecked Sendable は、コンパイラの Sendable チェックをバイパスする
/// 内部で適切な同期処理を行っている場合にのみ使用すること
final class ThreadSafeCache<Key: Hashable & Sendable, Value: Sendable>: @unchecked Sendable {
    private let lock = NSLock()
    private var storage: [Key: Value] = [:]

    func get(_ key: Key) -> Value? {
        lock.lock()
        defer { lock.unlock() }
        return storage[key]
    }

    func set(_ key: Key, value: Value) {
        lock.lock()
        defer { lock.unlock() }
        storage[key] = value
    }

    func remove(_ key: Key) {
        lock.lock()
        defer { lock.unlock() }
        storage.removeValue(forKey: key)
    }

    func clear() {
        lock.lock()
        defer { lock.unlock() }
        storage.removeAll()
    }

    var count: Int {
        lock.lock()
        defer { lock.unlock() }
        return storage.count
    }
}

// MARK: - DispatchQueue を使った同期

/// DispatchQueue による同期
final class QueueSynchronizedStore: @unchecked Sendable {
    private let queue = DispatchQueue(label: "com.app.store", attributes: .concurrent)
    private var _items: [String] = []

    var items: [String] {
        queue.sync { _items }
    }

    func append(_ item: String) {
        queue.async(flags: .barrier) {
            self._items.append(item)
        }
    }

    func removeAll() {
        queue.async(flags: .barrier) {
            self._items.removeAll()
        }
    }
}

// MARK: - os_unfair_lock を使った高性能ロック

import os

/// os_unfair_lock は NSLock より高速だが、使用には注意が必要
final class UnfairLockProtectedValue<T: Sendable>: @unchecked Sendable {
    private var _lock = os_unfair_lock()
    private var _value: T

    init(_ value: T) {
        _value = value
    }

    var value: T {
        os_unfair_lock_lock(&_lock)
        defer { os_unfair_lock_unlock(&_lock) }
        return _value
    }

    func withLock<R>(_ body: (inout T) throws -> R) rethrows -> R {
        os_unfair_lock_lock(&_lock)
        defer { os_unfair_lock_unlock(&_lock) }
        return try body(&_value)
    }
}

// MARK: - 使用例

func demonstrateUncheckedSendable() async {
    let cache = ThreadSafeCache<String, Int>()

    // 複数の Task から安全にアクセス
    await withTaskGroup(of: Void.self) { group in
        for i in 0..<100 {
            group.addTask {
                cache.set("key\(i)", value: i)
            }
        }
    }

    print("Cache count: \(cache.count)")

    // UnfairLockProtectedValue の使用例
    let counter = UnfairLockProtectedValue(0)

    await withTaskGroup(of: Void.self) { group in
        for _ in 0..<1000 {
            group.addTask {
                counter.withLock { $0 += 1 }
            }
        }
    }

    print("Counter: \(counter.value)")  // 1000
}

// MARK: - 警告: @unchecked Sendable の危険性

/// ⚠️ @unchecked Sendable は慎重に使用すること
/// 以下のような場合は使用しないこと:

// BAD: 同期処理なしで @unchecked Sendable を使用
// final class UnsafeExample: @unchecked Sendable {
//     var value: Int = 0  // データ競合の危険！
//
//     func increment() {
//         value += 1  // 複数スレッドから呼ばれると壊れる
//     }
// }

// MARK: - 推奨: Actor を使う方が安全

/// ほとんどの場合、actor を使う方が安全で簡単
actor SafeCache<Key: Hashable, Value> {
    private var storage: [Key: Value] = [:]

    func get(_ key: Key) -> Value? {
        storage[key]
    }

    func set(_ key: Key, value: Value) {
        storage[key] = value
    }
}

// actor を使う場合は await が必要だが、データ競合の心配がない
func useActorCache() async {
    let cache = SafeCache<String, Int>()
    await cache.set("key", value: 42)
    let value = await cache.get("key")
    print("Value: \(value ?? 0)")
}
