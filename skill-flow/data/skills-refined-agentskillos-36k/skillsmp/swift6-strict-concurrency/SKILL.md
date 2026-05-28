---
name: swift6-strict-concurrency
description: |
  This skill should be used when the user asks to "migrate to Swift 6",
  "enable strict concurrency", "fix Sendable errors", "add @MainActor",
  "resolve data race warnings", "implement actor isolation",
  "configure complete concurrency checking", "fix Swift 6 warnings",
  "make class Sendable", "handle @Sendable closures",
  "Swift 6 に移行", "Strict Concurrency を有効化", "Sendable エラーを修正",
  "@MainActor を追加", "データ競合警告を解決", "アクター分離を実装",
  "完全な並行性チェックを設定", "Swift 6 警告を修正",
  "クラスを Sendable にする", "@Sendable クロージャを扱う",
  or needs guidance on Swift 6 strict concurrency migration,
  Sendable protocol implementation, actor isolation patterns,
  data race safety, and migration strategies from Swift 5 to Swift 6.
version: 1.0.0
---

# Swift 6 Strict Concurrency

Swift 6 の Strict Concurrency モードへの移行・対応を支援するスキル。Sendable プロトコル、Actor 分離、データ競合の安全性などを網羅的にカバーする。

## Overview

**Target Platform**: iOS 17+ / macOS 14+ / Swift 6.0+

**主要な変更点**:
- Complete concurrency checking がデフォルトで有効
- すべての型がデータ競合に対して安全であることを保証
- Sendable プロトコルによる型安全な境界定義
- Actor isolation による排他的アクセス制御

**Core Concepts**:
- Sendable Protocol
- Actor Isolation (@MainActor, custom actors)
- @Sendable Closures
- Data Race Safety

## Quick Start Checklist

Swift 6 Strict Concurrency を有効化する手順：

1. **Xcode Build Settings で設定**
   ```
   SWIFT_STRICT_CONCURRENCY = complete
   ```

2. **または Package.swift で設定**
   ```swift
   .target(
       name: "MyTarget",
       swiftSettings: [
           .swiftLanguageMode(.v6)
       ]
   )
   ```

3. **段階的に有効化（推奨）**
   - `minimal` → `targeted` → `complete` の順で警告を解消

4. **主要なエラーを修正**
   - 非 Sendable 型のキャプチャ
   - Actor 境界を越えるデータアクセス
   - @MainActor の不足

## Xcode Project Configuration

### Build Settings

| 設定 | 値 | 説明 |
|-----|-----|-----|
| `SWIFT_STRICT_CONCURRENCY` | `minimal` | 最小限の警告（デフォルト） |
| `SWIFT_STRICT_CONCURRENCY` | `targeted` | @Sendable を明示した部分のみ |
| `SWIFT_STRICT_CONCURRENCY` | `complete` | 完全なデータ競合チェック |

### Package.swift

```swift
// Swift 6 言語モード
let package = Package(
    name: "MyPackage",
    platforms: [.iOS(.v17), .macOS(.v14)],
    targets: [
        .target(
            name: "MyTarget",
            swiftSettings: [
                .swiftLanguageMode(.v6)
            ]
        )
    ]
)

// Swift 5.x で段階的に有効化
.target(
    name: "MyTarget",
    swiftSettings: [
        .enableUpcomingFeature("StrictConcurrency")
    ]
)
```

詳細は [references/xcode-configuration.md](references/xcode-configuration.md) を参照。

## Sendable Protocol

### 自動準拠する型

以下の型は自動的に Sendable に準拠：

- **値型（struct/enum）**: すべてのプロパティが Sendable の場合
- **Actor**: 常に Sendable
- **基本型**: Int, String, Bool, etc.

```swift
// 自動的に Sendable
struct UserData: Sendable {
    let id: UUID
    let name: String
}

enum Status: Sendable {
    case pending
    case completed(Date)
}
```

### 手動準拠（Reference Types）

```swift
// final class + immutable properties
final class Config: Sendable {
    let apiKey: String
    let timeout: TimeInterval

    init(apiKey: String, timeout: TimeInterval) {
        self.apiKey = apiKey
        self.timeout = timeout
    }
}
```

### @unchecked Sendable

内部で同期処理を行う場合に使用（慎重に）：

```swift
final class ThreadSafeCache: @unchecked Sendable {
    private let lock = NSLock()
    private var storage: [String: Data] = [:]

    func get(_ key: String) -> Data? {
        lock.lock()
        defer { lock.unlock() }
        return storage[key]
    }

    func set(_ key: String, value: Data) {
        lock.lock()
        defer { lock.unlock() }
        storage[key] = value
    }
}
```

詳細は [references/sendable-guide.md](references/sendable-guide.md) を参照。

## Actor Isolation

### @MainActor

UI 更新を行うクラスに適用：

```swift
@Observable
@MainActor
class ViewModel {
    var items: [Item] = []
    var isLoading = false
    var errorMessage: String?

    func loadData() async {
        isLoading = true
        defer { isLoading = false }

        do {
            items = try await api.fetchItems()
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}
```

### Custom Actor

データの排他的アクセスが必要な場合：

```swift
actor ImageCache {
    private var cache: [URL: UIImage] = [:]

    func image(for url: URL) -> UIImage? {
        cache[url]
    }

    func setImage(_ image: UIImage, for url: URL) {
        cache[url] = image
    }

    func clear() {
        cache.removeAll()
    }
}

// 使用例
let cache = ImageCache()
let image = await cache.image(for: url)
```

### nonisolated

Actor 内で同期アクセスを許可：

```swift
actor DataManager {
    let id: String  // let は nonisolated でアクセス可能

    nonisolated var identifier: String {
        id  // await 不要
    }

    // Hashable 準拠
    nonisolated func hash(into hasher: inout Hasher) {
        hasher.combine(id)
    }
}
```

詳細は [references/actor-isolation.md](references/actor-isolation.md) を参照。

## @Sendable Closures

### 基本的な使用法

```swift
// Task は @Sendable クロージャを要求
Task {
    // このクロージャ内でキャプチャする値は Sendable でなければならない
    await performWork()
}

// 明示的な @Sendable
func performAsync(_ work: @Sendable @escaping () async -> Void) {
    Task { await work() }
}
```

### キャプチャリストの注意点

```swift
@MainActor
class ViewModel {
    var count = 0

    func increment() {
        // BAD: self は非 Sendable
        Task.detached {
            self.count += 1  // エラー
        }

        // GOOD: @MainActor に戻る
        Task {
            self.count += 1  // OK（MainActor を継承）
        }
    }
}
```

詳細は [examples/sendable-closures.swift](examples/sendable-closures.swift) を参照。

## Common Errors and Fixes

| エラーメッセージ | 原因 | 解決策 |
|----------------|------|--------|
| `Capture of 'x' with non-sendable type in @Sendable closure` | 非 Sendable 型をクロージャでキャプチャ | Sendable に準拠させるか actor を使用 |
| `Call to main actor-isolated method in synchronous nonisolated context` | @MainActor メソッドを非分離コンテキストから呼び出し | await を追加、または呼び出し元も @MainActor に |
| `Stored property 'x' of 'Sendable'-conforming class must be immutable` | Sendable クラスに var プロパティ | let に変更、または actor を使用 |
| `Actor-isolated property 'x' cannot be mutated from a non-isolated context` | アクター外からプロパティを変更 | await を使用してアクターメソッド経由で変更 |
| `Non-sendable type 'X' cannot cross actor boundary` | 非 Sendable 型をアクター境界で渡す | Sendable に準拠させる |
| `Task-isolated value of type 'X' passed as a strongly transferred parameter` | Task 間でのデータ転送 | Sendable に準拠させるか、コピーを渡す |

詳細は [references/common-errors.md](references/common-errors.md) を参照。

## Migration Strategy

### 段階的移行アプローチ

1. **Phase 1: 現状把握**
   ```bash
   # プロジェクト分析スクリプトを実行
   bash scripts/swift6-migration-analyzer.sh /path/to/project
   ```

2. **Phase 2: targeted で有効化**
   - `SWIFT_STRICT_CONCURRENCY = targeted` に設定
   - 明示的に @Sendable をマークした箇所のみ警告

3. **Phase 3: 主要な型を修正**
   - ViewModel → @MainActor を追加
   - 共有データ → actor に変換
   - 不変データ → Sendable に準拠

4. **Phase 4: complete で有効化**
   - `SWIFT_STRICT_CONCURRENCY = complete` に設定
   - すべての警告を解消

5. **Phase 5: Swift 6 に移行**
   - `.swiftLanguageMode(.v6)` を設定

### Before/After 例

```swift
// BEFORE: Swift 5 スタイル
class ViewModel: ObservableObject {
    @Published var items: [Item] = []

    func load() {
        Task {
            items = try await api.fetch()
        }
    }
}

// AFTER: Swift 6 スタイル
@Observable
@MainActor
class ViewModel {
    var items: [Item] = []

    func load() async {
        items = try await api.fetch()
    }
}
```

詳細は [references/migration-checklist.md](references/migration-checklist.md) を参照。

## Additional Resources

### Example Files
- [examples/sendable-value-types.swift](examples/sendable-value-types.swift) - 値型の Sendable 自動準拠
- [examples/sendable-reference-types.swift](examples/sendable-reference-types.swift) - クラスの Sendable 準拠
- [examples/unchecked-sendable.swift](examples/unchecked-sendable.swift) - @unchecked Sendable の使用
- [examples/mainactor-viewmodel.swift](examples/mainactor-viewmodel.swift) - @MainActor ViewModel パターン
- [examples/custom-actor.swift](examples/custom-actor.swift) - カスタムアクター実装
- [examples/nonisolated-methods.swift](examples/nonisolated-methods.swift) - nonisolated キーワード
- [examples/sendable-closures.swift](examples/sendable-closures.swift) - @Sendable クロージャ
- [examples/task-isolation.swift](examples/task-isolation.swift) - Task の分離コンテキスト
- [examples/migration-before-after.swift](examples/migration-before-after.swift) - 移行 Before/After
- [examples/swiftui-integration.swift](examples/swiftui-integration.swift) - SwiftUI との統合

### Reference Files
- [references/sendable-guide.md](references/sendable-guide.md) - Sendable 完全ガイド
- [references/actor-isolation.md](references/actor-isolation.md) - アクター分離詳細
- [references/common-errors.md](references/common-errors.md) - 頻出エラーと解決策
- [references/migration-checklist.md](references/migration-checklist.md) - 移行チェックリスト
- [references/xcode-configuration.md](references/xcode-configuration.md) - Xcode 設定ガイド
- [references/troubleshooting.md](references/troubleshooting.md) - トラブルシューティング

### Utility Scripts
- [scripts/swift6-migration-analyzer.sh](scripts/swift6-migration-analyzer.sh) - 移行分析スクリプト
