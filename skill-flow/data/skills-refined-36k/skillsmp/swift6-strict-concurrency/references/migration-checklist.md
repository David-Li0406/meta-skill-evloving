# Swift 5 → Swift 6 移行チェックリスト

Swift 5 プロジェクトを Swift 6 Strict Concurrency に移行するためのステップバイステップガイド。

## 移行の概要

### 推奨アプローチ

1. `targeted` モードで警告を確認
2. 主要な型から順に修正
3. `complete` モードで全警告を解消
4. Swift 6 言語モードに移行

### タイムライン目安

| フェーズ | 内容 | 期間目安 |
|---------|------|---------|
| Phase 1 | 現状把握・計画 | 1-2日 |
| Phase 2 | targeted モードで修正開始 | 1-2週間 |
| Phase 3 | complete モードで全修正 | 2-4週間 |
| Phase 4 | Swift 6 移行・テスト | 1週間 |

## Phase 1: 現状把握

### Step 1.1: プロジェクト分析

```bash
# プロジェクト構造の確認
find . -name "*.swift" | xargs grep -l "class.*ObservableObject" | wc -l
find . -name "*.swift" | xargs grep -l "@Published" | wc -l
find . -name "*.swift" | xargs grep -l "DispatchQueue" | wc -l
```

### Step 1.2: 優先度の決定

修正優先度の高い項目：
- [ ] ViewModel クラス
- [ ] シングルトン
- [ ] 共有可変状態
- [ ] Delegate パターン
- [ ] Completion Handler

### Step 1.3: テストカバレッジの確認

移行前にテストがあることを確認：
- [ ] Unit Tests
- [ ] UI Tests
- [ ] Integration Tests

## Phase 2: Targeted モードで修正開始

### Step 2.1: Build Settings の変更

```
SWIFT_STRICT_CONCURRENCY = targeted
```

または Package.swift:
```swift
.target(
    name: "MyTarget",
    swiftSettings: [
        .enableUpcomingFeature("StrictConcurrency")
    ]
)
```

### Step 2.2: ViewModel の移行

**Before:**
```swift
class ViewModel: ObservableObject {
    @Published var items: [Item] = []
    @Published var isLoading = false

    func load() {
        Task {
            items = try await fetch()
        }
    }
}
```

**After:**
```swift
@Observable
@MainActor
class ViewModel {
    var items: [Item] = []
    var isLoading = false

    func load() async {
        items = try await fetch()
    }
}
```

**チェックリスト:**
- [ ] `ObservableObject` → `@Observable`
- [ ] `@Published` を削除
- [ ] `@MainActor` を追加
- [ ] `@StateObject` → `@State`
- [ ] `@ObservedObject` → 直接使用または `@Bindable`

### Step 2.3: シングルトンの移行

**Before:**
```swift
class NetworkManager {
    static let shared = NetworkManager()
    private init() {}

    var baseURL: URL?

    func request(_ path: String) async throws -> Data {
        // ...
    }
}
```

**After:**
```swift
actor NetworkManager {
    static let shared = NetworkManager()
    private init() {}

    var baseURL: URL?

    func request(_ path: String) async throws -> Data {
        // ...
    }
}
```

**チェックリスト:**
- [ ] `class` → `actor`
- [ ] 呼び出し側に `await` を追加
- [ ] 不変データは `nonisolated` を検討

### Step 2.4: 共有可変状態の移行

**Before:**
```swift
class Cache {
    private let queue = DispatchQueue(label: "cache")
    private var storage: [String: Data] = [:]

    func get(_ key: String) -> Data? {
        queue.sync { storage[key] }
    }

    func set(_ key: String, _ value: Data) {
        queue.async { self.storage[key] = value }
    }
}
```

**After:**
```swift
actor Cache {
    private var storage: [String: Data] = [:]

    func get(_ key: String) -> Data? {
        storage[key]
    }

    func set(_ key: String, _ value: Data) {
        storage[key] = value
    }
}
```

**チェックリスト:**
- [ ] `DispatchQueue` ベースの同期 → `actor`
- [ ] `NSLock` ベースの同期 → `actor` または `@unchecked Sendable`
- [ ] グローバル変数 → `actor` でラップ

### Step 2.5: Delegate パターンの移行

**Before:**
```swift
protocol DataDelegate: AnyObject {
    func didReceive(_ data: Data)
}

class DataFetcher {
    weak var delegate: DataDelegate?

    func fetch() {
        Task {
            let data = await fetchData()
            delegate?.didReceive(data)
        }
    }
}
```

**After:**
```swift
@MainActor
protocol DataDelegate: AnyObject {
    func didReceive(_ data: Data)
}

@MainActor
class DataFetcher {
    weak var delegate: DataDelegate?

    func fetch() async {
        let data = await fetchData()
        delegate?.didReceive(data)
    }
}
```

**チェックリスト:**
- [ ] Protocol に `@MainActor` を追加
- [ ] 実装クラスにも `@MainActor` を追加
- [ ] または async メソッドに変更

### Step 2.6: Completion Handler の移行

**Before:**
```swift
func fetchUser(completion: @escaping (Result<User, Error>) -> Void) {
    URLSession.shared.dataTask(with: url) { data, _, error in
        // ...
        completion(.success(user))
    }.resume()
}
```

**After:**
```swift
func fetchUser() async throws -> User {
    let (data, _) = try await URLSession.shared.data(from: url)
    return try JSONDecoder().decode(User.self, from: data)
}
```

**チェックリスト:**
- [ ] `completion:` パラメータを削除
- [ ] `async throws` を追加
- [ ] `return` で結果を返す
- [ ] 呼び出し側を `await` に変更

## Phase 3: Complete モードで全修正

### Step 3.1: Build Settings の変更

```
SWIFT_STRICT_CONCURRENCY = complete
```

### Step 3.2: 残りの警告を修正

よくある警告：
- [ ] 非 Sendable 型のキャプチャ
- [ ] Protocol の Sendable 準拠
- [ ] Extension での isolation
- [ ] 暗黙的な MainActor

### Step 3.3: @Sendable クロージャの対応

```swift
// 修正が必要なパターン
Task {
    nonSendableObject.doSomething()  // Error
}

// 修正後
Task { @MainActor in
    nonSendableObject.doSomething()  // OK if object is @MainActor
}
```

## Phase 4: Swift 6 移行

### Step 4.1: 言語モードの変更

Package.swift:
```swift
.target(
    name: "MyTarget",
    swiftSettings: [
        .swiftLanguageMode(.v6)
    ]
)
```

Xcode:
```
SWIFT_VERSION = 6.0
```

### Step 4.2: 最終テスト

- [ ] 全 Unit Tests がパス
- [ ] 全 UI Tests がパス
- [ ] 手動テストで動作確認
- [ ] パフォーマンステスト

### Step 4.3: コードレビュー

- [ ] `@unchecked Sendable` の使用箇所を確認
- [ ] `nonisolated(unsafe)` の使用箇所を確認
- [ ] Actor reentrancy のリスクを確認

## よくある問題と解決策

### 問題 1: サードパーティライブラリが Sendable でない

```swift
// ワークアラウンド: @unchecked Sendable でラップ
final class SendableWrapper: @unchecked Sendable {
    let value: ThirdPartyType

    init(_ value: ThirdPartyType) {
        self.value = value
    }
}
```

### 問題 2: UIKit コールバックでの MainActor

```swift
// UIKit のコールバックは Main Thread だが、コンパイラは認識しない
@objc func buttonTapped() {
    MainActor.assumeIsolated {
        viewModel.handleTap()
    }
}
```

### 問題 3: 既存の非同期コードとの互換性

```swift
// 古い API を async/await に変換
func legacyAsync() async -> Data {
    await withCheckedContinuation { continuation in
        legacyAPI { data in
            continuation.resume(returning: data)
        }
    }
}
```

## 最終チェックリスト

- [ ] すべての警告が解消されている
- [ ] テストがパスしている
- [ ] `@unchecked Sendable` の使用は最小限
- [ ] `nonisolated(unsafe)` の使用は最小限
- [ ] ドキュメントが更新されている
- [ ] チームメンバーへの周知が完了
