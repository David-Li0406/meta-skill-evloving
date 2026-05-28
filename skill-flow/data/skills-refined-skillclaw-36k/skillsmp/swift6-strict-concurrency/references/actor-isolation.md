# Actor Isolation 詳細ガイド

Swift 6 における Actor 分離の詳細解説。

## 概要

Actor isolation は、データ競合を防ぐための Swift の仕組み。Actor 内のデータは排他的にアクセスされ、外部からは `await` を使ってのみアクセス可能。

## Actor の基本

### 定義と使用

```swift
actor Counter {
    private var count = 0

    func increment() {
        count += 1
    }

    func decrement() {
        count -= 1
    }

    func getCount() -> Int {
        count
    }
}

// 使用
let counter = Counter()
await counter.increment()
let value = await counter.getCount()
```

### Actor の特性

- Actor 内のすべてのプロパティとメソッドは actor-isolated
- 外部からのアクセスには `await` が必要
- Actor への参照は常に `Sendable`
- 一度に一つの操作のみが実行される（排他制御）

## @MainActor

### 概要

`@MainActor` は Main Thread（UI スレッド）上で実行されることを保証する Global Actor。

### クラス全体に適用

```swift
@Observable
@MainActor
class ViewModel {
    var items: [Item] = []
    var isLoading = false

    func loadItems() async {
        isLoading = true
        defer { isLoading = false }
        items = try await fetchItems()
    }
}
```

### メソッドに適用

```swift
class Service {
    @MainActor
    func updateUI() {
        // Main Thread で実行される
    }

    func fetchData() async -> Data {
        // どのスレッドでも実行可能
        return Data()
    }
}
```

### プロパティに適用

```swift
class Manager {
    @MainActor var currentUser: User?

    func setUser(_ user: User) async {
        await MainActor.run {
            currentUser = user
        }
    }
}
```

## nonisolated

### 基本的な使い方

Actor 内で `nonisolated` を使うと、actor isolation から除外される。

```swift
actor DataStore {
    let id: String  // let は暗黙的に nonisolated

    // 明示的な nonisolated
    nonisolated var identifier: String {
        id
    }

    nonisolated func formatID() -> String {
        "Store-\(id)"
    }
}

// await なしでアクセス可能
let store = DataStore(id: "main")
print(store.identifier)
print(store.formatID())
```

### Protocol 準拠

Hashable や Codable などの Protocol に準拠するには `nonisolated` が必要：

```swift
actor Document: Hashable {
    let id: UUID

    nonisolated static func == (lhs: Document, rhs: Document) -> Bool {
        lhs.id == rhs.id
    }

    nonisolated func hash(into hasher: inout Hasher) {
        hasher.combine(id)
    }
}
```

## isolated パラメータ

関数パラメータに `isolated` を付けると、その actor のコンテキストで実行される：

```swift
func performWork(on counter: isolated Counter) {
    // await なしで counter のメソッドを呼べる
    counter.increment()
    counter.increment()
}

// 使用
let counter = Counter()
await performWork(on: counter)
```

## Global Actor の定義

### カスタム Global Actor

```swift
@globalActor
actor DatabaseActor {
    static let shared = DatabaseActor()
}

// 使用
@DatabaseActor
class DatabaseService {
    func query(_ sql: String) -> [Row] {
        // DatabaseActor 上で実行される
    }
}

@DatabaseActor
func runQuery() async {
    // DatabaseActor 上で実行される
}
```

## MainActor.run と MainActor.assumeIsolated

### MainActor.run

非 MainActor コンテキストから MainActor に切り替える：

```swift
func backgroundWork() async {
    // バックグラウンドで処理
    let result = processData()

    // UI 更新のために MainActor に切り替え
    await MainActor.run {
        updateUI(with: result)
    }
}
```

### MainActor.assumeIsolated

すでに MainActor 上にいることがわかっている場合に使用（危険）：

```swift
// ⚠️ 慎重に使用
@objc func buttonTapped() {
    // UIKit のコールバックは Main Thread だが、
    // コンパイラはそれを認識できない
    MainActor.assumeIsolated {
        viewModel.updateState()
    }
}
```

## Actor Reentrancy

Actor のメソッド内で `await` すると、他の操作が割り込む可能性がある：

```swift
actor BankAccount {
    var balance: Int = 100

    func transfer(amount: Int, to other: BankAccount) async {
        guard balance >= amount else { return }

        balance -= amount  // Step 1
        await other.deposit(amount)  // Step 2: await 中に他の操作が入る可能性
        // Step 1 の時点の balance が変わっている可能性がある
    }

    func deposit(_ amount: Int) {
        balance += amount
    }
}
```

### 対策

```swift
actor BankAccount {
    var balance: Int = 100

    func transfer(amount: Int, to other: BankAccount) async -> Bool {
        // 状態チェックと変更を atomic に行う
        guard balance >= amount else { return false }
        balance -= amount

        // 転送は別の操作として実行
        await other.deposit(amount)
        return true
    }
}
```

## Task と Actor Isolation

### Task は親の isolation を継承

```swift
@MainActor
class ViewModel {
    var count = 0

    func work() {
        Task {
            // MainActor を継承
            count += 1  // OK
        }
    }
}
```

### Task.detached は isolation を継承しない

```swift
@MainActor
class ViewModel {
    var count = 0

    func work() {
        Task.detached {
            // MainActor から切り離される
            // self.count += 1  // Error

            await MainActor.run {
                self.count += 1  // OK
            }
        }
    }
}
```

## よくあるパターン

### ViewModel パターン

```swift
@Observable
@MainActor
class ViewModel {
    var items: [Item] = []
    private let repository: ItemRepository

    init(repository: ItemRepository) {
        self.repository = repository
    }

    func load() async {
        items = await repository.fetchAll()
    }
}

actor ItemRepository {
    func fetchAll() async -> [Item] {
        // データ取得
    }
}
```

### Singleton パターン

```swift
actor NetworkManager {
    static let shared = NetworkManager()
    private init() {}

    private var cache: [URL: Data] = [:]

    func fetch(_ url: URL) async throws -> Data {
        if let cached = cache[url] {
            return cached
        }
        let (data, _) = try await URLSession.shared.data(from: url)
        cache[url] = data
        return data
    }
}
```

## チェックリスト

- [ ] 共有可変状態には Actor を使用しているか
- [ ] UI 更新は @MainActor で行っているか
- [ ] Actor の Reentrancy を考慮しているか
- [ ] 不要な await を避けているか（nonisolated の活用）
- [ ] Protocol 準拠に nonisolated を使用しているか
