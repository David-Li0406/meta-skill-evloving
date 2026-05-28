// MARK: - Custom Actor
// カスタムアクターの実装例

import Foundation
import UIKit

// MARK: - 基本的な Actor: Image Cache

/// Actor はデータの排他的アクセスを保証する
/// 内部の状態は自動的にスレッドセーフになる
actor ImageCache {
    private var cache: [URL: UIImage] = [:]
    private var pendingTasks: [URL: Task<UIImage?, Never>] = [:]

    /// キャッシュから画像を取得
    func image(for url: URL) -> UIImage? {
        cache[url]
    }

    /// キャッシュに画像を保存
    func setImage(_ image: UIImage, for url: URL) {
        cache[url] = image
    }

    /// 画像を読み込み（キャッシュ優先、なければダウンロード）
    func loadImage(from url: URL) async -> UIImage? {
        // キャッシュにあれば返す
        if let cached = cache[url] {
            return cached
        }

        // 既にダウンロード中なら、そのタスクを待つ
        if let pendingTask = pendingTasks[url] {
            return await pendingTask.value
        }

        // 新しいダウンロードタスクを作成
        let task = Task<UIImage?, Never> {
            guard let (data, _) = try? await URLSession.shared.data(from: url),
                  let image = UIImage(data: data) else {
                return nil
            }
            return image
        }

        pendingTasks[url] = task
        let image = await task.value
        pendingTasks[url] = nil

        if let image {
            cache[url] = image
        }

        return image
    }

    /// キャッシュをクリア
    func clear() {
        cache.removeAll()
    }

    /// キャッシュのサイズを取得
    var count: Int {
        cache.count
    }
}

// MARK: - 使用例

func useImageCache() async {
    let cache = ImageCache()

    let url = URL(string: "https://example.com/image.png")!

    // await が必要（actor 境界を越えるため）
    if let image = await cache.loadImage(from: url) {
        print("Image loaded: \(image.size)")
    }
}

// MARK: - Actor: Database Manager

/// データベース操作を管理する Actor
actor DatabaseManager {
    private var connection: DatabaseConnection?
    private var transactionDepth = 0

    func connect() async throws {
        guard connection == nil else { return }
        connection = try await DatabaseConnection.open()
    }

    func disconnect() async {
        await connection?.close()
        connection = nil
    }

    func execute(_ query: String) async throws -> [Row] {
        guard let connection else {
            throw DatabaseError.notConnected
        }
        return try await connection.execute(query)
    }

    func transaction<T>(_ body: () async throws -> T) async throws -> T {
        transactionDepth += 1
        defer { transactionDepth -= 1 }

        if transactionDepth == 1 {
            try await execute("BEGIN TRANSACTION")
        }

        do {
            let result = try await body()
            if transactionDepth == 1 {
                try await execute("COMMIT")
            }
            return result
        } catch {
            if transactionDepth == 1 {
                try? await execute("ROLLBACK")
            }
            throw error
        }
    }
}

// ダミー型
struct DatabaseConnection {
    static func open() async throws -> DatabaseConnection { DatabaseConnection() }
    func close() async {}
    func execute(_ query: String) async throws -> [Row] { [] }
}
struct Row {}
enum DatabaseError: Error { case notConnected }

// MARK: - Actor: Rate Limiter

/// API リクエストのレートリミッター
actor RateLimiter {
    private let maxRequests: Int
    private let timeWindow: TimeInterval
    private var requestTimestamps: [Date] = []

    init(maxRequests: Int, timeWindow: TimeInterval) {
        self.maxRequests = maxRequests
        self.timeWindow = timeWindow
    }

    /// リクエストが許可されるかチェックし、許可されれば記録する
    func tryAcquire() -> Bool {
        let now = Date()
        let windowStart = now.addingTimeInterval(-timeWindow)

        // 古いタイムスタンプを削除
        requestTimestamps.removeAll { $0 < windowStart }

        // リクエスト数をチェック
        if requestTimestamps.count < maxRequests {
            requestTimestamps.append(now)
            return true
        }

        return false
    }

    /// 次のリクエストが可能になるまでの待機時間
    var waitTime: TimeInterval {
        guard requestTimestamps.count >= maxRequests,
              let oldest = requestTimestamps.first else {
            return 0
        }

        let windowStart = Date().addingTimeInterval(-timeWindow)
        return oldest.timeIntervalSince(windowStart)
    }
}

// MARK: - nonisolated と Actor

actor Counter {
    private var _count = 0

    /// let プロパティは nonisolated でアクセス可能
    let id: String

    init(id: String) {
        self.id = id
    }

    var count: Int {
        _count
    }

    func increment() {
        _count += 1
    }

    func decrement() {
        _count -= 1
    }

    /// nonisolated メソッド - actor の状態にアクセスしない
    nonisolated func description() -> String {
        "Counter(\(id))"  // id は let なので OK
    }
}

// MARK: - isolated パラメータ

/// isolated パラメータを使って、特定の actor 上で実行
func performOperation(on counter: isolated Counter) {
    // await なしで counter のメソッドを呼べる
    counter.increment()
    counter.increment()
    print("Count: \(counter.count)")
}

func useIsolatedParameter() async {
    let counter = Counter(id: "main")
    await performOperation(on: counter)
}

// MARK: - GlobalActor の定義

/// カスタム GlobalActor
@globalActor
actor NetworkActor {
    static let shared = NetworkActor()
}

/// NetworkActor 上で実行されるクラス
@NetworkActor
class NetworkService {
    func fetchData(from url: URL) async throws -> Data {
        let (data, _) = try await URLSession.shared.data(from: url)
        return data
    }
}
