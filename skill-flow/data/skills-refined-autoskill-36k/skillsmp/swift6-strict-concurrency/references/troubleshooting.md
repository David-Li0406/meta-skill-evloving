# Swift 6 Strict Concurrency トラブルシューティング

Swift 6 Strict Concurrency 移行時によく遭遇する問題と解決策。

## 一般的な問題

### 問題 1: 大量の警告が発生する

**症状:** `complete` モードを有効にすると、数百〜数千の警告が発生する。

**解決策:**

1. **段階的に対応:**
   ```
   SWIFT_STRICT_CONCURRENCY = targeted
   ```
   まず `targeted` から始めて、徐々に修正する。

2. **優先順位をつける:**
   - 最初に ViewModel と共有状態を修正
   - 次にユーティリティクラスを修正
   - 最後に細かい警告を修正

3. **モジュール単位で対応:**
   - 依存関係の少ないモジュールから開始
   - 段階的に上位モジュールを修正

---

### 問題 2: @Observable と @MainActor の組み合わせ

**症状:** `@Observable` と `@MainActor` を組み合わせると、View からのアクセスでエラーが発生する。

**解決策:**

```swift
// ✅ 正しいパターン
@Observable
@MainActor
class ViewModel {
    var items: [Item] = []
}

struct ContentView: View {
    @State private var viewModel = ViewModel()

    var body: some View {
        List(viewModel.items) { item in
            Text(item.name)
        }
        .task {
            await viewModel.loadItems()
        }
    }
}
```

**注意点:**
- `@State` は MainActor 上で初期化される
- `.task` 修飾子は MainActor を継承する
- `@Environment` でも同様に動作する

---

### 問題 3: UIKit のコールバック

**症状:** UIKit の delegate メソッドや target-action で MainActor 警告が発生する。

**解決策:**

```swift
class ViewController: UIViewController {
    @MainActor
    private var viewModel = ViewModel()

    @objc func buttonTapped(_ sender: UIButton) {
        // UIKit のコールバックは Main Thread だが、
        // コンパイラはそれを認識できない
        MainActor.assumeIsolated {
            viewModel.handleTap()
        }
    }

    // または Task を使用
    @objc func buttonTapped2(_ sender: UIButton) {
        Task { @MainActor in
            viewModel.handleTap()
        }
    }
}
```

---

### 問題 4: サードパーティライブラリが Sendable でない

**症状:** サードパーティライブラリの型を Task 内で使用するとエラーが発生する。

**解決策:**

```swift
// 方法 1: @preconcurrency import
@preconcurrency import ThirdPartyLibrary

// 方法 2: ラッパーを作成
final class SendableWrapper: @unchecked Sendable {
    let value: ThirdPartyType

    init(_ value: ThirdPartyType) {
        self.value = value
    }
}

// 方法 3: Actor でラップ
actor ThirdPartyManager {
    private var instance: ThirdPartyType

    func doSomething() {
        instance.doSomething()
    }
}
```

---

### 問題 5: Completion Handler を使う古い API

**症状:** 古い API の completion handler が @Sendable でない。

**解決策:**

```swift
// 古い API
func oldAPI(completion: @escaping (Data) -> Void) {
    // ...
}

// async/await にラップ
func newAPI() async -> Data {
    await withCheckedContinuation { continuation in
        oldAPI { data in
            continuation.resume(returning: data)
        }
    }
}

// エラーハンドリング付き
func newThrowingAPI() async throws -> Data {
    try await withCheckedThrowingContinuation { continuation in
        oldThrowingAPI { result in
            switch result {
            case .success(let data):
                continuation.resume(returning: data)
            case .failure(let error):
                continuation.resume(throwing: error)
            }
        }
    }
}
```

---

### 問題 6: Actor Reentrancy による予期しない動作

**症状:** Actor のメソッド内で `await` した後、状態が変わっている。

**原因:** Actor は reentrancy をサポートしており、`await` 中に他の操作が実行される可能性がある。

**解決策:**

```swift
actor BankAccount {
    var balance: Int = 100

    // ❌ 問題のあるパターン
    func withdraw(_ amount: Int) async -> Bool {
        guard balance >= amount else { return false }
        balance -= amount  // この後 await があると危険

        await notifyServer()  // この間に別の withdraw が実行される可能性

        return true
    }

    // ✅ 改善されたパターン
    func safeWithdraw(_ amount: Int) async -> Bool {
        // 状態チェックと変更を await の前に完了
        guard balance >= amount else { return false }
        balance -= amount

        // 通知は状態変更後に非同期で行う
        Task { await notifyServer() }

        return true
    }
}
```

---

### 問題 7: Protocol 準拠時の nonisolated 要求

**症状:** Protocol に準拠しようとすると `nonisolated` が必要というエラーが発生する。

**解決策:**

```swift
// Hashable 準拠
actor Document: Hashable {
    let id: UUID

    // nonisolated が必要
    nonisolated static func == (lhs: Document, rhs: Document) -> Bool {
        lhs.id == rhs.id
    }

    nonisolated func hash(into hasher: inout Hasher) {
        hasher.combine(id)
    }
}

// Codable 準拠
actor Settings: Codable {
    let version: Int
    private var theme: String

    enum CodingKeys: String, CodingKey {
        case version, theme
    }

    nonisolated init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        version = try container.decode(Int.self, forKey: .version)
        theme = try container.decode(String.self, forKey: .theme)
    }

    nonisolated func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(version, forKey: .version)
        // 注意: actor-isolated プロパティにはアクセスできない
    }
}
```

---

### 問題 8: @Environment での Actor 使用

**症状:** SwiftUI の Environment で Actor を使用するとエラーが発生する。

**解決策:**

```swift
// @Observable + @MainActor を使用
@Observable
@MainActor
class AppState {
    var isLoggedIn = false
}

// Environment Key
private struct AppStateKey: EnvironmentKey {
    @MainActor static let defaultValue = AppState()
}

extension EnvironmentValues {
    var appState: AppState {
        get { self[AppStateKey.self] }
        set { self[AppStateKey.self] = newValue }
    }
}

// 使用
struct ContentView: View {
    @Environment(AppState.self) private var appState

    var body: some View {
        Text(appState.isLoggedIn ? "Logged In" : "Logged Out")
    }
}
```

---

### 問題 9: テストでの async/await

**症状:** 非同期テストでタイムアウトや予期しない動作が発生する。

**解決策:**

```swift
// XCTestCase での async テスト
class ViewModelTests: XCTestCase {
    @MainActor
    func testLoadItems() async throws {
        let viewModel = ViewModel()
        await viewModel.loadItems()

        XCTAssertFalse(viewModel.items.isEmpty)
    }

    // expectation を使用する場合
    func testWithExpectation() {
        let expectation = expectation(description: "Items loaded")

        Task { @MainActor in
            let viewModel = ViewModel()
            await viewModel.loadItems()

            XCTAssertFalse(viewModel.items.isEmpty)
            expectation.fulfill()
        }

        wait(for: [expectation], timeout: 5.0)
    }
}
```

---

### 問題 10: Preview での @MainActor

**症状:** SwiftUI Preview で @MainActor 関連のエラーが発生する。

**解決策:**

```swift
@Observable
@MainActor
class ViewModel {
    var items: [Item] = []
}

struct ContentView: View {
    @State private var viewModel = ViewModel()

    var body: some View {
        List(viewModel.items) { item in
            Text(item.name)
        }
    }
}

// Preview
#Preview {
    ContentView()
}

// モックデータを使用する場合
#Preview {
    let viewModel = ViewModel()
    // @MainActor なので直接設定可能（Preview は Main Thread）
    viewModel.items = [
        Item(id: UUID(), name: "Preview Item")
    ]
    return ContentView()
}
```

## デバッグのヒント

### 1. データの流れを可視化

```swift
actor DebugStore {
    func process(_ data: Data) {
        print("[\(Date())] Processing on: \(Thread.current)")
        // ...
    }
}
```

### 2. Xcode の Thread Sanitizer を有効化

1. Product → Scheme → Edit Scheme
2. Run → Diagnostics
3. Thread Sanitizer を有効化

### 3. 警告を一時的に無視（デバッグ用）

```swift
// 一時的なワークアラウンド（本番では使用しない）
nonisolated(unsafe) var debugValue: Int = 0
```

## よくある質問

**Q: すべてのクラスを Actor にすべき？**
A: いいえ。共有可変状態を持つクラスのみ Actor にする。不変データや MainActor 上のみで使用するクラスは `@MainActor` で十分。

**Q: @unchecked Sendable はいつ使う？**
A: 内部で確実に同期処理（ロック等）を行っている場合のみ。可能な限り Actor を使用する。

**Q: パフォーマンスへの影響は？**
A: Actor の await はオーバーヘッドがあるが、通常のアプリでは無視できるレベル。パフォーマンスクリティカルな部分では `@unchecked Sendable` とロックを検討。
