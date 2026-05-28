# Swift 6 Strict Concurrency 頻出エラーと解決策

Swift 6 の Strict Concurrency モードで発生する一般的なエラーメッセージと、その解決方法を解説。

## エラー一覧

### 1. Capture of non-sendable type

**エラーメッセージ:**
```
Capture of 'x' with non-sendable type 'ClassName' in @Sendable closure
```

**原因:** `@Sendable` クロージャ（Task など）で非 Sendable 型をキャプチャしている。

**解決策:**

```swift
// ❌ Before
class Logger {
    func log(_ message: String) { print(message) }
}

let logger = Logger()
Task {
    logger.log("message")  // Error
}

// ✅ After - Actor を使用
actor SafeLogger {
    func log(_ message: String) { print(message) }
}

let logger = SafeLogger()
Task {
    await logger.log("message")  // OK
}

// ✅ After - Sendable に準拠
final class SendableLogger: Sendable {
    func log(_ message: String) { print(message) }
}
```

---

### 2. Call to main actor-isolated method

**エラーメッセージ:**
```
Call to main actor-isolated instance method 'xxx()' in a synchronous nonisolated context
```

**原因:** `@MainActor` で隔離されたメソッドを、非 MainActor コンテキストから同期的に呼び出している。

**解決策:**

```swift
@MainActor
class ViewModel {
    func updateUI() { }
}

// ❌ Before
func doWork(viewModel: ViewModel) {
    viewModel.updateUI()  // Error
}

// ✅ After - await を追加
func doWork(viewModel: ViewModel) async {
    await viewModel.updateUI()
}

// ✅ After - 呼び出し元も @MainActor に
@MainActor
func doWork(viewModel: ViewModel) {
    viewModel.updateUI()  // OK
}
```

---

### 3. Stored property must be immutable

**エラーメッセージ:**
```
Stored property 'x' of 'Sendable'-conforming class 'ClassName' must be immutable
```

**原因:** Sendable に準拠したクラスに `var` プロパティがある。

**解決策:**

```swift
// ❌ Before
final class Config: Sendable {
    var timeout: Int = 30  // Error
}

// ✅ After - let に変更
final class Config: Sendable {
    let timeout: Int

    init(timeout: Int = 30) {
        self.timeout = timeout
    }
}

// ✅ After - Actor を使用
actor Config {
    var timeout: Int = 30  // OK
}
```

---

### 4. Actor-isolated property mutation

**エラーメッセージ:**
```
Actor-isolated property 'x' can not be mutated from a non-isolated context
```

**原因:** Actor 外部から直接プロパティを変更しようとしている。

**解決策:**

```swift
actor Counter {
    var count = 0
}

// ❌ Before
func increment(counter: Counter) async {
    counter.count += 1  // Error
}

// ✅ After - メソッドを追加
actor Counter {
    var count = 0

    func increment() {
        count += 1
    }
}

func increment(counter: Counter) async {
    await counter.increment()  // OK
}
```

---

### 5. Non-sendable type crossing actor boundary

**エラーメッセージ:**
```
Non-sendable type 'ClassName' cannot cross actor boundary
```

**原因:** Actor メソッドのパラメータまたは戻り値が非 Sendable 型。

**解決策:**

```swift
// ❌ Before
class Item { var name: String = "" }

actor Store {
    func add(_ item: Item) { }  // Error
}

// ✅ After - Sendable に準拠
struct Item: Sendable {
    var name: String
}

actor Store {
    func add(_ item: Item) { }  // OK
}
```

---

### 6. Reference to captured var

**エラーメッセージ:**
```
Reference to captured var 'x' in concurrently-executing code
```

**原因:** 並行コード内で可変変数をキャプチャしている。

**解決策:**

```swift
// ❌ Before
var count = 0
Task {
    count += 1  // Error
}

// ✅ After - let でキャプチャ
let currentCount = count
Task {
    print(currentCount)  // OK（読み取りのみ）
}

// ✅ After - Actor を使用
actor Counter {
    var count = 0
    func increment() { count += 1 }
}

let counter = Counter()
Task {
    await counter.increment()  // OK
}
```

---

### 7. Sendable closure captures mutable self

**エラーメッセージ:**
```
Mutation of captured var 'self' in concurrently-executing code
```

**原因:** `Task.detached` 内で `self` のプロパティを変更しようとしている。

**解決策:**

```swift
@MainActor
class ViewModel {
    var count = 0

    // ❌ Before
    func work() {
        Task.detached {
            self.count += 1  // Error
        }
    }

    // ✅ After - Task を使用（MainActor を継承）
    func workFixed1() {
        Task {
            count += 1  // OK
        }
    }

    // ✅ After - MainActor.run を使用
    func workFixed2() {
        Task.detached {
            await MainActor.run {
                self.count += 1  // OK
            }
        }
    }
}
```

---

### 8. Cannot convert to Sendable

**エラーメッセージ:**
```
Converting non-sendable function value to '@Sendable () -> Void' may introduce data races
```

**原因:** 非 Sendable なクロージャを Sendable が必要な場所で使用。

**解決策:**

```swift
// ❌ Before
var state = 0
let closure = { state += 1 }
Task { closure() }  // Error

// ✅ After - 状態をキャプチャしない
Task {
    print("No captured state")  // OK
}

// ✅ After - Sendable な値をキャプチャ
let value = 42
Task {
    print(value)  // OK
}
```

---

### 9. Protocol does not conform to Sendable

**エラーメッセージ:**
```
Type 'X' does not conform to protocol 'Sendable'
```

**原因:** Protocol に Sendable 制約があるが、準拠する型が Sendable でない。

**解決策:**

```swift
protocol DataProtocol: Sendable {
    var id: UUID { get }
}

// ❌ Before
class BadData: DataProtocol {  // Error
    var id: UUID = UUID()
}

// ✅ After - struct を使用
struct GoodData: DataProtocol {
    let id: UUID
}

// ✅ After - final class + immutable
final class GoodDataClass: DataProtocol, Sendable {
    let id: UUID
    init(id: UUID) { self.id = id }
}
```

---

### 10. Implicitly asynchronous call

**エラーメッセージ:**
```
Expression is 'async' but is not marked with 'await'
```

**原因:** Actor 隔離されたメンバーへのアクセスに `await` がない。

**解決策:**

```swift
actor Store {
    var items: [String] = []
}

// ❌ Before
func getItems(store: Store) -> [String] {
    store.items  // Error
}

// ✅ After
func getItems(store: Store) async -> [String] {
    await store.items  // OK
}
```

---

## クイックリファレンス

| エラー | 主な原因 | 推奨解決策 |
|-------|---------|-----------|
| Capture of non-sendable | Task で非 Sendable をキャプチャ | Actor を使用 |
| Call to main actor-isolated | MainActor メソッドを直接呼び出し | await を追加 |
| Property must be immutable | Sendable クラスに var | let に変更または Actor 使用 |
| Cannot mutate from non-isolated | Actor プロパティを直接変更 | メソッド経由で変更 |
| Cannot cross actor boundary | 非 Sendable を Actor に渡す | Sendable に準拠 |
| Reference to captured var | var を並行コードでキャプチャ | let または Actor 使用 |
| Captures mutable self | detached Task で self を変更 | Task または MainActor.run |

## デバッグのヒント

1. **エラーの位置を特定**: エラーメッセージの行番号を確認
2. **データの流れを追跡**: どの Task/Actor 境界を越えているか確認
3. **Sendable チェック**: 関連する型が Sendable か確認
4. **Actor isolation チェック**: どの Actor context にいるか確認
5. **段階的修正**: `SWIFT_STRICT_CONCURRENCY = targeted` から始める
