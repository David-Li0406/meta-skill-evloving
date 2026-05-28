// MARK: - @Sendable Closures
// @Sendable クロージャの使用例とキャプチャリストの注意点

import Foundation
import SwiftUI

// MARK: - 基本的な @Sendable クロージャ

/// Task のクロージャは暗黙的に @Sendable
func basicSendableClosure() {
    let message = "Hello"  // String は Sendable

    Task {
        // message をキャプチャ（Sendable なので OK）
        print(message)
    }
}

/// 明示的な @Sendable 属性
func explicitSendable() {
    let handler: @Sendable () -> Void = {
        print("This is a sendable closure")
    }

    Task {
        handler()
    }
}

// MARK: - @Sendable クロージャを受け取る関数

/// @Sendable @escaping クロージャをパラメータに持つ関数
func performAsync(
    work: @Sendable @escaping () async -> Void
) {
    Task {
        await work()
    }
}

/// 結果を返す @Sendable クロージャ
func performAsyncWithResult<T: Sendable>(
    work: @Sendable @escaping () async throws -> T
) async throws -> T {
    try await work()
}

// MARK: - キャプチャリストの注意点

@MainActor
class ViewController {
    var count = 0
    let id = UUID()

    func demonstrateCaptures() {
        // ✅ GOOD: Task は MainActor を継承
        Task {
            self.count += 1  // OK - MainActor コンテキスト内
        }

        // ❌ BAD: Task.detached は MainActor から切り離される
        // Task.detached {
        //     self.count += 1  // Error: Actor-isolated property
        // }

        // ✅ GOOD: MainActor.run で明示的に MainActor に戻る
        Task.detached {
            await MainActor.run {
                self.count += 1  // OK
            }
        }

        // ✅ GOOD: let プロパティは nonisolated でアクセス可能
        Task.detached { [id = self.id] in
            print("ID: \(id)")  // OK - id は Sendable な UUID
        }
    }
}

// MARK: - Sendable な値のキャプチャ

struct UserData: Sendable {
    let name: String
    let age: Int
}

func capturesSendableValue() {
    let user = UserData(name: "Alice", age: 30)

    // Sendable な値はキャプチャ可能
    Task.detached {
        print("User: \(user.name), Age: \(user.age)")
    }
}

// MARK: - 非 Sendable 型のキャプチャを避ける

/// 非 Sendable クラス
class NonSendableLogger {
    func log(_ message: String) {
        print("[LOG] \(message)")
    }
}

func avoidNonSendableCapture() {
    let logger = NonSendableLogger()

    // ❌ BAD: 非 Sendable 型をキャプチャ
    // Task.detached {
    //     logger.log("message")  // Error: Capture of 'logger' with non-sendable type
    // }

    // ✅ GOOD: actor を使用
    let safeLogger = SafeLogger()
    Task.detached {
        await safeLogger.log("message")
    }
}

actor SafeLogger {
    func log(_ message: String) {
        print("[LOG] \(message)")
    }
}

// MARK: - withCheckedContinuation と @Sendable

/// 古いコールバック API を async/await に変換
func fetchDataAsync() async -> Data? {
    await withCheckedContinuation { continuation in
        // continuation.resume は @Sendable クロージャから呼び出し可能
        DispatchQueue.global().async {
            let data = Data()  // データ取得処理
            continuation.resume(returning: data)
        }
    }
}

/// エラーを投げるバージョン
func fetchDataThrowingAsync() async throws -> Data {
    try await withCheckedThrowingContinuation { continuation in
        DispatchQueue.global().async {
            do {
                let data = Data()
                continuation.resume(returning: data)
            } catch {
                continuation.resume(throwing: error)
            }
        }
    }
}

// MARK: - NotificationCenter と @Sendable

extension NotificationCenter {
    /// @Sendable クロージャを受け取る AsyncSequence
    func notifications(
        named name: Notification.Name
    ) -> AsyncStream<Notification> {
        AsyncStream { continuation in
            let observer = addObserver(
                forName: name,
                object: nil,
                queue: nil
            ) { notification in
                // このクロージャは @Sendable
                continuation.yield(notification)
            }

            continuation.onTermination = { @Sendable _ in
                NotificationCenter.default.removeObserver(observer)
            }
        }
    }
}

// MARK: - SwiftUI での @Sendable

struct ContentView: View {
    @State private var items: [String] = []

    var body: some View {
        List(items, id: \.self) { item in
            Text(item)
        }
        .task {
            // .task のクロージャは @Sendable かつ MainActor
            await loadItems()
        }
        .refreshable {
            // .refreshable のクロージャも @Sendable
            await loadItems()
        }
    }

    func loadItems() async {
        // ネットワークリクエストをシミュレート
        try? await Task.sleep(for: .seconds(1))
        items = ["Item 1", "Item 2", "Item 3"]
    }
}

// MARK: - ジェネリックな @Sendable クロージャ

/// 型パラメータに Sendable 制約を追加
func map<T: Sendable, U: Sendable>(
    value: T,
    transform: @Sendable (T) -> U
) -> U {
    transform(value)
}

/// async 版
func asyncMap<T: Sendable, U: Sendable>(
    value: T,
    transform: @Sendable (T) async -> U
) async -> U {
    await transform(value)
}

// MARK: - 使用例

func demonstrateSendableClosures() async {
    // 基本的な使用
    await performAsyncWithResult {
        // @Sendable クロージャ
        return "Result"
    }

    // キャプチャ
    let value = 42  // Int は Sendable
    Task.detached {
        print("Captured value: \(value)")
    }

    // map の使用
    let result = map(value: 10) { $0 * 2 }
    print("Mapped: \(result)")
}
